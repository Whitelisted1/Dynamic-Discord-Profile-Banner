from flask import Flask, request, Response, abort
from os.path import dirname, join, isdir, exists
import requests
import base64
from time import time

import discord_fetch_info

def encode_to_base64(content):
    return base64.b64encode(content).decode("utf-8")

directory = dirname(__file__)
app = Flask(__name__)

def getFile(file, mode="br"):
    f = open(join(directory, file), mode)
    contents = f.read()
    f.close()

    return contents

def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'  # Allow requests from any origin
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'  # Allow the Content-Type header
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'  # Allow the specified HTTP methods
    return response

@app.route("/assets/<path:path>")
def assets(path):
    response = Response(getFile(join(directory, "assets", path)))
    response = add_cors_headers(response)
    return response

@app.route("/getUserProfile/<userID>", methods=["GET"])
def home(userID):
    user = discord_fetch_info.get_user_data(userID)
    tags = user.get_user_badges()
    print(tags)

    r = requests.get(f"https://cdn.discordapp.com/avatars/{user.id}/{user.avatar}.webp?size=48")
    base64_decoded = encode_to_base64(r.content)

    text = getFile("template.svg", mode="r")
    text = text.replace("{{BASE64_ENCODED_PFP}}", base64_decoded)
    text = text.replace("{{DISCORD_DISPLAY_NAME}}", user.displayname).replace("{{DISCORD_USERNAME}}", user.username).replace("{{DISCORD_ID}}", user.id)

    # <image x="0" y="y" width="340px" height="48px" clip-path="url(#bannerClip)" href="data:image/webp;base64,{{BASE64_ENCODED_PROFILE_BANNER}}"></image>
    # <rect x="0" y="y" width="340px" height="48px" clip-path="url(#bannerClip)" fill="{{DISCORD_BANNER_COLOR}}"></rect>

    if user.banner is None:
        text = text.replace("{{DISCORD_PROFILE_BANNER}}", f'<rect x="0" y="y" width="340px" height="48px" clip-path="url(#bannerClip)" fill="{user.banner_color}"></rect>')
    else:
        r = requests.get(f"https://cdn.discordapp.com/banners/{user.id}/{user.banner}.webp?size=480") # ?size=480
        base64_decoded = encode_to_base64(r.content)

        text = text.replace("{{DISCORD_PROFILE_BANNER}}", f'<image id="profileBanner" x="0" y="0" clip-path="url(#bannerClip)" href="data:image/webp;base64,{base64_decoded}"></image>')

    tagReplaceText = ""
    currentX = 90

    if user.isBot:
        tagReplaceText += f'''<rect id="bannerClipRect" x="{currentX-1}%" y="64" width="28px" height="17px" rx="2px" fill="#5b65eb"/>
        <text x="{currentX}%" y="77" fill="white" font-size="12">BOT</text>'''
        currentX -= 10
        
    numTags = 0
    for tag in tags:
        # extension = discord_fetch_info.badgeNameToFileExtension[tag]
        extension = "png"
        path = join(directory, "assets", "profile_badges", f"{tag}.{extension}")
        if not exists(path):
            continue # Ignore this badge since we don't have an image of it

        numTags += 1

        f = open(path, "br")
        contents = f.read()
        f.close()

        # if extension == "svg":
        #     tagReplaceText += contents.decode().replace("{{STARTING_POS}}", f"{currentX},60")
        #     continue

        tagReplaceText += f'<image x="{currentX}%" y="60" height="24px" width="24px" href="data:image/webp;base64,{encode_to_base64(contents)}"></image>'
        currentX -= 7
    
    tagReplaceText = f'<rect x="{currentX+6}%" y="60" width="{(numTags * 24) + (6 * (numTags != 0))}px" height="24px" rx="4px" fill="#101215"/>' + tagReplaceText
    
    text = text.replace("{{PROFILE_BADGES}}", tagReplaceText)

    response = Response(text)
    response = add_cors_headers(response)
    
    response.headers['Content-Type'] = 'image/svg+xml'  # Set the correct Content-Type

    time_until_expiration = user.expires_at - time()
    response.headers['Cache-Control'] = f'max-age={time_until_expiration}' # Tell the website to not clear cache until we clear ours
    return response

if __name__ == "__main__":
    app.run(port=80, host="0.0.0.0")