import tkinter

tk = tkinter.Tk()
can = tkinter.Canvas(tk)
can.pack()
img = tkinter.PhotoImage(file="Assets/Building_B.gif")
img = img.subsample(img.width() // 50, img.height() // 60)
can.create_image((50, 50), image=img, tags = "token")

drag_data = {"x": 0, "y": 0, "item": None}

def OnTokenButtonPress(event):
    '''Being drag of an object'''
    # record the item and its location
    drag_data["item"] = can.find_closest(event.x, event.y)[0]
    drag_data["x"] = event.x
    drag_data["y"] = event.y

def OnTokenButtonRelease(event):
    '''End drag of an object'''
    # reset the drag information
    drag_data["item"] = None
    drag_data["x"] = 0
    drag_data["y"] = 0

def OnTokenMotion(event):
    '''Handle dragging of an object'''
    # compute how much this object has moved
    delta_x = event.x - drag_data["x"]
    delta_y = event.y - drag_data["y"]
    # move the object the appropriate amount
    can.move(drag_data["item"], delta_x, delta_y)
    # record the new position
    drag_data["x"] = event.x
    drag_data["y"] = event.y

    
    

tk.mainloop()
print("STUFF")