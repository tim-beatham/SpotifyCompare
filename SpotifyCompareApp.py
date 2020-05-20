from PyQt5 import QtWidgets, QtCore, QtGui
import urllib.request  # For opening and reading URLs

from Main import Game


class App(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.team_one = True
        self.popularity = 0

        self.setFixedSize(1000, 1000)
        self.layout = QtWidgets.QVBoxLayout()

        url = "https://i.scdn.co/image/0561b59a91a5e904ad2d192747715688d5f05012"
        data = urllib.request.urlopen(url).read()

        image = QtGui.QImage()
        image.loadFromData(data)

        self.image_label = QtWidgets.QLabel(self)
        self.layout.addWidget(self.image_label, alignment=QtCore.Qt.AlignCenter)

        self.popularity_label = QtWidgets.QLabel(self)
        self.layout.addWidget(self.popularity_label, alignment=QtCore.Qt.AlignCenter)

        self.team_won_label = QtWidgets.QLabel(self)
        self.layout.addWidget(self.team_won_label, alignment=QtCore.Qt.AlignCenter)

        self.team_label = QtWidgets.QLabel(self)
        self.layout.addWidget(self.team_label, alignment=QtCore.Qt.AlignCenter)

        self.text_box = ArtistTextArea(self)
        self.layout.addWidget(self.text_box)

        self.set_popularity_label(self.popularity)

        self.setLayout(self.layout)
        self.setWindowTitle("Spotify Popularity")
        self.show()

    def change_image(self, image):
        self.image_label.setPixmap(QtGui.QPixmap(image))
        self.image_label.setFixedSize(image.width(), image.height())
        self.image_label.setAlignment(QtCore.Qt.AlignCenter)

    def change_team(self):
        self.team_one = not self.team_one

        if self.team_one:
            self.team_label.setText("Team 1 Turn")
        else:
            self.team_label.setText("Team 2 Turn")

    def set_popularity_label(self, popularity):
        self.popularity = popularity
        self.popularity_label.setText("Popularity: " + str(popularity))

    def game_over(self):

        if self.team_one:
            self.team_won_label.setText("Team 2 has won!")
        else:
            self.team_label.setText("Team 1 has won!")

        self.team_one = True
        self.set_popularity(0)


    def get_popularity(self):
        return self.popularity

    def set_popularity(self, popularity):
        self.popularity = popularity


class ArtistTextArea(QtWidgets.QLineEdit):
    def __init__(self, parent):
        super().__init__(parent=parent)

        self.game = Game()

    def keyPressEvent(self, key_event):
        if key_event.key() == QtCore.Qt.Key_Return:
            artist = self.text()
            image = self.game.get_artist_image(artist)
            self.setText("")
            self.parent().change_image(image)

            # Retrieve the popularity score
            popularity = self.game.get_popularity_artist(artist)

            if popularity:
                if popularity > self.parent().get_popularity():
                    self.parent().set_popularity_label(popularity)
                    self.parent().change_team()
                else:
                    self.parent().set_popularity_label(popularity)
                    self.parent().game_over()

            else:
                self.parent().game_over()
                self.parent().set_popularity_label(0)





        else:
            super().keyPressEvent(key_event)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = App()

    app.exec_()
