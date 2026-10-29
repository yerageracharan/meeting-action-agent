"""Core task summary logic for the Tiny Taskboard demo."""


def summarize_tasks(tasks: list[dict[str, str]]) -> str:
    """Return a short summary based on a list of task dictionaries."""
    total = len(tasks)
    done = sum(1 for task in tasks if task.get("status") == "done")
    return f"{done} of {total} tasks completed"
