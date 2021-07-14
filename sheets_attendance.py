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

            month_index = 0
            while month_index < len(general_info):
                if general_info[month_index] == messages.MONTH_RU[month]:
                    break
                else:
                    month_index += 1
            index = month_index + 1
            while index < len(general_info):
                if general_info[index] == day:
                    break
                else:
                    index += 1
            return (user_info[index], user_info[1])
    except Exception as e:
        print(f"Error in checking attendance: {e}")
        return None

# result = sheet.values().get(spreadsheetId=sheet_id, range='1:1').execute()
# print(result)