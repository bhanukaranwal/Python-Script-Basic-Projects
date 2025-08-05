# Context-Aware Productivity Assistant — main.py

import os
import datetime
from typing import List

# Simulated modules for Calendar, To-do, and File status

class CalendarEvent:
    def __init__(self, title, start_time, end_time, location=None):
        self.title = title
        self.start_time = start_time
        self.end_time = end_time
        self.location = location

    def is_current(self):
        now = datetime.datetime.now()
        return self.start_time <= now <= self.end_time

class TodoItem:
    def __init__(self, description, due_date=None, complete=False):
        self.description = description
        self.due_date = due_date
        self.complete = complete

    def is_due_today(self):
        if self.due_date:
            return self.due_date.date() == datetime.datetime.now().date()
        return False

class FileStatus:
    def __init__(self, filepath, last_accessed):
        self.filepath = filepath
        self.last_accessed = last_accessed

    def is_recently_used(self):
        delta = datetime.datetime.now() - self.last_accessed
        return delta.days <= 1

class ProductivityAssistant:
    def __init__(self, calendar_events: List[CalendarEvent], todo_items: List[TodoItem], open_files: List[FileStatus]):
        self.calendar_events = calendar_events
        self.todo_items = todo_items
        self.open_files = open_files

    def current_focus(self):
        current_events = [e for e in self.calendar_events if e.is_current()]
        recent_files = [f for f in self.open_files if f.is_recently_used()]
        due_todos = [t for t in self.todo_items if not t.complete and t.is_due_today()]
        return {
            "current_events": current_events,
            "recent_files": recent_files,
            "due_todos": due_todos
        }

    def suggest_next_action(self):
        status = self.current_focus()
        messages = []

        if status['current_events']:
            for event in status['current_events']:
                messages.append(f"You have a meeting now: '{event.title}' at {event.location or 'unknown location'}.")

        if status['due_todos']:
            for todo in status['due_todos']:
                messages.append(f"Task due today: {todo.description}")

        if not messages:
            messages.append("No urgent items. Consider reviewing your to-do list or taking a break.")

        if status['recent_files']:
            last_file = max(status['recent_files'], key=lambda f: f.last_accessed)
            messages.append(f"You recently worked on: {os.path.basename(last_file.filepath)}")

        return messages

if __name__ == '__main__':
    now = datetime.datetime.now()
    events = [
        CalendarEvent("Team Meeting", now - datetime.timedelta(minutes=15), now + datetime.timedelta(minutes=45), "Zoom"),
        CalendarEvent("Project Planning", now + datetime.timedelta(hours=2), now + datetime.timedelta(hours=3))
    ]
    todos = [
        TodoItem("Finish report", now, False),
        TodoItem("Email client", now + datetime.timedelta(days=1), False),
        TodoItem("Backup files", None, True)
    ]
    files = [
        FileStatus("/path/to/code.py", now - datetime.timedelta(hours=1)),
        FileStatus("/path/to/notes.txt", now - datetime.timedelta(days=2))
    ]

    assistant = ProductivityAssistant(events, todos, files)
    suggestions = assistant.suggest_next_action()

    print("Productivity Assistant Suggestions:")
    for msg in suggestions:
        print(f"- {msg}")

# To extend:
# - Integrate with real calendar APIs (Google Calendar, Outlook, etc.)
# - Connect to OS filesystem and editors for open/recent files
# - Add a natural language chatbot interface
# - Implement notification popups, distraction blockers, or Pomodoro timer tools
