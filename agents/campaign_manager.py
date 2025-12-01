import time
from ..db.db_manager import DBManager
from .researcher import ResearchAgent
from .copywriter import CopywriterAgent

from .ambient import AmbientAgent

class CampaignManager:
    def __init__(self):
        self.db = DBManager()
        self.researcher = ResearchAgent(self.db)
        self.copywriter = CopywriterAgent(self.db)
        self.ambient = AmbientAgent(self.db)

    def run_cycle(self):
        print("[CampaignManager] Starting cycle...")
        
        # 0. Ambient Monitoring
        self.ambient.monitor()
        
        # 1. Identify -> Research
        identified = self.db.get_sponsors_by_status("Identified")
        for sponsor in identified:
            print(f"Assigning ResearchAgent to {sponsor['company_name']}")
            self.db.update_sponsor_status(sponsor['id'], "Researching")
            self.researcher.research_sponsor(sponsor['id'], sponsor['company_name'], sponsor['website'])
            # After research, we could immediately trigger copywriter or wait for next cycle.
            # Let's trigger immediately for speed in this demo.
            
            # Check if research exists (it should now)
            # In a real async system, we'd check DB.
            
            # 2. Researching -> Contacted (Draft -> Send)
            # For this demo, we'll assume "Researching" means "Ready for Copy" if artifact exists.
            
        # Re-fetch to see who is in Researching
        researching = self.db.get_sponsors_by_status("Researching")
        for sponsor in researching:
            # Check if artifact exists
            # We need a method to check artifacts. For now, assume if status is Researching, we try to copywrite.
            # But we just set it to Researching above.
            
            # Let's just do it:
            print(f"Assigning CopywriterAgent to {sponsor['company_name']}")
            
            research_content = self.db.get_research_artifact(sponsor['id'])
            if not research_content:
                print(f"No research found for {sponsor['company_name']}, skipping...")
                continue

            email = self.copywriter.generate_outreach(sponsor['id'], sponsor['company_name'], research_content)
            
            # Simulate sending
            print(f"Sending email to {sponsor['contact_email']}...")
            self.db.update_sponsor_status(sponsor['id'], "Contacted")
            self.db.log_event(sponsor['id'], "CampaignManager", "Email Sent", "Outreach sent via Gmail MCP.")

    def start(self, interval=10):
        while True:
            self.run_cycle()
            time.sleep(interval)

if __name__ == "__main__":
    manager = CampaignManager()
    manager.run_cycle()
