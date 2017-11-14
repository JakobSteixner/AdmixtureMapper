#!/usr/bin/python
# -*- coding: utf-8 -*-

from Tkinter import *
import subprocess as sb


class MapZapper(Frame):
    def __init__(self, master=None, curpagenumber=0):
        Frame.__init__(self, master)
        self.grid()
        self.curpagenumber = curpagenumber
        self.createWidgets()
        self.image = PhotoImage(name="euromap", file = "allregions123_Europe_%d.gif" % curpagenumber)
        #self.image.grid(column=0, columnspan=4,row=0, rowspan=4)
    def createWidgets(self):
        self.forwardButton = Button(self, text="Skip 5 generations forward", command=self.oneforward)
        self.forwardButton.grid(column=4, row=0)
        if self.curpagenumber > 0:
            self.backwardButton = Button(self, text="Skip 5 generations backward", command=self.onebackward)
            self.backwardButton.grid(column=4, row=1)
    def gotopage(self, master=None, newpagenumber=0):
        MapZapper(master=None, curpagenumber=newpagenumber)
        self.destroy()
    def oneforward(self):
        self.gotopage(None, self.curpagenumber+5)
    def onebackward(self):
        self.gotopage(None, self.curpagenumber-5)
    
main = MapZapper()
main.mainloop()