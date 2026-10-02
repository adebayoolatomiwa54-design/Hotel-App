from tkinter import *
from tkinter import ttk
import connect
from tkinter import messagebox as msg
import os
import sqlite3
def manager():
    os.system('python manager.py')
def recept():
    os.system('python rec.py')
def login():
    root.destroy()
    os.system('python intro.py')

def log():
    username=entu.get()
    password=entp.get()
    role=user_role.get()
    if username=="" and password=="" and role=="":
        msg.showinfo("Alert","Empty record not allowed, please fill the form!!!")
        return   
    connect.con 
    connect.cur 
    connect.cur.execute(''' select * from users where username=? and password=? and role=?''',(username,password,role))
    result=connect.cur.fetchone()
    if result:
        msg.showinfo("Success","Record found!!!")
        root.destroy()
        if role.lower()=="hotel manager":
            manager()
        elif role.lower()=="receptionist":
            recept()
            return
    else:
        msg.showinfo("Alert","UnAuthorized Login")
    # connect.con.close()
                     
root=Tk()
root.title("Loginpage")
root.geometry('400x400+500+0')
root.configure(background="#f91aa7")
root.resizable(0,0)
lblhead=Label(root,text="Login Page", font=("verdana",20,"bold"),bg="#f91aa7", fg="white")
lblhead.pack(pady=(60,20))

#username
fr=Frame(root, width=400, height=100, bg="#f91aa7" )
lblu=Label(fr, text="Username: ", font=("verdana",14),bg="#f91aa7",fg="white")
lblu.grid(row=0, column=0)
entu=Entry(fr,width=40, relief="flat")
entu.grid(row=0, column=1)

#Password
lblp=Label(fr, text="Password: ", font=("verdana",14),bg="#f91aa7",fg="white")
lblp.grid(row=1, column=0)
entp=Entry(fr,width=40, relief="flat", show="*")
entp.grid(row=1, column=1)

#user role
lblr=Label(fr, text="Role: ", font=("verdana",14),bg="#f91aa7",fg="white")
lblr.grid(row=2, column=0)
role=["hotel manager","receptionist"]
user_role=ttk.Combobox(fr,width=38, values=role)
user_role.grid(row=2, column=1)

btnLogin=Button(fr, width=15, bg="black", fg="white", text="LOGIN", command=log)
btnLogin.grid(row=3, column=1, pady=20)

btnReg=Button(fr, width=15, bg="black", fg="white",relief=FLAT,text="Don't have an account: login!", command=login)
btnReg.grid(row=4, column=1)


fr.pack(pady=20)
root.mainloop()