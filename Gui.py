from tkinter import*
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

listbox = Listbox(frame, yscrollcommand=scrollbar.set,font=("Times", "14","italic"),bg="grey")
listbox.pack(side=LEFT, fill=BOTH, expand=True)  # Распределить по всему окну
scrollbar.config(command=listbox.yview)

button = Button(frame, text="удалить",command=delete_item,bg="black",fg="white",width=16,font=("Times", "14","italic"))
button.pack()

add_button = Button(frame, text="Добавить в список", command=add_to_list,font=("Times", "14","italic"))
add_button.pack()

root.mainloop()
