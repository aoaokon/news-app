from flask import Flask, render_template, request
import requests

# Flaskアプリケーションを初期化
app = Flask(__name__)

# GNews APIの基本設定
API_KEY = "YOUR_API_KEY_HERE"
URL = "https://gnews.io/api/v4/search"


@app.route('/', methods=['GET'])
def index():
    # フォームからキーワード取得（なければデフォルト値）
    keyword = request.args.get('q', 'スポーツ')
    lang = request.args.get('lang', 'ja')  # 言語パラメータを取得（デフォルト:日本語）
    params = {
        'q': keyword,
        'lang': lang,
        'max': 10,
        'apikey': API_KEY
    }

    remaining = None
    try:
        response = requests.get(URL, params=params)
        print("--- 実際にリクエストしたURL ---")
        print(response.url)
        print("-----------------------------")
        response.raise_for_status()
        data = response.json()
        print("--- APIからの返り値 ---")
        print(data)
        print("----------------------")
        articles = data.get("articles", [])
        remaining = response.headers.get("X-RateLimit-Remaining")
    except requests.exceptions.RequestException as e:
        print(f"エラーが発生しました: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print("レスポンス内容:", e.response.text)
        articles = []

    return render_template('index.html', articles=articles, keyword=keyword, remaining=remaining, lang=lang)

if __name__ == '__main__':
    app.run(debug=True) # デバッグモードでアプリを実行