import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QFileDialog, QLabel, QPushButton, QListWidget,
    QHBoxLayout, QVBoxLayout, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PIL import Image, ImageOps
from PIL.ImageFilter import SHARPEN

# Инициализация приложения
app = QApplication([])
win = QWidget()
win.resize(1000, 800)
win.setWindowTitle('Photo Editor')

# Виджеты интерфейса
lb_image = QLabel("")
lb_image.setFixedSize(800, 600)
btn_dir = QPushButton("Папка")
lw_files = QListWidget()

btn_left = QPushButton("Лево")
btn_right = QPushButton("Право")
btn_flip = QPushButton("Зеркало")
btn_sharp = QPushButton("Резкость")
btn_bw = QPushButton("Ч/Б")
btn_reset = QPushButton("Сбросить")

# Компоновка элементов
layout_main = QHBoxLayout()
layout_left = QVBoxLayout()
layout_right = QVBoxLayout()
layout_tools = QHBoxLayout()

layout_left.addWidget(btn_dir)
layout_left.addWidget(lw_files)
layout_right.addWidget(lb_image, 95)

layout_tools.addWidget(btn_left)
layout_tools.addWidget(btn_right)
layout_tools.addWidget(btn_flip)
layout_tools.addWidget(btn_sharp)
layout_tools.addWidget(btn_bw)
layout_tools.addWidget(btn_reset)

layout_right.addLayout(layout_tools)
layout_main.addLayout(layout_left, 20)
layout_main.addLayout(layout_right, 80)

win.setLayout(layout_main)
win.show()

# Рабочая директория
workdir = ''

def filter_files(files, extensions):
    """Фильтрация файлов по заданным расширениям."""
    return [f for f in files if any(f.endswith(ext) for ext in extensions)]

def choose_workdir():
    """Выбор рабочей директории."""
    global workdir
    workdir = QFileDialog.getExistingDirectory()

def show_filenames_list():
    """Отображение списка изображений в рабочей папке."""
    extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
    choose_workdir()
    filenames = filter_files(os.listdir(workdir), extensions)
    lw_files.clear()
    lw_files.addItems(filenames)

class ImageProcessor:
    def __init__(self):
        self.image = None
        self.original_image = None  
        self.filename = None
        self.save_dir = "Modified/"

    def load_image(self, filename):
        """Загрузка изображения."""
        self.filename = filename
        fullname = os.path.join(workdir, filename)
        self.image = Image.open(fullname)
        self.original_image = self.image.copy()

    def reset(self):
        """Сброс изображения к оригинальному состоянию."""
        self.image = self.original_image.copy()
        self.save_and_show_image()

    def save_image(self):
        """Сохранение изображения в папку."""
        path = os.path.join(workdir, self.save_dir)
        os.makedirs(path, exist_ok=True)
        fullname = os.path.join(path, self.filename)
        self.image.save(fullname)

    def apply_filter(self, filter_function):
        """Применение фильтра к изображению и обновление его."""
        self.image = filter_function(self.image)
        self.save_and_show_image()

    def do_bw(self):
        self.apply_filter(ImageOps.grayscale)

    def do_left(self):
        self.apply_filter(lambda img: img.transpose(Image.ROTATE_90))

    def do_right(self):
        self.apply_filter(lambda img: img.transpose(Image.ROTATE_270))

    def do_flip(self):
        self.apply_filter(lambda img: img.transpose(Image.FLIP_LEFT_RIGHT))

    def do_sharpen(self):
        self.apply_filter(lambda img: img.filter(SHARPEN))

    def save_and_show_image(self):
        """Сохранение и отображение изображения."""
        self.save_image()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.show_image(image_path)

    def show_image(self, path):
        """Отображение изображения в QLabel."""
        lb_image.hide()
        pixmap = QPixmap(path).scaled(lb_image.width(), lb_image.height(), Qt.KeepAspectRatio)
        lb_image.setPixmap(pixmap)
        lb_image.show()

def show_chosen_image():
    """Отображение выбранного изображения."""
    if lw_files.currentRow() >= 0:
        filename = lw_files.currentItem().text()
        workimage.load_image(filename)
        workimage.show_image(os.path.join(workdir, workimage.filename))

# Обработчик закрытия окна
def close_event(event):
    reply = QMessageBox.question(win, 'Выход', 'Вы точно хотите выйти?',
                                 QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
    if reply == QMessageBox.Yes:
        event.accept()
    else:
        event.ignore()

win.closeEvent = close_event

# Создание экземпляра обработчика изображений
workimage = ImageProcessor()
lw_files.currentRowChanged.connect(show_chosen_image)

# Подключение кнопок к обработчикам
btn_bw.clicked.connect(workimage.do_bw)
btn_left.clicked.connect(workimage.do_left)
btn_right.clicked.connect(workimage.do_right)
btn_sharp.clicked.connect(workimage.do_sharpen)
btn_flip.clicked.connect(workimage.do_flip)
btn_reset.clicked.connect(workimage.reset)
btn_dir.clicked.connect(show_filenames_list)

# Запуск приложения
app.exec_()
