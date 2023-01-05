# Noise Recorder #

A retrieves white noise from the environment via the microphone and extracting the least significant bit.

## Invocation ##

```console
noiserecorder --help
```

Brings up help.

```console
noiserecorder
```

Generates 30 minutes (The user should be warned that this will take about 8 hours [30min (desired time)*16 (number of bits per sample)=8hrs]) of noise written to a dated file.

```console
noiserecorder pathname/filename.wav
```

Generates 30 minutes of noise written to a specific path.

```console
noiserecorder pathname/filename.wav <duration_in_seconds>
```

Generates specified duration of noise written to a specific path.

## Virtual Environment Requirements for Building ##

The following packages are needed:


* altgraph
* auto-py-to-exe
* bottle
* bottle-websocket
* cffi
* Eel
* future
* gevent
* gevent-websocket
* greenlet
* idle
* pefile
* pip
* pycparser
* pycryptodome
* pyinstaller
* pyinstaller-hooks-contrib
* pyparsing
* pywin32-ctypes
* setuptools
* sounddevice
* wheel
* whichcraft
* zope.event
* zope.interface