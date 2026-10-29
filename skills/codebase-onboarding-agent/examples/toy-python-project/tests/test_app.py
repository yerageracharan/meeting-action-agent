from taskboard.app import summarize_tasks


def test_summary_counts_completed_tasks():
    assert summarize_tasks([{"status": "done"}, {"status": "todo"}]) == "1 of 2 tasks completed"


def test_summary_handles_no_tasks():
    assert summarize_tasks([]) == "0 of 0 tasks completed"
