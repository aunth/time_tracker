import time
import sqlite3

def calculate_day(start, end):
    day_start = start.split()[2]
    day_end = end.split()[2]
    return int(day_end) - int(day_start)

def calculate_hours(start, end):
    hours_start = int(start.split()[3].split(':')[0])
    hours_end = int(end.split()[3].split(':')[0])
    if hours_end - hours_start < 0:
        return (24 - hours_start) + hours_end
    return hours_end - hours_start

def calculate_minute(start, end):
    minute_start = int(start.split()[3].split(':')[1])
    minute_end = int(end.split()[3].split(':')[1])
    if minute_end - minute_start < 0:
        return [-1, (60+minute_end) - minute_start]
    return [0, minute_end - minute_start]

def calculate_second(start, end):
    second_start = int(start.split()[3].split(':')[2])
    second_end = int(end.split()[3].split(':')[2])
    if second_end - second_start < 0:
        return [-1, (60+second_end) - second_start]
    return [0, second_end - second_start]

def calculate():
    global con
    global cursor
    global id_list
    global user_info
    time_start = user_info["start_time"]
    time_end = user_info["end_time"]
    time_in_day = calculate_day(time_start, time_end)
    time_in_hours = calculate_hours(time_start, time_end)
    time_in_minute = calculate_minute(time_start, time_end)# return a list lenght of 2 and list[0] represent amount of time which you should minus of last value and list[1] represent amount of minute 
    time_in_second = calculate_second(time_start, time_end)# return a list lenght of 2 and list[0] represent amount of time which you should minus of last value and list[1] represent amount of second
    return (f"You spend {str(time_in_day) + ' day ' if time_in_day > 0 else ''}" + 
    f"{(str(time_in_hours+time_in_minute[0]) + ' hours ') if time_in_hours+time_in_minute[0] > 0 else ''}" + 
    f"{(str(time_in_minute[1]+time_in_second[0]) + ' minute ') if time_in_minute[1]+time_in_second[0] > 0 else ''}" + 
    f"{str(time_in_second[1]) + ' second ' if time_in_second[1] > 0 else '1 second'}") 
    
def main_variable(id):
    global user_info
    global con
    global cursor
    global id_list
    user_info = {}
    user_info['start_time'] = user_info['end_time'] = 0
    id_list = []
    user_info['user_id'] = id
    con = sqlite3.connect("db/database.db", check_same_thread=False)
    cursor = con.cursor()

def clock_on():
    global cursor
    global id_list
    global user_info
    try:
        cursor.execute("SELECT total FROM user_info WHERE user_id=?", (user_info['user_id'], ))
    except:
        return "Last track don't stop. Stop it and try again"
    else:
        user_info['start_time'] = time.asctime()
        id_list.append(user_info["user_id"])
    
    
def clock_off():  
    global user_info
    global id_list
    global cursor
    if user_info["start_time"] != 0:   
        if user_info["user_id"]:
            user_info['end_time'] = time.asctime()
            total = calculate()
            cursor.execute("INSERT INTO user_info values (?, ?, ?, ?)", (user_info['user_id'], user_info['start_time'], user_info['end_time'], total))
            return "You are not tracked. Click on 'Check worked hours'"
        else:
            return "You wasn't tracked. Click on 'start tracking' please"
    else:
        return 'First you should click on "start tracking"'

def check_worked_hours():
    global con
    global id_list
    global cursor
    global user_info
    try:
        if len(id_list) != 0:
            cursor.execute("SELECT total FROM user_info WHERE user_id = ?", (user_info['user_id'], ))
            total = cursor.fetchall()[-1]
            con.commit()
        else:
            total = "First you should write something in database"
        return total
    except NameError:
        return "First you should write "


def check_worked_periods():
    global con
    global cursor
    result = ""
    try:
        cursor.execute("SELECT * FROM user_info WHERE user_id = ?", (user_info["user_id"],))
        all_periods = cursor.fetchall()
        if len(all_periods) > 0:
            for j, i in enumerate(all_periods):
                result += f"{j+1}. start: {i[1].split()[3]} end: {i[2].split()[3]}. {i[-1]}"+'\n'
            con.commit()
        else:
            result = "Database is empty. Click on 'start tracked' "
        return result
    except NameError:
        return "Database is empty. Click on 'start tracked'"

def clean_table():
    global cursor
    global con
    global id_list
    try:
        cursor.execute("DELETE FROM user_info WHERE user_id = ?", (user_info["user_id"], ))
        id_list = []
        con.commit()
        return "All data was deleted"
    except NameError:
        return "First you should write data in database"
    
    
