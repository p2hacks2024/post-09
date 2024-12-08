import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from icecream import ic
import json
import os

# spotifyインスタンスを作成
# test
sp = spotipy.Spotify(
    auth_manager=SpotifyClientCredentials(
        client_id="f2b07462203a4302866b30693c730e0e",  # Client ID
        client_secret="df34cab6e70d4a17b2c2b2a724143a39",  # Client Secret
    )
)

track_ids = []
results = sp.search(q="LE SSERAFIM", limit=5, type="track")
# ic(results["tracks"]["items"])
for track in results["tracks"]["items"]:
    track_id = track["id"]
    track_ids.append(track_id)


# スクリプトがあるディレクトリを取得
script_dir = os.path.dirname(os.path.realpath(__file__))

# 保存先ファイルパスを設定
file_path = os.path.join(script_dir, "track_ids.json")

# JSONに保存
with open(file_path, "w") as json_file:
    json.dump(track_ids, json_file, indent=4)

print("Track IDs saved to track_ids.json")
