import requests
import time
from modules.database import Session, GameQueue, GameDetails

def format_steam_price(game_data, price_key):
    # Safely handles 'is_free' games and missing price_overview
    # Returns a formatted string like '19.99 USD' or '0.00 FREE'
    if game_data.get('is_free') is True:
        return "0.00 FREE"
    
    p_ov = game_data.get('price_overview')
    if not p_ov:
        return None
        
    price_raw = p_ov.get(price_key)
    currency = p_ov.get('currency', 'USD')
    
    if price_raw is None:
        return f"0.00 {currency}"
        
    p_str = str(price_raw)
    # Handle edge cases where price might be less than 3 digits (e.g., 50 cents)
    if len(p_str) <= 2:
        return f"0.{p_str.zfill(2)} {currency}"
    
    return f"{p_str[:-2]}.{p_str[-2:]} {currency}"

def fetch_official_details():
    session = Session()
    # Fetch all games that are still 'pending'
    queue = session.query(GameQueue).filter(GameQueue.status == 'pending').all()
    
    total = len(queue)
    print(f"--- Starting Extraction for {total} games ---")

    for index, entry in enumerate(queue):
        appid = entry.appid
        url = f"https://store.steampowered.com/api/appdetails?appids={appid}&cc=de&l=english"
        
        try:
            response = requests.get(url, timeout=15)
            
            # Handle Rate Limiting (HTTP 429)
            if response.status_code == 429:
                print("\n[!] Rate limit hit. Sleeping for 90 seconds...")
                time.sleep(90)
                continue

            data_json = response.json()
            
            if data_json and str(appid) in data_json and data_json[str(appid)]['success']:
                g = data_json[str(appid)]['data']
                
                # Extracting lists/dicts safely
                devs = g.get('developers', [])
                pubs = g.get('publishers', [])
                cats = g.get('categories', [])
                gens = g.get('genres', [])
                ss   = g.get('screenshots', [])
                recs = g.get('recommendations', {})

                # Build the robust detail object
                detail = GameDetails(
                    appid = appid,
                    name = g.get('name'),
                    is_free = g.get('is_free'),
                    detailed_description = g.get('detailed_description'),
                    short_description = g.get('short_description'),
                    header_image = g.get('header_image'),
                    website = g.get('website'),
                    developers = ", ".join(devs) if devs else None,
                    publishers = ", ".join(pubs) if pubs else None,
                    initial_price = format_steam_price(g, 'initial'),
                    final_price = format_steam_price(g, 'final'),
                    categories = ", ".join([c['description'] for c in cats]) if cats else None,
                    genres = ", ".join([gen['description'] for gen in gens]) if gens else None,
                    screenshot1 = ss[0]['path_full'] if len(ss) > 0 else None,
                    screenshot2 = ss[1]['path_full'] if len(ss) > 1 else None,
                    screenshot3 = ss[2]['path_full'] if len(ss) > 2 else None,
                    recommendations = recs.get('total'),
                    release_date = g.get('release_date', {}).get('date'),
                    background_image = g.get('background')
                )
                
                session.merge(detail)
                entry.status = 'processed'
            else:
                # If success is False, the app might be a video, hardware, or region-locked
                entry.status = 'skipped'
            
            # Commit changes every iteration to ensure data isn't lost
            session.commit()
            
            # Simple Progress Tracking
            percent = ((index + 1) / total) * 100
            print(f"[{percent:.1f}%] Processed: {entry.name} ({appid})")

        except Exception as e:
            print(f"\n[!] Error on {appid}: {e}")
            session.rollback()
        
        # Polite delay to respect Steam's API policy
        time.sleep(1.5)

if __name__ == "__main__":
    fetch_official_details()
