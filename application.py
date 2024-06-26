import sys
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import Toplevel, Text
import subprocess
import os

from updateAvailability.AvailabilityUpdater import update_availability, avail_ranges
from utils.helperFunctions import convert_to_readable_time, quicksort_shifts, getLocationNames
from api_calls.schedule_source_api.schedule_source_api import getScheduleId, getEmptyShiftsForDay, getLocations, \
    getScheduleNames
from availabilityCalculator.main import filterEmptyShiftsForDay

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# Define the path to the Excel file
excel_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Timetable.xlsx")

def execute_backend_script(excel_file_path):
    # Run the backend script with the excel file path as an argument
    subprocess.run(
        [sys.executable, os.path.join(os.path.dirname(__file__), "gridGenerator", "gridGenerator.py"), excel_file_path])

def show_file_path(file_path):
    # Create a new top-level window
    new_window = tk.Toplevel(root)
    new_window.title("Generated Timetable")
    new_window.geometry("600x200")

    # Display the file path
    ttk.Label(new_window, text="Timetable generated at:").pack(pady=10)

    # Display the file path in a larger white font
    file_path_label = tk.Label(new_window, text=file_path, fg="black", font=("Helvetica", 15, "bold"))
    file_path_label.pack(pady=10)

    # Button to close the new window and terminate the program
    ttk.Button(new_window, text="OK", command=root.quit).pack(pady=10)

def on_ok():
    # Print the values entered in the entry fields
    print(f"Facility Name: {selected_facility_var.get()}")
    print(f"Schedule Name: {selected_schedule_var.get()}")
    print(f"External ID: {external_id.get()}")

    try:
        # Retrieve the schedule ID number based on the user input
        scheduleId = getScheduleId(selected_facility_var.get().rstrip(), selected_schedule_var.get().rstrip())
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch Schedule ID: {e}")

    # Show that the program is loading/executing
    print("Loading Window...")

    # Withdraw the main window
    root.withdraw()

    # Use the student ID entered by the user
    student_id = external_id.get()

    # Execute the backend script and get the file path
    execute_backend_script(excel_file_path)

    # Open window for listing available empty shifts
    if scheduleId:
        open_empty_shifts_window(student_id, scheduleId)

        # Call update_availability method
        update_availability(student_id, avail_ranges)
        print("Availability Updated")
    else:
        print("Error Retrieving the Schedule ID Number")

    # Show the file path in a new window
    show_file_path(excel_file_path)

def open_empty_shifts_window(studentId, scheduleId):
    new_window = Toplevel(root)
    new_window.title("Available Shifts")
    new_window.geometry("600x400")
    label = tk.Label(new_window, text="Shifts Available To Work")
    label.pack(pady=20)

    text_widget = Text(new_window)
    text_widget.pack(expand=True, fill='both')

    def printAllEmptyShifts(studentId, scheduleId):
        text_widget.insert(tk.END, " Day\t\t  Start\t\t  End\t\t  Station\n\n")
        for dayId in range(1, 8):
            printEmptyShiftsForDay(studentId, scheduleId, dayId)
            text_widget.insert(tk.END, "\n")

    def printEmptyShiftsForDay(studentId, scheduleId, dayId):
        dayString = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"][dayId - 1]
        emptyShifts = getEmptyShiftsForDay(scheduleId, dayId)
        emptyShifts = filterEmptyShiftsForDay(studentId, emptyShifts)
        emptyShifts = quicksort_shifts(emptyShifts)

        for shift in emptyShifts:
            readableStart = convert_to_readable_time(shift["ShiftStart"])
            readableEnd = convert_to_readable_time(shift["ShiftEnd"])
            text_widget.insert(tk.END,
                               f"{dayString}\t\t{readableStart}\t\t{readableEnd}\t\t{shift['StationName']}\n"
                               )

    printAllEmptyShifts(studentId, scheduleId)

    # Add a button to close the new window
    close_button = tk.Button(new_window, text="Close", command=new_window.destroy)
    close_button.pack(pady=10)

def select_location(event):
    selected_facility = selected_facility_var.get()
    on_location_change(selected_facility)

def on_location_change(newLocation):
    global schedule_name_list
    schedule_name_list = getScheduleNames(newLocation)
    initDropdowns()
    print("Location Changed to " + newLocation)

def initDropdowns():
    ttk.Label(root, text="Facility Name:").grid(column=0, row=0, padx=10, pady=5, sticky=tk.W)
    facility_name = ttk.Combobox(root, textvariable=selected_facility_var, values=sorted(location_name_list), width=30)
    facility_name.bind('<<ComboboxSelected>>', select_location)
    facility_name.grid(column=1, row=0, padx=10, pady=5)

    ttk.Label(root, text="Schedule Name:").grid(column=0, row=1, padx=10, pady=5, sticky=tk.W)
    schedule_name = ttk.Combobox(root, textvariable=selected_schedule_var, values=schedule_name_list, width=30)
    schedule_name.grid(column=1, row=1, padx=10, pady=5)

# Create the main window
root = tk.Tk()
root.title("Class Schedule Generator")
root.geometry("440x160")

location_list = getLocations()
location_name_list = getLocationNames(location_list)

selected_facility_var = tk.StringVar(root)
selected_schedule_var = tk.StringVar(root)

selected_facility_var.set("Select a location")

schedule_name_list = []

initDropdowns()

ttk.Label(root, text="External ID:").grid(column=0, row=2, padx=10, pady=5, sticky=tk.W)
external_id = ttk.Entry(root, width=30)
external_id.grid(column=1, row=2, padx=10, pady=5)

generate_button = ttk.Button(root, text="Generate Schedule", command=on_ok)
generate_button.grid(column=0, row=3, columnspan=2, pady=10)

for child in root.winfo_children():
    child.grid_configure(padx=10, pady=5)

root.mainloop()
