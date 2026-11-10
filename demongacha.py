import requests
import uuid

from threading import Timer

me = None

me_endpoint = "https://demongacha.com/api/me"
open_pack_endpoint = "https://demongacha.com/api/packs/open"

cookie = "sid="

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

def printCardsData(cards):
    for card in cards:
        holo = str(card.get("holo"))
        tier = card.get("tier")

        if tier == "Legendary":
            print(f"Level name: {card.get("name")}, Tier: LEGENDARY LETS GO!, Holo: {holo}")
        elif tier == "Mythic":
            print(f"Level name: {card.get("name")}, Tier: WHAT THE HELL! (MYTHIC), Holo: {holo}")
        else:
            print(f"Level name: {card.get("name")}, Tier: {tier}, Holo: {holo}")
        

def totalPacks(ps):
    return ps.get("packs") + (ps.get("bonus") or 0)

def loadMe():
    global me
    request = requests.get(url=me_endpoint, headers=get_headers)  
    if request.status_code == 200:
        me = request.json()
        return True
    else:
        return False

def openPack(all=False):
    if (totalPacks(me.get("packState"))) < 1:
        return False
    
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
    request = requests.post(url=open_pack_endpoint, headers=post_headers, json=payload)
    if request.status_code == 200:
        return request.json()
    else:
        return False


def main_loop():
    load_me_passed = None

    try:
        if loadMe() == True:
            load_me_passed = True
        else:
            load_me_passed = False
    except requests.exceptions.JSONDecodeError:
        print("json decode failed for some reason")

    if load_me_passed == True:
        try:
            if (response := openPack(True)) != False:
                print(f"OPENED {response.get("opened")} card(s)")
                print("\n")
                printCardsData(response.get("cards"))
                print("\n\n\n")
        except requests.exceptions.JSONDecodeError:
            print("json decode failed for some reason")
    else:
        print("Load me failed or no cards for some reason")

    Timer(60, main_loop).start()

main_loop()
        

    
