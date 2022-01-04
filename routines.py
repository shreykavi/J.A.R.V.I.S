#  routines.py

import os
import subprocess
from enum import Enum
from sys import platform

# Decorators to define event handlers
# TODO: make decorator take args for possible commands, ex. close == exit
class Routines(object):
    def __init__(self):
        self.routines = {} #map of routines to call
    def define(self, func):
        self.routines[func.__name__.replace("_routine", "")] = (func)
        return func
    def get(self, command):
        #do things and publish events
        return self.routines.get(command)

routines = Routines()

class BashCommand(Enum):
    # = (windows_command, osx_command)
    brave = {"win32": "/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe", "darwin": "open /Applications/Brave Browser.app"}
    discord = {"win32": "/Users/Shrey/AppData/Local/Discord/app-1.0.9003/Discord.exe"}

app_map = {
    # name : (default_args, command)
    'netflix': ("https://www.netflix.com/search?q=", BashCommand.brave),
    'plex': ("https://app.plex.tv/desktop#!/search?query=", BashCommand.brave),
    'youtube': ("https://www.youtube.com/results?search_query=", BashCommand.brave),
    'discord': ("", BashCommand.discord)
}

@routines.define
async def test_routine(message, app, args):
    await message.channel.send("JARVIS ran the test")

@routines.define
async def open_routine(message, app, args):
    default_args, bash_command = app_map.get(app, (None, None))

    try: 
        run_command = bash_command.value.get(platform)
    except:
        await message.channel.send(f"JARVIS can't open {app} on {platform}")
        return

    args = default_args + args.replace(" ", "+")
    process = subprocess.Popen([run_command, args], stdout=subprocess.PIPE)
    output, error = process.communicate()

@routines.define
async def exit_routine(message, app, args):
    if app == 'discord':
        os.system("TASKKILL /F /IM discord.exe")
    else:
        message.channel.send(f"JARVIS can't close {app}")

@routines.define
async def sleep_routine(message, app, args):
    os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
