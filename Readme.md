# Noise Recorder #

A retrieves white noise from the environment via the microphone and extracting the least significant bit.

## Invocation (Refer to steps below for installation) ##

```console
python -m noiserecorder --help
```

Brings up help.

```console
python -m noiserecorder
```

Generates 30 minutes (The user should be warned that this will take about 8 hours [30min (desired time)*16 (number of bits per sample)=8hrs]) of noise written to a dated file.

```console
python -m noiserecorder pathname/filename.wav
```

Generates 30 minutes of noise written to a specific path.

```console
python -m noiserecorder pathname/filename.wav <duration_in_seconds>
```

Generates specified duration of noise written to a specific path.

## Virtual Environment Requirements for Building ##

The following packages are needed:

### System Requirements ###

* Any system that supports Python.
  * Android /w Termux Installed?: Don't even try it! I am not sure that Android's permission system will allow audio to be recorded in the manner this software does (using sounddevice). I am not so sure about the python setup there. I have had problems with it before.
  * Anything OS not Windows/Linux/MacOS or anything running on a processor that is not Intel-based?: YMMV/I really don't know. (Hmm. I smell a Raspberry Pi project)
  * Any of the above. Try and report.
  * ⚠️ Important Safety Tip For Android/Termux: Just in case somebody does manages to get this working on an Android phone running Termux, Please for the love of all that is Good and Holy, don't waste your batteries, or at the very least have a friend that is not wasting their batteries when you are out in the middle of a wilderness and might get lost and need to call someone for help. Just in case gathering atmospheric noise in the middle of a desert or forest is tempting for you. I hear waterfalls are good sources of noise. Again, bring a friend with a charged phone not running this and stay safe! Remember it takes 16 seconds of recorded sound to generate 1 second of noise. Plus there is quite a bit of postprocessing at the end. I cannot be held responsible for someone getting lost or hurt and I do not want that for anybody either. So if you are going to proceed to gather noise from the wild natural  environment, be thoughtful of the following: Be safe, be smart, be vigilent, and most importantly stay alive and unharmed, and are able to come back home when you are done! You have been duly warned.
* Python 3.11 w/ pip (For best results use this version: You might be able to get away with using something as low as 3.9 but I strongly recommend using this listed version if you can)
* virtualenv and/or venv python pip packages.

### Python Virtual Enviroment Packages (AKA don't screw up your system's python!) ###

Install a virtual environment by doing the following: [You will have to replace the ~ with $env:USERPROFILE (powershell.exe/pwsh.exe) and /'s with \'s if you are on Windows]

`python3.11 -m venv --copies --upgrade-deps ~/path/to/noiserecorder_venv`

Virtualenv Instructions:

`python3.11 -m virtualenv --copies ~/path/to/noiserecorder_venv`

If you are using Windows Store Version of Python:

* Open Start Menu
* Search for Python 3.11
* Open Python 3.11

In the Python Prompt do the following (One line at a time):

```python
import os
os.system('pwsh') # Start Powershell
```

Once in Powershell Subprocess do the following (One line at a time):

```pwsh
cd # Go Home
python -m venv --copies --upgrade-deps $env:USERPROFILE\path\to\noiserecorder_venv
exit
```

Exit Windows Store Python:

```python
exit()
```

Enter your virtual environment:

bash:

`. ~/path/to/noiserecorder-venv/bin/activate`

Windows powershell/pwsh:

`. $env:USERPROFILE\path\to\noiserecorder-venv\bin\Activate.ps1`

Windows powershell/pwsh (A virtual environment installed using Windows Store Python):

`. $env:USERPROFILE\path\to\noiserecorder-venv\Scripts\Activate.ps1`

* wheel (You really should install this by itself first.)
* altgraph
* auto-py-to-exe (Just in case you want to build an self-contained executable. [You probably shouldn't! Your machine might flag the executable! ]
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
* pip (You don't have to install this venv/virtualenv should have done this for you.)
* pycparser
* pycryptodome (Encryption added for the peace of mind and privacy of any would be noise collector.)
* pyinstaller
* pyinstaller-hooks-contrib
* pyparsing
* setuptools (Same as pip, installed by virtual/venv already)
* sounddevice (Lets grab some sound and make some noise with it!)
* whichcraft
* zope.event
* zope.interface

Install these packages in the virtual environment:

bash:

```bash
for f in wheel altgraph bottle bottle-websocket cffi Eel future gevent gevent-websocket \
greenlet idle pefile pycparser pycryptodome pyinstaller \
pyinstaller-hooks-contrib pyparsing sounddevice \
whichcraft zope.event zope.interface
do
    python -m pip install "$f"
done
```

pwsh (Windows):

```pwsh
@('wheel','altgraph','bottle',
'bottle-websocket','cffi','Eel','future','gevent',
'gevent-websocket','greenlet','idle','pefile','pycparser',
'pycryptodome','pyinstaller','pyinstaller-hooks-contrib','pyparsing',
'sounddevice','whichcraft','zope.event','zope.interface') |
ForEach-Object {& python -m pip install "$_"}
```

Install noiserecorder itself:

bash:

```bash
# $PATH_TO_NOISERECORDER_SOURCE_MODULE is a stand-in for the actual path to your checked out copy of the noiserecorder module.
python install $PATH_TO_NOISERECORDER_SOURCE_MODULE # It is the folder that contains setup.py
```

pwsh (Windows):

```pwsh
# $env:PATH_TO_NOISERECORDER_SOURCE_MODULE is a stand-in for the actual path to your checked out out copy of the noiserecorder module.
cd $env:PATH_TO_NOISERECORDER_SOURCE_MODULE
& python install $env:PATH_TO_NOISERECORDER_SOURCE_MODULE # It is the folder that contains setup.py
```
