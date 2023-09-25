import os
import pygsheets
from dotenv import load_dotenv

load_dotenv()

def get_all_avatar():
    list_avatar = []
    gc = pygsheets.authorize(service_file = os.getenv("GOOGLE_SHEET_API_KEY_FILE"))
    sht = gc.open_by_url(os.getenv("SHEET"))
    wks_list = sht.worksheets()

    wks = sht[0]
    data_column_A = wks.get_col(1, include_tailing_empty=False)[1:]

    # Get identity
    row_index = 2
    for obj in data_column_A:
        list_avatar.append(obj)

    return list_avatar
