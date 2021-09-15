#Dank Memer Autofarm, v2
#Made by wHo#6933
#Report any error to me hehe, try and take a screenshot of the error too

"""
===== Available Functions =====
1. Auto beg
2. Auto dig
3. Auto fish
4. Auto hunt
5. Auto deposit
6. Save token and settings
7. Selling items
===============================

===== Functions to be added =====
1. Search, and all button related currency commands (once i figure out HOW THOSE DAMN BUTTONS WORK)
2. work (maybe)
=================================
"""

#Libraries
import ctypes
import datetime
import json
import sys
import threading
import time
import requests

from json.decoder import JSONDecodeError
from termcolor import colored

#variables
settings = None
color = None

begTimer = 55
digTimer = 50
fishTimer = 47
huntTimer = 42
depTimer = 120

exitProgram = False

isBegging = isDigging = isFishing = isHunting = isDepositing = isSelling = False

token = isBeg = isDig = isFish = isHunt = isDep = isSell = channel_id = None

runtimeErrors = []
toPrint = []

#color class, to format the message
class Color:
    def __init__(self):
        pass

    def init(self):
        return "[" + colored('INIT', 'yellow') + '] '

    def positive(self):
        return "[" + colored('+', 'green') + '] '

    def negative(self):
        return "[" + colored('-', 'red') + '] '

    def highlight(self, content):
        return colored(content, "yellow")

    def timer(self, time):
        if time == "RUNNING":
            return "[" + colored("RUNNING", "green") + "] "
        elif time == 0:
            return "[" + colored("RUNNING", "green") + "] "
        elif time == "DISABLED":
            return "[" + colored("DISABLED", "red") + "] "
        else:
            return "[" + colored(str(time) + "s", "yellow") + "] "

#Autofarm class
class AutoFarmer:
    def __init__(self, token, channel_id):
        self.channel_id = channel_id
        self.headers = {'Authorization': token}

    def beg(self):
        bThread = threading.Thread(target=self.send, args=("pls beg",))
        bThread.daemon = True
        bThread.start()

    def dig(self):
        dThread = threading.Thread(target=self.send, args=("pls dig",))
        dThread.daemon = True
        dThread.start()

    def fish(self):
        fThread = threading.Thread(target=self.send, args=("pls fish",))
        fThread.daemon = True
        fThread.start()

    def hunt(self):
        hThread = threading.Thread(target=self.send, args=("pls hunt",))
        hThread.daemon = True
        hThread.start()

    def dep(self):
        depThread = threading.Thread(target=self.send, args=("pls dep all",))
        depThread.daemon = True
        depThread.start()

    def sell(self):
        sellThread = threading.Thread(target=self.sell_item)
        sellThread.daemon = True
        sellThread.start()

    def sell_item(self):
        global isSelling

        isSelling = True

        time.sleep(3) #wait for some time to get the response msg
        r = requests.get(f'https://discordapp.com/api/v6/channels/{self.channel_id}/messages', headers=self.headers)
        
        data = r.json()

        index = 0
        while True: #check if message was sent by dank
            try:
                if data[index]['author']['id'] == '270904126974590976':
                    break
                index += 1
            except IndexError:
                logRuntimeError("Couldn't find Dank Memer's message.")
                return

        content = r.json()[index]['content']

        if 'nothing' in content.lower():
            isSelling = False
            return None
        
        content = content.split(" ") #parse the dank memer data to extract stuff to sell
        
        for i in content:
            if i.isdigit():
                startIndex = content.index(i)
        try:
            sellNumber = content[startIndex]
            sellName = content[startIndex + 1]
        except NameError:
            logRuntimeError("Couldn't find sell data, skipped selling.")
            isSelling = False
            return

        if sellName.lower().startswith("bank"):
            isSelling = False
            return

        self.send("pls sell " + sellName + " " + sellNumber)

        isSelling = False

    def send(self, content):
        global isBegging, isDigging, isFishing, isHunting, isDepositing, exitProgram

        arg = content.split(" ")[1]

        if arg == "beg": isBegging = True
        if arg == "dig": isDigging = True
        if arg == "fish": isFishing = True
        if arg == "hunt": isHunting = True
        if arg == "dep": isDepositing = True

        r = requests.post(f'https://discordapp.com/api/v6/channels/{self.channel_id}/messages', headers=self.headers, json={'content': content})
        if r.status_code != 200:
            print(color.negative() + "Error, discord returned an error response.")
            print(color.negative() + "Log: " + str(r.json()))
            print(color.negative() + "If it says \"Unauthorized\", check your token or channel id.")
            print(color.negative() + "Quitting program...")
            exitProgram = True

        if arg == "beg": isBegging = False
        if arg == "dig": isDigging = False
        if arg == "fish": isFishing = False
        if arg == "hunt": isHunting = False
        if arg == "dep": isDepositing = False

#settings class
class SettingsHandler:
    def __init__(self):
        pass

    def read(self):
        try:
            with open("settings.json", "r")as f:
                try:
                    options = json.load(f)
                except JSONDecodeError:
                    return "Key Error"
                try:
                    self.saveVariables(options['token'], options['beg'], options['dig'], options['fish'], options['hunt'], options['dep'], options['sell'], options['channel_id'])
                    return options
                except KeyError:
                    return "Key Error"
        except FileNotFoundError:
            return "File not found"

    def write(self, token, beg, dig, fish, hunt, dep, sell, channel_id):
        setting = {"token": token, "beg": beg, "dig": dig, "fish": fish, "hunt": hunt, "dep": dep, "sell": sell,"channel_id": channel_id}
        try:
            with open("settings.json", "x")as f:
                json.dump(setting, f)
                f.close()
        except FileExistsError:
            with open("settings.json", "w")as f:
                json.dump(setting, f)
                f.close()
        self.saveSettings(token, beg, dig, fish, hunt, dep, sell, channel_id)
        self.saveVariables(token, beg, dig, fish, hunt, dep, sell, channel_id)
        return setting

    def saveVariables(self, _token, beg, dig, fish, hunt, dep, sell, _channel_id):
        global token, isBeg, isDig, isFish, isHunt, isDep, isSell, channel_id
        token = _token
        isBeg = beg
        isDig = dig
        isFish = fish
        isHunt = hunt
        isDep = dep
        isSell = sell
        channel_id = _channel_id

    def saveSettings(self, token, beg, dig, fish, hunt, dep, sell, channel_id):
        global settings
        settings = {"token": token, "beg": beg, "dig": dig, "fish": fish, "hunt": hunt, "dep": dep, "sell": sell,"channel_id": channel_id}

#autofarm display class
class Display:
    def __init__(self) -> None:
        self.prevErrorLen = 1

    def update(self, begTimer, digTimer, fishTimer, huntTimer, depTimer):
        global toPrint

        errors = color.positive() + "None :D" if len(runtimeErrors) == 0 else '\n'.join(runtimeErrors)
        errorlen = 1 if errors == color.positive() + "None :D" else (len(errors.split('\n')))

        toPrint = [
            color.timer(begTimer) + "Beg Command" + " " * 80, #spaces were added to overwrite the entire line,
            color.timer(digTimer) + "Dig Command" + " " * 20, #as without spaces the length difference would cause a display issue
            color.timer(fishTimer) + "Fish Command" + " " * 20,
            color.timer(huntTimer) + "Hunt Command" + " " * 20,
            color.timer(depTimer) + "Dep Command" + " " * 20,
            "============================",
            "\nErrors:",
            errors,
        ]

        if errorlen > self.prevErrorLen:
            print("\n", end="")
            self.prevErrorLen += 1

        print("\033[F" * (len(toPrint) + 1 + errorlen))
        print('\n'.join(toPrint))

#parse settings
def parse_settings():
    global token, isBeg, isDig, isFish, isHunt, isDep, isSell, channel_id

    try:
        token = settings['token']
        isBeg = settings['beg']
        isDig = settings['dig']
        isFish = settings['fish']
        isHunt = settings['hunt']
        isDep = settings['dep']
        isSell = settings['sell']
        channel_id = settings['channel_id']
    except KeyError:
        print(color.negative() + "ERROR! Invalid settings file!")
        print(color.negative() + "Quitting program...")
        time.sleep(2)
        sys.exit(0)

#validate settings input
def settings_input(option):
    setting = input("Would you like to enable " + option + "?(y/n) ").lower()
    while setting not in "yn" and not "":
        setting = input(color.negative() + "Invalid choice, pls put y or n.\nWould you like to enable " + option + "?(y/n) ")
    if setting == "y":
        print(color.positive() + option.title() + " has been enabled!")
        return True
    else:
        print(color.negative() + option.title() + " has been disabled!")
        return False

def logRuntimeError(content):
    global runtimeErrors

    errorTime = str(datetime.datetime.now())
    errorTime = errorTime.split(".")[0]
    runtimeErrors.append("[" + colored(errorTime, "red") + "] " + str(content))

#settings setup
def setup_settings():
    global settings, token, isBeg, isDig, isFish, isHunt, isDep, isSell, channel_id

    print("\n===== Settings Setup =====")
    token = input("User Token pls (We won't hack ur account don't worry)\nIf you need help, visit https://www.youtube.com/watch?v=YEgFvgg7ZPI&t=45s\n > ")
    token = token.strip('"')
    print(color.positive() + "Token added!")
    isBeg = settings_input("begging")
    isDig = settings_input("digging")
    isFish = settings_input("fishing")
    isHunt = settings_input("hunting")
    isDep = settings_input("depositing")
    isSell = settings_input("selling")
    print("===== End of Setup =====")
    print("\n" + color.positive() + "Writing to settings file...")
    settingsHandler = SettingsHandler()
    settings = settingsHandler.write(token, isBeg, isDig, isFish, isHunt, isDep, isSell, "")
    print(color.positive() + "Successfully wrote settings!")

#put colors to screen
def color_init():
    global color

    #initialize colors
    kernel32 = ctypes.WinDLL('kernel32')
    hStdOut = kernel32.GetStdHandle(-11)
    mode = ctypes.c_ulong()
    kernel32.GetConsoleMode(hStdOut, ctypes.byref(mode))
    mode.value |= 4
    kernel32.SetConsoleMode(hStdOut, mode)

    #initialize color class for formatting
    color = Color()

#initialize everything
def initialize():
    global settings, color, channel_id, isBeg, isDig, isFish, isDep, isSell, isHunt

    #check if settings file exists
    try:
        settingsHandler = SettingsHandler()
        settings = settingsHandler.read()
        if settings == "File not found": raise FileNotFoundError
        elif settings == "Key Error":
            print("[" + colored("ERROR", "red") + "] Invalid Settings File!")
            print(colored("The data in the file was invalid, as there was either an update or it was messed with.", "red"))
            print(color.positive() + "Running Settings Setup.")
            setup_settings()
        else:
            print(color.positive() + "Settings file found, read settings.")
            choice = input(color.positive() + "Would you like to make changes to the settings? (y/n) (This would rerun settings setup)\n > ")
            if choice.lower() == "y": setup_settings()
            else: print(color.negative() + "No changes were made!")
    except FileNotFoundError:
        print(color.negative() + "Missing settings file...")
        setup_settings()

    #change channel id
    settingsHandler = SettingsHandler()

    if channel_id == "" or channel_id == None:
        channel_id = input(color.negative() + "Missing Channel Id\nPls input Channel Id: ")
        settingsHandler.write(token, isBeg, isDig, isFish, isHunt, isDep, isSell, channel_id)

    else:
        choice = input(color.positive() + "Channel id: " + channel_id + " detected, would you like to change it? (y for yes, any other input for no)\n > ")
        if choice.lower() == "y":
            channel_id = input("New id pls: ")
            print(color.positive() + "Channel Id successfully changed to: " + channel_id)
            settingsHandler.write(token, isBeg, isDig, isFish, isHunt, isDep, isSell, channel_id)

#exit program check
def check_exit():
    if exitProgram == True:
        time.sleep(2)
        sys.exit(0)

#auto farm
def auto_farm(token, channel_id):
    global begTimer, digTimer, fishTimer, huntTimer, depTimer, runtimeErrors

    #init display
    display = Display()

    if isBeg == False and isDig == False and isFish == False and isHunt == False:
        print(color.negative() + "All settings are disabled.")
        print(color.negative() + "Change settings.json for the autofarm to work.")
        print(color.negative() + "Press enter to quit autofarm.")
        input()
        sys.exit(0)

    autofarmer = AutoFarmer(token, channel_id)

    print("[" + colored("RUNNING", "green") + "] Autofarm Starting... (Takes around 6 seconds as it needs to bypass Dank Memer checks)")

    if isBeg: autofarmer.beg(); check_exit()
    time.sleep(2)
    if isDig: autofarmer.dig(); check_exit()
    time.sleep(2)
    if isFish: autofarmer.fish(); check_exit()
    time.sleep(2)
    if isHunt: autofarmer.hunt(); check_exit()

    print("\n" * 8, end="")
    
    while True:
        time.sleep(1)

        if begTimer == 0 and isBeg:
            autofarmer.beg()
            begTimer = 55
            check_exit()

        if digTimer == 0 and isDig:
            autofarmer.dig()
            autofarmer.sell()
            digTimer = 50
            check_exit()

        if fishTimer == 0 and isFish:
            autofarmer.fish()
            autofarmer.sell()
            fishTimer = 47
            check_exit()

        if huntTimer == 0 and isHunt:
            autofarmer.hunt()
            huntTimer = 42
            check_exit()

        if depTimer == 0 and isDep:
            autofarmer.dep()
            depTimer = 120
            check_exit()

        begTimer -= 1
        digTimer -= 1
        fishTimer -= 1
        huntTimer -= 1
        depTimer -= 1

        begDisplay = "DISABLED" if isBeg == False else begTimer
        digDisplay = "DISABLED" if isDig == False else digTimer
        fishDisplay = "DISABLED" if isFish == False else fishTimer
        huntDisplay = "DISABLED" if isHunt == False else huntTimer
        depDisplay = "DISABLED" if isDep == False else depTimer

        begDisplay = "RUNNING" if isBegging == True else begTimer
        digDisplay = "RUNNING" if isDigging == True else digTimer
        fishDisplay = "RUNNING" if isFishing == True else fishTimer
        huntDisplay = "RUNNING" if isHunting == True else huntTimer
        depDisplay = "RUNNING" if isDepositing == True else depTimer

        display.update(begDisplay, digDisplay, fishDisplay, huntDisplay, depDisplay)

#main function
def main():
    color_init()
    print("===== Dank Memer Autofarm =====\nVersion v0.0.2\nContact " + color.highlight("wHo#6933") + " if there are any errors.\n")
    print(color.highlight("BUG: When  errors are printed, it breaks the display.\n"))
    print("[" + colored("CHANGELOG", "yellow") + "]")
    print(color.positive() + "1. Added Selling")
    print(color.positive() + "2. Added a Runtime Error log (kinda broken tho)")
    print()
    print("===============================\n")
    print(color.init() + "Initializing autofarm.")
    initialize()
    print(color.highlight("\nChange/Delete settings.json if you want to make any changes to the settings.\n"))
    parse_settings()
    print(color.positive() + "Initialization finished.")
    print("\n===== Running Autofarm =====")
    auto_farm(token, channel_id)

if __name__ == "__main__":
    main()
