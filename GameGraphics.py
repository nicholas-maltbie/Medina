"""The Game Graphics stores the ability to draw different elements of the 
game on the screen using the TKinter package"""

from tkinter import *

class Board(Frame):
    """A board is a 2D layout of buttons representing all the different 
    aspects of a Board in Medina."""
    
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()

