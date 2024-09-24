from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# 음악 API 사용 (여기서는 예시로 Spotify API를 사용)
API_URL = "https://api.spotify.com/v1/search"
API_TOKEN = "BQDnZLSsoqpmO0IVLm37UOJpbDlc6V2WFlbY70NKYlr0MNgAIlK-2dJvc0-tZmXzTzi0iYpCGurJrFgSnU6SVFh5iZ3uxxIyt5RsyGeiN2aTfQNb6awpHw2FT2AhHx7VqBv1UkQre71IiIoTV19056oA812pQqvdcFlQuZfO-iTDndTaDhj8HKVtsKJ-CywaxFFQaQkeE7WFqDpWSu60VCSKFYMpE5I9w7Ih5veSy5Uhfat04GrxDro7Qeb91pBExD1pZJzp7OXqrWt68vFB0JDI2tFA_SRv8YVN9_UOT26pbyP8OdcS5n9a-MbdKzEGJavvAPyLQ8-5ehCuQd98cK0p9uSC3JpIMoo"  # Spotify API 토큰 입력


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


if __name__ == '__main__':
    app.run(debug=True)