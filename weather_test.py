import requests
import json

# APIキーと都市名を設定
api_key = "0fb960a3b60cb76bf4a14b358a74a7fb"
city = "Muroran"

# APIリクエストを構築
url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=ja"

try:
    # リクエストを送信
    response = requests.get(url)
    
    # レスポンスをJSONとして解析
    data = response.json()
    
    # レスポンスコードを確認
    if response.status_code == 200:
        # 天気情報を取得
        weather = data['weather'][0]['description']
        temp = data['main']['temp']
        humidity = data['main']['humidity']
        
        # 結果を表示
        print(f"\n{city}の天気情報:")
        print(f"天気: {weather}")
        print(f"気温: {temp}°C")
        print(f"湿度: {humidity}%")
    else:
        print(f"エラー: {data.get('message', '不明なエラー')}")
        print(f"ステータスコード: {response.status_code}")
        print(f"詳細: {json.dumps(data, indent=2, ensure_ascii=False)}")

except Exception as e:
    print(f"エラーが発生しました: {str(e)}")
