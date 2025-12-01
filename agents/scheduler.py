from ..mcp.calendar import CalendarMCP
from ..db.db_manager import DBManager

class SchedulerAgent:
    def __init__(self, db: DBManager):
        self.db = db
        self.calendar = CalendarMCP()

    def schedule_meeting(self, sponsor_id: int, sponsor_email: str):
        print(f"[SchedulerAgent] Scheduling for {sponsor_email}")
        
        # Propose slots
        proposal = self.calendar.propose_slots(sponsor_email)
        self.db.log_event(sponsor_id, "SchedulerAgent", "Slots Proposed", proposal)
        
        # In a real flow, we'd wait for a reply selecting a slot.
        # Here we simulate a confirmation.
        selected_slot = "2025-01-15T10:00:00"
        self.calendar.create_event(selected_slot, [sponsor_email])
        
        self.db.update_sponsor_status(sponsor_id, "Won") # Or Negotiating -> Won
        self.db.log_event(sponsor_id, "SchedulerAgent", "Meeting Confirmed", f"Booked for {selected_slot}")
