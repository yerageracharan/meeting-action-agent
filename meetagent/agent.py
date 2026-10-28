"""Task-focused agent: extract, validate, and format follow-up actions from meeting notes."""
from __future__ import annotations

import json
import re
from typing import Any, Callable

from .provider import chat_completion

SYSTEM_PROMPT = r"""You are Meeting Action Agent, a careful meeting-notes assistant.
Return ONLY valid JSON, with no markdown fences and no text outside the JSON.
Use this exact top-level shape:
{
  "meeting_summary": "short plain-English summary",
  "decisions": ["decision explicitly made in the notes"],
  "action_items": [
    {
      "task": "specific action",
      "owner": "person/team explicitly named, otherwise null",
      "due_date": "deadline explicitly stated, otherwise null",
      "priority": "high|medium|low|unknown",
      "evidence": "short exact quote from the notes supporting this task",
      "status": "assigned|needs_clarification"
    }
  ],
  "open_questions": ["unresolved question from the notes"],
  "risks_or_blockers": ["risk or blocker explicitly mentioned"],
  "assumptions_to_confirm": ["important detail that is ambiguous or missing"]
}
Rules:
- Use ONLY information present in the meeting notes. Never invent names, dates, decisions, or deadlines.
- Keep due_date exactly as stated; do not guess a calendar date from words like 'next Friday'. You may preserve that phrase.
- Every action item must have evidence copied verbatim from the notes. If you cannot find evidence, omit the action.
- Use null for an unknown owner or deadline. Do not fill gaps by guessing.
- Mark an item 'needs_clarification' if its owner or deadline is missing or ambiguous; otherwise mark it 'assigned'.
- Do not convert suggestions into decisions unless the notes say they were agreed.
- Be concise. An empty list is better than invented information.
"""

EXPECTED_LISTS = ("decisions", "action_items", "open_questions", "risks_or_blockers", "assumptions_to_confirm")


class AgentOutputError(ValueError):
    """Raised when model output cannot be interpreted as the required structure."""


def _parse_json(text: str) -> dict[str, Any]:
    text = text.strip()
    text = re.sub(r"^\x60\x60\x60(?:json)?\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s*\x60\x60\x60$", "", text)
    start, end = text.find("{"), text.rfind("}")
    if start < 0 or end < start:
        raise AgentOutputError("The model did not return a JSON object. Try another model or reduce the note length.")
    try:
        data = json.loads(text[start : end + 1])
    except json.JSONDecodeError as exc:
        raise AgentOutputError(f"The model returned malformed JSON: {exc.msg}.") from exc
    if not isinstance(data, dict):
        raise AgentOutputError("The model output must be a JSON object.")
    return data


def validate_output(data: dict[str, Any]) -> dict[str, Any]:
    """Validate essential fields and normalize predictable omissions without inventing content."""
    data.setdefault("meeting_summary", "")
    if not isinstance(data["meeting_summary"], str):
        raise AgentOutputError("meeting_summary must be text.")
    for key in EXPECTED_LISTS:
        if key not in data:
            data[key] = []
        if not isinstance(data[key], list):
            raise AgentOutputError(f"{key} must be a list.")
    cleaned = []
    for idx, item in enumerate(data["action_items"], start=1):
        if not isinstance(item, dict):
            raise AgentOutputError(f"Action item {idx} must be an object.")
        task = item.get("task")
        evidence = item.get("evidence")
        if not isinstance(task, str) or not task.strip():
            raise AgentOutputError(f"Action item {idx} is missing its task text.")
        if not isinstance(evidence, str) or not evidence.strip():
            raise AgentOutputError(f"Action item {idx} has no evidence quote; refusing to keep an unsupported task.")
        priority = str(item.get("priority", "unknown")).lower()
        if priority not in {"high", "medium", "low", "unknown"}:
            priority = "unknown"
        owner = item.get("owner")
        due_date = item.get("due_date")
        owner = owner.strip() if isinstance(owner, str) and owner.strip() else None
        due_date = due_date.strip() if isinstance(due_date, str) and due_date.strip() else None
        status = "assigned" if owner and due_date else "needs_clarification"
        cleaned.append({
            "task": task.strip(), "owner": owner, "due_date": due_date,
            "priority": priority, "evidence": evidence.strip(), "status": status,
        })
    data["action_items"] = cleaned
    return data


def analyze_notes(notes: str, model_call: Callable[[str, str], str] | None = None) -> dict[str, Any]:
    """Analyze notes with the configured model; model_call is injectable for tests."""
    if not isinstance(notes, str) or not notes.strip():
        raise ValueError("Meeting notes are empty. Paste notes or provide a text file.")
    if len(notes) > 100_000:
        raise ValueError("Notes exceed 100,000 characters. Split very long notes into smaller meetings.")
    call = model_call or (lambda system, user: chat_completion(system, user))
    user_prompt = "Extract the meeting details from the notes below. Return JSON only.\n\n<MEETING_NOTES>\n" + notes.strip() + "\n</MEETING_NOTES>"
    data = validate_output(_parse_json(call(SYSTEM_PROMPT, user_prompt)))
    for idx, item in enumerate(data["action_items"], start=1):
        if item["evidence"] not in notes:
            raise AgentOutputError(
                f"Action item {idx} contains an evidence quote that does not exactly appear in the original notes. "
                "The output was rejected rather than treated as grounded. Try again or use a different model."
            )
    return data
