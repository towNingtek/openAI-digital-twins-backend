from datetime import date
import requests
from dotenv import load_dotenv
import pygsheets
import os

def get_today():
  # 今日日期
  today = date.today()
  
  return today

def get_weather(location):
  weather = ""
  # url = "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=rdec-key-123-45678-011121314"
  url = "https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=rdec-key-123-45678-011121314"
  response = requests.get(url)
  if response.status_code == 200:
      data = response.json()
      list_location = data['records']['location']
      for obj in list_location:
          if obj['locationName'] == location:
              weather = weather + "早上:" + obj['weatherElement'][0]['time'][0]['parameter']['parameterName']
              weather = weather + "氣溫:" + obj['weatherElement'][2]['time'][0]['parameter']['parameterName'] + "-" + \
                      obj['weatherElement'][1]['time'][0]['parameter']['parameterName'] + " C, " + \
                      obj['weatherElement'][3]['time'][0]['parameter']['parameterName']
              weather = weather + "下午:" + obj['weatherElement'][0]['time'][1]['parameter']['parameterName']
              weather = weather + "氣溫:" + obj['weatherElement'][2]['time'][1]['parameter']['parameterName'] + "-" + \
                      obj['weatherElement'][1]['time'][1]['parameter']['parameterName'] + " C, " + \
                      obj['weatherElement'][3]['time'][1]['parameter']['parameterName']
              weather = weather + "晚上:" + obj['weatherElement'][0]['time'][2]['parameter']['parameterName']
              weather = weather + "氣溫:" + obj['weatherElement'][2]['time'][2]['parameter']['parameterName'] + "-" + \
                      obj['weatherElement'][1]['time'][2]['parameter']['parameterName'] + " C, " + \
                      obj['weatherElement'][3]['time'][2]['parameter']['parameterName']

  return weather

def get_record(recording, size):
  gc = pygsheets.authorize(service_file=os.getenv("GOOGLE_SHEET_API_KEY_FILE"))
  sht = gc.open_by_url(recording)
  worksheet = sht.sheet1
  # 讀取工作表的資料，最後的 2~60 筆資料
  num_rows_to_read = size
  all_values = worksheet.get_all_values(include_tailing_empty=False)
  column_a = worksheet.get_col(1, include_tailing_empty=False)

  # 获取最后一个非空值的行索引
  last_non_empty_row_index = len(column_a)

  if last_non_empty_row_index - 2 > num_rows_to_read:
      recording = [{"date": row[0], "value": row[1]} for row in all_values[last_non_empty_row_index-num_rows_to_read:last_non_empty_row_index]]
  else:
      recording = [{"date": row[0], "value": row[1]} for row in all_values[2:last_non_empty_row_index]]

  return recording
