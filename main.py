from PyQt6.QtWidgets import QApplication

from threading import Thread

from gui.gui import MainWindow
from twitchbot.bot import Bot
from sensorinterface import ArduinoComm

def tb():
    bot = Bot()
    bot.run()

if __name__ == "__main__":
    tb_thread = Thread(target=tb)
    tb_thread.run()