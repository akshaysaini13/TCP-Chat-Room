from tkinter import *
import threading
import tkinter
from tkinter import simpledialog
from tkinter import scrolledtext
import socket

HOST = socket.gethostbyname(socket.gethostname())
PORT = 8080
FORMAT = 'utf-8'


def send_text():
    message = f"{nickname}: {input_area.get('1.0','end')}"
    client.send(message.encode(FORMAT))
    input_area.delete('1.0','end')


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST,PORT))

win = Tk()
# win.withdraw()

nickname = simpledialog.askstring("Nickname", 'Please choose a nickname', parent=win)

win.configure(bg='lightgray')

chat_label = tkinter.Label(win, text='Chat', bg='lightgray', font=('Arial',12))
chat_label.pack(padx=20, pady=5)

text_area = tkinter.scrolledtext.ScrolledText(win)
text_area.pack(padx=20, pady=5)
text_area.config(state='disabled')

msg_label = tkinter.Label(win, text='Message: ', bg='lightgray', font=('Arial',12))
msg_label.pack(padx=20, pady=5)

input_area = tkinter.Text(win, height=3)
input_area.pack(padx=20, pady=5)

button_send = tkinter.Button(win, text='Send', command=send_text, font=('Arial',12))
button_send.pack(padx=20, pady=5)


def receive():
    while True:
        try:
            msg = client.recv(1024).decode(FORMAT)
            if msg == 'NICK':
                client.send(nickname.encode(FORMAT))
            else:
                text_area.config(state='normal') #normal state to a text
                text_area.insert('end', msg)
                text_area.yview('end') #scroll down with the text
                text_area.config(state='disabled')
        except:
            print("Error occured")
            


receive_thread = threading.Thread(target=receive)
receive_thread.start()

win.mainloop()