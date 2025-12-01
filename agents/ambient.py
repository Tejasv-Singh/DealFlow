from ..mcp.gmail import GmailMCP
from ..db.db_manager import DBManager
from .scheduler import SchedulerAgent

class AmbientAgent:
    def __init__(self, db: DBManager):
        self.db = db
        self.gmail = GmailMCP()
        self.scheduler = SchedulerAgent(db)

    def monitor(self):
        print("[AmbientAgent] Checking inbox...")
        messages = self.gmail.read_inbox()
        
        for msg in messages:
            # Logic to parse message and decide action
            # For demo, we assume the message is a "Yes" from a sponsor
            print(f"Processing message from {msg['from']}: {msg['snippet']}")
            
            # Find sponsor by email (mock lookup)
            # sponsor = self.db.find_sponsor_by_email(msg['from'])
            # For now, just pick the first 'Contacted' sponsor
            contacted = self.db.get_sponsors_by_status("Contacted")
            if contacted:
                sponsor = contacted[0]
                print(f"Matched to sponsor: {sponsor['company_name']}")
                
                if "yes" in msg['snippet'].lower():
                    print("Positive reply detected! Triggering Scheduler.")
                    self.db.update_sponsor_status(sponsor['id'], "Negotiating")
                    self.scheduler.schedule_meeting(sponsor['id'], sponsor['contact_email'] or "test@example.com")
                elif "later" in msg['snippet'].lower():
                    print("Snoozing until Q2...")
                    # Add to long term memory
                    self.db.log_event(sponsor['id'], "AmbientAgent", "Snoozed", "Added to Q2 memory")
