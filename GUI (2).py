import socket
import struct
import os
from server import read_json
from tkinter import*

def receive_file_size(sck: socket.socket):
    fmt = "<Q"
    expected_bytes = struct.calcsize(fmt)
    received_bytes = 0
    stream = bytes()

    while received_bytes < expected_bytes:
        chunk = sck.recv(expected_bytes - received_bytes)
        stream += chunk
        received_bytes += len(chunk)

    filesize = struct.unpack(fmt, stream)[0]

    return filesize

def receive_file(sck: socket.socket, filename):
    filesize = receive_file_size(sck)

    with open(filename, "wb") as f:
        received_bytes = 0

        while received_bytes < filesize:
            chunk = sck.recv(1024)

            if chunk:
                f.write(chunk)
                received_bytes += len(chunk)
    
    return read_json(filename)

def send_file(sck: socket.socket, filename):
    filesize = os.path.getsize(filename)

    sck.sendall(struct.pack("<Q", filesize))
    
    with open(filename, "rb") as f:
        while read_bytes := f.read(1024):
            sck.sendall(read_bytes)

def add_to_list():
    text = entry.get()
    listbox.insert(END, text)
    entry.delete(0, END)  # Очистить текстовое поле после добавления

def delete_item():
    index = listbox.curselection()[0]  # Получаем индекс выбранного элемента
    listbox.delete(index)  # Удаляем выбранный элемент из списка
    #button.grid_forget()  # Скрываем кнопку

def addButton_del(add_button):
    add_button.pack.forget()

def on_select(event):
    #button.grid(row=3,column=0)  # Показываем кнопку при выборе элемента списка
    show_button()

root = Tk()
root.title("Холодильник")
root.geometry("400x400")
root.resizable(False, False)


frame = Frame(root,bg="aquamarine4")
frame.pack(fill=BOTH, expand=True)  # Распределить по всему окну

entry = Entry(frame,bg="black",font=("Times", "14","italic"),fg="yellow")
entry.pack(fill=X)  # Распределить по горизонтали

scrollbar = Scrollbar(frame)
scrollbar.pack(side=RIGHT, fill=Y)

listbox = Listbox(frame, yscrollcommand=scrollbar.set,font=("Times", "14","italic"),bg="grey",fg="yellow")
listbox.pack(side=LEFT, fill=BOTH, expand=True)  # Распределить по всему окну
scrollbar.config(command=listbox.yview)

button = Button(frame, text="удалить",command=delete_item,bg="black",fg="white",width=16,font=("Times", "14","italic"))
button.pack(pady=80)

add_button = Button(frame, text="Добавить в список", command=add_to_list,font=("Times", "14","italic"))
add_button.pack()

root.mainloop()
