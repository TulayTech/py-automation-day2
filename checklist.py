# Import json and os modules to handle JSON data and file operations
import json
import os

# Define path to checklist JSON file to store checklist data
CHECKLIST_FILE = "checklist.json"

# ----------------------------
# Utility functions
# ----------------------------

# Function to load checklist from JSON file if it exists
def load_checklist():
    if os.path.exists(CHECKLIST_FILE):
        with open(CHECKLIST_FILE, "r") as file:
            return json.load(file)
    return [] # Returns an empty list if file does not exist

# Function to save checklist to JSON file
def save_checklist(checklist):
    with open(CHECKLIST_FILE, "w") as file:
        json.dump(checklist, file, indent=2)

# Function to display the checklist items
def display_checklist():
    """ Display checklist options """
    print("\n 📝 Checklist Menu: ")
    print("1. Add a new test step")
    print("2. View all test steps")
    print("3. Mark a step as completed")
    print("4. Exit")

# Function to display all checklist items with status
def view_checklist(checklist):
    if not checklist:
        print(" The checklist is empty")
        return
    for index, item in enumerate(checklist, 1):
        status = "✅" if item["completed"] else "❌"
        print(f"{index}. {item['name']} - {status}")

# ----------------------------
# Main app
# ----------------------------

# Main function to run the checklist application
def main():
    checklist = load_checklist()

    while True:
        display_checklist()
        choice = input("Choose an option (1-4): ")

        if choice == "1":
            step_name = input("Enter the name for this step: ")
            checklist.append({"name": step_name, "completed": False})
            save_checklist(checklist)
            print(f"Step '{step_name}' added to the checklist.")

        elif choice == "2":
            view_checklist(checklist)

        elif choice == "3":
            view_checklist(checklist)
            try:
                index = int(input("Enter the step number to mark as completed: "))
                if 1 <= index <= len(checklist):
                    checklist[index - 1]["completed"] = True
                    save_checklist(checklist)
                    print(f"Step '{checklist[index - 1]['name']}' marked as completed.")
                else:
                    print("⚠️Invalid step number.")
            except ValueError:
                print("⚠️Please enter a valid number.")

        elif choice == "4":
            print("⛔️Exiting the checklist application. Goodbye!")
            break
        else:
            print("⚠️Invalid choice. Please select a valid option (1-4).")

if __name__ == "__main__":
    main()