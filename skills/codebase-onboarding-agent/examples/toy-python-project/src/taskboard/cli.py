"""Command-line entry point for the Tiny Taskboard demo."""
from .app import summarize_tasks


def main() -> None:
    tasks = [
        {"title": "Read the README", "status": "done"},
        {"title": "Run the first test", "status": "todo"},
    ]
    print(summarize_tasks(tasks))


if __name__ == "__main__":
    main()
