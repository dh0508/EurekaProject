
from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_URL = "https://api.spotify.com/v1/search"
API_TOKEN = "BQBuh4Ih_MjIEvvtLaGJiaxjFUKEmnruwM9J3mrBa2DwQu6-rF0PZ3gg7vxdxHCrbE7-M33Rz0nqaz1ykWTVUNTPGT4zywhOFj7xd2QBO9MAPHgTZZ2eABgGHufByW5IdngnV0-QYUANzHtHJLJOemnaw4v4YpIhtj0qeaENDG41VQ6OkbxGZ8AhIR0KE6rxGMihWLIjZt8PIk9U44Ned0ov2QXCMw"  # Spotify API 토큰을 여기에 입력
#https://accounts.spotify.com/authorize?client_id=1e76dbac870f405bb430db9497177721&response_type=code&redirect_uri=http://localhost:5000/callback&scope=user-read-private%20user-read-email


def get_playlist_by_keyword(keyword):
    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }
    params = {
        "q": keyword,
        "type": "track",
        "limit": 10
    }
    response = requests.get(API_URL, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        tracks = data['tracks']['items']
        return [{
            'title': track['name'],
            'artist': track['artists'][0]['name'],
            'url': track['external_urls']['spotify']
        } for track in tracks]
    else:
        return []


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/generate', methods=['POST'])
def generate_playlist():
    keyword = request.form['keyword']
    playlist = get_playlist_by_keyword(keyword)
    return render_template('playlist.html', keyword=keyword, playlist=playlist)


@app.route('/callback')  # 인증 코드 처리를 위한 라우트
def callback():
    code = request.args.get('code')  # URL에서 인증 코드 가져오기
    token_url = 'https://accounts.spotify.com/api/token'
    payload = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': 'http://localhost:5000/callback',  # 등록한 리디렉션 URI
        'client_id': '1e76dbac870f405bb430db9497177721',  # 클라이언트 ID 입력
        'client_secret': '3bac78039a454d7cbb5aac63a711713e'  # 클라이언트 시크릿 입력
    }

    response = requests.post(token_url, data=payload)

    if response.status_code == 200:
        token_info = response.json()
        access_token = token_info['access_token']
        return f'Access Token: {access_token}'  # 액세스 토큰을 화면에 표시합니다.
    else:
        return f'Error: {response.status_code} - {response.text}'


if __name__ == '__main__':
    app.run(debug=True)  # Flask 서버를 실행합니다.
