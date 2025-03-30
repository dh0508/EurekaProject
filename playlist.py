import time
from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

# Spotify API 관련 설정
API_URL = "https://api.spotify.com/v1/search"
CLIENT_ID = '~~~~~~'
CLIENT_SECRET = '~~~~~~'
REDIRECT_URI = 'http://localhost:5000/callback'
TOKEN_URL = 'https://accounts.spotify.com/api/token'
AUTHORIZE_URL = 'https://accounts.spotify.com/authorize'
SCOPES = 'user-read-private user-read-email'

API_TOKEN = None
TOKEN_EXPIRATION = None

def update_token():
    """토큰이 만료되었거나 없으면 새로운 토큰을 받기 위해 인증을 요구합니다."""
    global API_TOKEN, TOKEN_EXPIRATION
    if not API_TOKEN or time.time() >= TOKEN_EXPIRATION:
        return redirect(url_for('authorize'))  # 토큰이 없거나 만료되면 인증을 요구하는 페이지로 리다이렉트
    return None  # 유효한 토큰이 있으면 None을 반환

@app.route('/')
def home():
    error = update_token()
    if error:  # error가 None이 아닐 때만 리다이렉트 처리
        return error
    return render_template('index.html')  # 토큰이 유효하면 index.html 렌더링

@app.route('/authorize')
def authorize():
    """사용자 인증 페이지로 이동"""
    auth_url = f'{AUTHORIZE_URL}?client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}&scope={SCOPES}'
    return redirect(auth_url)

@app.route('/callback')
def callback():
    code = request.args.get('code')  # URL에서 인증 코드 가져오기
    payload = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }

    response = requests.post(TOKEN_URL, data=payload)

    if response.status_code == 200:
        token_info = response.json()
        global API_TOKEN, TOKEN_EXPIRATION
        API_TOKEN = token_info['access_token']
        expires_in = token_info['expires_in']  # 토큰 유효 시간 (초)
        TOKEN_EXPIRATION = time.time() + expires_in  # 만료 시간 계산
        return redirect(url_for('home'))  # 토큰을 받은 후 홈으로 리다이렉트
    else:
        return f'Error: {response.status_code} - {response.text}'

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

@app.route('/generate', methods=['POST'])
def generate_playlist():
    keyword = request.form.get('keyword')  # 폼에서 키워드 받기
    playlist = get_playlist_by_keyword(keyword)  # 키워드로 플레이리스트 생성
    return render_template('playlist.html', keyword=keyword, playlist=playlist)

if __name__ == '__main__':
    app.run(debug=True)
