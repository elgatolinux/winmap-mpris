#!/usr/bin/env python3
import asyncio
import subprocess
from dbus_next.aio import MessageBus
from dbus_next.service import ServiceInterface, method, dbus_property
from dbus_next import Variant
from dbus_next.service import PropertyAccess
import os

import re

CLAMP_PATH = os.environ.get("WINAMP_CLAMP", r"Z:\usr\share\winamp-mpris\clamp.exe")

def run_clamp(arg):
    subprocess.Popen([
        "wine",
        CLAMP_PATH,
        arg
    ])

async def query_clamp(arg):
    try:
        proc = await asyncio.create_subprocess_exec(
            "wine", CLAMP_PATH, arg,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        stdout, _ = await proc.communicate()
        return stdout.decode('utf-8', errors='ignore').strip()
    except Exception:
        return ""

class Player(ServiceInterface):
    def __init__(self):
        super().__init__("org.mpris.MediaPlayer2.Player")
        self._playback_status = "Stopped"
        self._metadata = {
            "mpris:trackid": Variant("o", "/org/mpris/MediaPlayer2/TrackList/NoTrack"),
        }

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
        return self._playback_status

    @dbus_property(PropertyAccess.READ)
    def Metadata(self) -> 'a{sv}':
        return self._metadata

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

    async def update_state(self):
        try:
            # Update Status
            status_raw = await query_clamp("/STATUS")
            new_status = "Stopped"
            if "PLAYING" in status_raw:
                new_status = "Playing"
            elif "PAUSED" in status_raw:
                new_status = "Paused"
            
            if new_status != self._playback_status:
                self._playback_status = new_status
                self.emit_properties_changed({"PlaybackStatus": new_status})

            # Update Metadata
            title_raw = await query_clamp("/TITLE")
            # Remove " - Winamp" suffix if present (common in Winamp window titles)
            title_clean = re.sub(r' - Winamp$', '', title_raw)
            # Remove leading "x. " track number if present? Maybe too aggressive.
            
            artist = "Unknown Artist"
            title = title_clean
            
            # Common Winamp format: "Artist - Title"
            if " - " in title_clean:
                parts = title_clean.split(" - ", 1)
                artist = parts[0]
                title = parts[1]

            new_metadata = {
                "mpris:trackid": Variant("o", "/org/mpris/MediaPlayer2/TrackList/NoTrack"),
                "xesam:title": Variant("s", title),
                "xesam:artist": Variant("as", [artist]),
            }

            # Only emit if changed (ignoring deep comparison complexity, simple dict compare works for basic types)
            # Variant comparison might be tricky, checking string repr or extracting value
            if (self._metadata.get("xesam:title", Variant("s", "")).value != title or 
                self._metadata.get("xesam:artist", Variant("as", [])).value != [artist]):
                
                self._metadata = new_metadata
                self.emit_properties_changed({"Metadata": new_metadata})

        except Exception as e:
            # Ignore errors during polling to avoid crashing
            pass


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
    
    root = Root()
    player = Player()
    
    bus.export("/org/mpris/MediaPlayer2", root)
    bus.export("/org/mpris/MediaPlayer2", player)
    
    await bus.request_name("org.mpris.MediaPlayer2.winamp")
    
    # Polling loop
    while True:
        await player.update_state()
        await asyncio.sleep(1)

asyncio.run(main())
