import os
import sqlite3
import tkinter as tk
from MenuPage import MenuPage

root = tk.Tk()

dird = os.path.dirname(os.path.abspath(__file__))
dbpath = os.path.join(dird, "text.db")

if os.path.exists(dbpath):
    os.remove(dbpath)

conn = sqlite3.connect(dbpath)
conn.execute('CREATE TABLE "info" ("id" INTEGER, "name" TEXT, "url" TEXT, "comment" TEXT, "times" TEXT, "vecmatch" NUMERIC, PRIMARY KEY("id" AUTOINCREMENT));')

MenuPage(root)

root.mainloop()
