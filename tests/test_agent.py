import json
import pytest

from meetagent.agent import AgentOutputError, analyze_notes, validate_output
from meetagent.render import to_markdown

NOTES = "Priya will send the updated landing page copy to Marcus by Thursday."


def model_response(evidence=NOTES):
    return json.dumps({
        "meeting_summary": "Prepare and review landing page copy.",
        "decisions": ["No explicit launch decision in the supplied excerpt."],
        "action_items": [{
            "task": "Send the updated landing page copy to Marcus.",
            "owner": "Priya", "due_date": "Thursday", "priority": "medium",
            "evidence": evidence, "status": "assigned"
        }],
        "open_questions": [], "risks_or_blockers": [], "assumptions_to_confirm": []
    })


def test_extracts_grounded_action_item():
    result = analyze_notes(NOTES, model_call=lambda system, user: model_response())
    assert result["action_items"][0]["owner"] == "Priya"
    assert result["action_items"][0]["due_date"] == "Thursday"
    assert result["action_items"][0]["status"] == "assigned"


def test_rejects_evidence_not_present_in_notes():
    with pytest.raises(AgentOutputError, match="does not exactly appear"):
        analyze_notes(NOTES, model_call=lambda system, user: model_response("Marcus will launch on Monday."))


def test_missing_owner_or_deadline_needs_clarification():
    data = {"meeting_summary": "", "decisions": [], "action_items": [{
        "task": "Write FAQ", "owner": None, "due_date": None, "priority": "unknown",
        "evidence": "We discussed adding a customer FAQ.", "status": "assigned"
    }], "open_questions": [], "risks_or_blockers": [], "assumptions_to_confirm": []}
    cleaned = validate_output(data)
    assert cleaned["action_items"][0]["status"] == "needs_clarification"


def test_markdown_includes_evidence_and_status():
    result = analyze_notes(NOTES, model_call=lambda system, user: model_response())
    report = to_markdown(result)
    assert "Evidence from notes" in report
    assert "Thursday" in report
    assert "Assigned" in report


def test_empty_notes_are_rejected():
    with pytest.raises(ValueError, match="empty"):
        analyze_notes("   ", model_call=lambda system, user: "{}")


def test_validate_output_rejects_non_text_decision_and_risk_entries():
    invalid = {
        "meeting_summary": "Summary",
        "decisions": [{"decision": "launch"}],
        "action_items": [],
    }
    with pytest.raises(AgentOutputError, match="decisions item 1"):
        validate_output(invalid)


def test_validate_output_requires_object():
    with pytest.raises(AgentOutputError, match="JSON object"):
        validate_output(["not", "an", "object"])


def test_markdown_escapes_untrusted_meeting_text():
    report = to_markdown({
        "meeting_summary": "<script>alert(1)</script> [launch](https://example.com)",
        "decisions": ["# Do not turn this into a heading"],
        "action_items": [{
            "task": "[Open link](https://example.com)",
            "owner": "Priya_*",
            "due_date": "Thursday",
            "priority": "medium",
            "status": "assigned",
            "evidence": "`raw code`",
        }],
        "open_questions": ["<img src=x onerror=alert(1)>"],
        "risks_or_blockers": [],
        "assumptions_to_confirm": [],
    })
    assert "&lt;script&gt;" in report
    assert r"\[launch\]" in report
    assert r"\# Do not turn this into a heading" in report
    assert r"\[Open link\]" in report
    assert "&lt;img" in report
