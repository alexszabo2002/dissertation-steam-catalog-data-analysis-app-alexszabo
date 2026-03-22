import requests
import time
from modules.database import Session, GameQueue

def sync_popular_apps():
    session = Session()
    total_count = 0
    
    # We loop through pages 0 to 9 (10 pages total, ~1000 games per page)
    for page in range(0, 10):
        print(f"Requesting Page {page} from SteamSpy...")
        
        # Add the page parameter to the URL
        url = f"https://steamspy.com/api.php?request=all&page={page}"
        
        try:
            response = requests.get(url, timeout=15)
            data = response.json()
            
            if not data:
                print(f"No more data found on page {page}. Stopping...")
                break

            for appid, details in data.items():
                # Extract numeric owner estimate for your database if found (0 if not found)
                # SteamSpy returns a string like "10,000,000 .. 20,000,000"
                owners_str = details.get('owners', '0')
                
                new_app = GameQueue(
                    appid=int(appid), 
                    name=details.get('name', 'Unknown'),
                    owners=owners_str,
                    status='pending'
                )
                
                session.merge(new_app)
                total_count += 1
            
            # Commit after every page to save progress
            session.commit()
            print(f"Done with Page {page}. Total games in DB: approx. {total_count}")
            
            # Pause briefly between pages to be a "good citizen"
            time.sleep(2) 
            
        except Exception as e:
            print(f"Error on page {page}: {e}")
            break

    print(f"\nSuccess! Successfully added approximately {total_count} popular games to your queue.")

if __name__ == "__main__":
    sync_popular_apps()
