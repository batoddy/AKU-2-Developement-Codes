from tkinter import *

class RootGUI:
    def __init__(self):
        self.root = Tk()
        self.root.title("Serial Commununication")
        self.root.geometry("360x120")
        self.root.config(bg="white")

class ComGUI:
    def __init__(self,root):
        self.root = root
        self.frame = LabelFrame(
            root,text="Com Manager", padx=5, pady=5, bg="white")
        self.label_com = Label(
            self.frame, text="Available Ports: ", bg="white", width=15, anchor="w")
        self.label_bdw = Label(
            self.frame, text="Bandwidth: ", bg="white", width=15, anchor="w")
        self.ComOptionMenu()
        self.BdwOptionMenu()

        self.btn_refresh = Button(self.frame, text= "Refresh", width=10)
        self.btn_connect = Button(self.frame, text= "Connect", width=10, state="disabled")

        self.padx = 20
        self.pady = 5

        
        self.publish()

    def ComOptionMenu(self):
        coms = ["-","COM5","COM7","COM13"]
        self.clicked_com = StringVar()
        self.clicked_com.set(coms[0])
        self.drop_com = OptionMenu(
            self.frame, self.clicked_com, *coms)
        self.drop_com.config(width=10)

    def BdwOptionMenu(self):
        bdws = ["-","9600","115200"]
        self.clicked_bdw = StringVar()
        self.clicked_bdw.set(bdws[0])
        self.drop_bdw = OptionMenu(
            self.frame, self.clicked_bdw, *bdws)
        self.drop_bdw.config(width=10)

    def publish(self):
        self.frame.grid(row=0, column=0, rowspan=3, 
                        columnspan=3, padx=5, pady=5)
        self.label_com.grid(column=1, row=2)
        self.drop_com.grid(column=2, row=2, padx=self.padx, pady=self.pady)
        self.btn_refresh.grid(column=3, row=2)

        self.label_bdw.grid(column=1, row=3)
        self.drop_bdw.grid(column=2, row=3)
        self.btn_connect.grid(column=3, row=3)


if __name__ == "__main__":
    RootGUI()
    ComGUI()