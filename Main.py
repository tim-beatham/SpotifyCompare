import sys

from Connection import SetUpSpotipy
import ClientInfo


class Game:
    def __init__(self):
        # Connect to the spotipy API
        self.spotipyObj = SetUpSpotipy(ClientInfo.SPOTIPY_CLIENT_ID,
                                       ClientInfo.SPOTIPY_CLIENT_SECRET, ClientInfo.SPOTIPY_REDIRECT_URL)

        # Get the API client in which a user does not connect to spotify.
        self.spotipyAPI = self.spotipyObj.get_spotify_api_client()

    def get_popularity_artist(self, artist_name):
        """
        Given the name of the artist it returns the popularity index of the artist.
        :param artist_name: The name of the artist which we are searching for.
        :return: The popularity (0-100) of the artist.
        """
        results = self.spotipyAPI.search(q='artist:' + artist_name, type='artist')['artists']['items']
        if len(results) == 0:
            return None
        else:
            return results[0]['popularity']

    def game_loop(self):
        """The main game loop."""
        player_1_turn = True
        finished = False

        previous_point = 0
        while not finished:
            if player_1_turn:
                user_input = input("Player 1 please enter an artist name: ")
            else:
                user_input = input("Player 2 please enter an artist name: ")

            current_point = self.get_popularity_artist(user_input)

            if current_point > previous_point:
                previous_point = current_point
                player_1_turn = not player_1_turn
                print("Popularity: " + str(current_point))
            elif current_point <= previous_point:
                print("That artist is not more popular!")
                finished = True
            else:
                print("That artist does not exist!")
                finished = True

            if finished:
                if player_1_turn:
                    print("Player 2 wins!")
                else:
                    print("Player 1 wins!")


if __name__ == '__main__':
    gameObj = Game()
    gameObj.game_loop()
