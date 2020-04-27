import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/spreadsheets",
"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)

client = gspread.authorize(creds)

sheet = client.open("matches").sheet1

data = sheet.get_all_records()
headers = data.pop(0)
# print(data[0])

# sheetsdataframe = pd.DataFrame(data, columns=headers)
# print(df.head())