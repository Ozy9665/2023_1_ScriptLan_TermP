import sys
import tkinter
import tkinter.messagebox
from tkintermapview import TkinterMapView

class App(tkinter.Tk):

    APP_NAME = "gy"
    WIDTH = 800
    HEIGHT = 750

    def __init__(self, *args, **kwargs):
        tkinter.Tk.__init__(self, *args, **kwargs)

        self.title(self.APP_NAME)
        self.geometry(f"{self.WIDTH}x{self.HEIGHT}")

        self.protocol("WM_DELETE_WINDOW", self.on_closing)  # 종료될 때 호출
        self.bind("<Return>", self.search)