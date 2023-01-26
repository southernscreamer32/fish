from PyQt6.QtWidgets import QApplication

from threading import Thread
from multiprocessing import Process

from gui.gui import MainWindow
from twitchbot.bot import Bot
from sensorinterface import ArduinoComm

import openai
from twitchbot.config import OPEN_AI_KEY

def tb():
    openai.api_key = OPEN_AI_KEY

    global bot

    bot = Bot()
    bot.run()


def comms():
    ac = ArduinoComm()

    while True:
        window.display.info.tds.update_value(ac.tds)
        window.display.info.ph.update_value(round(ac.pH, 2))
        window.display.info.weight.update_value(ac.weight)

        if bot.activate_feed:
            bot.activate_feed = False
            ac.feed_num(2)

if __name__ == "__main__":
    app = QApplication([])

    window = MainWindow()

    tb_thread = Process(target=tb)
    tb_thread.start()

    comms_thread = Thread(target=comms)
    comms_thread.start()

    window.show()
    app.exec()

