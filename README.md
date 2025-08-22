📋 Day 2: Interactive Checklist with Save/Load

🎯 Goal

Build a terminal-based checklist app that lets testers track their steps interactively. Unlike Day 1, the app now remembers progress between runs by saving to a JSON file.

🛠 Features

This script:
	1.	Loads existing checklist items from day2_checklist.json (or starts with an empty list if it doesn’t exist).
	2.	Displays a menu with five options:
	•	Add a new item
	•	Show all items
	•	Mark an item as complete
	•	Remove an item (by number or name)
	•	Exit
	3.	Adds new test steps into the checklist.
	4.	Marks steps as complete with a ✅ (green check) or ❌ (red x).
	5.	Removes items by either their number or name (with validation to prevent mistakes).
	6.	Saves all changes back to day2_checklist.json so the list is remembered across runs.

📂 Files Created
	•	day2_checklist.json → Stores checklist items as JSON.
Example content:
[
  {"title": "Verify login screen", "is_done": false},
  {"title": "Check forgot password link", "is_done": true}
]

▶️ How to Run
	1.	Open a terminal in the day2/ folder.
	2.	Run: python3 day2_checklist.py

✅ Example Run
==== TEST CHECKLIST ====
1) Add a new checklist item
2) Show all items
3) Mark an item as complete
4) Remove an item (by number OR name)
5) Exit

Choose an option (1-5): 1
Enter the name of the checklist item you want to add: Verify login screen
✅ Added: Verify login screen

Choose an option (1-5): 2
1. Verify login screen ❌

Choose an option (1-5): 3
Enter the item number you want to mark complete: 1
✅ Marked complete: Verify login screen