import os
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file


GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')  # Replace with your actual API key
SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')  # Replace with your actual spreadsheet ID
SHEET_NAME = os.getenv('SHEET_NAME')  # Replace with your actual sheet name

def get_spreadsheet_data():
    service = build('sheets', 'v4', developerKey=GOOGLE_API_KEY)
    sheet = service.spreadsheets()
    all_rows = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=SHEET_NAME).execute()['values']
    # values = result.get('values', [])
    with open('spreadsheet_data.txt') as f:
        # print(f.read())  # Read the last row count from the file
        # return
        # last_row = int(f.read())
        last_row = int(f.read())
        # print(f"Last row count from file: {last_row}")
        # return all_rows, last_row  # Return the values from the spreadsheet
    new_rows = all_rows[last_row] if last_row is not None else []  # Get the new rows added since the last check
    count_new_rows = len(new_rows)
    if count_new_rows > last_row:
        with open('spreadsheet_data.txt', 'w') as f:
            print(f"New rows added: {count_new_rows}")
            f.write(str(count_new_rows))
    return all_rows, new_rows  # Return the values from the spreadsheet


# print(get_spreadsheet_data())
data, total_rows = get_spreadsheet_data()
print(f"Total rows in the spreadsheet: {total_rows}")
print(f"Data from the spreadsheet: {data}")

with open('spreadsheet_data.txt', 'w') as f:
    f.write(str(total_rows))