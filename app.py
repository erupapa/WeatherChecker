from flask import Flask, render_template, request, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import os
from datetime import datetime
import logging
from dotenv import load_dotenv
import requests

# 環境変数の読み込み
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'your-secret-key-here')

# ログ設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='weather_checker.log'
)

class WeatherForm(FlaskForm):
    city = StringField('都市名', validators=[DataRequired()])
    submit = SubmitField('天気をチェック')

class RateLimiter:
    def __init__(self, max_requests: int, time_period: int):
        self.max_requests = max_requests
        self.time_period = time_period
        self.requests = []
        
    def can_request(self):
        current_time = datetime.now()
        self.requests = [req for req in self.requests 
                        if req > current_time - timedelta(seconds=self.time_period)]
        
        if len(self.requests) < self.max_requests:
            self.requests.append(current_time)
            return True
        return False

def get_weather(city_name: str):
    try:
        api_key = os.getenv('OPENWEATHERMAP_API_KEY')
        if not api_key:
            return None, "エラー: APIキーが設定されていません"

        limiter = RateLimiter(max_requests=60, time_period=60)
        if not limiter.can_request():
            return None, "エラー: リクエスト制限に達しました。1分後に再度お試しください。"

        url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric&lang=ja"
        response = requests.get(url)
        data = response.json()

        if response.status_code == 429:
            logging.warning(f"Rate limit exceeded for city: {city_name}")
            return None, "エラー: リクエスト制限に達しました。後で再度お試しください。"
        elif response.status_code != 200:
            logging.error(f"API error for city {city_name}: {data.get('message', '不明なエラー')}")
            return None, f"エラー: {data.get('message', '不明なエラー')}"

        weather = data['weather'][0]['description']
        temp = data['main']['temp']
        humidity = data['main']['humidity']
        
        logging.info(f"Successfully fetched weather for {city_name}")
        return {
            'city': city_name,
            'weather': weather,
            'temp': temp,
            'humidity': humidity,
            'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }, None
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        return None, f"エラー: {str(e)}"

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = WeatherForm()
    weather_data = None
    error = None
    
    if form.validate_on_submit():
        city = form.city.data
        weather_data, error = get_weather(city)
        
    return render_template('index.html', form=form, weather=weather_data, error=error)

@app.route('/api/weather/<city>')
def api_weather(city):
    weather_data, error = get_weather(city)
    if error:
        return jsonify({'error': error}), 400
    return jsonify(weather_data)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
