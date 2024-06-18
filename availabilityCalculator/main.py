import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
external_directory = os.path.join(current_dir, "..")
sys.path.append(external_directory)


from api_calls.workday_api.workday_api import getStudentSchedule
from api_calls.schedule_source_api.schedule_source_api import getEmptyShiftsForDay
from utils.helperFunctions import convert_to_time, convert_to_readable_time, quicksort_shifts



#Determines what shifts are to be removed from the list of empty shifts and generates new list with those shifts removed
#Param: "studentId" - the unique university id number for the student we are looking into
#       "emptyShifts" - the list of empty shifts for a given facility's schedule
#Returns a new list of empty shifts with the necessary shifts removed
def filterEmptyShiftsForDay(studentId, emptyShifts):
    classes = getStudentSchedule(studentId)
    shiftsToRemove = []
    for shift in emptyShifts:
        if not(availableForShift(classes, shift)):
            shiftsToRemove.append(shift)
            
    emptyShifts = removeShifts(emptyShifts, shiftsToRemove)
    return emptyShifts


#Determines whether or not an employees class schedule conflicts with an empty facility shift
#Params: "classSchedule" - list of class sections a student is enrolled in (From Workday API call)
#        "shift" - the shift object we are determining whether or not the student is available for
# Return true, if the shift's start and end time is not within a student's class
# Return false if the shift has a time confliction with the student's class schedule
def availableForShift(classSchedule, shift):
    shiftDayNumber = shift["DayId"]
    if shiftDayNumber == 1:
        shiftDayLetter = "U"
    if shiftDayNumber == 2:
        shiftDayLetter = "M"
    if shiftDayNumber == 3:
        shiftDayLetter = "T"
    if shiftDayNumber == 4:
        shiftDayLetter = "W"
    if shiftDayNumber == 5:
        shiftDayLetter = "R"
    if shiftDayNumber == 6:
        shiftDayLetter = "F"
    if shiftDayNumber == 7:
        shiftDayLetter = "S"


    for course in classSchedule:
        if shiftDayLetter in course["meetingDays"]:
            courseStart = convert_to_time(course["start"])
            courseEnd = convert_to_time(course["end"])
            
            shiftStart = convert_to_time(shift["ShiftStart"])
            shiftEnd = convert_to_time(shift["ShiftEnd"])
            
            if not(shiftStart) or not(shiftEnd):
                break;

            available = (
                courseStart >= shiftEnd
                or courseEnd <= shiftStart
            )
            if not available:
                return False

    return True


#Removes shifts that the student employee is not available to work
#Params: "emptyShifts" - the list of all empty shifts for a facility
#        "shiftsToRemove" - the list of all shifts that an employee is not available to work
#Returns the new list of shifts that only the employee is available to work
def removeShifts(emptyShifts, shiftsToRemove):
    for shift in shiftsToRemove:
        if shift in emptyShifts:
            emptyShifts.remove(shift)
            
    return emptyShifts

