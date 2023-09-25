import os
import pygsheets
from dotenv import load_dotenv

load_dotenv()

obj_avatar = {"name":"", "location":"", "identity":"", "partner":"", "database":"", "recording":""}

def initial_avatar(name):
    gc = pygsheets.authorize(service_file = os.getenv("GOOGLE_SHEET_API_KEY_FILE"))
    sht = gc.open_by_url(os.getenv("SHEET"))
    wks_list = sht.worksheets()

    wks = sht[0]
    data_column_A = wks.get_col(1, include_tailing_empty=False)[1:]

    # Get identity
    row_index = 2
    for obj in data_column_A:
      if (obj == name):
        obj_avatar["name"] = name
        break
      row_index = row_index + 1

    # get profile
    row_values = wks.get_row(row_index)
    obj_avatar["location"] = row_values[1]
    obj_avatar["identity"] = row_values[2]
    obj_avatar["partner"] = row_values[3]
    obj_avatar["database"] = row_values[4]
    obj_avatar["recording"] = row_values[5]

    if (obj_avatar["name"] == ""):
        return None
    else:
        return obj_avatar
