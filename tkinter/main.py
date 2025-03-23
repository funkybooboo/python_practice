import tkinter as tk

class Main:
    count = 0
    def __init__(self):
        window = tk.Tk()
        window.geometry("500x500")
        self.label = tk.Label(text="0")
        self.label.pack()
        tk.Button(text="Increment", command=self.increment).pack()
        tk.Button(text="Decrement", command=self.decrement).pack()
        
        window.mainloop()

    def increment(self):
        self.count += 1
        self.label.config(text=f"{self.count}")

    def decrement(self):
        self.count -= 1
        self.label.config(text=f"{self.count}")

if __name__ == '__main__':
    Main()