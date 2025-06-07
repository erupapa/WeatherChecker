# 天気チェッカー

このアプリケーションは、OpenWeatherMapのAPIを使用して指定した都市の天気情報を取得するウェブアプリケーションです。

## セットアップ

## セットアップ

### ローカル開発環境
1. 必要なパッケージをインストール:
```bash
pip install -r requirements.txt
```

2. 環境変数を設定:
```bash
setx OPENWEATHERMAP_API_KEY "あなたのAPIキー"
setx FLASK_SECRET_KEY "あなたのシークレットキー"
```

3. アプリケーションを実行:
```bash
python app.py
```

アプリケーションは http://localhost:5000 でアクセスできます。

### Herokuへのデプロイ
1. Heroku CLIをインストール
2. アプリケーションを作成:
```bash
heroku create
```

3. 環境変数を設定:
```bash
heroku config:set OPENWEATHERMAP_API_KEY="あなたのAPIキー"
heroku config:set FLASK_SECRET_KEY="あなたのシークレットキー"
```

4. デプロイ:
```bash
git push heroku main
```

デプロイが完了すると、HerokuのURLでアプリケーションにアクセスできます。

## 使用方法

1. アプリケーションを起動
2. 「都市名」に検索したい都市名を入力
3. 「天気をチェック」ボタンをクリック
4. 天気情報が表示されます

## 注意事項

- 無料プランの制限（1分間に60リクエスト）に注意してください
- APIキーは環境変数を介して安全に管理されています
- エラーログは `weather_checker.log` ファイルに保存されます
