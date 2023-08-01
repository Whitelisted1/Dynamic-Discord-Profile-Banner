import requests
from time import time, sleep
from os.path import dirname, join

directory = dirname(__file__)

f = open(join(directory, "token"), "r")
DISCORD_BOT_TOKEN = f.read()
f.close()

def send_user_info_request(userID):
    r = requests.get(f"https://discord.com/api/v9/users/{userID}", headers={
        "Authorization": f"Bot {DISCORD_BOT_TOKEN}"
    })

    json = r.json()

    if r.status_code != 200:
        print(r.headers)
        print(r.status_code)
        print(json)

    if r.status_code == 400:
        return { "error": { "text": "Invalid userID provided", "code": 400 } }
    
    if r.status_code == 401:
        return { "error": { "text": "Server is unauthorized. Please contact me.", "code": 401 } }

    if r.status_code == 429:
        print("Being rate limited, waiting for rate limit to refresh")
        sleep(float(json['retry_after']))
        print("Sending new request ...")
        return send_user_info_request(userID)
    
    if r.status_code != 200:
        if "code" in json:
            return { "error": { "text": f"Unknown error, Discord gave error {json['code']}", "code": r.status_code } }
        
        return { "error": { "text": "Unknown error", "code": r.status_code } }
    
    return json

class cache:
    # cache_time = 60 * 60 # 1 hour
    cache_time = 60 * 60 * 24 # 1 day
    local_cache = {}

    def add_to_cache(userID, value):
        value.expires_at = time() + cache.cache_time
        # value.expires_at = time() + 1
        cache.local_cache[userID] = value
    
    def grab_from_cache(userID):
        if userID not in cache.local_cache:
            return None
        
        if cache.local_cache[userID].expires_at < time():
            del cache.local_cache[userID]
            return None
        
        return cache.local_cache[userID]

class discord_user:
    def __init__(self, user_object):
        self.id = user_object["id"]
        # user has migrated to handles
        if user_object["global_name"] != None:
            self.displayname = user_object["global_name"]
            self.username = user_object["username"]
            self.discriminator = ""
        else:
            self.displayname = user_object["username"]
            self.username = f'{user_object["username"]}#{user_object["discriminator"]}'
            self.discriminator = user_object["discriminator"]

        if user_object["banner_color"] == None:
            self.banner_color = "#000000"
        else:
            self.banner_color = user_object["banner_color"]

        self.avatar = user_object["avatar"]
        self.banner = user_object["banner"]
        self.public_flags = user_object["public_flags"]
        self.isBot = "bot" in user_object and user_object["bot"]
    
    def add_to_cache(self):
        cache.add_to_cache(self.id, self)
        return self
    
    def get_user_badges(self):

        # return ["STAFF", "PARTNER", "HYPESQUAD", "BUG_HUNTER_LEVEL_1", "HYPESQUAD_BRAVERY", "HYPESQUAD_BRILLIANCE", "HYPESQUAD_BALANCE", "PREMIUM_EARLY_SUPPORTER", "TEAM_PSEUDO_USER", "BUG_HUNTER_LEVEL_2", "VERIFIED_BOT", "VERIFIED_DEVELOPER", "CERTIFIED_MODERATOR", "BOT_HTTP_INTERACTIONS", "ACTIVE_DEVELOPER"]

        flags = self.public_flags
        tags = []
        
        if flags & (1 << 0):
            tags.append("STAFF")
        if flags & (1 << 1):
            tags.append("PARTNER")
        if flags & (1 << 2):
            tags.append("HYPESQUAD")
        if flags & (1 << 3):
            tags.append("BUG_HUNTER_LEVEL_1")
        if flags & (1 << 6):
            tags.append("HYPESQUAD_BRAVERY")
        if flags & (1 << 7):
            tags.append("HYPESQUAD_BRILLIANCE")
        if flags & (1 << 8):
            tags.append("HYPESQUAD_BALANCE")
        if flags & (1 << 9):
            tags.append("PREMIUM_EARLY_SUPPORTER")
        if flags & (1 << 10):
            tags.append("TEAM_PSEUDO_USER")
        if flags & (1 << 14):
            tags.append("BUG_HUNTER_LEVEL_2")
        if flags & (1 << 16):
            tags.append("VERIFIED_BOT")
        if flags & (1 << 17):
            tags.append("VERIFIED_DEVELOPER")
        if flags & (1 << 18):
            tags.append("CERTIFIED_MODERATOR")
        if flags & (1 << 19):
            tags.append("BOT_HTTP_INTERACTIONS")
        if flags & (1 << 22):
            tags.append("ACTIVE_DEVELOPER")
            
        return tags

    def get_from_id(user_id):
        cached = cache.grab_from_cache(user_id)

        if cached is None:
            user_data = send_user_info_request(user_id)
            if "error" in user_data:
                return user_data

            return discord_user(user_data).add_to_cache()

        return cached

def get_user_data(userID):
    try:
        return discord_user.get_from_id(int(userID))
    except:
        return { "error": { "text": "Invalid userID provided", "code": 400 } }