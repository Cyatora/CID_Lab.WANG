import tkinter as tk
from tkinter import *
from tkinter import ttk,messagebox
import threading
from tkinterweb import HtmlFrame 
import sqlite3
import pandas
import glob
import os
import shutil
from tkinter import filedialog
from datacapture import commentget
from ctget import *
from doc2vec2 import v2cv 
from datacapture import insertdb_
closing=True
class MenuPage:
    def __init__(self,master=None):
        self.root = master
        self.tmp=''
        self.result='https://news.yahoo.co.jp'
        self.tabControl = ttk.Notebook(self.root)
        self.tabControl.lift()
        self.root.protocol('WM_DELETE_WINDOW', lambda: self.thread_it(self.clos_window))
        self.root.geometry('1200x700+0+0')
        self.root.title('コメントフィルタリング')
        self.root.columnconfigure(0, weight=1)
        self.tab0 = ttk.Frame(self.tabControl) 
        self.tab1 = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab0, text ='ニュース')
        self.tabControl.add(self.tab1, text ='コメント欄')
        dird=os.path.dirname(os.path.abspath(__file__))
        self.dbpath=os.path.join(dird, "text.db")
        self.conn = sqlite3.connect(self.dbpath)
        self.excelfile=os.path.join(dird,'output.xlsx')
        self.frm1=Frame(self.tab0)
        self.frm2=Frame(self.tab1)
#####
        ##调整字体大小方法1
        # font = Font(size=12)  # 根据需要调整字体大小
        # 调整字体大小方法2：创建样式
        style = ttk.Style()
        style.configure('Treeview', font=('Meiryo', 12))  # 根据需要调整字体和字号，初始为10。字体最初是Arial
        columns = ('username',"comment")
        self.treeview = ttk.Treeview(self.frm2, show="headings", columns=columns,selectmode='browse')
        # 将样式应用于treeview
        self.treeview.configure(style='Treeview')
        self.treeview.heading("comment", text="コメント", anchor='w')
        self.treeview.column("username", width=60, anchor='w',stretch=False)
        self.treeview.column("comment",width=8000, anchor='w')  #评论列宽显示长度
        self.treeview.heading("username", text="名前",anchor='w') 
        self.treeview.heading("comment", text="コメント",anchor='w') 
        self.treeview_scrollbar_v = ttk.Scrollbar(self.frm2,orient=VERTICAL,command=self.treeview.yview) #tk.VERTICAL
        self.treeview_scrollbar_h = ttk.Scrollbar(self.frm2,orient=HORIZONTAL,command=self.treeview.xview) #tk.HORIZONTAL
        self.treeview.configure(yscrollcommand=self.treeview_scrollbar_v.set, xscrollcommand=self.treeview_scrollbar_h.set) 
        self.treeview_scrollbar_v.pack(side=RIGHT, fill=Y) #tk.RIGHT tk.Y
        self.treeview_scrollbar_h.pack(side=BOTTOM, fill=X) #tk.BOTTOM tk.X
        self.treeview.pack(expand=True, fill=BOTH) #tk.BOTH
#####
        self.htmlint=os.path.join(dird,'html/')
        self.filename=''        

        self.frame = HtmlFrame(self.frm1)
        self.create_page()

    def thread_start_check(self,func, *args):
        global t1
        t1 = threading.Thread(target=func,args=())
        t1.setDaemon(True)
        t1.start()
        


    def delrec(self):
        dird=os.path.dirname(os.path.abspath(__file__))
        dbpath=os.path.join(dird, "text.db")
        conn = sqlite3.connect(dbpath)
        conn.execute('delete from info')
        conn.execute("update sqlite_sequence SET seq = 0 where name ='info';")
        conn.commit()
    def create_page(self,event=0):
        self.tmp=''
        self.tabControl.pack(expand=True, fill ="both")
        
        self.tabControl.bind('<<NotebookTabChanged>>', self.on_tab_change)
##       
        self.frm1.place(x=0,y=50,height=800,width=1400)
        self.frm1.lift()
        self.frm2.config(height=610,width=1030) #评论区显示行数调整，初始为600；470的时候显示21条评论;460的时候显示20条评论;评论区显示列宽调整，初始为1030  
        self.frm2.place(x=0,y=0)
        self.frm2.lift()
        self.frm2.pack_propagate(0)

####
        btn3=Button(self.tab1,text='投稿する',command=self.localcomment)
        btn3.place(x=910,y=618,width=60)

        button_open = tk.Button(self.tab1, text='開く', command=self.open)
        button_open.place(x=1040,y=615,width=60)

        button_save = tk.Button(self.tab1, text='保存', command=self.save)
        button_save.place(x=1120,y=615,width=60)
                
        self.LineEdit = tk.Entry(self.tab0)
        self.LineEdit["borderwidth"] = "2px"
        self.LineEdit.place(x=0,y=0,width=1400)

        self.lbinpvar=Label(self.tab1,text='類似度を入力する')
        
        self.lbinpvar.place(x=1025,y=545,width=180)


        self.LineEditsc   = tk.Entry(self.tab1)
        self.LineEditsc["borderwidth"] = "2px"
        self.LineEditsc.place(x=1045,y=570,width=70)
        
        insertbtnsc = Button(self.tab1, text = "Enter", command = self.setscrvar)
        insertbtnsc.place(x=1135,y=567,width=50)
        
        insertbtn = Button(self.tab0, text = "URL訪問", command = self.select_file)
        insertbtn.place(x=1050,y=25,width=100)
        
        self.lbstatus=Label(self.tab1,text='ステータスバー',fg='blue')
        
        self.lbstatus.pack(side=BOTTOM,anchor='s')

        var_h1=tk.DoubleVar()

        var_h1.set(1.0)
        self.scale_v=tk.Scale(self.tab1,variable=var_h1,from_=12,to=0,
                              tickinterval=2,
                              label="類似度",
                              resolution=0.01, 
                              
                              orient=tk.VERTICAL,
                              command=self.vetor)
        self.scale_v.place(x=1050,y=0,height=540)
        self.scale_v.set(0)

        self.lb = Label(self.tab1, text="コメントを書く:")
        self.lb.place(x=0,y=620,width=100)

        
        self.nameline = tk.Entry(self.tab1)
        self.nameline["borderwidth"] = "2px"
        self.nameline.place(x=100,y=620,width=800)

        
        self.tt = tk.StringVar()
        self.tt.set("読み込みが完了したら類似度を入力してください")
        self.lb1 = tk.Label(self.tab1, textvariable=self.tt)
        self.lb1.pack()
        self.root.protocol('WM_DELETE_WINDOW' ,self.closewindow)
        
    def open(self):
        dbpath=filedialog.askopenfilename(filetypes=(("Database Flies","*.db"),("All files","*.*")))
        if dbpath:
            self.conn.close()
            self.conn=sqlite3.connect(dbpath)  
    
    def save(self):
        destination = filedialog.asksaveasfilename(defaultextension=".db", filetypes=(("Database Files", "*.db"), ("All files", "*.*")))
        if destination:
            self.conn.close()
            shutil.copy(self.dbpath,destination)
            self.conn=sqlite3.connect(self.dbpath)


    def localcomment(self):
        
        comment=self.nameline.get()
        cturl=self.result
        
        content=contentget(url=cturl)
        
        insertdb_('localuser',str(comment),'localhost',str(content))
        j=self.seldata('info')
        for i in j:
                self.treeview.insert('','end', values=(
                                                    i[1],
                                                    i[3],
                                                    ))
    def closewindow(self):
        global closing
        print('close windows')
        closing=False
    def setscrvar(self):
        inp=self.LineEditsc.get()
        self.scale_v.set(inp)
    def vetor(self,i):
        
        
        c=self.conn.cursor()
        
        c.execute(f"SELECT * from 'info' where vecmatch >= {i}")
        
        
        rows=c.fetchall()
        
        x=self.treeview.get_children()
        for item in x:
            self.treeview.delete(item)
        for i in rows:
                self.treeview.insert('','end', values=(
                                                    i[1],
                                                    i[3],
                                                    i[4]
                                                    ))

    def capture_(self):
        global closing,t1
        i=2
        print(f'url={self.result}/comments,url1=self.result')
        text=f'1ページ目を読み込んでいる'
        self.lbstatus.config(text=text)
        commentget(url=f'{self.result}/comments',url1=self.result).run()
        if closing==False:
             t1.join()
             print('close thread')
        x=True
        while x:

            self.lbstatus.config(text=f'{i}ページ目を読み込み中',fg='blue')
            a=commentget(url=f'{self.result}/comments?page={i}',url1=self.result).run()
            if a==False:
                self.lbstatus.config(text='読み込み完了',fg='red')
                break
            if closing==False:
                a=False
                t1.join()
                print('close thread')
                break
            i+=1
        
        
        
        self.lb1.pack_forget()
   

    
        
        
    def select_file(self):

        global t1 
        self.result=self.LineEdit.get()
        
        if self.result:
            if self.result.split('://')[0]=='http' or self.result.split('://')[0]=='https':
                self.frame.load_url(self.result)
            elif self.result=='':
                pass
            else:
                self.result='https://'+self.result
                self.frame.load_url(self.result)
                
        else:    
            pass
       
    def seldata(self,tb):
        c=self.conn.cursor()
        c.execute(f"SELECT * from '{tb}' where vecmatch>0")
        rows=c.fetchall()

        return rows
    
    def on_tab_change(self,event):
            global closing
            tab = event.widget.tab('current')['text']
            if tab == 'コメント欄':
                
                self.frame.pack_forget()
                if self.tmp=='':
                    print('empty')
                    self.thread_start_check(self.capture_)
                    j=self.seldata('info')
    
    
                    for i in j:
                        self.treeview.insert('','end', values=(
                                                            i[1],
                                                            i[3],
                                                            
                                                            ))
                    self.tmp=self.LineEdit.get()
                     
                elif self.tmp==self.LineEdit.get(): 
                    
                    self.lb1.pack_forget()
                    print('same')
                else:
                    
                    self.tmp=self.LineEdit.get()
                    self.delrec()
                    self.capture_()
                    
                    j=self.seldata('info')
        
        
                    for i in j:
                            self.treeview.insert('','end', values=(
                                                                i[1],
                                                                i[3],
                                                                
                                                                ))
                    print('diffrent')
                

            elif tab == 'ニュース':
                
                """A"""
                
                self.lb1.pack()

                self.frame.pack(fill="both", expand=True)
                self.frame.load_url(self.result) 