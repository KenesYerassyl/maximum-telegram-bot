import messages
from sheets import sheet
from sheets import attendance_sheet_id as sheet_id

def check_attendance(user_id, month):
    try:
        result = sheet.values().get(spreadsheetId=sheet_id, range=f'{messages.MONTH_RU[month]}!A2:A').execute()
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
            result1 = sheet.values().get(spreadsheetId=sheet_id, range=f'{messages.MONTH_RU[month]}!{needed_row}:{needed_row}').execute()
            user_info = result1.get('values', [])[0]
            return user_info
    except Exception as e:
        print(f"Error in checking attendance: {e}")
        return None
