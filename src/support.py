if __name__ == "__main__":
    print("Huh?")
    exit

from datetime import datetime
from colorama import *
import yaml

time = datetime.utcnow()
startup_date = f"{time.day}_{time.month}_{time.year}-{time.hour:02d}-{time.minute:02d}.{time.second:02d}.{time.microsecond:03d}"
startup_timestamp = time.timestamp()

path=f"{__file__}".replace("\\", "/")
path=path.replace("/support.py", "")

config=open(f"{path}/config.yaml")
config=yaml.load(config, Loader=yaml.FullLoader)
prefix=config.get("prefix")
cooldown=config.get("cooldown")

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