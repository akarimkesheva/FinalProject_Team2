#This is the main class of the Microwave

#This class links to our recipedata class
class SystemLogic:
    def __init__(self, database):
        self.db = database
        self.is_door_closed = True  # True means closed, False means open
        self.child_lock = False     # True means locked, False means off
        self.is_running = False     # Tracks if the microwave is currently cooking

    # Door commands
    def open_door(self):
        self.is_door_closed = False #Simulates opening the microwave door
        self.is_running = False
        return "Door is now Open"

#Simmulates closing the microwave door
    def close_door(self):
        self.is_door_closed = True
        return "Door is now Closed"

    # Child lock is on
    def set_lock_on(self):
        self.child_lock = True
        return "Child Lock Activated"

#Child lock is off
    def set_lock_off(self):
        self.child_lock = False
        return "Child Lock Deactivated"

    # Safety check, so the microwave is allowed to start
    def check_if_ready(self):
        if self.is_door_closed == False:
            return "Please,close the door"
            
        
        if self.child_lock == True:
            return "Please, turn off the child lock"
            
        #if everything is ok
        return "OK"

    # Recipe and manual connection 
    def get_preset(self, category, item_id):
        return self.db.get_cooking_data(category, item_id)

    def start_microwave(self):
        status = self.check_if_ready()
        if status == "OK":
            self.is_running = True
            return "STARTING"
        else:
            return status # Returns the specific error (Door or Lock)