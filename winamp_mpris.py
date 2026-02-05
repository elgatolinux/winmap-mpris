#!/usr/bin/env python3
import asyncio
import subprocess
from dbus_next.aio import MessageBus
from dbus_next.service import ServiceInterface, method, dbus_property
from dbus_next import Variant
from dbus_next.service import PropertyAccess
import os

CLAMP_PATH = os.environ.get("WINAMP_CLAMP", r"Z:\usr\share\winamp-mpris\clamp.exe")

def run_clamp(arg):
    subprocess.Popen([
        "wine",
        CLAMP_PATH,
        arg
    ])

class Player(ServiceInterface):
    def __init__(self):
        super().__init__("org.mpris.MediaPlayer2.Player")

    @method()
    def Play(self):
        run_clamp("/PLAY")

    @method()
    def Pause(self):
        run_clamp("/PAUSE")

    @method()
    def PlayPause(self):
        run_clamp("/PAUSE")

    @method()
    def Stop(self):
        run_clamp("/STOP")

    @method()
    def Next(self):
        run_clamp("/NEXT")

    @method()
    def Previous(self):
        run_clamp("/PREV")
    
    @dbus_property(PropertyAccess.READ)
    def PlaybackStatus(self) -> 's':
    	return "Playing"

    @dbus_property(PropertyAccess.READ)
    def CanPlay(self) -> 'b':
   	 return True

    @dbus_property(PropertyAccess.READ)
    def CanPause(self) -> 'b':
    	return True

    @dbus_property(PropertyAccess.READ)
    def CanGoNext(self) -> 'b':
    	return True

    @dbus_property(PropertyAccess.READ)
    def CanGoPrevious(self) -> 'b':
   	 return True


class Root(ServiceInterface):
    def __init__(self):
        super().__init__("org.mpris.MediaPlayer2")

    @dbus_property(PropertyAccess.READ)
    def Identity(self) -> 's':
    	return "Winamp"

    @dbus_property(PropertyAccess.READ)
    def SupportedUriSchemes(self) -> 'as':
    	return []

    @dbus_property(PropertyAccess.READ)
    def SupportedMimeTypes(self) -> 'as':
    	return []



async def main():
    bus = await MessageBus().connect()
    bus.export("/org/mpris/MediaPlayer2", Root())
    bus.export("/org/mpris/MediaPlayer2", Player())
    await bus.request_name("org.mpris.MediaPlayer2.winamp")
    await asyncio.get_event_loop().create_future()

asyncio.run(main())
