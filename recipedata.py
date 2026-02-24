#This class is responsible for all the Recipes in the Microwave
#Organized by categories
class recipedata:
    def __init__(self):
    
        self.menu = {
            "Meat & Chicken": {
                "01": {"name": "Frozen Chicken Breast", "power": 3, "time": 420},
                "02": {"name": "Ground Beef (Defrost)", "power": 3, "time": 300},
                "03": {"name": "Bacon Strips", "power": 10, "time": 180},
                "04": {"name": "Hot Dogs", "power": 9, "time": 45}
            },
            "Seafood": {
                "05": {"name": "White Fish Fillet", "power": 7, "time": 180},
                "06": {"name": "Salmon Steak", "power": 6, "time": 240},
                "07": {"name": "Frozen Shrimp", "power": 5, "time": 300}
            },
            "Vegetables & Grains": {
                "08": {"name": "Baked Potato", "power": 10, "time": 300},
                "09": {"name": "Steamed Broccoli", "power": 10, "time": 150},
                "10": {"name": "White Rice", "power": 10, "time": 600}
            },
            "Everyday Basics": {
                "11": {"name": "Reheat Leftover Plate", "power": 7, "time": 120},
                "12": {"name": "Bowl of Soup", "power": 10, "time": 180},
                "13": {"name": "Pizza Slice", "power": 6, "time": 45},
                "14": {"name": "Cup of Coffee/Tea", "power": 10, "time": 60}
            },
            "Snacks & Easy Meals": {
                "15": {"name": "Popcorn", "power": 10, "time": 120},
                "16": {"name": "Mac & Cheese Bowl", "power": 10, "time": 210},
                "17": {"name": "Frozen Burrito", "power": 9, "time": 150},
                "18": {"name": "Instant Ramen", "power": 10, "time": 180}
            },
            "Breakfast & Bakery": {
                "19": {"name": "Oatmeal", "power": 8, "time": 90},
                "20": {"name": "Scrambled Eggs (2)", "power": 7, "time": 60},
                "21": {"name": "Morning Muffin", "power": 5, "time": 20},
                "22": {"name": "Chocolate Mug Cake", "power": 9, "time": 90}
            },
            "Kids & Baby": {
                "23": {"name": "Chicken Nuggets", "power": 8, "time": 120},
                "24": {"name": "Baby Food Jar (Warm)", "power": 4, "time": 30},
                "25": {"name": "Milk Bottle (Gentle)", "power": 3, "time": 45}
            }
        }
# Grabs the main menu headings (like 'Seafood' or 'Breakfast')
 #Tells the microwave screen which category buttons to show.
    def get_categories(self):
        return list(self.menu.keys())
    
#Retrieves all food products associated with a specific category.
    def get_items_in_category(self, category_name):
        items = self.menu.get(category_name)
        if items:
            return items
        else:
            return f"Category '{category_name}' not found."
    

#Retrieves the final execution parameters for a specific food item.
    def get_cooking_data(self, category, item_id):
        category_data = self.menu.get(category)
        if category_data:
            # Return None if the ID isn't there
            return category_data.get(item_id, None)
        return None


# This part simulates the user using the microwave interface

if __name__ == "__main__":
    
    manager = RecipeData()

    print("--- Welcome to the World's Best Microwave ---")
    print("1: Recipe Mode | 2: Manual Time Mode")
    mode = input("Select Mode: ")

    if mode == "1": # Recipe mode
        categories = manager.get_categories()
        for i, cat in enumerate(categories):
            print(f"{i}. {cat}")

        # Simulate User picking a category
        choice_index = 3 
        if 0 <= choice_index < len(categories):
            selected_cat = categories[choice_index]
            print(f"\nUser selected: {selected_cat}")

            items = manager.get_items_in_category(selected_cat)
            for item_id, details in items.items():
                print(f"   [{item_id}] {details['name']}")

            selected_id = "14"
            food_data = manager.get_cooking_data(selected_cat, selected_id)

            print("\n--- FINAL COOKING COMMAND SENT TO MICROWAVE ---")
            if isinstance(food_data, dict):
                print(f"FOOD: {food_data['name']}")
                print(f"POWER LEVEL: {food_data['power']}")
                print(f"TIMER: {food_data['time']} seconds")
            else:
                print(f"Error: {food_data}")
        else:
            print(f"\nERROR: {choice_index} is not a valid choice.")

    elif mode == "2": # Manual entry
        user_time = input("Enter time in seconds: ")
        user_power = input("Enter power level (1-10): ")
        print(f"\n--- FINAL COOKING COMMAND SENT TO MICROWAVE ---")
        print(f"MANUAL MODE: {user_time} seconds at Power {user_power}")

    else:
        print("Invalid mode selected.")