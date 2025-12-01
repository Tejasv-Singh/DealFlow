from typing import List, Dict, Any

class CalendarMCP:
    def __init__(self):
        pass

    def get_free_slots(self, time_range: str) -> List[str]:
        print(f"[CalendarMCP] Checking free slots for {time_range}")
        return ["2025-01-15T10:00:00", "2025-01-15T14:00:00", "2025-01-16T11:00:00"]

    def create_event(self, slot: str, participants: List[str]) -> str:
        print(f"[CalendarMCP] Creating event at {slot} with {participants}")
        return "Event created"

    def propose_slots(self, email: str) -> str:
        slots = self.get_free_slots("next week")
        return f"Proposed slots sent to {email}: {slots}"
