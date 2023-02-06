#PyQt6 is GPL 3
from PyQt6.QtWidgets import QApplication

from threading import Thread
from multiprocessing import Process

from gui.gui import MainWindow
from twitchbot.bot import Bot
from sensorinterface import ArduinoComm

from config import *

from time import sleep

def tb():
    # # global bot
    bot = Bot()
    bot.run()

def comms():
    ac = ArduinoComm()

    while True:
        window.display.info.tds.update_value(ac.tds)
        window.display.info.ph.update_value(round(ac.pH, 2))
        window.display.info.weight.update_value(round(ac.weight,2))

        with open("twitchbot/feed", "r+") as f:
            if int(f.readlines()[0]) == 1:
                f.seek(0)
                f.truncate(0)

                f.write("0")

                ac.feed_num(2)

                print("feed activated")

        sleep(0.1)
        

if __name__ == "__main__":

    print("Code available at https://github.com/goldspaghetti/fish")

    app = QApplication([])

    window = MainWindow()

    # tts = TextToSpeech()


    tb_thread = Process(target=tb)
    tb_thread.start()

    comms_thread = Thread(target=comms)
    comms_thread.start()

    window.show()
    app.exec()

