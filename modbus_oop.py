import tkinter as tk
from tkinter import ttk
from tkinter import *
import tkinter
import datetime as dt
import pandas as pd
import pymongo
import cnfOperations as cnf
import recordMongo as rm
import sys
import plotly.express as px
import numpy as np


class ModbusOop(object):
    def __init__(self):
        self.count = int(cnf.cnfOperation.readModBusCount())
        self.root = tk.Tk()
        self.style = ttk.Style()
        self.style.map("Treeview", foreground=self.fixed_map("foreground"), background=self.fixed_map("background"))
        self.tree = ttk.Treeview(self.root)
        self.canvas = tk.Canvas(self.root, width=1580, height=600)

    def fixed_map(self, option):
        return [elm for elm in self.style.map("Treeview", query_opt=option) if elm[:2] != ("!disabled", "!selected")]

    def on_double_click(self, event):
        item = self.tree.identify('item', event.x, event.y)

        print(self.tree.item(item, "text"))

        myclient = pymongo.MongoClient(cnf.cnfOperation.readMongoDb())
        mydb = myclient[cnf.cnfOperation.readMy_Db()]
        mycol = mydb[cnf.cnfOperation.readMy_Col()]

        xs_doc = list(
            mycol.find(
                {"$and": [{"Sensor No": self.tree.item(item, "text")},
                          {"Time": {"$gte": "2021-05-31 13:14:58",
                                    "$lt": dt.datetime.now().strftime('%Y-%m-%d %X')}}]},
                {'_id': 0}))

        xs_res = [list(idx.values()) for idx in xs_doc]

        df = pd.DataFrame(list(xs_doc))
        df['Temp'] = df['Temp'].astype(np.float64)

        for index1, row in enumerate(xs_res):
            for index2, item in enumerate(row):
                try:
                    xs_res[index1][index2] = (float(item))
                except ValueError:
                    pass
        df = pd.DataFrame(xs_doc)
        df['Temp'] = df['Temp'].astype(np.float64)
        fig = px.line(df, x='Time', y='Temp', title='Temperature °C - Time', color='Sensor No')

        fig.update_xaxes(
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1m", step="month", stepmode="backward"),
                    dict(count=3, label="3m", step="month", stepmode="backward"),
                    dict(count=6, label="6m", step="month", stepmode="todate"),
                    dict(count=1, label="1y", step="year", stepmode="backward"),
                    dict(step="all")
                ])
            )
        )

        return fig.show()

    def _quit(event):
        sys.exit()

    def window_table(self):

        self.root.title("Sensor's Temperatures °C")
        self.root.geometry("480x630")
        self.root.grid()

        p1 = PhotoImage(file='images1.png')
        self.root.iconphoto(False, p1)

        self.tree.pack(side='top', fill=tkinter.BOTH, expand=True)

        verscrlbar = ttk.Scrollbar(self.root,
                                   orient="vertical",
                                   command=self.tree.yview)

        self.tree.configure(xscrollcommand=verscrlbar.set)

        self.tree["columns"] = ("1", "2", "3")

        self.tree['show'] = 'headings'

        self.tree.column("1", width=125, minwidth=30, anchor='c')
        self.tree.column("2", width=65, minwidth=30, anchor='c')
        self.tree.column("3", width=115, minwidth=30, anchor='c')

        self.tree.heading("1", text="Time")
        self.tree.heading("2", text="Sensor No")
        self.tree.heading("3", text="Temperature °C")

        self.tree.bind("<Double-1>", self.on_double_click)

        self.canvas.create_rectangle(10, 150, 1580, 170, fill='grey', outline='white', tag='rect1')
        self.canvas.create_rectangle(10, 500, 1580, 520, fill='grey', outline='white', tag='rect2')
        self.canvas.create_rectangle(365, 170, 385, 500, fill='grey', outline='white', tag='rect3')

        start3 = 45
        n = 1
        for z in range(26):
            self.canvas.create_text(start3, 140, text=n)
            self.canvas.create_text(start3, 530, text=n + 34)
            start3 += 60
            n += 1

        start4 = 195
        f = 27
        for t in range(8):
            self.canvas.create_text(395, start4, text=f)
            start4 += 40
            f += 1

        rem = rm.RecordMongo

        start_range = 0
        id_count = 1
        start = 40

        self.tree.tag_configure('high', foreground='red')
        self.tree.tag_configure('low', foreground='black')

        for record in rem.record_mongo()[-(self.count // 2):]:
            if float(record[1]) > 30.0:
                self.tree.insert("", index='end', text="%s" % int(record[0]), iid=start_range,
                                 values=(str(record[2]), int(record[0]), float(record[1])), tags=('high',))
                if record[0] <= 26.0:
                    # ust cizgi
                    x_to_add = 60
                    y_lower, y_upper = 150, 170
                    if float(record[1]) > 30.0:
                        self.canvas.create_rectangle(start, y_lower, start + 10, y_upper, fill='red', outline='white',
                                                     stipple='gray50', tag='rect4')
                    else:
                        self.canvas.create_rectangle(start, y_lower, start + 10, y_upper, fill='blue', outline='white',
                                                     stipple='gray50', tag='rect4')
                    start += x_to_add

                    if record[0] == 26:
                        start = 190

                elif 26.0 < record[0] < 35.0:
                    y_to_add = 40
                    x_lower, x_upper = 365, 385
                    if float(record[1]) > 25.0:
                        self.canvas.create_rectangle(x_lower, start, x_upper, start + 10, fill='red', outline='white',
                                                     stipple='gray50', tag='rect5')
                    else:
                        self.canvas.create_rectangle(x_lower, start, x_upper, start + 10, fill='blue', outline='white',
                                                     stipple='gray50', tag='rect5')
                    start += y_to_add
                    if record[0] == 34:
                        start = 40

                else:
                    # alt cizgi
                    x_to_add = 60
                    y_lower, y_upper = 500, 520
                    if float(record[1]) > 25:
                        self.canvas.create_rectangle(start, y_lower, start + 10, y_upper, fill='red', outline='white',
                                                     stipple='gray50', tag='rect6')
                    else:
                        self.canvas.create_rectangle(start, y_lower, start + 10, y_upper, fill='blue', outline='white',
                                                     stipple='gray50', tag='rect6')
                    start += x_to_add

            else:
                if record[0] <= 26.0:
                    # ust cizgi
                    x_to_add = 60
                    y_lower, y_upper = 150, 170
                    if float(record[1]) > 30.0:
                        self.canvas.create_rectangle(start, y_lower, start + 10, y_upper, fill='red', outline='white',
                                                     stipple='gray50', tag='rect4')
                    else:
                        self.canvas.create_rectangle(start, y_lower, start + 10, y_upper, fill='blue', outline='white',
                                                     stipple='gray50', tag='rect4')
                    start += x_to_add

                    if record[0] == 26:
                        start = 190

                elif 26.0 < record[0] < 35.0:
                    y_to_add = 40
                    x_lower, x_upper = 365, 385
                    if float(record[1]) > 25.0:
                        self.canvas.create_rectangle(x_lower, start, x_upper, start + 10, fill='red', outline='white',
                                                     stipple='gray50', tag='rect5')
                    else:
                        self.canvas.create_rectangle(x_lower, start, x_upper, start + 10, fill='blue', outline='white',
                                                     stipple='gray50', tag='rect5')
                    start += y_to_add
                    if record[0] == 34:
                        start = 40

                else:
                    # alt cizgi
                    x_to_add = 60
                    y_lower, y_upper = 500, 520
                    if float(record[1]) > 25:
                        self.canvas.create_rectangle(start, y_lower, start + 10, y_upper, fill='red', outline='white',
                                                     stipple='gray50', tag='rect6')
                    else:
                        self.canvas.create_rectangle(start, y_lower, start + 10, y_upper, fill='blue', outline='white',
                                                     stipple='gray50', tag='rect6')
                    start += x_to_add

            start_range += 1
            id_count += 1

        menu = Menu(self.root)
        self.root.config(menu=menu)
        menu.add_cascade(label='Quit', command=self._quit)

        self.tree.after(60000, self.update_window_table)
        self.canvas.pack()
        return self.root.mainloop()

    def update_window_table(self):
        rem = rm.RecordMongo

        start_range = 0
        id_count = 1
        start1 = 40

        for i in self.tree.get_children():
            self.tree.delete(i)

        for record in rem.record_mongo()[-(self.count // 2):]:
            if float(record[1]) > 30.0:
                self.tree.insert("", index='end', text="%s" % int(record[0]), iid=start_range,
                                 values=(str(record[2]), int(record[0]), float(record[1])), tags=('high',))
                self.canvas.create_rectangle(start1, 150, start1 + 10, 170, fill='red', outline='white',
                                             stipple='gray50', tag='rect4')

                start2 = 40
                for v in range(35, 61):
                    self.canvas.create_rectangle(start2, 500, start2 + 10, 520, fill='red', outline='white',
                                                 stipple='gray50', tag='rect5')
                    start2 += 60

                start3 = 190
                for y in range(27, 34):
                    self.canvas.create_rectangle(365, start3, 385, start3 + 10, fill='red', outline='white',
                                                 stipple='gray50')
                    start3 += 40

            else:
                self.tree.insert("", index='end', text="%s" % int(record[0]), iid=start_range,
                                 values=(str(record[2]), int(record[0]), float(record[1])), tags=('low',))
                self.canvas.create_rectangle(start1, 150, start1 + 10, 170, fill='blue', outline='white',
                                             stipple='gray50', tag='rect4')

                start2 = 40
                for v in range(35, 61):
                    self.canvas.create_rectangle(start2, 500, start2 + 10, 520, fill='blue', outline='white',
                                                 stipple='gray50')
                    start2 += 60

                start3 = 190
                for y in range(27, 34):
                    self.canvas.create_rectangle(365, start3, 385, start3 + 10, fill='blue', outline='white',
                                                 stipple='gray50')
                    start3 += 40

            start_range += 1
            start1 += 60
            id_count += 1

        self.root.update()
        self.root.update_idletasks()
        self.tree.after(60000, self.update_window_table)
        self.canvas.pack()
        return self.root.mainloop()
