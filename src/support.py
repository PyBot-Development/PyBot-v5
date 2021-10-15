if __name__ == "__main__":
    print("Huh?")
    #exit

from datetime import datetime
from colorama import *
import yaml
from random import choice
from PIL import Image, ImageFont, ImageDraw
from gtts import gTTS
from datetime import datetime


time = datetime.utcnow()
startup_date = f"{time.day}_{time.month}_{time.year}-{time.hour:02d}-{time.minute:02d}.{time.second:02d}.{time.microsecond:03d}"
startup_timestamp = time.timestamp()

path=f"{__file__}".replace("\\", "/")
path=path.replace("/support.py", "")

config=open(f"{path}/config.yaml")
config=yaml.load(config, Loader=yaml.FullLoader)
prefix=config.get("prefix")
cooldown=config.get("cooldown")

with open("data/alts.txt") as file:
    alts = file.readlines()
async def getAlt():
    return choice(alts)

def log(date, type, arg1, arg2):
    time = f"{date.hour:02d}:{date.minute:02d}:{date.second:02d}"
    if type == "COMMAND":
        print(f"""{Back.BLACK}{Fore.LIGHTYELLOW_EX}{time}{Style.RESET_ALL} [{Fore.LIGHTGREEN_EX}INFO{Style.RESET_ALL}] {Fore.LIGHTYELLOW_EX}{arg1}{Style.RESET_ALL}: {Fore.LIGHTGREEN_EX}Invoked Command{Style.RESET_ALL}: '{Fore.LIGHTWHITE_EX}{Back.LIGHTBLACK_EX}{arg2}{Style.RESET_ALL}'{Style.RESET_ALL}""")
    else:
        print(f"""{Back.BLACK}{Fore.LIGHTYELLOW_EX}{time}{Style.RESET_ALL} [{Fore.LIGHTGREEN_EX}{type}{Style.RESET_ALL}] {Fore.LIGHTYELLOW_EX}{arg1}{Style.RESET_ALL}: {Fore.LIGHTGREEN_EX}{arg2}{Style.RESET_ALL}""")

    with open(f"{path}/logs/{startup_date}.log", "a+") as file:
        type = type if type != "COMMAND" else "INFO"
        file.write(f"{time} [{type}] {arg1}: {arg2}\n")

class colours:
    default = 0x7842ff
    red = 0xffc7c7

class processing:
    async def GENERATE_CAN(name, text, bottom_text=""):
        if len(text) > 90 or len(bottom_text) > 90:
            return False
        def add_n(text, after:int):
            x = ""
            for i, letter in enumerate(text):
                if i % after == 0:
                    x += '\n'
                x += letter
            x = x[1:]
            return x

        text = add_n(text, 20)
        bottom_text = add_n(bottom_text, 30)

        W, H = (582,975)
        font_ = ImageFont.truetype(f"{path}/data/resources/fonts/NotoSansJP-Medium.otf", 50)
        font__ = ImageFont.truetype(f"{path}/data/resources/fonts/NotoSansJP-Medium.otf", 30)
        img = Image.open(f"{path}/data/resources/templates/can_template.png")

        draw = ImageDraw.Draw(img)
        w, h = draw.textsize(text, font=font_)
        w2, h2 = draw.textsize(bottom_text, font=font__)

        draw.text(((W-w)/2, 300-(h/2)), text, (255,255,0), font=font_)
        draw.text(((W-w2)/2, 700-(h2/2)), bottom_text, (0,0,0), font=font__)

        img.save(f"{path}/data/temp/{name}.png")
        return(f"{path}/data/temp/{name}.png")

    async def tts(txt, languag):
        date = str(datetime.utcnow()).replace(":", "-")
        speech = gTTS(text = u'{}'.format(txt), lang = languag, slow = False)
        speech.save(f"{path}/data/temp/{date}.mp3")
        return(f"{path}/data/temp/{date}.mp3")