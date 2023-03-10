import json
import sys
import threading
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.constants import *
import os.path
from DatabaseManager import DatabaseManager
from Stockdata import Stockdata

_script = sys.argv[0]
_location = os.path.dirname(_script)

_bgcolor = '#d9d9d9'
_fgcolor = '#000000'
_compcolor = 'gray40'
_ana1color = '#c3c3c3'
_ana2color = 'beige'
_tabfg1 = 'black'
_tabfg2 = 'black'
_tabbg1 = 'grey75'
_tabbg2 = 'grey89'
_bgmode = 'light'

_style_code_ran = 0


def _style_code():
    global _style_code_ran
    if _style_code_ran:
        return
    style = ttk.Style()
    if sys.platform == "win32":
        style.theme_use('winnative')
    style.configure('.', background=_bgcolor)
    style.configure('.', foreground=_fgcolor)
    style.configure('.', font='TkDefaultFont')
    style.map('.', background=
    [('selected', _compcolor), ('active', _ana2color)])
    if _bgmode == 'dark':
        style.map('.', foreground=
        [('selected', 'white'), ('active', 'white')])
    else:
        style.map('.', foreground=
        [('selected', 'black'), ('active', 'black')])
    style.map('TNotebook.Tab', background=
    [('selected', _bgcolor), ('active', _tabbg1),
     ('!active', _ana2color)], foreground=
              [('selected', _fgcolor), ('active', _tabfg1), ('!active', _tabfg2)])
    _style_code_ran = 1


class GUI:
    def __init__(self, top=None):
        self.databases = {}
        self.get_db()
        db = self.databases['Postgresql']
        self.db_manager = DatabaseManager(db['name'], db['user'], db['password'], db['host'], 5432)

        """This class configures and populates the toplevel window.
           top is the toplevel containing window."""

        top.geometry("974x650+292+148")
        top.minsize(120, 1)
        top.maxsize(1668, 1090)
        top.resizable(1, 1)
        top.title("Toplevel 0")
        top.configure(background="#d9d9d9")
        self.top = top
        self.host = tk.StringVar()
        self.usr = tk.StringVar()
        self.pwd = tk.StringVar()
        self.dbname = tk.StringVar()
        self.combobox = tk.StringVar()
        self.db_name = tk.StringVar()
        _style_code()
        self.main_notebook = ttk.Notebook(self.top)
        self.main_notebook.place(relx=0.0, rely=0.0, relheight=1.003
                                 , relwidth=0.998)
        self.main_notebook.configure(takefocus="")
        self.stocks_tab = tk.Frame(self.main_notebook)
        self.main_notebook.add(self.stocks_tab, padding=3)
        self.main_notebook.tab(0, text='''Stocks''', compound="left"
                               , underline='''-1''', )
        self.stocks_tab.configure(background="#d9d9d9")
        self.stocks_tab.configure(highlightbackground="#d9d9d9")
        self.stocks_tab.configure(highlightcolor="black")
        self.ai_tab = tk.Frame(self.main_notebook)
        self.main_notebook.add(self.ai_tab, padding=3)
        self.main_notebook.tab(1, text='''AI''', compound="left"
                               , underline='''-1''', )
        self.ai_tab.configure(background="#d9d9d9")
        self.ai_tab.configure(highlightbackground="#d9d9d9")
        self.ai_tab.configure(highlightcolor="black")
        self.predict_tab = tk.Frame(self.main_notebook)
        self.main_notebook.add(self.predict_tab, padding=3)
        self.main_notebook.tab(2, text='''Prediction''', compound="left"
                               , underline='''-1''', )
        self.predict_tab.configure(background="#d9d9d9")
        self.predict_tab.configure(highlightbackground="#d9d9d9")
        self.predict_tab.configure(highlightcolor="black")
        self.Labelframe1_1_1 = tk.LabelFrame(self.stocks_tab)
        self.Labelframe1_1_1.place(relx=0.764, rely=0.016, relheight=0.409
                                   , relwidth=0.221)
        self.Labelframe1_1_1.configure(relief='groove')
        self.Labelframe1_1_1.configure(foreground="#000000")
        self.Labelframe1_1_1.configure(text='''Database Configuration''')
        self.Labelframe1_1_1.configure(background="#d9d9d9")
        self.Labelframe1_1_1.configure(highlightbackground="#d9d9d9")
        self.Labelframe1_1_1.configure(highlightcolor="black")
        self.Label4_1_1_1 = tk.Label(self.Labelframe1_1_1)
        self.Label4_1_1_1.place(relx=0.093, rely=0.352, height=23, width=64
                                , bordermode='ignore')
        self.Label4_1_1_1.configure(activebackground="#f9f9f9")
        self.Label4_1_1_1.configure(anchor='w')
        self.Label4_1_1_1.configure(background="#d9d9d9")
        self.Label4_1_1_1.configure(compound='left')
        self.Label4_1_1_1.configure(cursor="fleur")
        self.Label4_1_1_1.configure(disabledforeground="#a3a3a3")
        self.Label4_1_1_1.configure(foreground="#000000")
        self.Label4_1_1_1.configure(highlightbackground="#d9d9d9")
        self.Label4_1_1_1.configure(highlightcolor="black")
        self.Label4_1_1_1.configure(text='''Host''')
        self.host_entry = tk.Entry(self.Labelframe1_1_1)
        self.host_entry.place(relx=0.514, rely=0.352, height=20, relwidth=0.393
                              , bordermode='ignore')
        self.host_entry.configure(background="white")
        self.host_entry.configure(disabledforeground="#a3a3a3")
        self.host_entry.configure(font="TkFixedFont")
        self.host_entry.configure(foreground="#000000")
        self.host_entry.configure(highlightbackground="#d9d9d9")
        self.host_entry.configure(highlightcolor="black")
        self.host_entry.configure(insertbackground="black")
        self.host_entry.configure(selectbackground="#c4c4c4")
        self.host_entry.configure(selectforeground="black")
        self.host_entry.configure(textvariable=self.host)
        self.usr_entry = tk.Entry(self.Labelframe1_1_1)
        self.usr_entry.place(relx=0.514, rely=0.469, height=20, relwidth=0.393
                             , bordermode='ignore')
        self.usr_entry.configure(background="white")
        self.usr_entry.configure(disabledforeground="#a3a3a3")
        self.usr_entry.configure(font="TkFixedFont")
        self.usr_entry.configure(foreground="#000000")
        self.usr_entry.configure(highlightbackground="#d9d9d9")
        self.usr_entry.configure(highlightcolor="black")
        self.usr_entry.configure(insertbackground="black")
        self.usr_entry.configure(selectbackground="#c4c4c4")
        self.usr_entry.configure(selectforeground="black")
        self.usr_entry.configure(textvariable=self.usr)
        self.pwd_entry = tk.Entry(self.Labelframe1_1_1)
        self.pwd_entry.place(relx=0.514, rely=0.586, height=20, relwidth=0.393
                             , bordermode='ignore')
        self.pwd_entry.configure(background="white")
        self.pwd_entry.configure(disabledforeground="#a3a3a3")
        self.pwd_entry.configure(font="TkFixedFont")
        self.pwd_entry.configure(foreground="#000000")
        self.pwd_entry.configure(highlightbackground="#d9d9d9")
        self.pwd_entry.configure(highlightcolor="black")
        self.pwd_entry.configure(insertbackground="black")
        self.pwd_entry.configure(selectbackground="#c4c4c4")
        self.pwd_entry.configure(selectforeground="black")
        self.pwd_entry.configure(textvariable=self.pwd)
        self.db_entry = tk.Entry(self.Labelframe1_1_1)
        self.db_entry.place(relx=0.514, rely=0.703, height=20, relwidth=0.393
                            , bordermode='ignore')
        self.db_entry.configure(background="white")
        self.db_entry.configure(disabledforeground="#a3a3a3")
        self.db_entry.configure(font="TkFixedFont")
        self.db_entry.configure(foreground="#000000")
        self.db_entry.configure(highlightbackground="#d9d9d9")
        self.db_entry.configure(highlightcolor="black")
        self.db_entry.configure(insertbackground="black")
        self.db_entry.configure(selectbackground="#c4c4c4")
        self.db_entry.configure(selectforeground="black")
        self.db_entry.configure(textvariable=self.dbname)
        self.Label4_2_1 = tk.Label(self.Labelframe1_1_1)
        self.Label4_2_1.place(relx=0.093, rely=0.469, height=23, width=52
                              , bordermode='ignore')
        self.Label4_2_1.configure(activebackground="#f9f9f9")
        self.Label4_2_1.configure(anchor='w')
        self.Label4_2_1.configure(background="#d9d9d9")
        self.Label4_2_1.configure(compound='left')
        self.Label4_2_1.configure(disabledforeground="#a3a3a3")
        self.Label4_2_1.configure(foreground="#000000")
        self.Label4_2_1.configure(highlightbackground="#d9d9d9")
        self.Label4_2_1.configure(highlightcolor="black")
        self.Label4_2_1.configure(text='''User''')
        self.Label5_1_1 = tk.Label(self.Labelframe1_1_1)
        self.Label5_1_1.place(relx=0.093, rely=0.586, height=23, width=74
                              , bordermode='ignore')
        self.Label5_1_1.configure(activebackground="#f9f9f9")
        self.Label5_1_1.configure(anchor='w')
        self.Label5_1_1.configure(background="#d9d9d9")
        self.Label5_1_1.configure(compound='left')
        self.Label5_1_1.configure(disabledforeground="#a3a3a3")
        self.Label5_1_1.configure(foreground="#000000")
        self.Label5_1_1.configure(highlightbackground="#d9d9d9")
        self.Label5_1_1.configure(highlightcolor="black")
        self.Label5_1_1.configure(text='''Password''')
        self.Label6_1_1 = tk.Label(self.Labelframe1_1_1)
        self.Label6_1_1.place(relx=0.093, rely=0.703, height=23, width=79
                              , bordermode='ignore')
        self.Label6_1_1.configure(activebackground="#f9f9f9")
        self.Label6_1_1.configure(anchor='w')
        self.Label6_1_1.configure(background="#d9d9d9")
        self.Label6_1_1.configure(compound='left')
        self.Label6_1_1.configure(disabledforeground="#a3a3a3")
        self.Label6_1_1.configure(foreground="#000000")
        self.Label6_1_1.configure(highlightbackground="#d9d9d9")
        self.Label6_1_1.configure(highlightcolor="black")
        self.Label6_1_1.configure(text='''Database''')
        self.test_button = tk.Button(self.Labelframe1_1_1)
        self.test_button.place(relx=0.327, rely=0.859, height=24, width=47
                               , bordermode='ignore')
        self.test_button.configure(activebackground="beige")
        self.test_button.configure(activeforeground="black")
        self.test_button.configure(background="#d9d9d9")
        self.test_button.configure(command=lambda: test_button(self))
        self.test_button.configure(compound='left')
        self.test_button.configure(cursor="fleur")
        self.test_button.configure(disabledforeground="#a3a3a3")
        self.test_button.configure(foreground="#000000")
        self.test_button.configure(highlightbackground="#d9d9d9")
        self.test_button.configure(highlightcolor="black")
        self.test_button.configure(pady="0")
        self.test_button.configure(text='''Test''')
        self.test_status = tk.Label(self.Labelframe1_1_1)
        self.test_status.place(relx=0.561, rely=0.859, height=23, width=78
                               , bordermode='ignore')
        self.test_status.configure(activebackground="#f9f9f9")
        self.test_status.configure(anchor='w')
        self.test_status.configure(background="#d9d9d9")
        self.test_status.configure(compound='left')
        self.test_status.configure(disabledforeground="#a3a3a3")
        self.test_status.configure(foreground="#000000")
        self.test_status.configure(highlightbackground="#d9d9d9")
        self.test_status.configure(highlightcolor="black")
        self.test_status.configure(text='''Untested''')
        self.Labelframe2 = tk.LabelFrame(self.stocks_tab)
        self.Labelframe2.place(relx=0.413, rely=0.016, relheight=0.407
                               , relwidth=0.352)
        self.Labelframe2.configure(relief='groove')
        self.Labelframe2.configure(foreground="#000000")
        self.Labelframe2.configure(text='''Saved Data''')
        self.Labelframe2.configure(background="#d9d9d9")
        self.download_entry = tk.Entry(self.Labelframe2)
        self.download_entry.place(relx=0.235, rely=0.118, height=20
                                  , relwidth=0.188, bordermode='ignore')
        self.download_entry.configure(background="white")
        self.download_entry.configure(disabledforeground="#a3a3a3")
        self.download_entry.configure(font="TkFixedFont")
        self.download_entry.configure(foreground="#000000")
        self.download_entry.configure(insertbackground="black")
        self.Label4 = tk.Label(self.Labelframe2)
        self.Label4.place(relx=0.059, rely=0.118, height=21, width=54
                          , bordermode='ignore')
        self.Label4.configure(anchor='w')
        self.Label4.configure(background="#d9d9d9")
        self.Label4.configure(compound='left')
        self.Label4.configure(disabledforeground="#a3a3a3")
        self.Label4.configure(foreground="#000000")
        self.Label4.configure(text='''Symbol''')
        self.data_download = tk.Button(self.Labelframe2)
        self.data_download.place(relx=0.469, rely=0.118, height=24, width=108
                                 , bordermode='ignore')
        self.data_download.configure(activebackground="beige")
        self.data_download.configure(activeforeground="black")
        self.data_download.configure(background="#d9d9d9")
        self.data_download.configure(command=self.stock_download)
        self.data_download.configure(compound='left')
        self.data_download.configure(disabledforeground="#a3a3a3")
        self.data_download.configure(foreground="#000000")
        self.data_download.configure(highlightbackground="#d9d9d9")
        self.data_download.configure(highlightcolor="black")
        self.data_download.configure(pady="0")
        self.data_download.configure(text='''Update/Download''')
        self.download_status = tk.Label(self.Labelframe2)
        self.download_status.place(relx=0.059, rely=0.235, height=21, width=104
                                   , bordermode='ignore')
        self.download_status.configure(anchor='w')
        self.download_status.configure(background="#d9d9d9")
        self.download_status.configure(compound='left')
        self.download_status.configure(disabledforeground="#a3a3a3")
        self.download_status.configure(foreground="#000000")
        self.download_status.configure(text='''Status: Awaiting Input''')
        self.db_combo = ttk.Combobox(self.stocks_tab)
        self.db_combo.place(relx=0.795, rely=0.064, relheight=0.035
                            , relwidth=0.148)
        self.value_list = ['databases', ]
        database_names = []
        for database in self.databases:
            database_names.append(self.databases[f"{database}"]['name'])
        self.db_combo.configure(values=database_names)
        self.db_combo.configure(textvariable=self.combobox)
        self.db_combo.configure(takefocus="")
        self.db_combo.bind("<<ComboboxSelected>>", lambda event: db_select(self.db_combo.get(), self))
        self.Button1 = tk.Button(self.stocks_tab)
        self.Button1.place(relx=0.785, rely=0.367, height=24, width=47)
        self.Button1.configure(activebackground="beige")
        self.Button1.configure(activeforeground="black")
        self.Button1.configure(background="#d9d9d9")
        self.Button1.configure(compound='left')
        self.Button1.configure(disabledforeground="#a3a3a3")
        self.Button1.configure(foreground="#000000")
        self.Button1.configure(highlightbackground="#d9d9d9")
        self.Button1.configure(highlightcolor="black")
        self.Button1.configure(pady="0")
        self.Button1.configure(text='''Save''')
        self.Button1.configure(command=lambda: save_db(self))
        self.dbname_entry = tk.Entry(self.stocks_tab)
        self.dbname_entry.place(relx=0.878, rely=0.112, height=20
                                , relwidth=0.087)
        self.dbname_entry.configure(background="white")
        self.dbname_entry.configure(disabledforeground="#a3a3a3")
        self.dbname_entry.configure(font="TkFixedFont")
        self.dbname_entry.configure(foreground="#000000")
        self.dbname_entry.configure(insertbackground="black")
        self.dbname_entry.configure(textvariable=self.db_name)
        self.Label4_1_1_1_1 = tk.Label(self.stocks_tab)
        self.Label4_1_1_1_1.place(relx=0.785, rely=0.112, height=23, width=64)
        self.Label4_1_1_1_1.configure(activebackground="#f9f9f9")
        self.Label4_1_1_1_1.configure(anchor='w')
        self.Label4_1_1_1_1.configure(background="#d9d9d9")
        self.Label4_1_1_1_1.configure(compound='left')
        self.Label4_1_1_1_1.configure(disabledforeground="#a3a3a3")
        self.Label4_1_1_1_1.configure(foreground="#000000")
        self.Label4_1_1_1_1.configure(highlightbackground="#d9d9d9")
        self.Label4_1_1_1_1.configure(highlightcolor="black")
        self.Label4_1_1_1_1.configure(text='''Name''')
        self.top.mainloop()

    def get_db(self):
        with open('databases.json', 'r') as f:
            self.databases = json.load(f)

    def stock_download(self, symbol="ohi"):
        if symbol == "":
            symbol = self.download_entry.get()
        db_manager = DatabaseManager(self.databases['Postgresql']['database'], self.databases['Postgresql']['user'], self.databases['Postgresql']['password'], self.databases['Postgresql']['host'], 5432)
        # Then, create a Stockdata instance with the DatabaseManager instance
        stock_data = Stockdata(db_manager)

        # Finally, download the data for the OHI symbol
        download_thread = threading.Thread(target=stock_data.download_data, args=(symbol,))
        download_thread.start()

        print(stock_data)


def test_button(db):
    db_manager_test = DatabaseManager(db.db_entry.get(), db.usr_entry.get(), db.pwd_entry.get(), db.host_entry.get(),
                                      5432)
    if db_manager_test.connect() is not None:
        db.test_status.config(text="Success!")
    else:
        db.test_status.config(text="Fail!")


def save_db(db):
    with open('databases.json', 'r') as f:
        data = json.load(f)
    new_obj = {'name': db.dbname_entry.get(), 'user': db.usr_entry.get(), 'password': db.pwd_entry.get(),
               'host': db.host_entry.get(), 'database': db.db_entry.get()}
    data[f"{db.dbname_entry.get()}"] = new_obj
    with open('databases.json', 'w') as f:
        json.dump(data, f)
    database_names = []
    for database in db.databases:
        database_names.append(db.databases[f"{database}"]['name'])
    db.db_combo.configure(values=database_names)


def db_select(selection, target):
    with open('databases.json', 'r') as f:
        data = json.load(f)
    target.dbname_entry.delete(0, tk.END)
    target.db_entry.delete(0, tk.END)
    target.usr_entry.delete(0, tk.END)
    target.pwd_entry.delete(0, tk.END)
    target.host_entry.delete(0, tk.END)

    target.dbname_entry.insert(0, data[f"{selection}"]['name'])
    target.db_entry.insert(0, data[f"{selection}"]['database'])
    target.usr_entry.insert(0, data[f"{selection}"]['user'])
    target.pwd_entry.insert(0, data[f"{selection}"]['password'])
    target.host_entry.insert(0, data[f"{selection}"]['host'])


if __name__ == "__main__":
    root = tk.Tk()
    GUI = GUI(root)
