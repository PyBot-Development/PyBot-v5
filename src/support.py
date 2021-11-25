"""
Discord Pybot Support
~~~~~~~~~~~~~~~~~

Support File with stuff

:copyright: (c) 2021-2021 M2rsho
:license: MIT, see LICENSE for more details.

"""

if __name__ == "__main__":
    print("Huh?")
    exit

from datetime import datetime
from colorama import *
import yaml
from random import choice
from PIL import Image, ImageFont, ImageDraw
from gtts import gTTS
from datetime import datetime
import requests
from io import BytesIO

time = datetime.utcnow()
startup_date = f"{time.day}_{time.month}_{time.year}-{time.hour:02d}-{time.minute:02d}.{time.second:02d}.{time.microsecond:03d}"
startup_timestamp = time.timestamp()

path = f"{__file__}".replace("\\", "/")
path = path.replace("/support.py", "")

config = open(f"{path}/config.yaml")
config = yaml.load(config, Loader=yaml.FullLoader)
prefix = config.get("prefix")
cooldown = config.get("cooldown")

with open(f"{path}/data/alts.txt") as file:
    alts = file.readlines()


async def getAlt():
    return choice(alts)


def log(date, type, arg1, arg2):
    time = f"{date.hour:02d}:{date.minute:02d}:{date.second:02d}"
    if type == "COMMAND":
        print(
            f"""{Back.BLACK}{Fore.LIGHTYELLOW_EX}{time}{Style.RESET_ALL} [{Fore.LIGHTGREEN_EX}INFO{Style.RESET_ALL}] {Fore.LIGHTYELLOW_EX}{arg1}{Style.RESET_ALL}: {Fore.LIGHTGREEN_EX}Invoked Command{Style.RESET_ALL}: '{Fore.LIGHTWHITE_EX}{Back.LIGHTBLACK_EX}{arg2}{Style.RESET_ALL}'{Style.RESET_ALL}""")
    else:
        print(
            f"""{Back.BLACK}{Fore.LIGHTYELLOW_EX}{time}{Style.RESET_ALL} [{Fore.LIGHTGREEN_EX}{type}{Style.RESET_ALL}] {Fore.LIGHTYELLOW_EX}{arg1}{Style.RESET_ALL}: {Fore.LIGHTGREEN_EX}{arg2}{Style.RESET_ALL}""")

    with open(f"{path}/logs/{startup_date}.log", "a+") as file:
        type = type if type != "COMMAND" else "INFO"
        file.write(f"{time} [{type}] {arg1}: {arg2}\n")


class colours:
    default = 0x7842ff
    red = 0xff7777
    green = 0x77dd77
    yellow = 0xeb9226
class processing:
    async def GENERATE_CAN(name, text, bottom_text=""):
        if len(text) > 90 or len(bottom_text) > 90:
            return False

        def add_n(text, after: int):
            x = ""
            for i, letter in enumerate(text):
                if i % after == 0:
                    x += '\n'
                x += letter
            x = x[1:]
            return x

        text = add_n(text, 20)
        bottom_text = add_n(bottom_text, 30)

        W, H = (582, 975)
        font_ = ImageFont.truetype(
            f"{path}/data/resources/fonts/NotoSansJP-Medium.otf", 50)
        font__ = ImageFont.truetype(
            f"{path}/data/resources/fonts/NotoSansJP-Medium.otf", 30)
        img = Image.open(f"{path}/data/resources/templates/can_template.png")

        draw = ImageDraw.Draw(img)
        w, h = draw.textsize(text, font=font_)
        w2, h2 = draw.textsize(bottom_text, font=font__)

        draw.text(((W-w)/2, 300-(h/2)), text, (255, 255, 0), font=font_)
        draw.text(((W-w2)/2, 700-(h2/2)), bottom_text, (0, 0, 0), font=font__)

        img.save(f"{path}/data/temp/{name}.png")
        return(f"{path}/data/temp/{name}.png")

    async def tts(txt, languag):
        date = str(datetime.utcnow()).replace(":", "-")
        speech = gTTS(text=u'{}'.format(txt), lang=languag, slow=False)
        speech.save(f"{path}/data/temp/{date}.mp3")
        return(f"{path}/data/temp/{date}.mp3")

    async def overlay(background_url, foreground, user_id):
        response=requests.get(background_url)
        background = Image.open(BytesIO(response.content)).resize((1024, 1024), Image.ANTIALIAS).convert("RGBA")

        foreground = Image.open(foreground).resize((1024, 1024), Image.ANTIALIAS).convert("RGBA")
        background.paste(foreground, (0, 0), foreground)
        background.save(f"{path}/data/temp/{user_id}.png")
        return(f"{path}/data/temp/{user_id}.png")

    async def overlay_position(background_url, foreground, xy, xsys, user_id, image_size):
        img = Image.new('RGBA', image_size, (255, 0, 0, 0))

        response=requests.get(background_url)
        background = Image.open(BytesIO(response.content)).resize(xsys, Image.ANTIALIAS).convert("RGBA")

        foreground = Image.open(foreground).convert("RGBA")

        img.paste(background, xy, background)
        img.paste(foreground, (0, 0), foreground)

        img.save(f"{path}/data/temp/{user_id}.png")
        return(f"{path}/data/temp/{user_id}.png")
        
from requests import Session
import json

sfa_url = 'https://api.mojang.com/user/security/challenges'

class check():
    def __init__(self, loginpassword):
        self.result = self.check_alt(loginpassword)

    def secure_check(self, token):
        session = Session()
        headers = {'Pragma': 'no-cache', "Authorization": f"Bearer {token}"}
        z = session.get(url=sfa_url, headers=headers).text
        return z == '[]'

    def check_alt(self, loginpassword):
        session = Session()
        alt = loginpassword.split(":", 1)
        jsonheaders = {"Content-Type": "application/json", 'Pragma': 'no-cache'}
        email = str(alt[0]).replace("\n", "")
        password = str(alt[1]).replace("\n", "")
        payload = ({
            "agent": {                              
                "name": "Minecraft",                
                "version": 1                                                 
            },
            "username": f"{email}",                                  
            "password": f"{password}",  
            "requestUser": True
        })
        bad = 'Invalid credentials'
        answer = session.post(url="https://authserver.mojang.com/authenticate", json=payload, headers=jsonheaders, timeout=10000)
        if (
            bad in answer.text
            or 'Client sent too many requests too fast.' in answer.text
        ):
            return json.loads(answer.text)["errorMessage"]
        ajson = answer.json()
        username = ajson['availableProfiles'][0]['name']
        token = ajson['accessToken']
        uuid = ajson['availableProfiles'][0]["id"]
        securec = self.secure_check(token)
        return f'''
Original Combo: `{loginpassword}`
Username: `{username}`
UUID: `{uuid}`
Email: `{email}`
Password: `{password}`
Sfa: `{securec}`
'''

import sqlite3

class database:
    def __init__(self, path):
        self.con = sqlite3.connect(path)
        self.cur = self.con.cursor()

        self.cur.execute('''CREATE TABLE IF NOT EXISTS users (id integer, username text, balance integer, banned integer, admin integer, reason text, banned_by text, date text, duration integer)''')

    async def getUser(self, user):
        u = self.cur.execute(f'''SELECT * FROM users WHERE id={user.id}''').fetchone()
        if u is None:
            self.cur.execute(f'INSERT INTO users VALUES (?, ?, 10000, 0, 0, "None", "None", "None", 0)', (user.id, str(user), ))
            self.con.commit()
        return self.cur.execute(f'''SELECT * FROM users WHERE id="{user.id}"''').fetchone()

    async def getAllUsers(self):
        return self.cur.execute(f'''SELECT * FROM users''').fetchall()

    def getAllUsers_sync(self):
        return self.cur.execute(f'''SELECT * FROM users''').fetchall()
        
    async def setBalance(self, user, balance: int):
        await self.getUser(user)
        self.cur.execute(f'''UPDATE users SET balance={balance} WHERE id={user.id}''')
        self.con.commit()

    async def addBalance(self, user, balance: int):
        balance = await self.getBalance(user) + balance
        self.cur.execute(f'''UPDATE users SET balance={balance} WHERE id={user.id}''')
        self.con.commit()

    async def removebalance(self, user, balance: int):
        balance = await self.getBalance(user) - balance
        self.cur.execute(f'''UPDATE users SET balance={balance} WHERE id={user.id}''')
        self.con.commit()

    async def getBalance(self, user):
        balance = (await self.getUser(user))[2]
        return balance 

    async def banUser(self, user , reason, date, author):
        await self.getUser(user)
        self.cur.execute(f'''UPDATE users SET banned=1, reason=?, date=?, banned_by=? WHERE id={user.id}''', (str(reason), str(date), str(author)))
        self.con.commit()

    async def unbanUser(self, user):
        await self.getUser(user)
        self.cur.execute(f'''UPDATE users SET banned=0, reason="None", date="None", banned_by="None" WHERE id={user.id}''')
        self.con.commit()

    async def opUser(self, user):
        await self.getUser(user)
        self.cur.execute(f'''UPDATE users SET admin=1 WHERE id={user.id}''')
        self.con.commit()

    async def deopUser(self, user):
        await self.getUser(user)
        self.cur.execute(f'''UPDATE users SET admin=0 WHERE id={user.id}''')
        self.con.commit()

    async def getBanned(self):
        u = list(self.cur.execute(f'''SELECT id FROM users WHERE banned="1"''').fetchall())
        banned = [list(item) for item in u]
        return banned

    async def getOps(self):
        u = list(self.cur.execute(f'''SELECT id FROM users WHERE admin="1"''').fetchall())
        ops = [list(item) for item in u]
        return ops


def convertToBitcoin(amount, currency):
    data = requests.get("http://api.bitcoincharts.com/v1/weighted_prices.json")
    bitcoins = data.json()
    converted = amount / float(bitcoins[currency]["24h"])
    return converted

globalData = database(path=f"{path}/data/database.db")