"""
DAY 2:
Interactive Checklist with JSON Save/Load

SCRIPT:
- A terminal app that lets teh user add steps, view the list, and mark steps as complete.
App remembers the list between runs. Save data to JSON file.

1. Loads existing checklist items from 'day2_checklist.json' (or start with an empty list if none).
2. Display a simple menu with four options (add, view, mark complete, remove, exit)
3. Allow users to add new steps to the checklist.
4. Allow users to mark steps as complete with ✅(green check) or ❌(red x).
5. Allow users to remove an item by it's name or number, with input validation.
6. Saves changes back to 'day2_checklist.json' so the list is remembered between runs.
"""

# IMPORT MODULES
from pathlib import Path # Path provides clean, cross-platform file paths.
import json              # JSON lets us save Python lists/dictionaries to disk as text

# ------------------------
# FILE PATHS
# ------------------------

# Directory where script lives. Checklist file will save in same place as script.
# NO MATTER WHERE IT RUN'S FROM
PROJECT_DIRECTORY = Path(__file__).resolve().parent
CHECKLIST_FILE_PATH = PROJECT_DIRECTORY / "day2_checklist.json"

# -------------------------------------
# ACCESS DATA: load and save checklist
# -------------------------------------

"""
Purpose:
- Try and restore user's previous checklist when APP launches 🚀
- If file does not exist (usually during first run), return with an empty list (APP continues)

Return Type:
- A list of dictionaries. Each dictionary is one item.
Ex: {"title": "Verify Login Screen", "is_done" false}
"""
def load_checklist_from_disk() -> list[dict]: # read from disk, promise to return a list of dictionaries
    if not CHECKLIST_FILE_PATH.exists():
        return [] # If file does nto exist, start with an empty list

    try:
        raw_text = CHECKLIST_FILE_PATH.read_text(encoding = "utf-8") # open file and read all text inside.
        maybe_items = json.loads(raw_text) # Try converting text into Python data (a list of dictionaries)

    # If data is a proper list of dictionaries, return the data
        if isinstance(maybe_items, list) and all(isinstance(i, dict) for i in maybe_items):
            return maybe_items

        # If file format is incorrect, warn user and start clean.
        print("⚠️ Found checklist file, but format looked unexpected: Starting clean...")
        return []
        # If an error occurs while reading or parsing, catch error and start with an empty list.
    except Exception as error:
        print(f"⚠️ Could not read checklist file: {error}. Starting clean...")
        return []

# Saves/Writes the current list of checklist items to JSON. Progress is when program closes and reopens
def save_checklist_to_disk(checklist_items: list[dict]) -> None:
    try:
        CHECKLIST_FILE_PATH.write_text( # Try to write file
            json.dumps(checklist_items, indent = 2), # Save list in JSON format
            encoding = "utf-8"
        )
    # If saving fails (ex; no permission or disk error), we tell the user without crashing.
    except Exception as error:
        print(f"❌ Could not save checklist to disk: {error}")

# --------------------------------------------------------------
# UI : Displaying Menu and Checklist Items
# --------------------------------------------------------------
# Prints list of menu options so users knows what to do
def display_menu_options() -> None:
    print("\n ==== TEST CHECKLIST ====")
    print("1) Add a new checklist item")
    print("2) Show all items")
    print("3) Mark an item as complete")
    print("4) Remove an item (by number OR name)")
    print("5) Exit")

# Shows entire checklist.
# Each item is displayed with progress status with ✅(green check) or ❌(red x)
def show_all_items(checklist_items: list[dict]) -> None:
    if not checklist_items:
        print("No item yet. Select option 1. to add your first step.")
        return

    # Get the title of the checklist item, or show untitled if missing
    for display_number, item in enumerate(checklist_items, start = 1):
        title_text = item.get("title", "(untitled)")

        # Convert the "is_done" field to a True or False
        is_done_flag = bool(item.get("is_done"))

        # Show a checkmark if checklist item is complete, if not show an X.
        status_icon = "✅" if is_done_flag else "❌"

        # Print item with it's number ad status.
        print(f"{display_number}. {title_text} {status_icon}")

# -----------------------------------------------------------
# FUNCTIONS: Adding, marking complete, and removing items
# -----------------------------------------------------------
# This function allows users to add items to checklist
def add_new_item_to_checklist(checklist_items: list[dict]) -> None:
    user_title_input = input("Enter the name of the checklist item you want to add: ").strip()
    if not user_title_input:
        print("⚠️ Item title cannot be empty. ")
        return

    # Create a dictionary for the new item, set progress to false
    new_item = {"title": user_title_input, "is_done": False}

    # Add the new item to the list
    checklist_items.append(new_item)

    # Save the updated list to a JSON file.
    save_checklist_to_disk(checklist_items)

    # Confirm to user that the item was added
    print(f"✅ Added: {user_title_input}")

# This function allows the user to mark an item as complete by it's number.
def mark_item_complete_by_number(checklist_items: list[dict]) -> None:

    # If item is not in the checklist, tell the user to first add somethjing.
    if not checklist_items:
        print("The checklist is empty, you must first add something")
        return

    # Display checklist items to the user
    show_all_items(checklist_items)

    # Ask user for item number and verify entry
    item_number_entry = input("Enter the item item number you want to mark complete: ").strip()
    if not item_number_entry.isdigit():
        print("⚠️ Please enter a whole number like 1, 2, or 3.")
        return

    user_number = int(item_number_entry)
    if not (1 <= user_number <= len(checklist_items)):
        print("⚠️ That number is not in the list. Try again.")
        return

    # Convert number entry to readable python index
    # Choses the item based on the number that the user types
    list_item_index = user_number - 1
    chosen_item = checklist_items[list_item_index]

    # If the item has been completed, inform the user and do nothing
    if chosen_item.get("is_done"):
        print(f"ℹ️ '{chosen_item.get('title', '(untitled)')}' is already marked complete.")
        return

    chosen_item['is_done'] = True
    save_checklist_to_disk(checklist_items)
    print(f"✅ Marked complete: {chosen_item.get('title')} ")

# Allows user to remove an item by name or number entry.
# If multiple items partially match an item name, ask the user chose which one to remove.
def remove_item_by_number_or_name(checklist_items: list[dict]) -> None:
    # If item is not in the checklist, tell the user to first add something.
    if not checklist_items:
        print("No item to remove, you must first add something")
        return

    # Show the current items to help the user chose.
    show_all_items(checklist_items)

    # Ask for input (could be a number or item name)
    user_input = input("Enter the number OR name of the checklist item to remove: ").strip()
    if not user_input:
        print("⚠️ You typed nothing. Removal canceled.")
        return

    # If the input is a digit, we treat it as a number.
    if user_input.isdigit():
        user_number = int(user_input)
        if not (1 <= user_number <= len(checklist_items)):
            print("⚠️ That number is not in the list. ")
            return
        removed_item = checklist_items.pop(user_number - 1)
        save_checklist_to_disk(checklist_items)
        print(f"🗑️ Removed: {removed_item['title']}")
    else:
        # Otherwise, we treat it as a name
        for item in checklist_items:
            if item.get("title", "").lower() == user_input.lower():
                checklist_items.remove(item)
                save_checklist_to_disk(checklist_items)
                print(f"🗑️ Removed: {removed_item['title']}")
                return
            print("⚠️ Could not find an item with that name.")

# -------------------------------------------------------------------
# MAIN LOOP
# -------------------------------------------------------------------

"""
Main Function for check list app.
Displays the user menu un user chooses to and option or to exit.
"""
def main():
    checklist_items = load_checklist_from_disk()

    while True:
        display_menu_options()
        choice = input("Choose an option (1-5): ").strip()

        if choice == "1":
            add_new_item_to_checklist(checklist_items)
        elif choice == "2":
            show_all_items(checklist_items)
        elif choice == "3":
            mark_item_complete_by_number(checklist_items)
        elif choice == "4":
            remove_item_by_number_or_name(checklist_items)
        elif choice == "5":
            print("👋 Goodbye!")
            break
        else:
            print("⚠️ Invalid choice. Please pick 1-5.")

# -------------------------------------------------------------------
# RUN PROGRAM
# -------------------------------------------------------------------

if __name__ == "__main__":
    main()