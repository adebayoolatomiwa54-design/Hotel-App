
# import tkinter as tk
# root=tk.Tk()
# root.title("Introduction to GUI")
# root.geometry('400x700+500+0')
# root.configure(background="#feccfe")
# root.resizable(0,0)
# root.mainloop()
from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry
import connect
from tkinter import messagebox as msg
import sqlite3 as sql
import os

def login():
    root.destroy()
    os.system('python login.py')

def reg():
    username=entu.get()
    name=entn.get()
    password=entp.get()
    email=entem.get()
    gender=entg.get()
    address=entad.get(1.0, "end")
    age=date_entry.get()
    role=user_role.get()

    if "@" not in email:
        msg.showerror("prompt","email must contain @!!!")
    if name=="" and username=="" and password=="" and email=="" and role=="":
        msg.showinfo("Alert","Empty field not allowed please fill the form correctly")
        return   
    try:
            connect.con
            connect.cur
            connect.cur.execute(''' insert into users(
            name,username,email,password,gender,address,age,role) values(?,?,?,?,?,?,?,?)
            ''',(name,username,email,password,gender,address,age,role))
            connect.con.commit()
            msg.showinfo("success","message sent successfully ")
            login()
            entu.delete(0,'end')
            entn.delete(0,'end')
            entp.delete(0,'end')
            entem.delete(0,'end')
            entg.delete(0,'end')
            entad.delete(1.0,'end')
            date_entry.delete(0,'end')
    except sql.IntegrityError:
            msg.showerror("error",f"{username} and {email} already exists... try another entry!!!")

        
root=Tk()
root.title("Introduction to GUI")
root.geometry('400x500+500+0')
root.configure(background="#f91aa7")
root.resizable(0,0)

lblhead=Label(root,text="Registration Page", font=("verdana",20,"bold"),bg="#f91aa7",fg="white")
lblhead.pack()
# name, age,gender,email,passoword,username,address 
# www.tpointtech.com/tkinter
fr=Frame(root, width=400, height=100, bg="#f91aa7")
lbln=Label(fr, text="Name: ", font=("verdana",14),bg="#f91aa7",fg="white")
lbln.grid(row=0,column=0)
entn=Entry(fr,width=40, relief="flat")
entn.grid(row=0, column=1)
# email
lblem=Label(fr, text="Email: ", font=("verdana",14),bg="#f91aa7",fg="white")
lblem.grid(row=1,column=0)
entem=Entry(fr,width=40, relief="flat")
entem.grid(row=1, column=1)

# Username
lblu=Label(fr, text="UserName: ", font=("verdana",14),bg="#f91aa7",fg="white")
lblu.grid(row=2,column=0)
entu=Entry(fr,width=40, relief="flat")
entu.grid(row=2, column=1)

# Password
lblp=Label(fr, text="Password: ", font=("verdana",14),bg="#f91aa7",fg="white")
lblp.grid(row=3,column=0)
entp=Entry(fr,width=40, relief="flat", show="*")
entp.grid(row=3, column=1)

# Gender
gender=["Male","Female"]
lblg=Label(fr, text="Gender: ", font=("verdana",14),bg="#f91aa7",fg="white")
lblg.grid(row=4,column=0)
entg=ttk.Combobox(fr,width=38,values=gender)
entg.grid(row=4, column=1)

# Addess
lblad=Label(fr, text="Address: ", font=("verdana",14),bg="#f91aa7",fg="white")
lblad.grid(row=5,column=0)
entad=Text(fr,width=30, height=5)
entad.grid(row=5, column=1)

#user role
lblr=Label(fr, text="Role: ", font=("verdana",14),bg="#f91aa7",fg="white")
lblr.grid(row=6, column=0)
role=["hotel manager","receptionist"]
user_role=ttk.Combobox(fr,width=38, values=role)
user_role.grid(row=6, column=1)

# Age
lblag=Label(fr, text="DOB: ", font=("verdana",14),bg="#f91aa7",fg="white")
lblag.grid(row=7,column=0)
date_entry = DateEntry(fr, width=38, borderwidth=2)
date_entry.grid(row=7, column=1)

already=Button(fr, width=40, bg="#f91aa7", fg="white", text="Already have an account login!", command=login, relief="flat")
already.grid(row=9,column=1)

btnReg=Button(fr, width=15, bg="black", fg="white", text="Sign up", command=reg)
btnReg.grid(row=8,column=1)
fr.pack()
root.mainloop()