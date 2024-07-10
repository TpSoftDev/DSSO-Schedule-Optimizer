from datetime import datetime
from openpyxl.reader.excel import load_workbook
from openpyxl.workbook import Workbook
from copy import copy


#Converts a string representing a time value and converts it to a programmable datetime.time() object
#Param: time_str - the time value in string format (e.g "12:00:00 AM" or "1900-05-10T13:00:00")
#Returns the same time, but as an instance datetime.time()
def convert_to_time(time_str):
    try:
        if "T" in time_str:  # Check if input is in "YYYY-MM-DDTHH:MM:SS" format
            datetime_obj = datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%S")
        else:  # Assuming the default format is "%I:%M:%S %p"
            datetime_obj = datetime.strptime(time_str, "%I:%M:%S %p")
        return datetime_obj.time()
    except ValueError:
        return None


#Parses a datetime object and returns the readable, string equivilant
#Param: datetime - the datetime object that can either be formatted by datte and time, or date only
#Returns the same time in a readable, string format
def convert_to_readable_time(datetime_obj):
    try:
        # Try to parse the datetime string with both date and time
        dt = datetime.strptime(datetime_obj, "%Y-%m-%dT%H:%M:%S")
        # Format the datetime object to a readable 12-hour time string
        readable_time = dt.strftime("%I:%M %p")
    except ValueError:
        # If the above fails, try to parse the string as a date only
        dt = datetime.strptime(datetime_obj, "%Y-%m-%d")
        # Format the datetime object to indicate it's a whole day
        readable_time = "12:00 AM"  # Representing the start of the day

    return readable_time


#Utilizes the quicksort algorithm to display shifts from earliest start time to latest start time
#Param - shifts - the list of shift objects (in json format) that are unordereds
#Returns the sorted list of shifts from earliest start time to latest start time
#Used by the availability calculator to display empty shifts in a more readable format
def quicksort_shifts(shifts):
    if len(shifts) <= 1:
        return shifts
    else:
        pivot = shifts[len(shifts) // 2]["ShiftStart"]
        left = [x for x in shifts if x["ShiftStart"] < pivot]
        middle = [x for x in shifts if x["ShiftStart"] == pivot]
        right = [x for x in shifts if x["ShiftStart"] > pivot]
        return quicksort_shifts(left) + middle + quicksort_shifts(right)


#Retrieves the list of strings representing each facilities name
#Used to ensure that the list displayed in the app's dropdown menu are purely strings and not json objects
#Param - locations - list of json objects with an "ExternalBusinessIdField"
#Returns the list of strings each representing the value of the ExternalBusinessId field for each location
def getLocationNames(locations):
    string_list = []
    for item in locations:
        string_list.append(item["ExternalBusinessId"])
    return string_list


#Converts tsv data into json objects that are easier to parse through
#Needed for the getAllActiveEmployees function in the SS api call because the response defaults to tsv format
#Param - tsv_data - the data response gotten back from SS api at endpoint /Employees
#Returns the same data set, but in json format instead of tsv
def parse_tsv(tsv_data):
    # Split data into lines
    lines = tsv_data.strip().split('\r\n')
    # Extract headers
    headers = lines[0].split('\t')
    # Parse each line into a dictionary
    data = [
        dict(zip(headers, line.split('\t')))
        for line in lines[1:]
    ]
    return data


def copy_worksheet(source_sheet, target_sheet):
    for row in source_sheet.iter_rows():
        for cell in row:
            new_cell = target_sheet.cell(row=cell.row, column=cell.column, value=cell.value)
            if cell.has_style:
                new_cell.font = copy(cell.font)
                new_cell.border = copy(cell.border)
                new_cell.fill = copy(cell.fill)
                new_cell.number_format = copy(cell.number_format)
                new_cell.protection = copy(cell.protection)
                new_cell.alignment = copy(cell.alignment)



