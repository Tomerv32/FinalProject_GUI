import sys, os
sys.path.append('./EMOTIVcortex/')   # Add Cortex API subfolder to path
import EMOTIVcortex.record
from PyQt5.QtWidgets import QApplication, QLabel, QGridLayout, QWidget, QPushButton, QDesktopWidget
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import threading

# noconsole when done
# pyinstaller -i img/ico.ico  --name LearningGUI --onefile --hidden-import websocket --hidden-import json --hidden-import pydispatch --add-data "EMOTIVcortex/*.py;." gui.py

# currently:
# can only record once in every window (on purpose)
# error recording sometimes - headset connects and disconnect..


def threaded_func():
    # fix printing here!
    curr_direc = BeginTrainWindow.directions[BeginTrainWindow.curr_ind]
    # Turn off printing
    print_done = True
    print(f"Start recording {curr_direc}")
    # sys.stdout = open(os.devnull, 'w')
    try:
        print("Trying to connect")
        EMOTIVcortex.record.get_record(f"{full_name}_{curr_direc}", f"{curr_direc}", f"{path}{curr_direc}/", record_length)
    except:
        # sys.stdout = sys.__stdout__
        print(f"Error recording {curr_direc}")
        print_done = False
    # Turn on printing
    # sys.stdout = sys.__stdout__

    # temp
    if print_done:
        print(f"Done recording {curr_direc}")


def win_geo_show(win):
    # Center window to user's screen
    win.setWindowIcon(QIcon(media_path + "ico.ico"))

    win.setWindowFlag(Qt.WindowMaximizeButtonHint, False)
    win.show()
    qr = win.frameGeometry()
    cp = QDesktopWidget().availableGeometry().center()
    qr.moveCenter(cp)
    win.move(qr.topLeft())
    win.setFixedSize(win.width(), win.height())


class WelcomeWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Mind Controlled Robotic Platform'
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)

        # Sizing the window
        pix_margin = 10
        win_width = 820
        win_height = 580
        self.resize(win_width, win_height)

        # Add header
        header_width = win_width - pix_margin*2
        header_height = 60
        header_left = pix_margin
        header_top = pix_margin*2
        self.header = QLabel(self)
        self.header.setGeometry(header_left, header_top, header_width, header_height)
        self.header.setAlignment(Qt.AlignHCenter | Qt.AlignTop)

        # Add text
        self.text = QLabel(self)
        text_width = win_width - pix_margin*2
        text_height = 440
        text_left = pix_margin
        text_top = pix_margin + header_height
        self.text.setGeometry(text_left, text_top, text_width, text_height)
        self.text.setAlignment(Qt.AlignHCenter | Qt.AlignTop)

        # Adding GIF
        gif_width = 240
        gif_height = 180
        brain_gif = QMovie(media_path + "giphy.gif")
        brain_gif.start()

        # Adding GIF Label
        brain_gif_l = QLabel(self)
        brain_gif_l.setMovie(brain_gif)
        brain_gif_l_left = int((win_width - gif_width)/2)
        brain_gif_l_top = pix_margin + header_height + 40
        brain_gif_l.setGeometry(brain_gif_l_left, brain_gif_l_top, gif_width, gif_height)

        # Add Push Button
        button_width = 200
        button_height = 35
        button_left = int((win_width - button_width)/2)
        button_top = int(win_height - button_height - pix_margin*2)
        self.button = QPushButton(self)
        self.button.setGeometry(button_left, button_top, button_width, button_height)
        self.button.clicked.connect(self.on_click)

        # Run window
        self.retranslateUi()
        win_geo_show(self)

    def retranslateUi(self):
        # Set text to labels
        _translate = QCoreApplication.translate
        self.header.setText(_translate("Form", u"<html><head/><body><p align=\"center\"><span style=\" font-size:16pt; font-weight:600;\">Welcome to the &quot;EEG Learning GUI&quot;</span></p></body></html>", None))
        self.text.setText(_translate("Form", u"<html><head/><body><p align=\"center\"><span style=\" font-size:12pt;\">In this process we will guide you how to create a constant thoughts about &quot;</span><span style=\" font-size:12pt; font-weight:600;\">moving</span><span style=\" font-size:12pt;\">&quot;.</span><br><br><br><br><br><br><br><br><br><br><br><br><p align=\"center\"><span style=\" font-size:12pt;\">The main goal is to create a way of thinking that <br/>you will be able to reproduce when using our system.</span></p><p align=\"center\"><span style=\" font-size:12pt;\">After this step, we will record your thoughts - forward, backwards, right, left,<br/>so our system will be able to recognize them in the future.</span></p><p align=\"center\"><br/></p><p align=\"center\"><span style=\" font-size:12pt;\">For best results, we need you to be </span><span style=\" font-size:12pt; font-weight:600;\">concentrated</span><span style=\" font-size:12pt;\"> as possible.<br/>Please make s"
                        "ure there are no distractions around you.</span></p></body></html>", None))
        font = QFont(); font.setPointSize(10); font.setWeight(100)
        self.button.setFont(font)
        self.button.setText(_translate("Form", u"I'm ready - let's start!", None))

    @pyqtSlot()
    def on_click(self):
        global win
        self.close()
        win = BeginTrainWindow()


class BeginTrainWindow(QWidget):
    directions = ["Forward", "Backwards", "Right", "Left", "Neutral"]
    curr_ind = 0

    def __init__(self):
        super().__init__()
        self.title = 'Training Intro'
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)

        # Sizing the window
        pix_margin = 10
        win_width = 850
        win_height = 830
        self.resize(win_width, win_height)

        # Add header
        header_width = win_width - pix_margin*2
        header_height = 60
        header_left = pix_margin
        header_top = pix_margin*2
        self.header = QLabel(self)
        self.header.setGeometry(header_left, header_top, header_width, header_height)
        self.header.setAlignment(Qt.AlignHCenter | Qt.AlignTop)

        # Add text
        self.text = QLabel(self)
        text_width = win_width - pix_margin*2
        text_height = 750
        text_left = pix_margin
        text_top = pix_margin + header_height
        self.text.setGeometry(text_left, text_top, text_width, text_height)
        self.text.setAlignment(Qt.AlignHCenter | Qt.AlignTop)

        # Adding GIF
        gif_width = 800
        gif_height = 450
        example_gif = QMovie(media_path + "f.gif")
        example_gif.start()

        # Adding GIF Label
        example_gif_l = QLabel(self)
        example_gif_l.setMovie(example_gif)
        example_gif_l_left = int((win_width - gif_width)/2)
        example_gif_l_top = pix_margin + header_height + 180
        example_gif_l.setGeometry(example_gif_l_left, example_gif_l_top, gif_width, gif_height)

        # Add Push Button
        button_width = 160
        button_height = 35
        button_left = int((win_width - button_width)/2)
        button_top = int(win_height - button_height - pix_margin*2)
        self.button = QPushButton(self)
        self.button.setGeometry(button_left, button_top, button_width, button_height)
        self.button.clicked.connect(self.on_click)

        # Run window
        self.retranslateUi()
        win_geo_show(self)

    def retranslateUi(self):
        # Set text to labels
        _translate = QCoreApplication.translate
        self.header.setText(_translate("Form", u"<html><head/><body><p align=\"center\"><span style=\" font-size:16pt; font-weight:600;\">Training Intro</span></p></body></html>", None))
        self.text.setText(_translate("Form", u"<html><head/><body><p align=\"center\"><span style=\" font-size:12pt;\">In the few next steps you will be able to train you mind before recording the data.</span></p><p align=\"center\"><span style=\" font-size:12pt;\">The following GIF (animated picture) will accompany us throughout the process,<br/>and will be shown in different orieantation every time.</span></p><p align=\"center\"><span style=\" font-size:12pt;\">As example, in this screen, You are moving </span><span style=\" font-size:12pt; font-weight:600;\">Forward</span><span style=\" font-size:12pt;\">,<br/>so the instructions will ask you to think about forward.</span></p><p align=\"center\"><br/></p><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><p align=\"center\"><span style=\" font-size:12pt; font-weight:600;\">Take your time</span><span style=\" font-size:12pt;\"> finding the most accurate thought for each direction,<br/>and move to the next screen only when you are ready.</span></p></body></html>", None))
        font = QFont(); font.setPointSize(10); font.setWeight(100)
        self.button.setFont(font)
        self.button.setText(_translate("Form", u"Start Training", None))

    @pyqtSlot()
    def on_click(self):
        global win
        self.close()
        win = RecordWindow(BeginTrainWindow.directions[BeginTrainWindow.curr_ind], False)


class RecordWindow(QWidget):
    def __init__(self, direction, record):
        super().__init__()
        self.record = record    # Boolean
        if self.record:
            self.title = 'Recording'
        else:
            self.title = 'Training'
        self.direction = direction
        self.text_cell = "Focus your mind on &quot;moving&quot; around the object in the GIF."
        self.button_text = "Next Direction"
        self.task = 0
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)

        # Sizing the window
        pix_margin = 10
        win_width = 850
        win_height = 680
        if self.record:
            win_height = 710
        self.resize(win_width, win_height)

        # Add header
        header_width = win_width - pix_margin*2
        header_height = 60
        header_left = pix_margin
        header_top = pix_margin*2
        self.header = QLabel(self)
        self.header.setGeometry(header_left, header_top, header_width, header_height)
        self.header.setAlignment(Qt.AlignHCenter | Qt.AlignTop)

        # Add text
        self.text = QLabel(self)
        text_width = win_width - pix_margin*2
        text_height = 80
        text_left = pix_margin
        text_top = pix_margin + header_height
        self.text.setGeometry(text_left, text_top, text_width, text_height)
        self.text.setAlignment(Qt.AlignHCenter | Qt.AlignTop)

        if self.direction == BeginTrainWindow.directions[0]:
            gif_path = "f.gif"
        elif self.direction == BeginTrainWindow.directions[1]:
            gif_path = "b.gif"
        elif self.direction == BeginTrainWindow.directions[2]:
            gif_path = "r.gif"
        elif self.direction == BeginTrainWindow.directions[3]:
            gif_path = "l.gif"
        else:
            gif_path = "not_moving.gif"
            self.text_cell = "Focus your mind on the pictures in front of you"
            if self.record:
                self.button_text = "Done"

        # Adding GIF
        gif_width = 800
        gif_height = 450
        moving_gif = QMovie(media_path + gif_path)
        moving_gif.start()

        # Adding GIF Label
        moving_gif_l = QLabel(self)
        moving_gif_l.setMovie(moving_gif)
        moving_gif_l_left = int((win_width - gif_width)/2)
        moving_gif_l_top = pix_margin + header_height + text_height
        moving_gif_l.setGeometry(moving_gif_l_left, moving_gif_l_top, gif_width, gif_height)

        if self.record:
            # Add Push Button
            start_button_width = 160
            start_button_height = 35
            start_button_left = int((win_width - start_button_width)/2)
            start_button_top = int(win_height - start_button_height - pix_margin*6)
            self.start_button = QPushButton(self)
            self.start_button.setGeometry(start_button_left, start_button_top, start_button_width, start_button_height)
            self.start_button.clicked.connect(self.on_click_start)

        # Add Push Button
        button_width = 160
        button_height = 35
        button_left = int((win_width - button_width)/2)
        button_top = int(win_height - button_height - pix_margin*2)
        self.button = QPushButton(self)
        self.button.setGeometry(button_left, button_top, button_width, button_height)
        self.button.clicked.connect(self.on_click)

        # Run window
        self.retranslateUi()
        win_geo_show(self)

    def retranslateUi(self):
        # Set text to labels
        _translate = QCoreApplication.translate
        self.header.setText(_translate("Form", f"<html><head/><body><p align=\"center\"><span style=\" font-size:16pt; font-weight:600;\">{self.title}</span></p></body></html>", None))
        self.text.setText(_translate("Form", f"<html><head/><body><p align=\"center\"><span style=\" font-size:12pt;\">Please concentrate: <span style=\" font-weight:600;\">{self.direction}</span></span></p><p align=\"center\"><span style=\" font-size:12pt;\">{self.text_cell}</span></p></body></html>", None))
        font = QFont(); font.setPointSize(10);
        self.button.setFont(font)
        self.button.setText(_translate("Form", f"{self.button_text}", None))
        if self.record:
            font.setWeight(100)
            self.start_button.setFont(font)
            self.start_button.setText(_translate("Form", f"Start Recording", None))



    @pyqtSlot()
    def on_click_start(self):
        # check if concentrated
        # check if headset is connected
        # another small window to verify all above?? ^ ^ ^
        try:
            if not self.task:
                self.task = threading.Thread(target=threaded_func)
                self.task.start()
        #   self.start_button.setEnabled(False)
        except:
            print("try again")

    @pyqtSlot()
    def on_click(self):
        self.close()
        # try to minimize logic here

        global win
        BeginTrainWindow.curr_ind += 1
        if BeginTrainWindow.curr_ind != len(BeginTrainWindow.directions) and not self.record:
            win = RecordWindow(BeginTrainWindow.directions[BeginTrainWindow.curr_ind], False)

        elif BeginTrainWindow.curr_ind == len(BeginTrainWindow.directions) and not self.record:
            BeginTrainWindow.curr_ind = 0
            win = RecordWindow(BeginTrainWindow.directions[BeginTrainWindow.curr_ind], True)

        elif BeginTrainWindow.curr_ind != len(BeginTrainWindow.directions) and self.record:
            win = RecordWindow(BeginTrainWindow.directions[BeginTrainWindow.curr_ind], True)
        else:
            print("END")


if __name__ == '__main__':
    # Params
    media_path = r"./img/"
    full_name = "david_g"
    path = r"C:/EEGrecords/"
    record_length = 5

    # Create folders for recordings
    for i in BeginTrainWindow.directions:
        if not os.path.exists(path+i):
            os.makedirs(path+i)

    # Running GUI
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    win = WelcomeWindow()
    # Internal USE
    # win = RecordWindow(BeginTrainWindow.directions[BeginTrainWindow.curr_ind], True)
    sys.exit(app.exec_())
