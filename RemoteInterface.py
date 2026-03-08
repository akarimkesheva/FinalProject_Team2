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
================================

Revisions by: Noah Beach
Revision Date: 03/03/2026

Revisions:
- Integrated the GUI with the SystemLogic backend
- Linked preset food selections to recipe data
- Added child lock on/off buttons
- Added door open/close buttons
- Added manual cooking mode with time and power input
- Updated cooking behavior to check for safety conditions before starting

"""
from tkinter import *
from recipedata import RecipeData
from SystemLogic import SystemLogic

class RemoteInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Microwave")
        self.root.configure(bg="#2C2C2C")
        self.data = RecipeData()
        self.logic = SystemLogic(self.data)

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
        canvas.tag_bind(label, "<Enter>", lambda e: canvas.itemconfig(ring, outline="#FFFFFF"))
        canvas.tag_bind(label, "<Leave>", lambda e: canvas.itemconfig(ring, outline="#D3D3D3"))

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
        # These buttons were added so the user can use manual mode and test safety features
        manual_btn = Button(self.menu_frame, text="MANUAL MODE", font=("Arial", 10, "bold"), 
                          fg="#D3D3D3", bg="#4A4A4A",
                          relief="flat", command=self.show_manual_mode)
        manual_btn.grid(row=40, column=0, columnspan=2, pady=10)

        lock_on_btn = Button(self.menu_frame, text="LOCK ON", font=("Arial", 9, "bold"), 
                          fg="#D3D3D3", bg="#4A4A4A",
                          relief="flat", command=self.enable_child_lock)
        lock_on_btn.grid(row=50, column=0, pady=10)

        lock_off_btn = Button(self.menu_frame, text="LOCK OFF", font=("Arial", 9, "bold"), 
                          fg="#D3D3D3", bg="#4A4A4A",
                          relief="flat", command=self.disable_child_lock)
        lock_off_btn.grid(row=50, column=1, pady=10)

        open_door_btn = Button(self.menu_frame, text="OPEN DOOR", font=("Arial", 9, "bold"), 
                          fg="#D3D3D3", bg="#4A4A4A",
                          relief="flat", command=self.open_door)
        open_door_btn.grid(row=51, column=0, pady=10)

        close_door_btn = Button(self.menu_frame, text="CLOSE DOOR", font=("Arial", 9, "bold"), 
                          fg="#D3D3D3", bg="#4A4A4A",
                          relief="flat", command=self.close_door)
        close_door_btn.grid(row=51, column=1, pady=10)
    
    def show_items(self, category):
        self.clear_buttons()
        self.display.config(text=f"Items: {category}")

        items = self.data.get_items_in_category(category)
        for i, (item_id, details) in enumerate(items.items()):
            self.create_ring_button(self.menu_frame, details['name'],
                                    lambda c=category, i_id=item_id: self.start_cooking(c, i_id),
                                    i//2, i%2)


        back_btn = Button(self.menu_frame, text="BACK", font=("Arial", 9, "bold"), 
                          fg="#D3D3D3", bg="#4A4A4A",
                          relief="flat", command=self.load_main_menu)
        back_btn.grid(row=99, column=0, columnspan=2, pady=20)

    def enable_child_lock(self):
        message = self.logic.set_lock_on()
        self.display.config(text=message)

    def disable_child_lock(self):
        message = self.logic.set_lock_off()
        self.display.config(text=message)

    def open_door(self):
        message = self.logic.open_door()
        self.display.config(text=message)

    def close_door(self):
        message = self.logic.close_door()
        self.display.config(text=message)

    def show_manual_mode(self):
        self.clear_buttons()
        self.display.config(text="MANUAL MODE")

        time_label = Label(self.menu_frame, text="Time (seconds):", bg="#2C2C2C", fg="#D3D3D3",
              font=("Arial", 12))
        time_label.grid(row=0, column=0, pady=10)

        self.time_entry = Entry(self.menu_frame, font=("Arial", 12), width=12)
        self.time_entry.grid(row=0, column=1, pady=10)

        power_label = Label(self.menu_frame, text="Power (1-10):", bg="#2C2C2C", fg="#D3D3D3",
              font=("Arial", 12))
        power_label.grid(row=1, column=0, pady=10)

        self.power_entry = Entry(self.menu_frame, font=("Arial", 12), width=12)
        self.power_entry.grid(row=1, column=1, pady=10)

        start_btn = Button(self.menu_frame, text="START MANUAL", font=("Arial", 9, "bold"), 
                          fg="#D3D3D3", bg="#4A4A4A",
                          relief="flat", command=self.start_manual_cooking)
        start_btn.grid(row=2, column=0, columnspan=2, pady=20)

        back_btn = Button(self.menu_frame, text="BACK", font=("Arial", 9, "bold"), 
                          fg="#D3D3D3", bg="#4A4A4A",
                          relief="flat", command=self.load_main_menu)
        back_btn.grid(row=3, column=0, columnspan=2, pady=20)

    def start_manual_cooking(self):
        # Makes sure the user input is numbers with the range
        try:
            cook_time = int(self.time_entry.get())
            power = int(self.power_entry.get())
        except ValueError:
            self.display.config(text="INPUT ERROR")
            error_label = Label(self.menu_frame, text="Please enter valid numbers.", bg="#2C2C2C", fg="#D3D3D3",
                  font=("Arial", 12))
            error_label.grid(row=4, column=0, columnspan=2, pady=20)
            return

        if cook_time <= 0:
            self.display.config(text="TIME ERROR")
            error_label = Label(self.menu_frame, text="Time must be greater than 0.", bg="#2C2C2C", fg="#D3D3D3",
                  font=("Arial", 12))
            error_label.grid(row=4, column=0, columnspan=2, pady=20)
            return

        if power < 1 or power > 10:
            self.display.config(text="POWER ERROR")
            error_label = Label(self.menu_frame, text="Power must be 1 to 10.", bg="#2C2C2C", fg="#D3D3D3",
                  font=("Arial", 12))
            error_label.grid(row=4, column=0, columnspan=2, pady=20)
            return

        self.clear_buttons()

        status = self.logic.start_microwave()

        if status != "STARTING":
            self.display.config(text="BLOCKED")
            info_text = status
        else:
            min, sec = divmod(cook_time,60)
            self.display.config(text=f"{min:02}:{sec:02}")
            info_text = f"MANUAL COOKING\nPower: {power}"
            self.update_countdown(cook_time)

        info_label = Label(self.menu_frame, text=info_text, bg="#2C2C2C", fg="#D3D3D3",
              font=("Arial", 12))
        info_label.grid(row=0, column=0, pady=20)

        cancel_canvas = Canvas(self.menu_frame, width=150, height=60, bg="#2C2C2C", highlightthickness=0)
        cancel_canvas.grid(row=1, column=0, pady=10)
        ring = cancel_canvas.create_oval(10, 10, 140, 50, outline="#B22222", width=4)
        txt = cancel_canvas.create_text(75, 30, text="CANCEL", fill="#B22222", font=("Arial", 10, "bold"))
        
        cancel_canvas.tag_bind(ring, "<Button-1>", lambda e: self.load_main_menu())
        cancel_canvas.tag_bind(txt, "<Button-1>", lambda e: self.load_main_menu())
    
    def update_countdown(self, seconds_left):
        if not self.logic.is_running or seconds_left < 0:
            if seconds_left <= 0 and self.logic.is_running:
                self.display.config(text="DONE!")
                self.logic.is_running = False
            return
        
        min, sec = divmod(seconds_left, 60)
        self.display.config(text=f"{min:02}:{sec:02}")

        self.root.after(1000, lambda: self.update_countdown(seconds_left -1))

    def start_cooking(self, category, item_id):
        self.clear_buttons()

        food_dict = self.logic.get_preset(category, item_id)

        if not food_dict:
            self.display.config(text="ERROR")
            error_label = Label(self.menu_frame, text="Food preset not found.", bg="#2C2C2C", fg="#D3D3D3",
              font=("Arial", 12))
            error_label.grid(row=0, column=0, pady=20)
            return

        status = self.logic.start_microwave()

        #This line formates the time to look like a real microwave
        if status != "STARTING":
            self.display.config(text="BLOCKED")
            info_text = status
        else:
            min, sec = divmod(food_dict['time'],60)
            self.display.config(text=f"{min:02}:{sec:02}")
            info_text = f"COOKING: {food_dict['name']}\nPower: {food_dict['power']}"

            self.update_countdown(food_dict['time'])

        info_label = Label(self.menu_frame, text=info_text, bg="#2C2C2C", fg="#D3D3D3",
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
