from dotenv import load_dotenv
import os
from langchain.tools.base import BaseTool
import spotipy  # pyright: ignore
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import json

# .envファイルの読み込み
load_dotenv()


# 環境変数を取得
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

if not SPOTIFY_CLIENT_ID:
    raise ValueError(
        "SPOTIFY_CLIENT_ID is not set in the .env file or environment variables."
    )
if not SPOTIFY_CLIENT_SECRET:
    raise ValueError(
        "SPOTIFY_CLIENT_SECRET is not set in the .env file or environment variables."
    )

token = "AQAuE_VNB_2l9y-te-X5Ox0oaFczaZ7m5SPLYu34WU-lNQZjDkkfPhpTiVrQdsxxkcQU76-7Rmr0SgSETIPFOEaSNZLmZRU7A7Iau5KO5wNqOF-HuLi59BSDtOHwgbKZGMqWTc71NEzAZbYfRoeKfHGDnJmJgYq87LFXDmDmo_u8w04ghLgXaM60RWVXQDk9xglCiw"


class SpotifyTool(BaseTool):
    """Tool that fetches audio features of saved tracks from Spotify."""

    name: str = "SpotifyTool"
    description: str = (
        "A tool that fetches audio features of the most recently saved tracks from Spotify."
        "This tool does not require any arguments."
    )

    def _run(self, *args, **kwargs) -> str:
        # Spotify認証オブジェクトを作成
        sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                client_id=SPOTIFY_CLIENT_ID,
                client_secret=SPOTIFY_CLIENT_SECRET,
                redirect_uri="http://localhost:8888/callback",
                scope="user-top-read user-library-read user-read-playback-state playlist-read-private user-read-recently-played playlist-read-collaborative playlist-modify-public playlist-modify-private",
            )
        )
        result = sp.current_user_saved_tracks(limit=10)

        # 仮定: result['items'] はトラックのリスト
        tracks = [item["track"]["id"] for item in result["items"]]
        # # 各トラックのオーディオ特性を取得
        # audio_features_list = [sp.audio_features(track)[0] for track in tracks]

        # # uriとtrack_hrefを削除
        # for features in audio_features_list:
        #     if "uri" in features:
        #         del features["uri"]
        #     if "track_href" in features:
        #         del features["track_href"]
        #     if "analysis_url" in features:
        #         del features["analysis_url"]

        print(tracks[0])
        audio_feature = sp.audio_features("4qalTfgOn1uj22GqC1jQXz")

        # JSON形式に変換
        audio_features_json = json.dumps(audio_feature)
        print(audio_features_json)
        return  # audio_features_json

    async def _arun(self, *args, **kwargs) -> str:
        """Use the SpotifyTool asynchronously."""
        return self._run()


foo = SpotifyTool()
print(foo._run())
