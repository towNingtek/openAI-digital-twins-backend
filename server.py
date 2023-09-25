import os
import json
from flask import Flask, request, jsonify, abort
from flask_cors import CORS
from avatar import initial_avatar
from dotenv import load_dotenv
from gsheet import get_all_avatar

from ai import chat_to_openai, content_injection_farm, content_injection_loved, content_injection_esg

load_dotenv()

app = Flask(__name__)
CORS(app)  # 在應用程式上啟用 CORS

@app.route('/get_avatar', methods=['GET', 'POST'])
def get_avatar():
    if request.method == 'POST':
        # 處理 POST 請求
        data = request.json  # 假設請求的資料是 JSON 格式
        if (data["api_key"] != os.getenv("API_KEY")):
            abort(403, description = "Permission denied")

        # 從 G-Sheet 上獲取側寫
        obj_avatar = initial_avatar(data["name"])

        # 在這裡進行 POST 資料的處理，然後回應適當的資料
        return jsonify(obj_avatar)

    # Get avatar
    return jsonify(obj_avatar)

@app.route('/list_avatar', methods=['GET', 'POST'])
def list_avatar():
    if request.method == 'POST':
        # 處理 POST 請求
        data = request.json  # 假設請求的資料是 JSON 格式

        # 從 G-Sheet 上獲取側寫
        list_avatars = get_all_avatar()

    # Get avatar
    return jsonify({"status":True, "avatar":list_avatars})

@app.route('/chat_to_avatar', methods=['GET', 'POST'])
def chat_to_avatar():
    if request.method == 'POST':
        # 處理 POST 請求
        data = request.json  # 假設請求的資料是 JSON 格式
        if (data["api_key"] != os.getenv("API_KEY")):
            abort(403, description = "Permission denied")

        # Content injection
        # 從 G-Sheet 上獲取側寫
        obj_avatar = initial_avatar(data["name"])

        messages = None
        if obj_avatar["database"] == "滴灌感測器":
            messages = content_injection_farm(data["name"], obj_avatar, data["message"])
        elif obj_avatar["database"] == "親人":
            messages = content_injection_loved(data["name"], obj_avatar, data["message"])
        elif obj_avatar["database"] == "ESG管理師":
            messages = content_injection_esg(data["name"], obj_avatar, data["message"])
        else:
            messages = [ {"role": "user", "content": data["message"]} ]

        # Chat to ai
        response = chat_to_openai(messages)

    return jsonify({"status":"OK", "message":response})

if __name__ == '__main__':
    app.run(debug = True, port = 7628)
