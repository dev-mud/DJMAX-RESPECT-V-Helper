from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QStackedWidget, QMessageBox, QCheckBox, QSpinBox
from PyQt5.QtWidgets import QLabel, QPushButton, QLineEdit, QTextEdit
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtTest import *
from functools import partial
from threading import Thread
from bs4 import BeautifulSoup
import sys, os
import math
import random
import json
import requests
import re

PROGRAM_NAME = 'DJMAX RESPECT V Helper'
VERSION = '1.4.0'
song_DB_path = 'songs.json'

W_width = 560 #창 가로 길이
W_height = 980 #창 세로 길이

MAX_MULTI_SELECT = 10 #'한 번에 뽑기' 최대 개수
MAX_ROULETTE_INPUT = 10 #룰렛 항목 최대 개수

DIAMETER = 500 #룰렛판 지름

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.load_Data()
        self.init_UI()
        
    def init_UI(self):
        self.setWindowTitle(f'{PROGRAM_NAME} {VERSION}')
        self.init_font()
        
        #메인 위젯(QStackedWidget #1)
        self.create_main_layout()
        self.main_widget = QWidget()
        self.main_widget.setLayout(self.main_layout)
        
        self.thumbnail_label = QLabel()
        self.thumbnail_pixmap = QPixmap('ICON/1.png')
        self.thumbnail_label.setPixmap(self.thumbnail_pixmap)
        self.select_button = QPushButton('SELECT')
        self.select_button.clicked.connect(self.click_select_button)
        self.roulette_button = QPushButton('룰렛')
        self.roulette_button.clicked.connect(self.click_roulette_button)
        
        self.right_layout.addWidget(self.thumbnail_label)
        self.right_layout.addWidget(self.select_button)
        self.right_layout.addWidget(self.roulette_button)
        
        #'한 번에 뽑기' 위젯(QStackedWidget #2)
        self.multi_select_widget = QWidget()
        self.create_multi_select_layout()
        
        #룰렛 위젯(QStackedWidget #3)
        self.roulette_widget = RouletteWidget(self)

        self.setFixedSize(W_width, W_height)
        self.init_stacked_widget()
        self.set_label()
        self.set_css()
        self.change_label_background(self.data_label[2], self.data_label[3])
        
        self.show()
        
    def init_font(self):
        self.font = QFont()
        self.font.setFamily('돋움')
        self.font.setPointSize(14)
        self.smallfont = QFont()
        self.smallfont.setPointSize(12)
        
    def init_stacked_widget(self):
        self.stack = QStackedWidget(self)
        self.stack.setGeometry(0, 0, W_width, W_height)
        self.stack.addWidget(self.main_widget)
        self.stack.addWidget(self.multi_select_widget)
        self.stack.addWidget(self.roulette_widget)
        
    def set_css(self):   
        self.option_label.setStyleSheet(
            'QLabel {'
            f'font : bold;'
            '}'
        )
        
        self.memo_label.setStyleSheet(
            'QLabel {'
            f'font : bold;'
            '}'
        )
        
        self.memo_edit.setStyleSheet(
            'QTextEdit {'
            f'background-color : rgb(247,241,237);'
            'color : rgb(47,54,95);'
            'font : bold 28px;'
            'border : 2px solid rgb(47,54,95);'
            '}'
        )
        
        self.select_button.setStyleSheet(
            'QPushButton {'
            f'background-color : rgb(247,241,237);'
            'color : rgb(47,54,95);'
            'font : bold;'
            '}'
            'QPushButton::hover {'
            f'background-color : rgb(47,54,95);'
            'color : rgb(247,241,237);'
            'font : bold;'
            '}'
            'QPushButton::pressed {'
            f'background-color : rgb(247,241,237);'
            'color : rgb(47,54,95);'
            'font : bold;'
            '}'
        )
        
        self.roulette_button.setStyleSheet(
            'QPushButton {'
            f'background-color : rgb(247,241,237);'
            'color : rgb(47,54,95);'
            'font : bold;'
            '}'
            'QPushButton::hover {'
            f'background-color : rgb(47,54,95);'
            'color : rgb(247,241,237);'
            'font : bold;'
            '}'
            'QPushButton::pressed {'
            f'background-color : rgb(247,241,237);'
            'color : rgb(47,54,95);'
            'font : bold;'
            '}'
        )
        
        for button in self.category_select_button:
            button.setStyleSheet(
                'QPushButton {'
                f'background-color : rgb(247,241,237);'
                'color : rgb(47,54,95);'
                '}'
                'QPushButton::hover {'
                f'background-color : rgb(47,54,95);'
                'color : rgb(247,241,237);'
                '}'
                'QPushButton::pressed {'
                f'background-color : rgb(247,241,237);'
                'color : rgb(47,54,95);'
                '}'
            )
        
        for button in self.btn_select_button:
            button.setStyleSheet(
                'QPushButton {'
                f'background-color : rgb(247,241,237);'
                'color : rgb(47,54,95);'
                '}'
                'QPushButton::hover {'
                f'background-color : rgb(47,54,95);'
                'color : rgb(247,241,237);'
                '}'
                'QPushButton::pressed {'
                f'background-color : rgb(247,241,237);'
                'color : rgb(47,54,95);'
                '}'
            )
        
        for button in self.difficulty_select_button:
            button.setStyleSheet(
                'QPushButton {'
                f'background-color : rgb(247,241,237);'
                'color : rgb(47,54,95);'
                '}'
                'QPushButton::hover {'
                f'background-color : rgb(47,54,95);'
                'color : rgb(247,241,237);'
                '}'
                'QPushButton::pressed {'
                f'background-color : rgb(247,241,237);'
                'color : rgb(47,54,95);'
                '}'
            )
            
        for button in self.level_select_button:
            button.setStyleSheet(
                'QPushButton {'
                f'background-color : rgb(247,241,237);'
                'color : rgb(47,54,95);'
                '}'
                'QPushButton::hover {'
                f'background-color : rgb(47,54,95);'
                'color : rgb(247,241,237);'
                '}'
                'QPushButton::pressed {'
                f'background-color : rgb(247,241,237);'
                'color : rgb(47,54,95);'
                '}'
            )
            
        for attribute_label in self.attribute_label:
            attribute_label.setStyleSheet(
                'QLabel {'
                f'background-color : rgb(47,54,95);'
                'color : rgb(247,241,237);'
                'font : bold;'
                '}'
            )
            
        for filter_label in self.filter_attribute:
            filter_label.setStyleSheet(
                'QLabel {'
                f'font : bold;'
                '}'
            )
        
        self.multi_select_widget.setStyleSheet(
            'QLabel {'
            f'font : 18px;'
            '}'
            'QPushButton {'
            f'background-color : rgb(247,241,237);'
            'color : rgb(47,54,95);'
            '}'
            'QPushButton::hover {'
            f'background-color : rgb(47,54,95);'
            'color : rgb(247,241,237);'
            '}'
            'QPushButton::pressed {'
            f'background-color : rgb(247,241,237);'
            'color : rgb(47,54,95);'
            '}'
        )    
    
    def crawling_from_archive(self):
        self.floor = []
        self.floor_num = []
        self.floor_count = []
        self.floor_category = []
        self.floor_sname = []
        self.floor_level = []
        self.floor_button = []
        
        for button in [4, 5, 6, 8]:
            res = requests.get('https://v-archive.net/grade/' + str(button) + '/SC')
            soup = BeautifulSoup(res.text, 'html.parser')
            dlc = soup.find_all('span', attrs={"class" : "dlc_code_wrap"})
            song_name = soup.find_all('a', attrs={"class" : "title_name"})
            difficulty = soup.find_all('span', class_=re.compile("^pattern"))
            floor_number = soup.find_all('div', attrs={"class" : "floor_number"})
            floor_patterns = soup.find_all('div', attrs={"class" : "floor_patterns noscore"})
            
            self.floor_count = []
            self.floor_num = []
            
            for i, txt in enumerate(floor_number):
                self.floor_num.append(txt.text.strip())
                self.floor_count.append(len(floor_patterns[i].find_all('div', attrs={"class" : "record"})))
                
                for j in range(self.floor_count[i]):
                    self.floor.append(self.floor_num[i])  
            
            for i, txt in enumerate(song_name):
                self.floor_category.append(txt.text.strip())
                self.floor_sname.append(song_name[i].text.strip())
                if 'SC' in difficulty[i].text.strip():
                    self.floor_level.append(difficulty[i].text.strip())
                else:
                    self.floor_level.append(difficulty[i].text.strip().split(' ')[1])
                self.floor_button.append(button)
        
    def load_Data(self):
        with open(song_DB_path, 'r', encoding='utf-8') as f:
            song_json = json.load(f, strict=False)
        
        try: 
            self.crawling_from_archive()    
        except:
            pass
        self.set_data(song_json)
        
    def set_data(self, data):
        self.song_name = []
        self.artist= []
        self.level = []
        self.level_range = [str(i+1) for i in range(15)] + ['SC ' + str(i+1) for i in range(15)]
        self.level_flag = []
        self.level_color = [['255', '255', '0'], ['255', '127', '0'], ['255', '0', '0'], ['224', '0', '117'], ['198', '4', '227'], ['61', '102', '255']]
        self.category = []
        self.category_flag = []
        self.category_color = [['255', '191', '0'], ['0', '178', '255'], ['246', '40', '40'], ['210', '129', '22'], ['114', '137', '255'], ['255', '237', '193'], ['106', '0', '24'], ['249', '109', '27'], ['203', '29', '64'], ['116', '37', '221'], ['193', '17', '0'], ['1', '52', '131'], ['30', '182', '17'], ['252', '89', '206'], ['255','202','183'], ['85', '137', '252'], ['0', '41', '17'], ['0', '0', '0'], ['0', '0', '0'], ['0', '0', '0'], ['0', '0', '0'], ['0', '0', '0'], ['0', '0', '0'], ['0', '0', '0'], ['0', '0', '0'], ['0', '0', '0'], ['0', '0', '0'], ['0', '0', '0'], ['0', '0', '0'], ['255', '133', '1']]
        self.category_font_color = [['231', '117', '63'], ['160', '77', '247'], ['115', '7', '49'], ['0', '0', '0'], ['43', '97', '178'], ['115', '115', '115'], ['220', '27', '73'], ['46', '58', '66'], ['245', '220', '142'], ['59', '10', '112'], ['0', '0', '0'], ['255', '161', '0'], ['7', '119', '221'], ['0', '0', '0'], ['0', '0', '0'], ['0', '0', '0'], ['10', '217', '0'], ['128', '128', '128'], ['128', '128', '128'], ['128', '128', '128'], ['128', '128', '128'], ['128', '128', '128'], ['128', '128', '128'], ['128', '128', '128'], ['128', '128', '128'], ['128', '128', '128'], ['128', '128', '128'], ['128', '128', '128'], ['128', '128', '128'], ['0', '0', '0']]
        self.category_name = ['RESPECT', 'PORTABLE 1', 'PORTABLE 2', 'PORTABLE 3', 'TRILOGY', 'CLAZZIQUAI', 'BLACK SQUARE', 'V EXTENSION', 'V EXTENSION 2', 'V EXTENSION 3', 'V EXTENSION 4', 'V EXTENSION 5', 'EMOTIONAL SENSE', 'TECHNIKA 1', 'TECHNIKA 2', 'TECHNIKA 3', 'TECHNIKA TUNE Q', 'GUILTY GEAR', "GIRLS' FRONTLINE", 'GROOVE COASTER', 'DEEMO', 'CYTUS', 'CHUNITHM', 'ESTIMATE', 'NEXON', 'MUSE DASH', 'EZ2ON', 'MAPLESTORY', 'FALCOM', 'CLEAR PASS']
        self.difficulty = ['NORMAL', 'HARD', 'MAXIMUM', 'SC']
        self.difficulty_flag = []
        self.difficulty_color = [['255', '255', '0'], ['255', '102', '0'], ['255', '0', '0'], ['198', '4', '227']]
        self.keys = ['곡', 'ARTIST', 'CATEGORY', 'BUTTON', 'DIFFICULTY', 'LEVEL']
        self.filter = ['CATEGORY', 'BUTTON', 'DIFFICULTY', 'LEVEL']
        self.button = [4,5,6,8]
        self.button_flag = []
        self.button_color = [['0', '255', '0'], ['0', '255', '255'], ['255', '153', '0'], ['28', '31', '133']]
        self.duplication = ['Alone(Nauts)', 'Alone(Marshmellow)', 'Urban Night(hYO)', 'Urban Night(Electronic Boutique)', 'Voyage(makou)', 'Voyage(SOPHI)', 'Showdown(LeeZu)', 'Showdown(Andy Lee)']
        self.status_flag = False
     
        for i, key in enumerate(data):
            if key not in self.duplication:
                self.song_name.append(key)
            else:
                self.song_name.append(key.split('(')[0])
            self.artist.append(data[key]['artist'])
            self.category.append(data[key]['category'])
            self.level.append(data[key]['difficulty'])
            
        for i in self.category_name:
            self.category_flag.append(True)
            
        for i in self.button:
            self.button_flag.append(True)
            
        for i in self.difficulty:
            self.difficulty_flag.append(True)
            
        for i in self.level_range:
            self.level_flag.append(True)
    
    def set_label(self):
        self.attribute_label = []
        self.data_label = []
        
        for i, key in enumerate(self.keys):
            self.attribute_label.append(QLabel(key))
            self.data_label.append(QLabel())
            self.attribute_label[i].setFont(self.smallfont)
            self.data_label[i].setFont(self.smallfont)
            self.v_layout[0].addWidget(self.attribute_label[i])
            self.v_layout[1].addWidget(self.data_label[i])
            
        self.attribute_label.append(QLabel('FLOOR'))
        self.data_label.append(QLabel(''))
        self.attribute_label[6].setFont(self.smallfont)
        self.data_label[6].setFont(self.smallfont)
        self.v_layout[0].addWidget(self.attribute_label[6])
        self.v_layout[1].addWidget(self.data_label[6])
            
        self.data_label[0].setText(self.song_name[0])
        self.data_label[3].setText(str(self.button[0]) + ' BUTTON')
        self.data_label[4].setText(self.difficulty[0])
        self.set_label_text(0,0,0)
        
        self.data_label[2].setAlignment(Qt.AlignCenter)
        self.data_label[3].setAlignment(Qt.AlignCenter)
        
    def set_label_text(self, song_index, button_index, difficulty_index):
        self.data_label[0].setText(self.song_name[song_index])
        self.data_label[1].setText(self.artist[song_index])
        self.data_label[2].setText(self.category[song_index])
        if button_index != -1 and difficulty_index != -1:
            self.data_label[3].setText(str(self.button[button_index]))
            self.data_label[4].setText(self.difficulty[difficulty_index])
            self.data_label[5].setText(self.search_level(self.song_name[song_index], self.button[button_index], self.difficulty[difficulty_index]))
        else:
            self.data_label[3].setText('')
            self.data_label[4].setText('')
            self.data_label[5].setText('')
        
    def create_main_layout(self):
        self.main_layout = QVBoxLayout()
        self.top_layout = QHBoxLayout()
        self.v_layout = [QVBoxLayout(), QVBoxLayout()]
        self.right_layout = QVBoxLayout()
        self.option_layout = QHBoxLayout()
        self.memo_layout = QHBoxLayout()
        self.filter_layout = QVBoxLayout()
        self.inter_filter_layout = []
        self.category_layout = []
        self.select_button_layout = [QHBoxLayout() for i in range(4)]
        self.button_layout = QHBoxLayout()
        self.difficulty_layout = QHBoxLayout()
        self.level_layout = []
        self.filter_attribute = []
        self.category_filter_button = []
        self.button_filter_button = []
        self.difficulty_filter_button = []
        self.level_filter_button = []
        self.category_select_button = [QPushButton('모두 선택'), QPushButton('선택 해제')]
        self.btn_select_button = [QPushButton('모두 선택'), QPushButton('선택 해제')]
        self.difficulty_select_button = [QPushButton('모두 선택'), QPushButton('선택 해제')]
        self.level_select_button = [QPushButton('모두 선택'), QPushButton('선택 해제')]
        self.option_label = QLabel('OPTION')
        self.option_checkbox = QCheckBox('룰렛 SKIP')
        self.option_checkbox_2 = QCheckBox('한번에 뽑기')
        self.option_checkbox_3 = QCheckBox('ONLY SONGS(필터 X)')
        self.multi_select_count_spinbox = QSpinBox()
        self.memo_label = QLabel('MEMO\n(Beta)')
        self.memo_edit = QTextEdit()
        self.top_layout.addLayout(self.v_layout[0], 1)
        self.top_layout.addLayout(self.v_layout[1], 5)
        self.top_layout.addLayout(self.right_layout, 1)
        self.main_layout.addLayout(self.top_layout, 5)
        self.main_layout.addLayout(self.memo_layout, 1)
        self.main_layout.addLayout(self.option_layout, 1)
        self.main_layout.addLayout(self.filter_layout, 20)
        self.option_layout.addWidget(self.option_label)
        self.option_layout.addWidget(self.option_checkbox)
        self.option_layout.addWidget(self.option_checkbox_2)
        self.option_layout.addWidget(self.multi_select_count_spinbox)
        self.option_layout.addWidget(self.option_checkbox_3)
        self.option_checkbox_2.stateChanged.connect(self.click_option_checkbox_2)
        self.memo_layout.addWidget(self.memo_label)
        self.memo_layout.addWidget(self.memo_edit)
        self.memo_edit.setMinimumHeight(50)
        
        for i, filter in enumerate(self.filter):
            self.inter_filter_layout.append(QVBoxLayout())
            self.filter_layout.addLayout(self.inter_filter_layout[i])
            self.filter_attribute.append(QLabel(self.filter[i]))
            self.inter_filter_layout[i].addWidget(self.filter_attribute[i])
            self.inter_filter_layout[i].addLayout(self.select_button_layout[i])
            
            if i == 0:
                self.select_button_layout[i].addWidget(self.category_select_button[0])
                self.select_button_layout[i].addWidget(self.category_select_button[1])
                self.category_select_button[0].clicked.connect(self.select_all_category_filter)
                self.category_select_button[1].clicked.connect(self.deselect_all_category_filter)
                
                for j in range(math.ceil(len(self.category_name)/5.0)):
                    self.category_layout.append(QHBoxLayout())
                    self.inter_filter_layout[i].addLayout(self.category_layout[j])
                    self.category_layout[j].setAlignment(Qt.AlignLeft)
            
            if i == 1:
                self.select_button_layout[i].addWidget(self.btn_select_button[0])
                self.select_button_layout[i].addWidget(self.btn_select_button[1])
                self.btn_select_button[0].clicked.connect(self.select_all_button_filter)
                self.btn_select_button[1].clicked.connect(self.deselect_all_button_filter)
                self.inter_filter_layout[i].addLayout(self.button_layout)
                
            if i == 2:
                self.select_button_layout[i].addWidget(self.difficulty_select_button[0])
                self.select_button_layout[i].addWidget(self.difficulty_select_button[1])
                self.difficulty_select_button[0].clicked.connect(self.select_all_difficulty_filter)
                self.difficulty_select_button[1].clicked.connect(self.deselect_all_difficulty_filter)
                self.inter_filter_layout[i].addLayout(self.difficulty_layout)
                
            if i == 3:
                self.select_button_layout[i].addWidget(self.level_select_button[0])
                self.select_button_layout[i].addWidget(self.level_select_button[1])
                self.level_select_button[0].clicked.connect(self.select_all_level_filter)
                self.level_select_button[1].clicked.connect(self.deselect_all_level_filter)
                
                for j in range(math.ceil(len(self.level_range)/5.0)):
                    self.level_layout.append(QHBoxLayout())
                    self.inter_filter_layout[i].addLayout(self.level_layout[j])
                    self.level_layout[j].setAlignment(Qt.AlignLeft)
                
        for i, category in enumerate(self.category_name):
            idx = math.floor(i/5.0)
            self.category_filter_button.append(QPushButton(category))
            self.category_layout[idx].addWidget(self.category_filter_button[i])
            self.category_filter_button[i].clicked.connect(partial(self.click_category, i))
            self.category_filter_button[i].setMinimumHeight(30)
            self.category_filter_button[i].setMinimumWidth(105)
            self.category_filter_button[i].setStyleSheet(
                "QPushButton {"
                + "background-color : rgb(247,241,237);"
                + "color : rgb(" + self.category_font_color[i][0] + ", " + self.category_font_color[i][1] + ", " + self.category_font_color[i][2] + ");"
                + "border : 2px solid rgb(" + self.category_color[i][0] + ", " + self.category_color[i][1] + ", " + self.category_color[i][2] + ");"
                + "font : 10px, bold;"
                + "}"
                + "QPushButton::hover {"
                + "background-color : rgb(" + self.category_color[i][0] + ", " + self.category_color[i][1] + ", " + self.category_color[i][2] + ");"
                + "color : rgb(" + self.category_font_color[i][0] + ", " + self.category_font_color[i][1] + ", " + self.category_font_color[i][2] + ");"
                + "font : 10px, bold;"
                + "}"
            )
        
        for i, button in enumerate(self.button):
            self.button_filter_button.append(QPushButton(str(self.button[i]) + ' BUTTON'))
            self.button_layout.addWidget(self.button_filter_button[i])
            self.button_filter_button[i].clicked.connect(partial(self.click_button_filter, i))
            self.button_filter_button[i].setMinimumHeight(30)
            self.button_filter_button[i].setStyleSheet(
                "QPushButton {"
                + "background-color : rgb(247,241,237);"
                + "color : rgb(" + self.button_color[i][0] + ", " + self.button_color[i][1] + ", " + self.button_color[i][2] + ");"
                + "border : 2px solid rgb(" + self.button_color[i][0] + ", " + self.button_color[i][1] + ", " + self.button_color[i][2] + ");"
                + "}"
                + "QPushButton::hover {"
                + "background-color : rgb(" + self.button_color[i][0] + ", " + self.button_color[i][1] + ", " + self.button_color[i][2] + ");"
                + "color : rgb(247,241,237);"
                + "}"
            )
        
        for i, difficulty in enumerate(self.difficulty):
            self.difficulty_filter_button.append(QPushButton(str(self.difficulty[i])))
            self.difficulty_layout.addWidget(self.difficulty_filter_button[i])
            self.difficulty_filter_button[i].clicked.connect(partial(self.click_difficulty_filter, i))
            self.difficulty_filter_button[i].setMinimumHeight(30)
            self.difficulty_filter_button[i].setStyleSheet(
                "QPushButton {"
                + "background-color : rgb(247,241,237);"
                + "color : rgb(" + self.difficulty_color[i][0] + ", " + self.difficulty_color[i][1] + ", " + self.difficulty_color[i][2] + ");"
                + "border : 2px solid rgb(" + self.difficulty_color[i][0] + ", " + self.difficulty_color[i][1] + ", " + self.difficulty_color[i][2] + ");"
                + "}"
                + "QPushButton::hover {"
                + "background-color : rgb(" + self.difficulty_color[i][0] + ", " + self.difficulty_color[i][1] + ", " + self.difficulty_color[i][2] + ");"
                + "color : rgb(47,54,95);"
                + "}"
            )
        
        for i, level in enumerate(self.level_range):
            idx = math.floor(i/5.0)
            self.level_filter_button.append(QPushButton(level))
            self.level_layout[idx].addWidget(self.level_filter_button[i])
            self.level_filter_button[i].clicked.connect(partial(self.click_level_filter, i))
            self.level_filter_button[i].setMinimumHeight(30)
            self.level_filter_button[i].setMinimumWidth(105)
            self.level_filter_button[i].setStyleSheet(
                "QPushButton {"
                + "background-color : rgb(247,241,237);"
                + "border : 2px solid rgb(" + self.level_color[int(i/5)][0] + ", " + self.level_color[int(i/5)][1] + ", " + self.level_color[int(i/5)][2] + ");"
                + "}"
                + "QPushButton::hover {"
                + "background-color : rgb(" + self.level_color[int(i/5)][0] + ", " + self.level_color[int(i/5)][1] + ", " + self.level_color[int(i/5)][2] + ");"
                + "}"
            )
            
        self.top_layout.setAlignment(Qt.AlignTop)
        self.option_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.filter_layout.setAlignment(Qt.AlignTop)
        self.main_layout.setAlignment(Qt.AlignTop)
        
        self.multi_select_count_spinbox.setEnabled(False)
        
    def create_multi_select_layout(self):
        self.multi_select_layout = QVBoxLayout()
        self.multi_select_song_layout = [QHBoxLayout() for i in range(MAX_MULTI_SELECT)]
        self.multi_select_text_layout = [QVBoxLayout() for i in range(MAX_MULTI_SELECT)]
        self.multi_select_thumbnail_label = [QLabel() for i in range(MAX_MULTI_SELECT)]
        self.multi_select_thumbnail_pixmap = [QPixmap() for i in range(MAX_MULTI_SELECT)]
        self.multi_select_song_name_label = [QLabel() for i in range(MAX_MULTI_SELECT)]
        self.multi_select_category_label = [QLabel() for i in range(MAX_MULTI_SELECT)]
        self.multi_select_button_label = [QLabel() for i in range(MAX_MULTI_SELECT)]
        self.multi_select_difficulty_label = [QLabel() for i in range(MAX_MULTI_SELECT)]
        self.multi_select_level_label = [QLabel() for i in range(MAX_MULTI_SELECT)]
        self.multi_select_home_button = QPushButton('확인')
        
        self.multi_select_widget.setLayout(self.multi_select_layout)
        
        for i, layout in enumerate(self.multi_select_song_layout):
            self.multi_select_layout.addLayout(layout)
            self.multi_select_thumbnail_label[i].setPixmap(self.multi_select_thumbnail_pixmap[i])
            layout.addWidget(self.multi_select_thumbnail_label[i], stretch = 1)
            layout.addLayout(self.multi_select_text_layout[i], stretch = 5)
        
        for i, label in enumerate(self.multi_select_song_name_label):
            self.multi_select_text_layout[i].addWidget(label)
        
        for i, label in enumerate(self.multi_select_category_label):
            self.multi_select_text_layout[i].addWidget(label)
#            label.setAlignment(Qt.AlignCenter)
            
        for i, label in enumerate(self.multi_select_button_label):
            self.multi_select_text_layout[i].addWidget(label)
#            label.setAlignment(Qt.AlignCenter)
            
        for i, label in enumerate(self.multi_select_difficulty_label):
            self.multi_select_text_layout[i].addWidget(label)
            
        for i, label in enumerate(self.multi_select_level_label):
            self.multi_select_text_layout[i].addWidget(label)    
            
        self.multi_select_layout.addWidget(self.multi_select_home_button)
        self.multi_select_home_button.clicked.connect(self.return_to_home)
        
    def return_to_home(self):
        self.stack.setCurrentIndex(0)
    
    def change_label_background(self, label, button_label):
        if label.text() not in self.category_name: #카테고리 체크
            label.setStyleSheet("background-color : rgb(247, 241 237);")
            return
        
        for i, category in enumerate(self.category_name):
            if category == label.text():
                label.setStyleSheet("background-color : rgb(" + self.category_color[i][0] + ", " + self.category_color[i][1] + ", " + self.category_color[i][2] + ");"
                + "color : rgb(" + self.category_font_color[i][0] + ", " + self.category_font_color[i][1] + ", " + self.category_font_color[i][2] + ");"
                + "font : bold;"
                )
        
        if button_label.text().split(' ')[0] not in list(str(self.button)): #버튼 체크
            button_label.setStyleSheet("background-color : rgb(247, 241 237);")
            return
        
        for i, button in enumerate(self.button):
            if str(button) == button_label.text().split(' ')[0]:
                button_label.setStyleSheet("background-color : rgb(" + self.button_color[i][0] + ", " + self.button_color[i][1] + ", " + self.button_color[i][2] + ");"
                + "color : rgb(247, 241, 237);"
                + "font : bold;"
                )
    
    def click_option_checkbox_2(self):
        if self.option_checkbox_2.isChecked():
            self.multi_select_count_spinbox.setEnabled(True)
        else:
            self.multi_select_count_spinbox.setEnabled(False)
    
    def check_filter(self):
        category_filter = self.filtering_category()
        if len(category_filter) == 0:
            QMessageBox.information(self, 'BEXTER is GOD', '카테고리를 선택하세요')
            self.select_button.setEnabled(True)
            return
        
        button_filter = self.filtering_button()
        if len(button_filter) == 0:
            QMessageBox.information(self, 'BEXTER is GOD', '버튼을 선택하세요')
            self.select_button.setEnabled(True)
            return
        
        difficulty_filter = self.filtering_difficulty()
        if len(difficulty_filter) == 0:
            QMessageBox.information(self, 'BEXTER is GOD', '난이도를 선택하세요')
            self.select_button.setEnabled(True)
            return
        
        level_filter = self.filtering_level()
        if len(level_filter) == 0:
            QMessageBox.information(self, 'BEXTER is GOD', '레벨을 선택하세요')
            self.select_button.setEnabled(True)
            return
        
        return category_filter, button_filter, difficulty_filter, level_filter
    
    def click_select_button(self):
        count = [0 for i in range(len(self.song_name))]
        
        if self.option_checkbox_3.isChecked() == False:
            try:
                category_filter, button_filter, difficulty_filter, level_filter = self.check_filter()
            except TypeError:
                return
        
        if self.option_checkbox_2.isChecked():
            if self.multi_select_count_spinbox.value() > MAX_MULTI_SELECT or self.multi_select_count_spinbox.value() <= 1:
                QMessageBox.information(self, 'BEXTER is GOD', '2~' + str(MAX_MULTI_SELECT) + ' 사이의 수를 입력하세요')
                return
            if self.option_checkbox_3.isChecked():
                category_filter, button_filter, difficulty_filter, level_filter = [], [], [], []
            self.stack.setCurrentIndex(1)
            self.multi_select_music(category_filter, button_filter, difficulty_filter, level_filter)
            return

        self.select_button.setEnabled(False)        
        
        self.select_button.setStyleSheet(
            'QPushButton {'
            f'background-color : rgb(247,241,237);'
            'color : rgba(47,54,95,70);'
            'font : bold;'
            '}'
        )
        
        delay_time = 1
        max_delay_time = random.randrange(1000, 1400)   

        if self.option_checkbox.isChecked(): #룰렛 스킵 옵션 체크 여부
            delay_time = max_delay_time * 0.9999
        
        while(delay_time < max_delay_time):
            while True:
                song_index = random.randrange(0, len(self.song_name))
                button_index = random.randrange(0, len(self.button))
                difficulty_index = random.randrange(0, len(self.difficulty))
                level = self.search_level(self.song_name[song_index], self.button[button_index], self.difficulty[difficulty_index])

                if self.option_checkbox_3.isChecked():
                    self.set_label_text(song_index, -1, -1)
#                    self.countLog.loc[self.countLog['곡'] == self.song_name[song_index], 'Count'] += 1
                else:
                    if (self.category[song_index] in category_filter) and (self.button[button_index] in button_filter) and (self.difficulty[difficulty_index] in difficulty_filter) and (level in level_filter) and ('-' not in level):
                        self.set_label_text(song_index, button_index, difficulty_index)
                    else:
                        continue

                if os.path.exists('ICON/' + str(song_index+1) + '.png'):
                    self.thumbnail_pixmap = QPixmap('ICON/' + str(song_index+1) + '.png')
                else:
                    self.thumbnail_pixmap = QPixmap('ICON/NO IMAGE.png')
                    
                self.thumbnail_label.setPixmap(self.thumbnail_pixmap) 
                self.change_label_background(self.data_label[2], self.data_label[3])
                
                if not self.option_checkbox_3.isChecked():
                    floor_index = list(filter(lambda x: self.floor_sname[x] == self.data_label[0].text(), range(len(self.floor_sname))))
                    index_tmp = -1
                    
                    for idx in floor_index:
                        if self.floor_button[idx] == int(self.data_label[3].text()) and self.floor_level[idx] == self.data_label[5].text():
                            index_tmp = idx
                    
                    if index_tmp != -1:
                        self.data_label[6].setText(self.floor[index_tmp])
                    else:
                        self.data_label[6].setText('')
                else:
                    self.data_label[6].setText('')
                        
                break
                
            QTest.qWait(int(delay_time))
            
            delay_time = delay_time * 1.1

        self.select_button.setStyleSheet(
            'QPushButton {'
            f'background-color : rgb(247,241,237);'
            'color : rgb(47,54,95);'
            'font : bold;'
            '}'
            'QPushButton::hover {'
            f'background-color : rgb(47,54,95);'
            'color : rgb(247,241,237);'
            'font : bold;'
            '}'
            'QPushButton::pressed {'
            f'background-color : rgb(247,241,237);'
            'color : rgb(47,54,95);'
            'font : bold;'
            '}'
        )
        
        self.select_button.setEnabled(True)
     
    def click_roulette_button(self):
        self.stack.setCurrentIndex(2)
    
    def click_category(self, i):
        if self.category_flag[i] == True:
            self.category_filter_button[i].setStyleSheet(
                "QPushButton {"
                + "background-color : rgb(" + self.category_color[i][0] + ", " + self.category_color[i][1] + ", " + self.category_color[i][2] + ");"
                + "color : rgb(" + self.category_font_color[i][0] + ", " + self.category_font_color[i][1] + ", " + self.category_font_color[i][2] + ");"
                + "border : 2px solid rgb(" + self.category_color[i][0] + ", " + self.category_color[i][1] + ", " + self.category_color[i][2] + ");"
                + "font : 10px, bold;"
                + "}"
            )
            self.category_flag[i] = False
        else:
            self.category_filter_button[i].setStyleSheet(
                "QPushButton {"
                + "background-color : rgb(247,241,237);"
                + "color : rgb(" + self.category_font_color[i][0] + ", " + self.category_font_color[i][1] + ", " + self.category_font_color[i][2] + ");"
                + "border : 2px solid rgb(" + self.category_color[i][0] + ", " + self.category_color[i][1] + ", " + self.category_color[i][2] + ");"
                + "font : 10px, bold;"
                + "}"
                + "QPushButton::hover {"
                + "background-color : rgb(" + self.category_color[i][0] + ", " + self.category_color[i][1] + ", " + self.category_color[i][2] + ");"
                + "color : rgb(" + self.category_font_color[i][0] + ", " + self.category_font_color[i][1] + ", " + self.category_font_color[i][2] + ");"
                + "font : 10px, bold;"
                + "}"
            )
            self.category_flag[i] = True
       
    def click_button_filter(self, i):
        if self.button_flag[i] == True:
            self.button_filter_button[i].setStyleSheet(
                "QPushButton {"
                + "background-color : rgb(" + self.button_color[i][0] + ", " + self.button_color[i][1] + ", " + self.button_color[i][2] + ");"
                + "color : rgb(247,241,237);"
                + "border : 2px solid rgb(" + self.button_color[i][0] + ", " + self.button_color[i][1] + ", " + self.button_color[i][2] + ");"
                + "}"
            )
            self.button_flag[i] = False
        else:
            self.button_filter_button[i].setStyleSheet(
                "QPushButton {"
                + "background-color : rgb(247,241,237);"
                + "color : rgb(" + self.button_color[i][0] + ", " + self.button_color[i][1] + ", " + self.button_color[i][2] + ");"
                + "border : 2px solid rgb(" + self.button_color[i][0] + ", " + self.button_color[i][1] + ", " + self.button_color[i][2] + ");"
                + "}"
                + "QPushButton::hover {"
                + "background-color : rgb(" + self.button_color[i][0] + ", " + self.button_color[i][1] + ", " + self.button_color[i][2] + ");"
                + "color : rgb(247,241,237);"
                + "}"
            )
            self.button_flag[i] = True
                
    def click_difficulty_filter(self, i):
        if self.difficulty_flag[i] == True:
            self.difficulty_filter_button[i].setStyleSheet(
                "QPushButton {"
                + "background-color : rgb(" + self.difficulty_color[i][0] + ", " + self.difficulty_color[i][1] + ", " + self.difficulty_color[i][2] + ");"
                + "color : rgb(47,54,95);"
                + "border : 2px solid rgb(" + self.difficulty_color[i][0] + ", " + self.difficulty_color[i][1] + ", " + self.difficulty_color[i][2] + ");"
                + "}"
            )
            self.difficulty_flag[i] = False
        else:
            self.difficulty_filter_button[i].setStyleSheet(
                "QPushButton {"
                + "background-color : rgb(247,241,237);"
                + "color : rgb(" + self.difficulty_color[i][0] + ", " + self.difficulty_color[i][1] + ", " + self.difficulty_color[i][2] + ");"
                + "border : 2px solid rgb(" + self.difficulty_color[i][0] + ", " + self.difficulty_color[i][1] + ", " + self.difficulty_color[i][2] + ");"
                + "}"
                + "QPushButton::hover {"
                + "background-color : rgb(" + self.difficulty_color[i][0] + ", " + self.difficulty_color[i][1] + ", " + self.difficulty_color[i][2] + ");"
                + "color : rgb(47,54,95);"
                + "}"
            )
            self.difficulty_flag[i] = True
         
    def click_level_filter(self, i):
        if self.level_flag[i] == True:
            self.level_filter_button[i].setStyleSheet(
                "QPushButton {"
                + "background-color : rgb(" + self.level_color[int(i/5)][0] + ", " + self.level_color[int(i/5)][1] + ", " + self.level_color[int(i/5)][2] + ");"
                + "border : 2px solid rgb(" + self.level_color[int(i/5)][0] + ", " + self.level_color[int(i/5)][1] + ", " + self.level_color[int(i/5)][2] + ");"
                + "}"
            )
            self.level_flag[i] = False
        else:
            self.level_filter_button[i].setStyleSheet(
                "QPushButton {"
                + "background-color : rgb(247,241,237);"
                + "border : 2px solid rgb(" + self.level_color[int(i/5)][0] + ", " + self.level_color[int(i/5)][1] + ", " + self.level_color[int(i/5)][2] + ");"
                + "}"
                + "QPushButton::hover {"
                + "background-color : rgb(" + self.level_color[int(i/5)][0] + ", " + self.level_color[int(i/5)][1] + ", " + self.level_color[int(i/5)][2] + ");"
                + "}"
            )
            self.level_flag[i] = True

    def select_all_category_filter(self):
        for i, button in enumerate(self.category_filter_button):
            if self.category_flag[i] == True:
                button.setStyleSheet(
                    "QPushButton {"
                    + "background-color : rgb(" + self.category_color[i][0] + ", " + self.category_color[i][1] + ", " + self.category_color[i][2] + ");"
                    + "color : rgb(" + self.category_font_color[i][0] + ", " + self.category_font_color[i][1] + ", " + self.category_font_color[i][2] + ");"
                    + "border : 2px solid rgb(" + self.category_color[i][0] + ", " + self.category_color[i][1] + ", " + self.category_color[i][2] + ");"
                    + "font : 10px, bold;"
                    + "}"
                )
                self.category_flag[i] = False
    
    def select_all_button_filter(self):
        for i, button in enumerate(self.button_filter_button):
            if self.button_flag[i] == True:
                button.setStyleSheet(
                    "QPushButton {"
                    + "background-color : rgb(" + self.button_color[i][0] + ", " + self.button_color[i][1] + ", " + self.button_color[i][2] + ");"
                    + "color : rgb(247,241,237);"
                    + "border : 2px solid rgb(" + self.button_color[i][0] + ", " + self.button_color[i][1] + ", " + self.button_color[i][2] + ");"
                    + "}"
                )
                self.button_flag[i] = False
                
    def select_all_difficulty_filter(self):
        for i, button in enumerate(self.difficulty_filter_button):
            if self.difficulty_flag[i] == True:
                button.setStyleSheet(
                    "QPushButton {"
                    + "background-color : rgb(" + self.difficulty_color[i][0] + ", " + self.difficulty_color[i][1] + ", " + self.difficulty_color[i][2] + ");"
                    + "color : rgb(47,54,95);"
                    + "border : 2px solid rgb(" + self.difficulty_color[i][0] + ", " + self.difficulty_color[i][1] + ", " + self.difficulty_color[i][2] + ");"
                    + "}"
                )
                self.difficulty_flag[i] = False
                
    def select_all_level_filter(self):
        for i, button in enumerate(self.level_filter_button):
            if self.level_flag[i] == True:
                button.setStyleSheet(
                    "QPushButton {"
                    + "background-color : rgb(" + self.level_color[int(i/5)][0] + ", " + self.level_color[int(i/5)][1] + ", " + self.level_color[int(i/5)][2] + ");"
                    + "border : 2px solid rgb(" + self.level_color[int(i/5)][0] + ", " + self.level_color[int(i/5)][1] + ", " + self.level_color[int(i/5)][2] + ");"
                    + "}"
                )
                self.level_flag[i] = False
    
    def deselect_all_category_filter(self):
        for i, button in enumerate(self.category_filter_button):
            if self.category_flag[i] == False:
                button.setStyleSheet(
                    "QPushButton {"
                    + "background-color : rgb(247,241,237);"
                    + "color : rgb(" + self.category_font_color[i][0] + ", " + self.category_font_color[i][1] + ", " + self.category_font_color[i][2] + ");"
                    + "border : 2px solid rgb(" + self.category_color[i][0] + ", " + self.category_color[i][1] + ", " + self.category_color[i][2] + ");"
                    + "font : 10px, bold;"
                    + "}"
                    + "QPushButton::hover {"
                    + "background-color : rgb(" + self.category_color[i][0] + ", " + self.category_color[i][1] + ", " + self.category_color[i][2] + ");"
                    + "color : rgb(" + self.category_font_color[i][0] + ", " + self.category_font_color[i][1] + ", " + self.category_font_color[i][2] + ");"
                    + "font : 10px, bold;"
                    + "}"
                )
                self.category_flag[i] = True
    
    def deselect_all_button_filter(self):
        for i, button in enumerate(self.button_filter_button):
            if self.button_flag[i] == False:
                button.setStyleSheet(
                    "QPushButton {"
                    + "background-color : rgb(247,241,237);"
                    + "color : rgb(" + self.button_color[i][0] + ", " + self.button_color[i][1] + ", " + self.button_color[i][2] + ");"
                    + "border : 2px solid rgb(" + self.button_color[i][0] + ", " + self.button_color[i][1] + ", " + self.button_color[i][2] + ");"
                    + "}"
                    + "QPushButton::hover {"
                    + "background-color : rgb(" + self.button_color[i][0] + ", " + self.button_color[i][1] + ", " + self.button_color[i][2] + ");"
                    + "color : rgb(247,241,237);"
                    + "}"
                )
                self.button_flag[i] = True
    
    def deselect_all_difficulty_filter(self):
        for i, button in enumerate(self.difficulty_filter_button):
            button.setStyleSheet(
                "QPushButton {"
                + "background-color : rgb(247,241,237);"
                + "color : rgb(" + self.difficulty_color[i][0] + ", " + self.difficulty_color[i][1] + ", " + self.difficulty_color[i][2] + ");"
                + "border : 2px solid rgb(" + self.difficulty_color[i][0] + ", " + self.difficulty_color[i][1] + ", " + self.difficulty_color[i][2] + ");"
                + "}"
                + "QPushButton::hover {"
                + "background-color : rgb(" + self.difficulty_color[i][0] + ", " + self.difficulty_color[i][1] + ", " + self.difficulty_color[i][2] + ");"
                + "color : rgb(47,54,95);"
                + "}"
            )
            self.difficulty_flag[i] = True
            
    def deselect_all_level_filter(self):
        for i, button in enumerate(self.level_filter_button):
            if self.level_flag[i] == False:
                button.setStyleSheet(
                    "QPushButton {"
                    + "background-color : rgb(247,241,237);"
                    + "border : 2px solid rgb(" + self.level_color[int(i/5)][0] + ", " + self.level_color[int(i/5)][1] + ", " + self.level_color[int(i/5)][2] + ");"
                    + "}"
                    + "QPushButton::hover {"
                    + "background-color : rgb(" + self.level_color[int(i/5)][0] + ", " + self.level_color[int(i/5)][1] + ", " + self.level_color[int(i/5)][2] + ");"
                    + "}"
                )
                self.level_flag[i] = True
     
    def filtering_category(self):
        tmp = []
        for i, flag in enumerate(self.category_flag):
            if flag == False:
                tmp.append(self.category_name[i])
                
        return tmp

    def filtering_button(self):
        tmp = []
        for i, flag in enumerate(self.button_flag):
            if flag == False:
                tmp.append(self.button[i])
                
        return tmp    
            
    def filtering_difficulty(self):
        tmp = []
        for i, flag in enumerate(self.difficulty_flag):
            if flag == False:
                tmp.append(self.difficulty[i])
                
        return tmp
        
    def filtering_level(self):
        tmp = []
        for i, flag in enumerate(self.level_flag):
            if flag == False:
                tmp.append(self.level_range[i])
                
        return tmp        
    
    def search_level(self, song, button, difficulty):
        level = ''

        song_index = self.song_name.index(song)
        button_index = self.button.index(button)
        difficulty_index = self.difficulty.index(difficulty)
        
        if difficulty_index == 3:
            level = 'SC ' + self.level[song_index][button_index][difficulty_index]
        else:
            level = self.level[song_index][button_index][difficulty_index]
            
        return level
    
    def multi_select_music(self, category_filter, button_filter, difficulty_filter, level_filter):
        self.multi_select_home_button.setEnabled(False)
        self.sname_replica = self.song_name.copy() #중복 선곡 방지 체크용으로 복사하는 리스트(ONLY SONGS 모드에서만 적용)
        
        self.reset_multi_select()
        
        music_count = self.multi_select_count_spinbox.value()

        self.th = [Thread(target=self.spin_roulette, args=(i, category_filter, button_filter, difficulty_filter, level_filter)) for i in range(music_count)] #멀티스레드로 룰렛 따로 돌리기(n번째 곡과 n+1 곡 사이에는 1초 정도의 텀을 두고 선곡됨)  
        
        for th in self.th:
            th.start()
            QTest.qWait(1000)
    
    def reset_multi_select(self):
        for i in range(MAX_MULTI_SELECT):
            self.multi_select_thumbnail_label[i].setPixmap(QPixmap())
            self.multi_select_song_name_label[i].setText('')
            self.multi_select_category_label[i].setText('')
            self.multi_select_button_label[i].setText('')
            self.multi_select_difficulty_label[i].setText('')
            self.multi_select_level_label[i].setText('')
            self.multi_select_thumbnail_label[i].setStyleSheet("font : 12px;")
            self.multi_select_song_name_label[i].setStyleSheet("font : 15px;")
            self.multi_select_category_label[i].setStyleSheet("font : 12px;")
            self.multi_select_button_label[i].setStyleSheet("font : 12px;")
            self.multi_select_difficulty_label[i].setStyleSheet("font : 12px;")
            self.multi_select_level_label[i].setStyleSheet("font : 12px;")
            
    def spin_roulette(self, index, category_filter, button_filter, difficulty_filter, level_filter):
        song_index_final = 0 #최종 선곡 인덱스 저장용

        while True:
            song_index = random.randrange(0, len(self.sname_replica))
            button_index = random.randrange(0, len(self.button))
            difficulty_index = random.randrange(0, len(self.difficulty))
            level = self.search_level(self.song_name[song_index], self.button[button_index], self.difficulty[difficulty_index])
            if self.option_checkbox_3.isChecked() and self.sname_replica[song_index] != '': #ONLY SONGS모드에서 중복 선곡 방지
                song_index_final = song_index 
                
                self.multi_select_song_name_label[index].setText(self.sname_replica[song_index])
                self.multi_select_category_label[index].setText(self.category[song_index])
                self.multi_select_button_label[index].setText('')
                self.multi_select_difficulty_label[index].setText('')
                self.multi_select_level_label[index].setText('')
                
                if os.path.exists('ICON/' + str(song_index+1) + '.png'):
                    self.multi_select_thumbnail_pixmap[index] = QPixmap('ICON/' + str(song_index+1) + '.png')
                else:
                    self.multi_select_thumbnail_pixmap[index] = QPixmap('ICON/NO IMAGE.png')
                    
                self.multi_select_thumbnail_label[index].setPixmap(self.multi_select_thumbnail_pixmap[index])  
                empty_label = QLabel()
                self.change_label_background(self.multi_select_category_label[index], empty_label)    
                break
            else:
                if (self.category[song_index] in category_filter) and (self.button[button_index] in button_filter) and (self.difficulty[difficulty_index] in difficulty_filter) and (level in level_filter) and ('-' not in level):
                    self.multi_select_song_name_label[index].setText(self.song_name[song_index])
                    self.multi_select_category_label[index].setText(self.category[song_index])
                    self.multi_select_button_label[index].setText(str(self.button[button_index]) + ' BUTTON')
                    self.multi_select_difficulty_label[index].setText(self.difficulty[difficulty_index])
                    self.multi_select_level_label[index].setText(self.search_level(self.song_name[song_index], self.button[button_index], self.difficulty[difficulty_index]))
                    
                    if os.path.exists('ICON/' + str(song_index+1) + '.png'):
                        self.multi_select_thumbnail_pixmap[index] = QPixmap('ICON/' + str(song_index+1) + '.png')
                    else:
                        self.multi_select_thumbnail_pixmap[index] = QPixmap('ICON/NO IMAGE.png')
                        
                    self.multi_select_thumbnail_label[index].setPixmap(self.multi_select_thumbnail_pixmap[index])  
                    empty_label = QLabel()
                    self.change_label_background(self.multi_select_category_label[index], empty_label)
                    break
                else:
                    continue
            
        self.sname_replica[song_index_final] = '' #선곡된 곡은 빈 칸으로
        
        if index == int(self.multi_select_count_spinbox.value())-1:
            self.multi_select_home_button.setEnabled(True)
        
class RouletteWidget(QWidget):
    def __init__(self, parent):
        super(RouletteWidget, self).__init__(parent)
        self.parent = parent
        self.count = 10
        self.roulette_rotate = 0
        self.rainbow_palette = [[255, 150, 138], [255, 174, 165], [255, 197, 191], [255, 216, 190], [255, 200, 162], [212, 240, 240], [143, 202, 202], [204, 226, 203], [182, 207, 182], [151, 193, 169]]
        self.max_time = 10000 #룰렛이 돌아가는 시간
        self.frame = 143 #초당 프레임 수
        self.time_per_frame = int(1000 / self.frame)
        self.roulette_speed = 1
        self.acceleration = random.randrange(400, 600)/1000
        self.input = ['' for i in range(MAX_ROULETTE_INPUT)]
        self.roulette_pin_flag = False
        self.init_UI()
        
    def init_UI(self):
        self.roulette_layout = QVBoxLayout()
        self.roulette_botton_layout = QVBoxLayout()
        self.roulette_button_layout = QHBoxLayout()
        self.spin_roulette_button = QPushButton('빙글빙글 돌아가는')
        self.home_button = QPushButton('확인')
        self.roulette_result_label = QLabel()
        self.roulette_input_layout = []
        self.roulette_input_field = []
        self.roulette_add_button = QPushButton('+')
        self.roulette_remove_button = QPushButton('-')
        self.roulette_probability_label = []
        
        self.roulette_layout.addWidget(self.roulette_result_label)
        self.roulette_botton_layout.addLayout(self.roulette_button_layout)
        self.roulette_button_layout.addWidget(self.roulette_add_button)
        self.roulette_button_layout.addWidget(self.spin_roulette_button)
        self.roulette_button_layout.addWidget(self.roulette_remove_button)
        
        for i in range(MAX_ROULETTE_INPUT):
            self.roulette_input_layout.append(QHBoxLayout())
            self.roulette_input_field.append(QLineEdit())
            self.roulette_probability_label.append(QLabel('10%'))
            
            self.roulette_botton_layout.addLayout(self.roulette_input_layout[i])
            self.roulette_input_layout[i].addWidget(self.roulette_input_field[i])
            self.roulette_input_layout[i].addWidget(self.roulette_probability_label[i])
               
        self.setLayout(self.roulette_layout)
        self.roulette_layout.addLayout(self.roulette_botton_layout)
        self.roulette_botton_layout.addWidget(self.home_button)
        
        self.roulette_result_label.setAlignment(Qt.AlignCenter)
        self.roulette_botton_layout.setAlignment(Qt.AlignBottom)
        
        self.roulette_add_button.clicked.connect(self.add_roulette)
        self.roulette_remove_button.clicked.connect(self.remove_roulette)
        self.spin_roulette_button.clicked.connect(self.spin_roulette)
        self.home_button.clicked.connect(self.parent.return_to_home)
        
        self.set_css()
    
    def set_css(self):
        self.roulette_result_label.setStyleSheet(
            'QLabel {'
            f'background-color : rgb(255,0,0);'
            'color : black;'
            'font : bold 15px;'
            '}'
        )
        self.roulette_result_label.setMaximumHeight(30)
        
        self.spin_roulette_button.setStyleSheet(
            'QPushButton {'
            f'background-color : rgb(247,241,237);'
            'color : rgb(47,54,95);'
            'font : bold;'
            '}'
            'QPushButton::hover {'
            f'background-color : rgb(47,54,95);'
            'color : rgb(247,241,237);'
            'font : bold;'
            '}'
            'QPushButton::pressed {'
            f'background-color : rgb(247,241,237);'
            'color : rgb(47,54,95);'
            'font : bold;'
            '}'
        )
        
        self.home_button.setStyleSheet(
            'QPushButton {'
            f'background-color : rgb(247,241,237);'
            'color : rgb(47,54,95);'
            'font : bold;'
            '}'
            'QPushButton::hover {'
            f'background-color : rgb(47,54,95);'
            'color : rgb(247,241,237);'
            'font : bold;'
            '}'
            'QPushButton::pressed {'
            f'background-color : rgb(247,241,237);'
            'color : rgb(47,54,95);'
            'font : bold;'
            '}'
        )
        
        for i, edit in enumerate(self.roulette_input_field):
            edit.setStyleSheet(
                'QLineEdit {'
                f'background-color : rgb(' + str(self.rainbow_palette[i][0]) + ',' + str(self.rainbow_palette[i][1]) + ',' + str(self.rainbow_palette[i][2]) + ',);'
                'color : rgb(47,54,95);'
                'font : bold 15px;'
                'border : 2px solid rgb(47,54,95);'
                '}'
            )
            edit.setMinimumHeight(27)
        
        
        self.roulette_add_button.setStyleSheet(
            'QPushButton {'
            f'background-color : rgb(247,241,237);'
            'color : rgb(47,54,95);'
            'font : bold 15px;'
            '}'
            'QPushButton::hover {'
            f'background-color : rgb(47,54,95);'
            'color : rgb(247,241,237);'
            'font : bold 15px;'
            '}'
            'QPushButton::pressed {'
            f'background-color : rgb(247,241,237);'
            'color : rgb(47,54,95);'
            'font : bold 15px;'
            '}'
        )
        
        self.roulette_remove_button.setStyleSheet(
            'QPushButton {'
            f'background-color : rgb(247,241,237);'
            'color : rgb(47,54,95);'
            'font : bold 15px;'
            '}'
            'QPushButton::hover {'
            f'background-color : rgb(47,54,95);'
            'color : rgb(247,241,237);'
            'font : bold 15px;'
            '}'
            'QPushButton::pressed {'
            f'background-color : rgb(247,241,237);'
            'color : rgb(47,54,95);'
            'font : bold 15px;'
            '}'
        )
        
        for attribute_label in self.roulette_probability_label:
            attribute_label.setStyleSheet(
                'QLabel {'
                f'color : rgb(47,54,95);'
                'font : bold;'
                '}'
            )
    
    def add_roulette(self):
        if self.count < MAX_ROULETTE_INPUT:
            self.count += 1
            self.roulette_input_field[self.count-1].setEnabled(True)
            self.roulette_input_field[self.count-1].setStyleSheet(
                'QLineEdit {'
                f'background-color : rgb(' + str(self.rainbow_palette[self.count-1][0]) + ',' + str(self.rainbow_palette[self.count-1][1]) + ',' + str(self.rainbow_palette[self.count-1][2]) + ',);'
                'color : rgb(47,54,95);'
                'font : bold 15px;'
                'border : 2px solid rgb(47,54,95);'
                '}'
            )
            self.input[self.count-1] = self.roulette_input_field[self.count-1].text()
            for i in range(self.count):
                self.roulette_probability_label[i].setText(str(int(100 / (self.count))) + '%')
            
            self.update()
    
    def remove_roulette(self):
        if self.count > 2:
            self.roulette_input_field[self.count-1].setEnabled(False)
            self.roulette_input_field[self.count-1].setStyleSheet(
                'QLineEdit {'
                f'background-color : rgb(128,128,128);'
                'color : rgb(47,54,95);'
                'font : bold 15px;'
                'border : 2px solid rgb(47,54,95);'
                '}'
            )
            self.input[self.count-1] = ''
            self.roulette_probability_label[self.count-1].setText('00%')
            for i in range(self.count-1):
                self.roulette_probability_label[i].setText(str(int(100 / (self.count-1))) + '%')
                
            self.count -= 1
            
            self.update()
    
    def spin_roulette(self):
        self.roulette_add_button.setEnabled(False)
        self.spin_roulette_button.setEnabled(False)
        self.spin_roulette_button.setText('빙글빙글 돌아가는 룰렛')
        self.roulette_remove_button.setEnabled(False)
        
        
        for i in range(self.count):
            self.input[i] = self.roulette_input_field[i].text()
            
        time = 0
        
        qp = QPainter()
        
        qp.begin(self)
        
        while(self.max_time > time):
            self.roulette_rotate += self.roulette_speed
            
            if self.max_time / 2 < time:
                self.roulette_speed -= self.acceleration
            else:
                self.roulette_speed += self.acceleration
            
            time += self.time_per_frame
            QTest.qWait(self.time_per_frame)
            self.update()
            
        qp.end()   
        
        self.roulette_add_button.setEnabled(True)
        self.spin_roulette_button.setEnabled(True)
        self.spin_roulette_button.setText('빙글빙글 돌아가는')
        self.roulette_remove_button.setEnabled(True)
    
    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.draw_roulette_pin(qp)
        self.draw_pie(qp, self.count, int(self.roulette_rotate)) #(Qpainter 객체, 항목 수, 룰렛 각도)
        qp.end()

    def draw_pie(self, qp, n, rotate):
        font = QFont('돋움', 10)
        font.setBold(True)
        qp.setFont(font)
        qp.drawText(int(W_width / 2) - 85, 30, '돌려돌려 돌림판')
        roulette_center_x = int(W_width / 2)
        roulette_center_y = 50 + (DIAMETER / 2)
        radius = DIAMETER / 2 * 0.75
        
        for i in range(n):
            qp.setPen(QPen(Qt.black, 2))
            qp.drawPie(int(W_width / 2 - DIAMETER / 2), 50, DIAMETER, DIAMETER, int(270 * 16 + 360 * 16 / n * i) - rotate, int(360 * 16 / n))
            color = QColor(self.rainbow_palette[i][0], self.rainbow_palette[i][1], self.rainbow_palette[i][2])
            brush = QBrush(color)
            qp.setBrush(brush)
            qp.drawPie(int(W_width / 2 - DIAMETER / 2), 50, DIAMETER, DIAMETER, int(270 * 16 + 360 * 16 / n * i) - rotate, int(360 * 16 / n))
        
        for i in range(n):
            font = QFont('돋움', 30 - int(len(self.roulette_input_field[i].text()) * 1.5))
            qp.setFont(font)
            angle = 110 + (360 / n)  * (i + 1) * (-1) + rotate / 16
            x = roulette_center_x + (radius * math.cos(math.radians(angle))) - 100
            y = roulette_center_y + (radius * math.sin(math.radians(angle))) - 20
            qp.drawText(QRect(int(x), int(y), 200, 50), Qt.AlignCenter, self.roulette_input_field[i].text())

        self.set_result_label(self.rainbow_palette[int(rotate / 360 / 16 * n % n)][0], self.rainbow_palette[int(rotate / 360 / 16 * n % n)][1], self.rainbow_palette[int(rotate / 360 / 16 * n % n)][2], int(rotate / 360 / 16 * n % n))     
    
    def draw_roulette_pin(self, qp):
        qp.setPen(QPen(Qt.red, 0))
        qp.setBrush(QBrush(Qt.red))
        #핀 정의
        points = QPolygon([
            QPoint(int(W_width / 2), 50 + DIAMETER),   # 상단 꼭지점
            QPoint(int(W_width / 2) - 10, 70 + DIAMETER),   # 하단 왼쪽 꼭지점
            QPoint(int(W_width / 2) + 10, 70 + DIAMETER)   # 하단 오른쪽 꼭지점
        ])

        #핀 그리기
        qp.drawPolygon(points)
        qp.setPen(QPen(Qt.black, 2))
        
    def set_result_label(self, red, green, blue, idx):
        self.roulette_result_label.setStyleSheet(
            'QLabel {'
            f'background-color : rgb(' + str(red) + ',' + str(green) + ',' + str(blue) + ');'
            'color : black;'
            'font : bold 22px;'
            '}'
        )
        self.roulette_result_label.setText(self.input[idx])
            
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())