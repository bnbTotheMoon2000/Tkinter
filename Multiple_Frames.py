import tkinter as tk

class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="主界面")
        label.pack(pady=10, padx=10)

        button1 = tk.Button(self, text="切换到界面1", command=lambda: controller.show_page(Page1))
        button1.pack()

        button2 = tk.Button(self, text="切换到界面2", command=lambda: controller.show_page(Page2))
        button2.pack()

class Page1(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="界面1")
        label.pack(pady=10, padx=10)

        button = tk.Button(self, text="返回主界面", command=lambda: controller.show_page(MainPage))
        button.pack()

class Page2(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="界面2")
        label.pack(pady=10, padx=10)

        button = tk.Button(self, text="返回主界面", command=lambda: controller.show_page(MainPage))
        button.pack()

class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        self.pages = {}

        for Page in (MainPage, Page1, Page2):
            page_name = Page.__name__
            page = Page(container, self)
            self.pages[page_name] = page
            page.grid(row=0, column=0, sticky="nsew")

        self.show_page(MainPage)

    def show_page(self, page_class):
        page_name = page_class.__name__
        page = self.pages[page_name]
        page.tkraise()

app = App()
app.mainloop()
