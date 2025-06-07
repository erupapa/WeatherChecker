import requests
import time
from datetime import datetime

class WeatherChecker:
    def __init__(self, api_key):
        self.api_key = api_key
        self.requests_count = 0
        self.last_request_time = None
        self.max_requests_per_minute = 60  # 1分間に最大60リクエスト
        
    def get_weather(self, city_name: str):
        # 最後のリクエストからの経過時間を計算
        current_time = time.time()
        if self.last_request_time:
            elapsed_time = current_time - self.last_request_time
            
            # 1分未満の場合、リクエスト数をチェック
            if elapsed_time < 60:
                if self.requests_count >= self.max_requests_per_minute:
                    remaining_time = 60 - elapsed_time
                    return f"エラー: 利用制限に達しました。{remaining_time:.0f}秒後に再度お試しください。"
            else:
                # 1分以上経過した場合はリクエスト数をリセット
                self.requests_count = 0
                
        # リクエスト数を増加
        self.requests_count += 1
        self.last_request_time = current_time
        
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={self.api_key}&units=metric&lang=ja"
        response = requests.get(url)
        data = response.json()

        if response.status_code != 200:
            return f"エラー: {data.get('message', '不明なエラー')}"

        weather = data['weather'][0]['description']
        temp = data['main']['temp']
        humidity = data['main']['humidity']
        
        return f"{city_name}の天気: {weather}, 気温: {temp}°C, 湿度: {humidity}%"

if __name__ == "__main__":
    # APIキーを設定
    API_KEY = "0fb960a3b60cb76bf4a14b358a74a7fb"
    
    # WeatherCheckerインスタンスを作成
    checker = WeatherChecker(API_KEY)
    
    # テスト用の都市名
    cities = ["Tokyo", "Osaka", "Nagoya"]
    
    try:
        for city in cities:
            weather_info = checker.get_weather(city)
            print(f"\n{city}の天気情報:")
            print(weather_info)
            
            # 1秒間隔でリクエストを送信
            time.sleep(1)
    except Exception as e:
        print(f"エラーが発生しました: {str(e)}")
