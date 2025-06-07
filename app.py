from flask import Flask, request, jsonify
from weather_checker import WeatherChecker

app = Flask(__name__)

# APIキーを設定
API_KEY = "0fb960a3b60cb76bf4a14b358a74a7fb"

# WeatherCheckerインスタンスを作成
checker = WeatherChecker(API_KEY)

@app.route('/weather/<city>', methods=['GET'])
def get_weather(city):
    weather_info = checker.get_weather(city)
    return jsonify({"city": city, "weather": weather_info})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
