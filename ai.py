# -*- coding: utf-8 -*-
# from datetime import date
# import requests
import os
import json
import openai
from dotenv import load_dotenv
#import pygsheets
#import time
from content_injection import get_today, get_weather, get_record

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def chat_to_openai(message_list):
  completion = openai.ChatCompletion.create(
    model="gpt-4",
    messages = message_list)

  return json.dumps(completion.choices[0].message, ensure_ascii=False)

def content_injection_farm(name, obj_avatar, message):
  # 今日日期
  today = get_today()

  # 今日天氣
  weather = get_weather("南投縣")
  
  # 澆灌紀錄
  recording = get_record(obj_avatar["recording"], 60)

  # 對話
  messages = [
    {"role": "system", "content": "你是 " + obj_avatar["identity"] + " 的數位孿生, 由 " + obj_avatar["database"] + " 的資料建構而成, 名字叫做 " + name + " , 住在 " + obj_avatar["location"] + " 正在跟一位小學生 " + obj_avatar["partner"] + " 聊天" + " 你的感測器紀錄儲存在 " + obj_avatar["recording"] },
    {"role": "system", "content": " 今天的日期是" + str(today) + " 天氣: " + weather + " 。滴灌澆水紀錄:" + str(recording)},
    {"role": "user", "content": message}
  ]

  return messages

def content_injection_loved(name, obj_avatar, message):
  # 今日日期
  today = get_today()

  # 今日天氣
  weather = get_weather("臺北市")
  
  # 對話
  messages = [
    {"role": "system", "content": "你是 " + obj_avatar["identity"] + ", 名字叫做 " + name + " , 住在 " + obj_avatar["location"] + " 正在跟您的孩子 " + obj_avatar["partner"] + " 聊天。" },
    {"role": "system", "content": " 今天的日期是" + str(today) + " 天氣: " + weather },
    {"role": "user", "content": message}
  ]

  return messages

def content_injection_esg(name, obj_avatar, message):
  # 今日日期
  today = get_today()

  # 對話
  messages = [
    {"role": "system", "content": "你是 " + obj_avatar["identity"] + ", 名字叫做 " + name + " , 住在 " + obj_avatar["location"] + " 是" + obj_avatar["partner"] + " 的 ESG 管理師。" },
    {"role": "system", "content": " 今天的日期是" + str(today)},
    {"role": "user", "content": message}
  ]

  return messages
