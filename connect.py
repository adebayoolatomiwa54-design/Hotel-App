import sqlite3 as sql 
con=sql.connect('hotel.db')
con.row_factory = sql.Row
cur=con.cursor()

cur.execute(''' create table if not exists users(
   id integer primary key autoincrement,
   name varchar(20) not null,
   email varchar unique not null, 
   username varchar unique not null, 
   password varchar not null,
   gender text not null,
   address varchar not null,
   role varchar not null,
   age varchar not null
) ''')


cur.execute(''' create table if not exists rooms(
  id integer primary key autoincrement,
  room_no varchar unique not null,
  room_type varchar  not null, 
  price real not null, 
  status varchar not null default 'available'
)  ''')

cur.execute(''' create table if not exists guests(
  id integer primary key autoincrement,
  full_name varchar  not null,
  phone varchar  not null, 
  email varchar not null, 
  address varchar not null
  
)  ''')

cur.execute(''' create table if not exists bookings(
  id integer primary key autoincrement,
  guest_id integer  not null,
  room_id integer  not null, 
  checkin varchar not null, 
  checkout varchar,
  adults integer default 1,
  children integer default 0,
  status varchar not null default 'checked in',
  total real default 0,
  created_at varchar not null, 
  foreign key (guest_id) references guests(id),
  foreign key (room_id) references rooms(id)
)  ''')

