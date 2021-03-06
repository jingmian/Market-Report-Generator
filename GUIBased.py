import tkinter as tk
from WindPy import *
import datetime
from Services import Index_Overview, XueQiuCrawler_Find3Pages, Derivatives_Overview, Appendix


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.create_widgets()

    def DateSetter(self):
        return datetime.datetime.today().strftime('%Y%m%d')

    def create_widgets(self):
        self.label_date = tk.Label(window, text='日期：').grid(row=0, column=0, sticky="W")

        self.string_date = tk.StringVar()
        self.string_date.set(self.DateSetter())
        self.entry_date = tk.Entry(window, textvariable=self.string_date, width=10).grid(row=0, column=1)

        self.label_date_note = tk.Label(window, text='默认为当天，注意修改', fg="red").grid(row=0, column=2, columnspan=2, sticky="W")

        self.StockIndexButton = tk.Button(text="股票市场", command=self.stock_index, width=10)
        self.StockIndexButton.grid(row=1, column=0)

        self.VolumeButton = tk.Button(text="成交量", command=self.volume, width=10)
        self.VolumeButton.grid(row=1, column=1)

        self.StrategyButton = tk.Button(text="宏观策略", command=self.strategy, width=10)
        self.StrategyButton.grid(row=1, column=2)

        self.DerivativeButton = tk.Button(text="期货市场", width=10, command=self.deravatives)
        self.DerivativeButton.grid(row=1, column=3)

        self.text_window = tk.Text(window, width=45, height=35)
        self.text_window.grid(row=2, column=0, columnspan=4)
        self.text_window.insert(tk.END, "【注意事项】\n\n")
        self.text_window.insert(tk.END, "1.股票市场及成交量数据在收盘后可立即获得；\n")
        self.text_window.insert(tk.END, "2.宏观策略数据一般在15:30之后发布，19:00后必定可得；\n")
        self.text_window.insert(tk.END, "3.点击按钮后稍微卡顿是因为正在从数据库中获取数据，属于正常现象。")

    def check_date(self):
        DATE = self.string_date.get()
        weekday = datetime.datetime(int(DATE[0:4]), int(DATE[4:6]), int(DATE[6:8])).weekday()
        if weekday == 5 or weekday == 6:
            self.text_window.insert("end", '日期不在周一至周五的范围内，请重新输入。')
            return False
        else:
            return True

    def stock_index(self):
        self.text_window.delete('1.0', 'end')

        if self.check_date() is True:
            DATE = self.string_date.get()

            # Chinese Market
            Stock_ID_CN = '000001.SH,399001.SZ,399006.SZ'
            Stock_ID_List_CN = Stock_ID_CN.split(',')
            self.text_window.insert("end", Index_Overview.overview_china(Stock_ID_List_CN, DATE) + '\n')
            # US Market
            Stock_Name_US = '美国三大股指'
            Stock_ID_US = "DJI.GI,SPX.GI,IXIC.GI"
            Stock_ID_List_US = Stock_ID_US.split(',')
            self.text_window.insert("end", Index_Overview.overview_others(Stock_Name_US, Stock_ID_List_US, DATE) + '\n')
            # European Market
            Stock_Name_EU = '欧洲三大股指'
            Stock_ID_EU = "FTSE.GI,FCHI.GI,GDAXI.GI"
            Stock_ID_List_EU = Stock_ID_EU.split(',')
            self.text_window.insert("end", Index_Overview.overview_others(Stock_Name_EU, Stock_ID_List_EU, DATE) + '\n')
            # Asian Market
            Stock_Name_Asia = '亚太股市'
            Stock_ID_Asia = "N225.GI,KS11.GI,AS51.GI"
            Stock_ID_List_Asia = Stock_ID_Asia.split(',')
            self.text_window.insert("end", Index_Overview.overview_others(Stock_Name_Asia, Stock_ID_List_Asia, DATE) + '\n')
            self.text_window.see(tk.END)

    def volume(self):
        self.text_window.delete('1.0', 'end')

        if self.check_date() is True:
            DATE = self.string_date.get()

            Stock_ID_CN = '000001.SH,399001.SZ,399006.SZ'
            Stock_ID_List_CN = Stock_ID_CN.split(',')
            self.text_window.insert("end", Index_Overview.volume(Stock_ID_List_CN, DATE))
            self.text_window.see(tk.END)

    def strategy(self):
        self.text_window.delete('1.0', 'end')

        if self.check_date() is True:
            DATE = self.string_date.get()

            self.text_window.insert("end", XueQiuCrawler_Find3Pages.get_comment(date=DATE))
            self.text_window.see(tk.END)

    def deravatives(self):
        self.text_window.delete('1.0', 'end')

        if self.check_date() is True:
            DATE = self.string_date.get()

            ID_Dictionary = Appendix.derivatives_getter()
            self.text_window.insert("end", "上证50股指期货\n")
            self.text_window.insert("end", Derivatives_Overview.market_overview(ID_Dictionary['IH_Series'], DATE, '上证50股指期货') + '\n')
            self.text_window.insert("end", "中证500股指期货\n")
            self.text_window.insert("end", Derivatives_Overview.market_overview(ID_Dictionary['IC_Series'], DATE, '中证500股指期货') + '\n')
            self.text_window.insert("end", "沪深300股指期货\n")
            self.text_window.insert("end", Derivatives_Overview.market_overview(ID_Dictionary['IF_Series'], DATE, '沪深300股指期货') + '\n')


if __name__ == "__main__":
    w.start()

    window = tk.Tk()
    window.title('日报数据简易生成插件')
    window.geometry('330x530')
    window.iconbitmap('./static/icon.ico')

    app = Application(master=window)
    app.mainloop()
