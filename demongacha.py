import requests
import uuid

from threading import Timer

FAIL = 400
SUPRESS_FEEDBACK = False

me_endpoint = "https://demongacha.com/api/me"
open_pack_endpoint = "https://demongacha.com/api/packs/open"

cookie = "sid="

if not cookie.startswith("sid="):
    temp = "sid=" + cookie
    cookie = temp

get_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/158.0.0.0 Safari/537.36",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9,te;q=0.8",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Cookie": cookie
    }

post_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/158.0.0.0 Safari/537.36",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9,te;q=0.8",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Cookie": cookie,   
        "Content-Type": "application/json"
    }

def printOpenPackReturn(response, wait_time):
    if not SUPRESS_FEEDBACK:    
        print(f"wait time: {wait_time}")
        print("\n")

        cards = response.get("cards")
        print(f"OPENED {response.get("opened")} card(s)")
        print("\n")
        for card in cards:
            holo = str(card.get("holo"))
            tier = card.get("tier")
        
            if tier == "Legendary":
                print(f"Level name: {card.get("name")}, Tier: LEGENDARY LETS GO!, Holo: {holo}")
            elif tier == "Mythic":
                print(f"Level name: {card.get("name")}, Tier: WHAT THE HELL! (MYTHIC), Holo: {holo}")
            else:
                print(f"Level name: {card.get("name")}, Tier: {tier}, Holo: {holo}")
        print("\n\n\n")
        

def totalPacks(ps):
    return ps.get("packs") + (ps.get("bonus") or 0)

def loadMe(session):
    try:
        request = session.get(url=me_endpoint, headers=get_headers)  
        if request.status_code == 200:
            return request.json()
        else:
            print("load me failed for some reason")
            return FAIL
    except requests.exceptions.JSONDecodeError:
        print("json decode failed for some reason")
        
def openPack(session, all=False):
    me = loadMe(session)
    if me == FAIL:
        return FAIL, 0

    wait_time = ((me.get("packState").get("nextPackAt") - me.get("packState").get("serverNow")) / 1000) + 1

    if (totalPacks(me.get("packState"))) < 1:
        return False, wait_time
    
    n = None
    if (all):
        n = totalPacks(me.get("packState"))
    else:
        n = 1

    requestId = str(uuid.uuid4())
    payload = {
        "count": n,
        "requestId": requestId
    }

    try:
        request = session.post(url=open_pack_endpoint, headers=post_headers, json=payload)
        if request.status_code == 200:
            return request.json(), wait_time
        else:
            print("open pack failed for some reason")
            return FAIL, 0
    except requests.exceptions.JSONDecodeError:
        print("json decode failed for some reason")
        return FAIL, 0

def main_loop():
    with requests.Session() as session:
        response, wait_time = openPack(session, True)
        if response == FAIL:
            return
        elif response != False and response != FAIL:
            printOpenPackReturn(response, wait_time)
        
        Timer(wait_time, main_loop).start()
    
main_loop()
        
