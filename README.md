# Winamp MPRIS Bridge

`winamp-mpris` is a bridge that exposes an MPRIS 2 (Media Player Remote Interfacing Specification) D-Bus interface for Winamp running under Wine on Linux. This allows you to control Winamp using your desktop environment's media player controls (media keys, sound menu, etc.) and view track metadata.

## Features

- **Playback Control**: Play, Pause, Stop, Next, Previous.
- **Metadata**: Displays current Track Title and Artist.
- **Status**: Reports playback status (Playing, Paused, Stopped).
- **Integration**: Works with standard MPRIS controllers like `playerctl`, GNOME Shell, KDE Plasma, etc.

## Prerequisites

- Linux
- Wine
- Winamp installed and running under Wine
- Python 3
- `python-dbus-next` library

## Installation

### Arch Linux

This project includes a `PKGBUILD` for easy installation on Arch Linux.

1. Clone the repository:
   ```bash
   git clone https://github.com/elgatolinux/winamp-mpris.git
   cd winamp-mpris
   ```

2. Build and install the package:
   ```bash
   makepkg -si
   ```

### Manual Installation (Other Distributions)

1. Install the required Python library:
   ```bash
   pip install dbus-next
   ```

2. Copy the files to appropriate system locations:
   - `winamp_mpris.py` -> `/usr/bin/winamp-mpris` (make executable)
   - `CLAmp.exe` -> `/usr/share/winamp-mpris/clamp.exe`
   - `winamp-mpris.service` -> `~/.config/systemd/user/winamp-mpris.service` (or `/etc/systemd/user/`)

## Usage

### Starting the Service

After installation, you can start the service using the included helper script (if installed via package):

```bash
winamp-mprisd
```

Or manually using systemctl:

```bash
systemctl --user enable --now winamp-mpris.service
```

### Configuration

The bridge communicates with Winamp using `CLAmp.exe`. By default, it looks for this executable at `Z:\usr\share\winamp-mpris\clamp.exe`.

If you installed `CLAmp.exe` in a different location, set the `WINAMP_CLAMP` environment variable before running the service or script:

```bash
export WINAMP_CLAMP="Z:\path\to\your\clamp.exe"
```

## How it Works

This tool runs a Python script that implements the MPRIS D-Bus interface. When it receives a command (e.g., "Next"), it calls `CLAmp.exe` via `wine` to send the corresponding command to the Winamp window. It polls Winamp periodically to update the playback status and metadata.

## License

MIT
