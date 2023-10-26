import tkinter as tk
from tkinter import ttk
import sqlite3
#главное окно
class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

    def init_main(self):
        toolbar = tk.Frame(bg = "#d7d7d7", bd = 2)
        toolbar.pack(side=tk.TOP, fill=tk.X)


        #добавление
        self.add_img = tk.PhotoImage(file="./img/add.png")
        btn_add = tk.Button(toolbar, bg= "#d7d7d7", bd = 1,
                            image=self.add_img,
                            command=self.open_child)
        btn_add.pack(side=tk.LEFT)

        #обновить
        self.upd_img = tk.PhotoImage(file="./img/update.png")
        btn_upd = tk.Button(toolbar, bg= "#d7d7d7", bd = 1,
                            image=self.upd_img,
                            command=self.open_update_dialog)
        btn_upd.pack(side=tk.LEFT)


         #удаление
        self.del_img = tk.PhotoImage(file="./img/delete.png")
        btn_del = tk.Button(toolbar, bg= "#d7d7d7", bd = 1,
                            image=self.del_img,
                            command=self.delete_records)
        btn_del.pack(side=tk.LEFT)



        #поиск
        self.search_img = tk.PhotoImage(file="./img/search.png")
        btn_search = tk.Button(toolbar, bg= "#d7d7d7", bd = 1,
                            image=self.search_img,
                            command=self.open_search)
        btn_search.pack(side=tk.LEFT)


         #кнопка обновления  таблицы
        self.refresh_img = tk.PhotoImage(file="./img/refresh.png")
        btn_refresh = tk.Button(toolbar, bg= "#d7d7d7", bd = 1,
                            image=self.refresh_img,
                            command=self.view_records)
        btn_refresh.pack(side=tk.LEFT)




        #таблица
        self.tree = ttk.Treeview(self,
                                 columns=("ID", "name", "tel", "email"),
                                 height=45,
                                 show="headings")
        #праметры столбца
        self.tree.column("ID", width=45, anchor=tk.CENTER)
        self.tree.column("name", width=300, anchor=tk.CENTER)
        self.tree.column("tel", width=150, anchor=tk.CENTER)
        self.tree.column("email", width=150, anchor=tk.CENTER)




        self.tree.heading("ID", text="ID")
        self.tree.heading("name", text="ФИО")
        self.tree.heading("tel", text="Телефон")
        self.tree.heading("email", text="E-mail")


        self.tree.pack(side=tk.LEFT)

    def records(self, name, tel, email):
        self.db.insert_data(name, tel, email)
        self.view_records()

    def view_records(self):
        self.db.cur.execute("""SELECT * FROM users""")
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert("","end", values=row) 
         for row in self.db.cur.fetchall()]
        
    def update_record(self, name, tel, email):
        id = self.tree.set(self.tree.selection()[0], '#1')
        self.db.cur.execute(""" UPDATE users SET name=?, tel=?, email=? WHERE ID=?  """, (name, tel, email, id))

        self.db.conn.commit()
        self.view_records()

# метод удаления данных
    def delete_records(self):
        for row in self.tree.selection(): 
            self.db.cur.execute(""" DELETE FROM users WHERE id = ? """,(self.tree.set(row, '#1'),))
        self.db.conn.commit()
        self.view_records()
        

#метод поиска данных
    def serch_records(self,name):
         name = ("%" + name + "%", )
         self.db.cur.execute("SELECT * FROM users WHERE name LIKE ?", (name))
         [self.tree.delete(i) for i in self.tree.get_children()] 
         [self.tree.insert("","end", values=row) for row in self.db.cur.fetchall()]


#метод добавления
    def open_child(self):
        Child()

    def open_update_dialog(self):
        Update()

    def open_search(self):
        Search()


#класс дочернего окна
class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    def init_child(self):
        self.title("Добавление")
        self.geometry("400x200")
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()

        #############################################################################################
        label_name = tk.Label(self, text="ФИО")
        label_name.place(x=50, y=20)
        label_tel = tk.Label(self, text="Телефон")
        label_tel.place(x=50, y=50)
        label_email = tk.Label(self, text="E-mail")
        label_email.place(x=50, y=80)

        self.entry_name = tk.Entry(self)
        self.entry_name.place(x=200, y=20)
        self.entry_tel = tk.Entry(self)
        self.entry_tel.place(x=200, y=50)
        self.entry_email = tk.Entry(self)
        self.entry_email.place(x=200, y=80)
        ##############################################################################################
        self.btn_cancel = tk.Button(self, text = "Закрыть", command=self.destroy)
        self.btn_cancel.place(x=220, y=160)

        self.btn_add = tk.Button(self, text = "добавить")
        self.btn_add.place(x=300, y=160)
        self.btn_add.bind("<Button-1>", lambda event:
                          self.view.records(self.entry_name.get(),
                                            self.entry_tel.get(),
                                            self.entry_email.get()))



class Update (Child):
    def __init__(self):
        super().__init__()
        self.db=db
        self.init_update()
        self.default_data()

    def init_update(self):
        self.title('редактировать позицию')
        self.btn_add.destroy()          
        
        self.btn_upd = tk.Button(self, text = "Редактировать")
        self.btn_upd.bind("<Button-1>", 
                        lambda ev: self.view.update_record(
                            self.entry_name.get(),
                            self.entry_tel.get(),
                            self.entry_email.get()))
        self.btn_upd.bind("<Button-1>", lambda ev: self.destroy(), add = "+")
        self.btn_upd.place(x=300, y=160)


    def default_data(self):
        id = self.view.tree.set(self.view.tree.selection()[0], '#1')
        self.db.cur.execute(""" SELECT * FROM users WHERE ID=?""", (id))

        row = self.db.cur.fetchone()
        self.entry_name.insert(0, row[1])
        self.entry_tel.insert(0, row[2])
        self.entry_email.insert(0, row[3])
        

#класс окна поиска
class Search(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_Search()
        self.view = app

    def init_Search(self):
        self.title("Поиск")
        self.geometry("300x100")
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()

        #создание формы
        label_name = tk.Label(self, text="ФИО")
        label_name.place(x=30, y=30)
        

        self.entry_name = tk.Entry(self)
        self.entry_name.place(x=150, y=30)

        btn_cancel = tk.Button(self, text = "Закрыть", command=self.destroy)
        btn_cancel.place(x=160, y=70)
        
        self.btn_btn = tk.Button(self, text = "Найти")
        self.btn_btn.place(x=230, y=70)
        self.btn_btn.bind("<Button-1>", lambda ev: self.view.serch_records(self.entry_name.get()))
        self.btn_btn.bind("<Button-1>", lambda ev: self.destroy(), add = "+")





#класс бд
class Db:
    def __init__(self):
        self.conn = sqlite3.connect("Contacts.db")
        self.cur = self.conn.cursor()
        self.cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY NOT NULL,
                    name TEXT,
                    tel  TEXT,
                    email TEXT
                
                )""")
        self.conn.commit()

#добавление в базу данных
    def insert_data(self, name, tel, email):
        self.cur.execute(""" INSERT INTO users (name, tel, email) VALUES (?, ?, ?)""", (name, tel, email))
        self.conn.commit()
    


if __name__ == "__main__":
    root = tk.Tk()
    db = Db()
    app = Main(root)
    app.pack()
    root.title("Список")
    root.geometry("816x400")
    root.resizable(False, False)
    root.configure(bg='white')
    root.mainloop()


