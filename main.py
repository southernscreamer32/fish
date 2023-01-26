from PyQt6.QtWidgets import QApplication

from threading import Thread
from multiprocessing import Process

from gui.gui import MainWindow
from twitchbot.bot import Bot
from sensorinterface import ArduinoComm

def tb():
    # global bot
    bot = Bot()
    bot.run()

def comms():
    # global ac
    ac = ArduinoComm()

    # while True:
    #     window.display.info.tds.update_value(ac.tds)
    #     window.display.info.ph.update_value(ac.pH)
    #     window.display.info.weight.update_value(ac.weight)

if __name__ == "__main__":
    app = QApplication([])

    window = MainWindow()
    window.show()

    tb_thread = Process(target=tb)
    tb_thread.run()

    comms_thread = Thread(target=comms)
    comms_thread.start()

    app.exec()

