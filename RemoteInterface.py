"""This class simulates the program Graphical User Interface, or GUI, for the Microwave.
   It creates the visual layout, input, and ring buttons for the program.

   Author: Jalen Gillespie
   Date: 2/22/2026 
=================================
   [Color References]:

   Dark Gray = 2C2C2C
   Light Gray = D3D3D3
   White = FFFFFF
   Red = B22222

=================================

   *Note to self, remove this comment from header after finishing*:
    -Fix the scaling when making program fullscreen
    -Update to layout to make it look more like a microwave
    -Change the buttons to look more like microwave buttons (maybe with an image?)
    -Change the program title once we all decide on the program name.
    -Connect this program with SystemLogic class (or whatever we name it)
     whenever the class gets finished.
    
    -Maybe turn the hexacdecimal colors into variables, might be easier to read?
    -Finish adding comments to some of the lines, or change if it feels too vague.
    -After partner updates the recipedata, make sure that the program won't have to open
     up by pressing input in the terminal
    -Add a manual time mode

"""
from tkinter import *
from recipedata import RecipeData
class RemoteInterface:
    def __init__(self, root):
        self.root = root
        #We need to figure out a name for out program, and i'll change it here
        self.root.title("Microwave Program")
        self.root.configure(bg="#2C2C2C")
        self.data = RecipeData()

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)

        self.display = Label (root, text="Select Mode", bg="black", fg="lime",
                             font=("Courier", 22, "bold"), width=18, height=2,
                             pady=10, highlightthickness=2, highlightbackground="#D3D3D3")
        self.display.pack(pady=20, padx=20)

        self.menu_frame = Frame(root, bg="#2C2C2C")

        self.menu_frame.pack(pady=10, fill=BOTH, expand=True)

        self.load_main_menu()

    def clear_buttons(self):
        for widget in self.menu_frame.winfo_children():
            widget.destroy()
    
    def create_ring_button(self, parent, text, command, row, col):
        # creates multiple circular "ring" buttons like on some real microwaves

        canvas = Canvas(parent, width=150, height=60, bg="#2C2C2C",
                        highlightthickness=0, cursor="hand2")
        canvas.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

        ring = canvas.create_oval(10, 10, 140, 50, outline="#D3D3D3", width=4)

        label = canvas.create_text(75, 30, text=text, fill="#D3D3D3",
                                   font=("Arial", 10, "bold"), width=120, justify=CENTER)
        
        canvas.tag_bind(ring, "<Button-1>", lambda e: command())
        canvas.tag_bind(label, "<Button-1>", lambda e: command())

        canvas.tag_bind(ring, "<Enter>", lambda e: canvas.itemconfig(ring, outline="#FFFFFF"))
        canvas.tag_bind(ring, "<Leave>", lambda e: canvas.itemconfig(ring, outline="#D3D3D3"))

    def load_main_menu(self):
        self.clear_buttons()
        self.display.config(text="CHOOSE CATEGORY")

        self.menu_frame.columnconfigure(0, weight=1)
        self.menu_frame.columnconfigure(1, weight=1)

        categories = self.data.get_categories()
        for i, cat in enumerate(categories):
            self.create_ring_button(self.menu_frame, cat,
                                    lambda c=cat: self.show_items(c),
                                    i//2, i%2)
    
    def show_items(self, category):
        self.clear_buttons()
        self.display.config(text=f"Items: {category}")

        items = self.data.get_items_in_category(category)
        for i, (item_id, details) in enumerate(items.items()):
            self.create_ring_button(self.menu_frame, details['name'],
                                    lambda d=details: self.start_cooking(d),
                                    i//2, i%2)


        back_btn = Button(self.menu_frame, text="BACK", font=("Arial", 9, "bold"), 
                          fg="#D3D3D3", bg="#4A4A4A",
                          relief="flat", command=self.load_main_menu)
        back_btn.grid(row=99, column=0, columnspan=2, pady=20)

    def start_cooking(self, food_dict):
        self.clear_buttons()

        """Note to partners: whenever the System Logic class,
           or whatever we rename it to, is complete then it will
           be added to this function.
        """

        #This line formates the time to look like a real microwave
        min, sec = divmod(food_dict['time'],60)
        self.display.config(text=f"{min:02}:{sec:02}")

        info_label = Label(self.menu_frame, f"COOKING: {food_dict['name']}", bg="#2C2C2C", fg="#D3D3D3",
              font=("Arial", 12))
        info_label.grid(row=0, column=0, pady=20)

        cancel_canvas = Canvas(self.menu_frame, width=150, height=60, bg="#2C2C2C", highlightthickness=0)
        cancel_canvas.grid(row=1, column=0, pady=10)
        ring = cancel_canvas.create_oval(10, 10, 140, 50, outline="#B22222", width=4)
        txt = cancel_canvas.create_text(75, 30, text="CANCEL", fill="#B22222", font=("Arial", 10, "bold"))
        
        cancel_canvas.tag_bind(ring, "<Button-1>", lambda e: self.load_main_menu())
        cancel_canvas.tag_bind(txt, "<Button-1>", lambda e: self.load_main_menu())

root = Tk()
my_gui = RemoteInterface(root)
root.mainloop()