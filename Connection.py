import spotipy
import spotipy.util as util
import sys
from spotipy.oauth2 import SpotifyClientCredentials


class SetUpSpotipy:
    """Sets up the connections to the API."""

    def __init__(self, client_id, client_secret, redirect_url=None, username=None, scope=None):
        """
        Sets the environment variables and user information.
        :param client_id: The client ID this is found in the Spotify API reference.
        :param client_secret: The client secret is found in the Spotify API reference.
        :param redirect_url: What page to visit when the user has logged in. This is optional.
        :param username: The username of the user who wants to login. This is optional
        :param scope: The scope in which we are to access the user's information.
        """
        self.SPOTIPY_CLIENT_ID = client_id
        self.SPOTIPY_CLIENT_SECRET = client_secret

        if redirect_url:
            self.SPOTIPY_REDIRECT_URL = redirect_url

        if username:
            self.username = username

        if scope:
            self.scope = scope

    def get_spotify_api_client(self):
        """
        Sets up the connection to the API.
        :return: The Spotify API client.
        """
        return spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(self.SPOTIPY_CLIENT_ID,
                                                                                   self.SPOTIPY_CLIENT_SECRET))

    def get_spotify_api_user(self):
        """
        Sets up the connection to the API using the user's information.
        :return: The Spotify API client. None if the information has not been passed.
        """
        if self.SPOTIPY_REDIRECT_URL and self.username and self.scope:
            token = util.prompt_for_user_token(self.username, self.scope, self.SPOTIPY_CLIENT_ID,
                                               self.SPOTIPY_CLIENT_SECRET, self.SPOTIPY_REDIRECT_URL)
            return spotipy.Spotify(auth=token)

        else:
            return None


