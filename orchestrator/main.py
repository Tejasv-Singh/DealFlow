import sys
import os
import time
import threading

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dealflow.db.db_manager import DBManager
from dealflow.agents.campaign_manager import CampaignManager

def seed_data(db: DBManager):
    sponsors = db.get_all_sponsors()
    if not sponsors:
        print("Seeding test sponsors...")
        db.add_sponsor("Acme Corp", "https://acme.com")
        db.add_sponsor("Globex", "https://globex.com")
        db.add_sponsor("Soylent Corp", "https://soylent.com")

def main():
    print("Starting DealFlow Autonomous System...")
    db = DBManager()
    seed_data(db)
    
    manager = CampaignManager()
    
    try:
        manager.start(interval=5)
    except KeyboardInterrupt:
        print("Stopping system...")

if __name__ == "__main__":
    main()
