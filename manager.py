import tkinter
from PIL import Image,ImageTk
from tkinter import ttk
import connect
from tkinter import messagebox as msg
import sqlite3
from datetime import datetime

# demo of room price 
connect.con 
connect.cur
connect.cur.execute("select count(*) as c from rooms ")
count = connect.cur.fetchone()[0]  # Accessing the first element of the tuple
if count == 0:
    rooms=[
        ("101","Single Room",25000),
        ("102","Single Room",25000),
        ("103","Double Room",50000),
        ("104","Double Room",50000),
        ("201","Deluxe Room",75000),
        ("202","Deluxe Room",75000),
        ("301","Suite Room",100000),
        ("302","Suite Room",100000),
    ]
    connect.cur.executemany(
        "insert into rooms(room_no,room_type,price) values(?,?,?)",
        rooms
    )
    connect.con.commit()
    # connect.con.close()
class hotel_app():
    def __init__(self,root):
        self.root=root

        self.root.title("Manager Account")
        self.root.geometry('1350x1200+0+0')
        self.root.configure(bg="#fff")
        self.style=ttk.Style()
        self.main_ui()

    def main_ui(self):
        img=Image.open('images/logo.png')
        img=img.resize((200,100))
        img_tk=ImageTk.PhotoImage(img)
        img=Image.open('images/logo.png')
        img=img.resize((200,100))
        img_tk=ImageTk.PhotoImage(img)

        self.head=ttk.Frame(self.root,padding=12)
        self.head.pack(fill="x")
        # Create a label and keep a reference to the image
        lbl=tkinter.Label(self.head, image=img_tk)
        lbl.image = img_tk  # Keep a reference to avoid garbage collection
        lbl.place(x=0, y=0)

        ttk.Label(
            self.head,text="HOTEL MANAGEMENT SYSTEM",font=("verdana",20,"bold"),
            foreground="#000"
            ).pack(side="top")

        ttk.Label(self.head,text="logged in",font=("verdana",10,"bold"),
        ).pack(side="right", padx=10)
        ttk.Button(self.head,text="log out",command=self.logout).pack(side="right", padx=10)
     
        self.notebook=ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=5)

        self.dashboard_tab=ttk.Frame(self.notebook,padding=15)
        # lab=ttk.Label(self.dashboard_tab,text="Welcome Home")
        # lab.place(x=0,y=0)
        # self.dashboard_tab.place(x=0,y=0)
        self.rooms_tab=ttk.Frame(self.notebook,padding=15)
        self.guests_tab=ttk.Frame(self.notebook,padding=15)
        self.checkin_tab=ttk.Frame(self.notebook,padding=15)
        self.checkout_tab=ttk.Frame(self.notebook,padding=15)
        self.users_tab=ttk.Frame(self.notebook,padding=15)

        self.notebook.add(self.dashboard_tab,text="Dashboard")
        self.notebook.add(self.rooms_tab,text="Rooms")
        self.notebook.add(self.guests_tab,text="Guests")
        self.notebook.add(self.checkin_tab,text="Check-in/Allocation")
        self.notebook.add(self.checkout_tab,text="Check-out")
        self.notebook.add(self.users_tab,text="Users")
        
        # functions for tabs
        self.build_dashboard()
        self.build_rooms()
        self.build_guests()
        self.build_checkin()
        self.build_checkout()
        self.build_users()

    def build_dashboard(self):
         ttk.Label(
            self.dashboard_tab,
            text="Hotel Dashboard",
            font=("verdana", 22, "bold")
        ).pack(anchor="w", pady=(0, 20))
         self.cards = {}
         card_frame = ttk.Frame(self.dashboard_tab)
         card_frame.pack(fill="x")
         for title in ["Total Rooms", "Available", "Occupied", "Guests", "Active Bookings"]:
            f = ttk.LabelFrame(card_frame, text=title, padding=25)
            f.pack(side="left", fill="both", expand=True, padx=5)
            label = ttk.Label(f, text="0", font=("verdana", 26, "bold"))
            label.pack()
            self.cards[title] = label
         ttk.Label(
            self.dashboard_tab,
            text="Quick actions",
            font=("Arial", 15, "bold")
        ).pack(anchor="w", pady=(35, 10))
         actions = ttk.Frame(self.dashboard_tab)
         actions.pack(anchor="w")
         ttk.Button(
            actions, text="Allocate / Check In",
            command=lambda: self.notebook.select(self.checkin_tab)
        ).pack(side="left", padx=5)
         ttk.Button(
            actions, text="Manage Rooms",
            command=lambda: self.notebook.select(self.rooms_tab)
        ).pack(side="left", padx=5)
         ttk.Button(
            actions, text="Manage Guests",
            command=lambda: self.notebook.select(self.guests_tab)
        ).pack(side="left", padx=5)
         ttk.Button(
            actions, text="Check Out",
            command=lambda: self.notebook.select(self.checkout_tab)
        ).pack(side="left", padx=5)

         self.refreshDashboard()


    def refreshDashboard(self):
        connect.con 
        connect.cur 
        total=connect.cur.execute("select count(*) as c from rooms").fetchone()['c']
        
        guests=connect.cur.execute("select count(*) as c from guests").fetchone()['c']

        available=connect.cur.execute('''select count(*) as c from rooms
        where status='available' 
        ''').fetchone()['c']

        occupied=connect.cur.execute('''select count(*) as c from rooms
        where status='Occupied' 
        ''').fetchone()['c']
        bookings=connect.cur.execute('''select count(*) as c from bookings
        where status='Checked In' 
        ''').fetchone()['c']

        self.cards['Total Rooms'].config(text=str(total))
        self.cards['Available'].config(text=str(available))
        self.cards['Occupied'].config(text=str(occupied))
        self.cards['Guests'].config(text=str(guests))
        self.cards['Active Bookings'].config(text=str(bookings))


    def build_rooms(self):
        
        form = ttk.LabelFrame(self.rooms_tab, text="Room Information", padding=12)
        form.pack(fill="x")
        ttk.Label(form, text="Room No").grid(row=0, column=0, padx=5, pady=5)
        self.room_no = ttk.Entry(form, width=15)
        self.room_no.grid(row=0, column=1, padx=5)
        ttk.Label(form, text="Room Type").grid(row=0, column=2, padx=5)
        rooms=["Single room", "Double room", "Deluxe room", "Suite room"]
        self.room_type = ttk.Combobox(
            form, values=rooms,
            state="readonly", width=15
        )
        self.room_type.grid(row=0, column=3, padx=5)
        self.room_type.set("Single room")
        ttk.Label(form, text="Price / Night").grid(row=0, column=4, padx=5)
        self.room_price = ttk.Entry(form, width=15)
        self.room_price.grid(row=0, column=5, padx=5)
        ttk.Button(
            form, text="Add Room",command=self.add_rooms
        ).grid(row=0, column=6, padx=10)
        ttk.Button(
            form, text="Delete Room",command=self.delete_rooms
        ).grid(row=0, column=7, padx=5)
        cols = ("id", "room_no", "type", "price", "status")
        self.room_tree = ttk.Treeview(
            self.rooms_tab, columns=cols, show="headings", height=18
        )
     
        headings = {
            "id": "Positon", "room_no": "Room No",
            "type": "Type", "price": "Price/Night", "status": "Status"
        }

        for column in cols:
            self.room_tree.heading(column, text=headings[column])
            self.room_tree.column(column, width=5)
        self.refresh_rooms()
        self.room_tree.pack(fill="both", expand=True, pady=12)
        
    def add_rooms(self):
        room_no=self.room_no.get().strip()
        room_type=self.room_type.get().strip()
        price_text=self.room_price.get()

        if not room_no or not price_text:
            msg.showinfo("Validator", "Enter room no and price")
            return
        # if room_no=="" or price_text==:
        try:
            price=float(price_text)
        except ValueError:
            msg.showinfo("Validator","price must be numeric")
            return 
        connect.con
        connect.cur

        try:
            connect.cur.execute("insert into rooms (room_no,room_type, price) values(?,?,?) ",
            (room_no,room_type,price))
            connect.con.commit()
            msg.showinfo("Success","Room added successfully")

            # delete after insertion 
            self.room_no.delete(0,"end")
            self.room_price.delete(0,"end")

        except sqlite3.IntegrityError:
            msg.showerror("Error","Room no already exists")
        finally:
            connect.con.close

        self.refreshall()

    def delete_rooms(self):    
        selected=self.room_tree.selection()
        if not selected:
            msg.showwarning("Select","select a room first")
            return 
        room_id=self.room_tree.item(selected[0])["values"][0]

        connect.con 
        connect.cur
        active=connect.cur.execute("select id from bookings where room_id=? and status='Checked In'",
        (room_id,)).fetchone()
        if active:
            # connect.con.close()
            msg.showerror("Error", "Occupied rooms cannot be deleted")
            return

        connect.cur.execute("delete from rooms where id=?",(room_id,))
        connect.con.commit()
        # connect.con.close()
        self.refreshall()

    def refreshall(self):
        self.refresh_rooms()
        self.build_dashboard()
        self.build_guests()
        self.build_checkin()
        self.build_checkout()
        self.build_users()
        self.build_users()
        self.build_guests()
        self.refresh_guests()
        # self.check_out()


    def refresh_rooms(self):
        for item in self.room_tree.get_children():
            self.room_tree.delete(item)

        connect.con 
        connect.cur 
        rows=connect.cur.execute(
            "select * from rooms order by room_no"
        ).fetchall()

        # connect.con.close()

        for r in rows:
            self.room_tree.insert(
                "", "end",
                  values=(r[0], r[1], r[2], f'₦{r[3]:,.2f}', r[4])
            )
    def logout(self):
        if msg.askyesno("Logout","Are you sure you want to logout?"):
            root.destroy()
            return


      # ---------- GUESTS ----------
    def build_guests(self):
        form = ttk.LabelFrame(self.guests_tab, text="Guest Information", padding=12)
        form.pack(fill="x")

        labels = ["Full Name", "Phone", "Email", "Address"]
        self.guest_entries = []

        for i, label in enumerate(labels):
            ttk.Label(form, text=label).grid(row=0, column=i*2, padx=5)
            e = ttk.Entry(form, width=22)
            e.grid(row=0, column=i*2+1, padx=5)
            self.guest_entries.append(e)

        ttk.Button(
            form, text="Add Guest", command=self.add_guest
        ).grid(row=0, column=8, padx=10)

        cols = ("id", "name", "phone", "email", "address")
        self.guest_tree = ttk.Treeview(
            self.guests_tab, columns=cols, show="headings", height=18
        )
        for c, text, width in [
            ("id", "ID", 20), ("name", "Full Name", 60),
            ("phone", "Phone", 80), ("email", "Email", 60),
            ("address", "Address", 200)
        ]:
            self.guest_tree.heading(c, text=text)
            self.guest_tree.column(c, width=width)
        self. refresh_guests()
        self.guest_tree.pack(fill="both", expand=True, pady=12)

    def add_guest(self):
        values = [e.get().strip() for e in self.guest_entries]

        if not values[0]:
            msg.showwarning("Validation", "Guest name is required.")
            return

        connect.con
        connect.cur
        connect.cur.execute(
            "INSERT INTO guests(full_name,phone,email,address) VALUES(?,?,?,?)",
            values
        )
        connect.con.commit()
        # msg.showinfo("success","Submitted successfully")
        # connect.con.close()

        for e in self.guest_entries:
            e.delete(0, "end")

        msg.showinfo("Success", "Guest registered.")

        self.refresh_guests()

    def refresh_guests(self):
        for item in self.guest_tree.get_children():
             self.guest_tree.delete(item)

        connect.con 
        connect.cur 
        rows=connect.cur.execute(
            "select * from guests order by id"
        ).fetchall()

        # connect.con.close()

        for r in rows:
             self.guest_tree.insert(
                "", "end",
                  values=(r[0], r[1], r[2], r[3], r[4])
            )

    def build_checkin(self):
        form = ttk.LabelFrame(
            self.checkin_tab,
            text="Room Allocation and Guest Check-In",
            padding=15
        )
        form.pack(fill="x")

        ttk.Label(form, text="Guest").grid(row=0, column=0, padx=5, pady=8)
        self.checkin_guest = ttk.Combobox(form, state="readonly", width=35)
        self.checkin_guest.grid(row=0, column=1, padx=5)

        ttk.Label(form, text="Available Room").grid(row=0, column=2, padx=5)
        self.checkin_room = ttk.Combobox(form, state="readonly", width=40)
        self.checkin_room.grid(row=0, column=3, padx=5)

        ttk.Label(form, text="Adults").grid(row=1, column=0, padx=5)
        self.adults = ttk.Spinbox(form, from_=1, to=20, width=8)
        self.adults.grid(row=1, column=1, sticky="w", padx=5)
        self.adults.set(1)

        ttk.Label(form, text="Children").grid(row=1, column=2, padx=5)
        self.children = ttk.Spinbox(form, from_=0, to=20, width=8)
        self.children.grid(row=1, column=3, sticky="w", padx=5)
        self.children.set(0)

        ttk.Button(
            form, text="CHECK IN / ALLOCATE ROOM",
            command=self.check_in
        ).grid(row=2, column=0, columnspan=4, pady=15)

        ttk.Button(
            form, text="Refresh Available Rooms",
            command=self.refresh_checkin_options
        ).grid(row=2, column=4, padx=10)

        cols = (
            "id", "guest", "room", "type",
            "checkin", "adults", "children", "total", "status"
        )
        self.booking_tree = ttk.Treeview(
            self.checkin_tab, columns=cols, show="headings", height=14
        )

        for c, text, width in [
            ("id", "ID", 50), ("guest", "Guest", 180),
            ("room", "Room", 80), ("type", "Type", 100),
            ("checkin", "Check-In", 150), ("adults", "Adults", 70),
            ("children", "Children", 80), ("total", "Total", 100),
            ("status", "Status", 100)
        ]:
            self.booking_tree.heading(c, text=text)
            self.booking_tree.column(c, width=width)

        self.refresh_checkin_options()
        self.booking_tree.pack(fill="both", expand=True, pady=12)

    def refreshcheckin(self):
        for item in self.booking_tree.get_children():
            self.booking_tree.delete(item)
        connect.con
        connect.cur
        rows=connect.cur.execute("""
            SELECT b.*, g.full_name, r.room_no, r.room_type, r.price, b.children
            FROM bookings b
            JOIN guests g ON g.id=b.guest_id
            JOIN rooms r ON r.id=b.room_id
            WHERE b.status='Checked In
            ORDER BY b.id DESC 
            """).fetchall()
            # conn.close()
            
        today = datetime.now().date()
        for b in rows:
            checkin_date = datetime.strptime(
            b["checkin"], "%Y-%m-%d %H:%M:%S"
            ).date()
            nights + max(1, (today - checkin_date).days)
            estimated = nights *b ["price"]

            self.booking_tree.insert(
                 "", "end",
                 values=(
                      b["id"],b ["full_name"], b["room-no"],
                      b["room_type"], b["checkin"], nights,
                      b["children"],
                      f"N{estimated:,.2F}",
                      b["status"]
            ))
        
   
    def check_in(self):
        guest_value = self.checkin_guest.get()
        room_value = self.checkin_room.get()

        if not guest_value or not room_value:
            msg.showwarning(
                "Validation", "Select a guest and an available room."
            )
            return

        guest_id = int(guest_value.split("|")[0])
        room_id = int(room_value.split("|")[0])

        try:
            adults = int(self.adults.get())
            children = int(self.children.get())
        except ValueError:
            msg.showerror("Validation", "Adults and children must be numbers.")
            return

        connect.con
        connect.cur
        room = connect.cur.execute(
            "SELECT * FROM rooms WHERE id=? AND status='available'",
            (room_id,)
        ).fetchone()

        if not room:
            # connect.con.close()
            msg.showerror("Error", "Room is no longer available.")
            # self.refreshall()
            return

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        connect.cur.execute("""
            INSERT INTO bookings
            (guest_id,room_id,checkin,adults,children,status,total,created_at)
            VALUES(?,?,?,?,?,'Checked In',?,?)
        """, (guest_id, room_id, now, adults, children, room[3], now))

        connect.cur.execute(
            "UPDATE rooms SET status='Occupied' WHERE id=?",
            (room_id,)
        )

        connect.con.commit()


        msg.showinfo(
            "Check-In Successful",
            f"Guest checked in.\nRoom: {room[1]}\n"
            f"Rate: ₦{room[3]:,.2f} per night"
        )
        # self.refreshall()

    def refresh_checkin_options(self):
        connect.con
        connect.cur

        guests = connect.cur.execute(
            "SELECT id,full_name,phone,email,address FROM guests ORDER BY full_name"
        ).fetchall()

        rooms = connect.cur.execute("""
            SELECT id,room_no,room_type,price
            FROM rooms
            WHERE status='Available'
            ORDER BY room_no
        """).fetchall()

        # conn.close()

        self.checkin_guest["values"] = [
            f"{g[0]} | {g[1]} | {g[2]}| {g[3]}| {g[4]}"
            for g in guests
        ]
        self.checkin_room["values"] = [
            f"{r[0]} | Room {r[1]} | {r[2]} | ₦{r[3]:,.2f}"
            for r in rooms
        ]
        if self.checkin_guest["values"] and not self.checkin_guest.get():
            self.checkin_guest.current(0)

        if self.checkin_room["values"] and not self.checkin_room.get():
            self.checkin_room.current(0)

   
      # ---------- CHECK OUT ----------
    def build_checkout(self):
        ttk.Label(
            self.checkout_tab,
            text="Active Guests / Check-Out",
            font=("Arial", 18, "bold")
        ).pack(anchor="w")

        cols = (
            "id", "guest", "room", "type", "checkin",
            "nights", "rate", "total", "status"
        )

        self.checkout_tree = ttk.Treeview(
            self.checkout_tab, columns=cols, show="headings", height=15
        )

        for c, text, width in [
            ("id", "Booking", 70), ("guest", "Guest", 190),
            ("room", "Room", 80), ("type", "Type", 100),
            ("checkin", "Check-In", 150), ("nights", "Nights", 80),
            ("rate", "Rate", 100), ("total", "Estimated Total", 130),
            ("status", "Status", 100)
        ]:
            self.checkout_tree.heading(c, text=text)
            self.checkout_tree.column(c, width=width)

        self.checkout_tree.pack(fill="both", pady=15)

        ttk.Button(
            self.checkout_tab,
            text="CHECK OUT SELECTED GUEST",
            command=self.check_out
        ).pack(anchor="e")

        self.refresh_checkout()

    
    def refresh_checkout(self):
        for item in self.checkout_tree.get_children():
            self.checkout_tree.delete(item)

        connect.con
        connect.cur
        rows = connect.cur.execute("""
            SELECT b.*, g.full_name, r.room_no, r.room_type, r.price
            FROM bookings b
            JOIN guests g ON g.id=b.guest_id
            JOIN rooms r ON r.id=b.room_id
            WHERE b.status='Checked In'
            ORDER BY b.id DESC
        """).fetchall()
        # conn.close()

        today = datetime.now().date()

        for b in rows:
            checkin_date = datetime.strptime(
                b["checkin"], "%Y-%m-%d %H:%M:%S"
            ).date()
            nights = max(1, (today - checkin_date).days)
            estimated = nights * b["price"]

            self.checkout_tree.insert(
                "", "end",
                values=(
                    b["id"], b["full_name"], b["room_no"],
                    b["room_type"], b["checkin"], nights,
                    f"₦{b['price']:,.2f}",
                    f"{estimated:,.2f}",
                    b["status"]
                )
            )

    def check_out(self):
        selected = self.checkout_tree.selection()

        if not selected:
            msg.showwarning("Select", "Select at least one booking to check out.")
            return
        # Collect selected bookings
        bookings_selected = []
        for item in selected:
            values = self.checkout_tree.item(item)["values"]
            bookings_selected.append({
                "id": values[0],
                "guest": values[1],
                "room_no": values[2],
                "total": values[7]
            })
        # Confirmation message
        details = "\n".join(
            f"• {b['guest']} - Room {b['room_no']}"
            for b in bookings_selected
        )
        if not msg.askyesno(
            "Confirm Check-Out",
            f"Check out the following {len(bookings_selected)} booking(s)?\n\n"
            f"{details}"
        ):
            return
        try:
            checkout = datetime.now()
            checkout_str = checkout.strftime("%Y-%m-%d %H:%M:%S")

            checkout_results = []

            for b in bookings_selected:

                booking = connect.cur.execute(
                    """
                    SELECT room_id, checkin
                    FROM bookings
                    WHERE id=? AND status='Checked In'
                    """,
                    (b["id"],)
                ).fetchone()

                # Booking may have already been checked out
                if not booking:
                    continue

                checkin_dt = datetime.strptime(
                    booking["checkin"],
                    "%Y-%m-%d %H:%M:%S"
                )

                # Calculate number of nights
                nights = max(
                    1,
                    (checkout.date() - checkin_dt.date()).days
                )

                # Get room price
                room = connect.cur.execute(
                    """
                    SELECT price
                    FROM rooms
                    WHERE id=?
                    """,
                    (booking["room_id"],)
                ).fetchone()

                if not room:
                    continue

                final_total = nights * room["price"]

                # Update booking
                connect.cur.execute(
                    """
                    UPDATE bookings
                    SET checkout=?,
                        status='Checked Out',
                        total=?
                    WHERE id=?
                    """,
                    (
                        checkout_str,
                        final_total,
                        b["id"]
                    )
                )

                # Make room available
                connect.cur.execute(
                    """
                    UPDATE rooms
                    SET status='Available'
                    WHERE id=?
                    """,
                    (booking["room_id"],)
                )

                checkout_results.append({
                    "guest": b["guest"],
                    "room_no": b["room_no"],
                    "nights": nights,
                    "total": final_total
                })

            # Save all changes at once
            connect.con.commit()

            if not checkout_results:
                msg.showerror(
                    "Error",
                    "None of the selected bookings are still active."
                )
                # self.refresh_all()
                return

            # Calculate grand total
            grand_total = sum(
                item["total"] for item in checkout_results
            )

            # Create result message
            result = ""

            for item in checkout_results:
                result += (
                    f"Guest: {item['guest']}\n"
                    f"Room: {item['room_no']}\n"
                    f"Nights: {item['nights']}\n"
                    f"Bill: ₦{item['total']:,.2f}\n"
                    f"{'-' * 35}\n"
                )

            result += f"\nGRAND TOTAL: ₦{grand_total:,.2f}"

            msg.showinfo(
                "Check-Out Complete",
                f"{len(checkout_results)} booking(s) checked out successfully.\n\n"
                f"{result}"
            )

            # Refresh Treeview
            # self.refresh_all()

        except Exception as e:
            connect.con.rollback()

            msg.showerror(
                "Check-Out Error",
                f"An error occurred during check-out:\n\n{e}"
            )
        # Collect selected bookings
            bookings_selected = []

            for item in selected:
                values = self.checkout_tree.item(item)["values"]

                bookings_selected.append({
                    "id": values[0],
                    "guest": values[1],
                    "room_no": values[2],
                    "total": values[7]
                })

                # Confirmation message
                details = "\n".join(
                    f"• {b['guest']} - Room {b['room_no']}"
                    for b in bookings_selected
                )

                if not msg.askyesno(
                    "Confirm Check-Out",
                    f"Check out the following {len(bookings_selected)} booking(s)?\n\n"
                    f"{details}"
                ):
                    return

            try:
                connect.cur.execute(
                    """
                    UPDATE rooms
                    SET status='available'
                    WHERE id=?
                    """,
                    (booking["room_id"],)
                )

                checkout_results.append({
                    "guest": b["guest"],
                    "room_no": b["room_no"],
                    "nights": nights,
                    "total": final_total
                })

            # Save all changes at once
                connect.con.commit()

                if not checkout_results:
                    msg.showerror(
                        "Error",
                        "None of the selected bookings are still active."
                    )
                    self.refresh_all()
                    return

                # Calculate grand total
                grand_total = sum(
                    item["total"] for item in checkout_results
                )

                # Create result message
                result = ""

                for item in checkout_results:
                    result += (
                        f"Guest: {item['guest']}\n"
                        f"Room: {item['room_no']}\n"
                        f"Nights: {item['nights']}\n"
                        f"Bill: ₦{item['total']:,.2f}\n"
                        f"{'-' * 35}\n"
                    )

                result += f"\nGRAND TOTAL: ₦{grand_total:,.2f}"

                msg.showinfo(
                    "Check-Out Complete",
                    f"{len(checkout_results)} booking(s) checked out successfully.\n\n"
                    f"{result}"
                )

                # Refresh Treeview
                self.refresh_all()

            except Exception as e:
                connect.con.rollback()

            msg.showerror(
                "Check-Out Error",
                f"An error occurred during check-out:\n\n{e}"
            )
    
        
    def build_users(self):
        form = ttk.LabelFrame(self.users_tab, text="Create User", padding=15)
        form.pack(fill="x")

        ttk.Button(
            form, text="Edit User"
        ).grid(row=0, column=0, padx=10)

        ttk.Label(form, text="UserID").grid(row=2, column=2, padx=5)
        self.user_id= ttk.Entry(form,width=20)
        self.user_id.grid(row=2, column=2, padx=5)

        ttk.Button(
            form, text="Find User"
        ).grid(row=2, column=6, padx=10)
       
        ttk.Button(
            form, text="Delete User"
        ).grid(row=2, column=7, padx=10)
       


        cols = ("id", "username", "role")
        self.user_tree = ttk.Treeview(
            self.users_tab, columns=cols, show="headings", height=18
        )
        for c, text in [
            ("id", "ID"), ("username", "Username"), ("role", "Role")
        ]:
            self.user_tree.heading(c, text=text)
            self.user_tree.column(c, width=180)

        self.user_tree.pack(fill="both", expand=True, pady=15)
    def refreshUser(self):
        for item in self.user_tree.get_children():
            self.user_tree.delete(item)

        connect.con
        connect.cur
        rows=connect.cur.execute(
            "select * from users order by id"
        ).fetchall()

        #connect.con.close()

        for r in rows:
            self.user_tree.insert(
                "", "end",
                values=(r[0], r[1], r[2], r[3], r[4])
            )


__name__=="__main__"
root=tkinter.Tk()
hotel_app(root)
root.mainloop()