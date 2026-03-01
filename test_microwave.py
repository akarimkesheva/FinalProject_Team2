#This file is for testing Microwave's working logic

from recipedata import RecipeData
from SystemLogic import SystemLogic

# Setup the system
db = RecipeData()
logic = SystemLogic(db)

print("TESTING THE MICROWAVE ")

# TEST 1: Check if we can get a recipe
print("\nTest 1: Fetching 'Cup of Coffee'...")
recipe = logic.get_preset("Everyday Basics", "14")
if recipe:
    print(f"SUCCESS: Found {recipe['name']} ({recipe['time']} seconds)")

# TEST 2: Try to start with the door OPEN
print("\nTest 2: Attempting to start with Door Open...")
logic.open_door() # Force door open
result = logic.start_microwave()
print(f"RESULT: {result}") # Should say "Please, close the door"

# TEST 3: Try to start with Child Lock ON
print("\nTest 3: Closing door but turning on Child Lock...")
logic.close_door()
logic.set_lock_on()
result = logic.start_microwave()
print(f"RESULT: {result}") # Should say "Please,turn off the child lock"

# TEST 4: Successful Start
print("\nTest 4: Turning off Lock and Starting...")
logic.set_lock_off()
result = logic.start_microwave()
print(f"RESULT: {result}") # Should say "STARTING"