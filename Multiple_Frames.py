import tkinter as tk

class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        self.main = tk.Frame.__init__(self, parent)
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

        # Label
        page1_title_label = tk.Label(self,text='Signature Verification',font=("Arial",30))
        # page1_title_label.grid(row=1,column=0,padx=5,pady=10)
        page1_title_label.place(x=300,y=400)
        page1_url_label = tk.Label(self,text='base url',font=("Arial",30))
        page1_url_label.place(x=50,y=100)
        # page1_path_label = tk.Label(self,text='base url',font=("Arial",10))
        # page1_path_label.grid(row=2,column=0,padx=5,pady=10)
        # page1_description_label = tk.Label(self,text='Customized the querystring:',font=("Arial",20))
        # page1_description_label.grid(row=3,column=0,padx=5,pady=10)
        

        # # Entry
        # page1_url_entry = tk.Entry(self,font=("Arial",10))
        # page1_url_entry.grid(row=1,column=1)
        # page1_path_entry = tk.Entry(self,font=("Arial",10)) 
        # page1_path_entry.grid(row=2,column=1)
        # page1_content_entry = tk.Text(self,height=6,width=150,font=("Arial",10))
        # page1_content_entry.grid(row=6,column=0,padx=5,pady=10)


        # Text 
        
        # page1_querystring_display_label = tk.Label(self,text=tk.StringVar(page1_content_text.get(0,tk.END)),font=("Arial",20))
        # page1_querystring_display_label.grid(row=4,column=0,padx=5,pady=10)


        #  Button
        # page1_return_button = tk.Button(self, text="返回主界面", command=lambda: controller.show_page(MainPage))
        # page1_return_button.grid(row=0,column=4,padx=5,pady=10)


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
        self.title("Binance API test tool")
        self.geometry("800x600+100+100")
        self.iconbitmap("resources/binance.ico")

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
