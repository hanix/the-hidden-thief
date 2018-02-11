# The Hidden Thief
This is the repository that contains all the code that was shown during the malware workshop I hosted at
[Hack.ini event (Feb 2018)](https://www.facebook.com/events/400045293741628/).
#  Disclaimer
The scripts here are for educational and demonstration purposes **only**.
By using them, you agree that I will not be held accountable for any illegal activities you may use them in.
#  Requirements
 1. A Windows 7 machine.
 2. Python 2.7.14 (32Bit)
 3. Pywin32-221.win32-py2.7 ([here](https://sourceforge.net/projects/pywin32/files/pywin32/Build%20221/))
 4. PyHook-1.5.1.win32-py2.7 ([here](https://sourceforge.net/projects/pyhook/files/pyhook/1.5.1/))
 5. Requests-2.18.4 (*pip install requests*)
 6. PyInstaller-3.3.1 (*pip install pyinstaller*)
#  Folders 
*Payload folder* contains the three variants of the keylogger (Local mode, Live mode using HTTP and  Furtive mode using FTP).

*Infector folder* contains the script that is used to trick a user into installing our malware onto his computer.
# Commands
To convert your python script to a windows executable, use:

    pyinstaller -F --noconsole filename .py

To generate and exe that includes a payload, use:

    pyinstaller -F --add-data "payload.exe;." scriptname .py
