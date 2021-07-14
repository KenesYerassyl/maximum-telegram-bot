import messages
from sheets import sheet
from sheets import attendance_sheet_id as sheet_id

def check_attendance(user_id, month, day):
    try:
        result = sheet.values().get(spreadsheetId=sheet_id, range='A2:A').execute()
        values = result.get('values', [])
        needed_row = -1
        if values == None:
            return None
        for row in range(len(values)):
            if values[row] != None and len(values[row]) > 0 and values[row][0] == user_id:
                needed_row = row
                break
        if needed_row == -1:
            return None
        else:
            needed_row += 2

            user_row = sheet.values().get(spreadsheetId=sheet_id, range=f'{needed_row}:{needed_row}').execute()
            user_info = user_row.get('values', [])[0]

            general_row = sheet.values().get(spreadsheetId=sheet_id, range='1:1').execute()
            general_info = general_row.get('values', [])[0]

            #finding the start of a month
            start_index = 0
            while start_index < len(general_info):
                if general_info[start_index] == messages.MONTH_RU[month]:
                    break
                else:
                    start_index += 1
            
            index = start_index + 1

            #finding the end of a month
            while index < len(general_info) and general_info[index].isdigit():
                index += 1
            finish_index = min(len(general_info)-1, index)

            #checking the range 
            index = start_index + 1
            found = False
            while index <= finish_index:
                if general_info[index] == day:
                    found = True
                    break
                else:
                    index += 1
            return (user_info[index], user_info[1]) if found else None
    except Exception as e:
        print(f"Error in checking attendance: {e}")
        return None