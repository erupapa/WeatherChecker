import requests

def get_weather(city_name: str, api_key: str):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric&lang=ja"
    response = requests.get(url)
    data = response.json()

    if response.status_code != 200:
        return f"エラー: {data.get('message', '不明なエラー')}"

    weather = data['weather'][0]['description']
    temp = data['main']['temp']
    humidity = data['main']['humidity']
    return f"{city_name}の天気: {weather}, 気温: {temp}°C, 湿度: {humidity}%"

if __name__ == "__main__":
    city = "Muroran"
    api_key = "0fb960a3b60cb76bf4a14b358a74a7fb"
    print(f"\n{city}の天気を取得中...")
    result = get_weather(city, api_key)
    print(f"結果: {result}")
