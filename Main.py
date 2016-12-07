"""This is the main file that allows a user to interact with the project
via a graphical user interface"""
import tkinter as tk
from tkinter import PhotoImage
from tkinter import font

def main():
    window = tk.Tk()
    window.title("Medina")
    img = PhotoImage(file='Assets/icon.gif')
    window.tk.call('wm', 'iconphoto', window._w, img)

    title_font = font.Font(family='Helvetica', size=36, weight='bold')
    normal_font = font.Font(family='Helvetica', size=16, weight='bold')

    title = tk.Label(window, text="Medina", font = title_font)
    title.grid(row=0, columnspan=5, sticky='NSEW')

    def make_player_selector(r, player_num):
        start = tk.Label(window, text="Player " + str(player_num) + ")")
        start.grid(row = r, sticky='W')

    for i in range(4):
        make_player_selector(i + 1, i + 1)

    window.mainloop()

if __name__ == "__main__":
    main()
