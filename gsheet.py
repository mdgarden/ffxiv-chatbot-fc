import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = [
'https://spreadsheets.google.com/feeds',
'https://www.googleapis.com/auth/drive',
]
json_file_name = 'fc-chatbot-298206-0f1e9c108c8b.json'

credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file_name, scope)
gc = gspread.authorize(credentials)

spreadsheet_url = 'https://docs.google.com/spreadsheets/d/13PHjRMsNZDmLISZeglFW7sqSuWHnc9UXf4Bndwu5HTY/edit#gid=0'

# 스프레드 시트 문서 가져오기 
doc = gc.open_by_url(spreadsheet_url)

# 시트 선택하기
worksheet = doc.worksheet('시트1')

cell_data = worksheet.acell('B3').value
print(cell_data)