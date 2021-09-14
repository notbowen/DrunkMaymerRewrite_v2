#Dank Memer Autofarm, v2
#Made by wHo#6933
#Report any error to me hehe, try and take a screenshot of the error too

"""
===== Available Functions =====
1. Auto beg
2. Auto dig
3. Auto fish
4. Auto hunt
5. Save token and settings
===============================

===== Functions to be added =====
1. Search, and all button related currency commands (once i figure out HOW THOSE DAMN BUTTONS WORK)
2. work (maybe)
3. Auto deposit
=================================
"""

#Libraries
import requests
import ctypes
import json
import time
import sys
import threading

from termcolor import colored

#variables
settings = None
color = None

begTimer = 50
digTimer = 45
fishTimer = 43
huntTimer = 40

token = isBeg = isDig = isFish = isHunt = channel_id = None

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
        if time == 0:
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
        bThread.start()

    def dig(self):
        dThread = threading.Thread(target=self.send, args=("pls beg",))
        dThread.start()

    def fish(self):
        fThread = threading.Thread(target=self.send, args=("pls beg",))
        fThread.start()

    def hunt(self):
        hThread = threading.Thread(target=self.send, args=("pls beg",))
        hThread.start()

    def send(self, content):
        r = requests.post(f'https://discordapp.com/api/v6/channels/{self.channel_id}/messages', headers=self.headers, json={'content': content})
        if r.status_code != 200:
            print(color.negative() + "Error, discord returned an error response.")
            print(color.negative() + "Log: " + str(r.json()))
            print(color.negative() + "Quitting program due to error...")
            time.sleep(2)
            sys.exit(0)

#settings class
class SettingsHandler:
    def __init__(self):
        pass

    def read(self):
        try:
            with open("settings.json", "r")as f:
                options = json.load(f)
                self.saveVariables(options['token'], options['beg'], options['dig'], options['fish'], options['hunt'], options['channel_id'])
                return options
        except FileNotFoundError:
            return "File not found"

    def write(self, token, beg, dig, fish, hunt, channel_id):
        setting = {"token": token, "beg": beg, "dig": dig, "fish": fish, "hunt": hunt, "channel_id": channel_id}
        try:
            with open("settings.json", "x")as f:
                json.dump(setting, f)
                f.close()
        except FileExistsError:
            with open("settings.json", "w")as f:
                json.dump(setting, f)
                f.close()
        self.saveSettings(token, beg, dig, fish, hunt, channel_id)
        self.saveVariables(token, beg, dig, fish, hunt, channel_id)
        return setting

    def saveVariables(self, _token, beg, dig, fish, hunt, _channel_id):
        global token, isBeg, isDig, isFish, isHunt, channel_id
        token = _token
        isBeg = beg
        isDig = dig
        isFish = fish
        isHunt = hunt
        channel_id = _channel_id

    def saveSettings(self, token, beg, dig, fish, hunt, channel_id):
        global settings
        settings = {"token": token, "beg": beg, "dig": dig, "fish": fish, "hunt": hunt, "channel_id": channel_id}

#autofarm display class
class Display:
    def __init__(self) -> None:
        pass

    def update(self, begTimer, digTimer, fishTimer, huntTimer):
        print("\033[F" * 5)
        print(
            color.timer(begTimer) + "Beg Command" + " " * 10, #spaces were added to overwrite the entire line,
            color.timer(digTimer) + "Dig Command" + " " * 10, #as without spaces the length difference would cause a display issue
            color.timer(fishTimer) + "Fish Command" + " " * 10,
            color.timer(huntTimer) + "Hunt Command" + " " * 10,
            sep="\n"
            )

#parse settings
def parse_settings():
    global token, isBeg, isDig, isFish, isHunt, channel_id

    try:
        token = settings['token']
        isBeg = settings['beg']
        isDig = settings['dig']
        isFish = settings['fish']
        isHunt = settings['hunt']
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

#settings setup
def setup_settings(color):
    global settings, token, isBeg, isDig, isFish, isHunt, channel_id

    print("\n===== Settings Setup =====")
    token = input("User Token pls (We won't hack ur account don't worry)\nIf you need help, visit https://www.youtube.com/watch?v=YEgFvgg7ZPI&t=45s\n > ")
    print(color.positive() + "Token added!")
    isBeg = settings_input("begging")
    isDig = settings_input("digging")
    isFish = settings_input("fishing")
    isHunt = settings_input("hunting")
    print("===== End of Setup =====")
    print("\n" + color.positive() + "Writing to settings file...")
    settingsHandler = SettingsHandler()
    settings = settingsHandler.write(token, isBeg, isDig, isFish, isHunt, "")
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
    global settings, color, channel_id, isBeg, isDig, isFish, isHunt

    #check if settings file exists
    try:
        settingsHandler = SettingsHandler()
        settings = settingsHandler.read()
        if settings == "File not found": raise FileNotFoundError
        print(color.positive() + "Settings file found, read settings.")
    except FileNotFoundError:
        print(color.negative() + "Missing settings file...")
        setup_settings(color)

    #change channel id
    settingsHandler = SettingsHandler()

    if channel_id == "" or channel_id == None:
        channel_id = input(color.negative() + "Missing Channel Id\nPls input Channel Id: ")
        settingsHandler.write(token, isBeg, isDig, isFish, isHunt, channel_id)

    else:
        choice = input(color.positive() + "Channel id: " + channel_id + " detected, would you like to change it? (y for yes, any other input for no)\n > ")
        if choice.lower() == "y":
            channel_id = input("New id pls: ")
            print(color.positive() + "Channel Id successfully changed to: " + channel_id)
            settingsHandler.write(token, isBeg, isDig, isFish, isHunt, channel_id)

#auto farm
def auto_farm(token, channel_id):
    global begTimer, digTimer, fishTimer, huntTimer

    #init display
    display = Display()

    if isBeg == False and isDig == False and isFish == False and isHunt == False:
        print(color.negative() + "All settings are disabled.")
        print(color.negative() + "Change settings.json for the autofarm to work.")
        print(color.negative() + "Press enter to quit autofarm.")
        input()
        sys.exit(0)

    autofarmer = AutoFarmer(token, channel_id)
    if isBeg: autofarmer.beg()
    if isDig: autofarmer.dig()
    if isFish: autofarmer.fish()
    if isHunt: autofarmer.hunt()

    #make space on screen for display output
    print('\n'*4, end="")
    
    while True:
        time.sleep(1)

        if begTimer == 0 and isBeg:
            autofarmer.beg()
            begTimer = 45

        if digTimer == 0 and isDig:
            autofarmer.dig()
            digTimer = 40

        if fishTimer == 0 and isFish:
            autofarmer.fish()
            fishTimer = 40

        if huntTimer == 0 and isHunt:
            autofarmer.hunt()
            huntTimer = 40

        begTimer -= 1
        digTimer -= 1
        fishTimer -= 1
        huntTimer -= 1

        begDisplay = "DISABLED" if isBeg == False else begTimer
        digDisplay = "DISABLED" if isDig == False else digTimer
        fishDisplay = "DISABLED" if isFish == False else fishTimer
        huntDisplay = "DISABLED" if isHunt == False else huntTimer

        display.update(begDisplay, digDisplay, fishDisplay, huntDisplay)

#main function
def main():
    color_init()
    print("===== Dank Memer Autofarm =====\nContact " + color.highlight("wHo#6933") + " if there are any errors.\n")
    print(color.init() + "Initializing autofarm.")
    initialize()
    print(color.highlight("\nChange/Delete settings.json if you want to make any changes to the settings.\n"))
    parse_settings()
    print(color.positive() + "Initialization finished.")
    print("\n===== Running Autofarm =====")
    auto_farm(token, channel_id)

if __name__ == "__main__":
    main()
