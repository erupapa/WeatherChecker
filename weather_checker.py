import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json
import os
from datetime import datetime, timedelta
import time
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ログ設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='weather_checker.log'
)

class RateLimiter:
    def __init__(self, max_requests: int, time_period: int):
        self.max_requests = max_requests
        self.time_period = time_period  # 秒単位
        self.requests = []
        
    def can_request(self):
        current_time = datetime.now()
        # 古いリクエストを削除
        self.requests = [req for req in self.requests 
                        if req > current_time - timedelta(seconds=self.time_period)]
        
        if len(self.requests) < self.max_requests:
            self.requests.append(current_time)
            return True
        return False

def get_weather(city_name: str):
    try:
        # APIキーを環境変数から取得
        api_key = os.getenv('OPENWEATHERMAP_API_KEY')
        if not api_key:
            return "エラー: APIキーが設定されていません。環境変数 OPENWEATHERMAP_API_KEY を設定してください。"

        # レートリミッターの設定（1分間に60リクエスト）
        limiter = RateLimiter(max_requests=60, time_period=60)
        if not limiter.can_request():
            return "エラー: リクエスト制限に達しました。1分後に再度お試しください。"

        url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric&lang=ja"
        response = requests.get(url)
        data = response.json()

        if response.status_code == 429:
            logging.warning(f"Rate limit exceeded for city: {city_name}")
            return "エラー: リクエスト制限に達しました。後で再度お試しください。"
        elif response.status_code != 200:
            logging.error(f"API error for city {city_name}: {data.get('message', '不明なエラー')}")
            return f"エラー: {data.get('message', '不明なエラー')}"

        weather = data['weather'][0]['description']
        temp = data['main']['temp']
        humidity = data['main']['humidity']
        
        logging.info(f"Successfully fetched weather for {city_name}")
        return f"{city_name}の天気: {weather}\n気温: {temp}°C\n湿度: {humidity}%"
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        return f"エラー: {str(e)}"
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric&lang=ja"
        response = requests.get(url)
        data = response.json()

        if response.status_code == 429:
            return "エラー: リクエスト制限に達しました。後で再度お試しください。"
        elif response.status_code != 200:
            return f"エラー: {data.get('message', '不明なエラー')}"

        weather = data['weather'][0]['description']
        temp = data['main']['temp']
        humidity = data['main']['humidity']
        return f"{city_name}の天気: {weather}\n気温: {temp}°C\n湿度: {humidity}%"
    except Exception as e:
        return f"エラー: {str(e)}"

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("天気チェッカー")
        self.root.geometry("400x300")
        
        # アイコン設定
        try:
            self.root.iconbitmap('weather.ico')
        except:
            pass

        # メインフレーム
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # シティ名入力
        ttk.Label(self.main_frame, text="都市名:").grid(row=0, column=0, padx=5, pady=5)
        self.city_entry = ttk.Entry(self.main_frame, width=30)
        self.city_entry.grid(row=0, column=1, padx=5, pady=5)

        # 検索ボタン
        self.search_button = ttk.Button(
            self.main_frame,
            text="天気をチェック",
            command=self.check_weather
        )
        self.search_button.grid(row=1, column=0, columnspan=2, pady=10)

        # 結果表示
        self.result_text = tk.Text(self.main_frame, height=10, width=40)
        self.result_text.grid(row=2, column=0, columnspan=2, pady=5)

    def check_weather(self):
        city_name = self.city_entry.get()
        
        if not city_name:
            messagebox.showerror("エラー", "都市名を入力してください")
            return

        result = get_weather(city_name)
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, result)

if __name__ == "__main__":
    # Test the weather function
    test_city = "Muroran"
    test_api_key = "0fb960a3b60cb76bf4a14b358a74a7fb"
    
    print("\nテスト: ムロランの天気を取得")
    result = get_weather(test_city, test_api_key)
    print(result)
    print("\nアプリケーションを開始")
    
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()
