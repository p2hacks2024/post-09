from dotenv import load_dotenv
import spotipy  # pyright: ignore
from spotipy.oauth2 import SpotifyClientCredentials  # pyright: ignore
import json  # pyright: ignore
import os
from typing import List
from models.activity import Music
import icecream as ic  # pyright: ignore


def get_music_id(query: str) -> List[Music]:  # pyright: ignore
    # 環境変数を取得
    SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
    SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

    # spotifyインスタンスを作成
    sp = spotipy.Spotify(
        auth_manager=SpotifyClientCredentials(
            client_id=SPOTIFY_CLIENT_ID,  # Client ID
            client_secret=SPOTIFY_CLIENT_SECRET,  # Client Secret
        )
    )

    musics: List[Music] = []
    results = sp.search(q=query, limit=5, type="track")  # pyright: ignore
    for track in results["tracks"]["items"]:  # pyright: ignore
        track_name = str(track["name"])  # pyright: ignore
        track_id = str(track["id"])  # pyright: ignore
        album_id = str(track["album"]["id"])  # pyright: ignore
        popularity = int(track["popularity"])  # pyright: ignore
        musics.append(
            Music(
                track_name=track_name,
                track_id=track_id,
                album_id=album_id,
                popularity=popularity,
            )
        )
    return musics

    # # スクリプトがあるディレクトリを取得
    # script_dir = os.path.dirname(os.path.realpath(__file__))

    # # 保存先ファイルパスを設定
    # file_path = os.path.join(script_dir, "track_ids.json")

    # # JSONに保存
    # with open(file_path, "w") as json_file:
    #     json.dump(track_ids, json_file, indent=4)

    # print("Track IDs saved to track_ids.json")
