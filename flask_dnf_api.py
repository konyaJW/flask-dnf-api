import os
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

BASE_URL = "https://api.neople.co.kr/df/"
API_KEY = os.getenv("API_KEY")  # 환경 변수에서 API 키 불러오기

@app.route('/')
def home():
    return "Flask 던파 API 서버가 정상적으로 실행되었습니다!"

@app.route('/equipment', methods=['GET'])
def get_character_equipment():
    server = request.args.get('server', 'diregie')
    character_name = request.args.get('character')

    if not character_name:
        return jsonify({"error": "캐릭터명을 입력해주세요."}), 400

    character_endpoint = f"servers/{server}/characters"
    params = {"characterName": character_name, "wordType": "full", "apikey": API_KEY}

    character_response = requests.get(BASE_URL + character_endpoint, params=params)
    if character_response.status_code == 200:
        character_data = character_response.json()
        if "rows" in character_data and character_data["rows"]:
            character_id = character_data["rows"][0]["characterId"]

            equip_endpoint = f"servers/{server}/characters/{character_id}/equip/equipment"
            equip_response = requests.get(f"{BASE_URL}{equip_endpoint}?apikey={API_KEY}")

            if equip_response.status_code == 200:
                return jsonify(equip_response.json())
        return jsonify({"error": "캐릭터를 찾을 수 없습니다."}), 404
    else:
        return jsonify({"error": f"API 요청 실패: {character_response.status_code}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
