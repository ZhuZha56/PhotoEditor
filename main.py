import os
from PyQt5.QtWidgets import (
    QApplication, QWidget,
    QFileDialog,
    QLabel, QPushButton, QListWidget,
    QHBoxLayout, QVBoxLayout
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PIL import Image
from PIL import ImageOps
from PIL.ImageFilter import SHARPEN

app = QApplication([])
win = QWidget()
win.resize(1000, 800)
win.setWindowTitle('Easy Editor')

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

r = QHBoxLayout()
l1 = QVBoxLayout()        
l2 = QVBoxLayout()
l1.addWidget(btn_dir)
l1.addWidget(lw_files)
l2.addWidget(lb_image, 95)

r_tools = QHBoxLayout()
r_tools.addWidget(btn_left)
r_tools.addWidget(btn_right)
r_tools.addWidget(btn_flip)
r_tools.addWidget(btn_sharp)
r_tools.addWidget(btn_bw)
r_tools.addWidget(btn_reset)
l2.addLayout(r_tools)

r.addLayout(l1, 20)
r.addLayout(l2, 80)
win.setLayout(r)

win.show()

workdir = ''

def filter(files, extensions):
    return [filename for filename in files if any(filename.endswith(ext) for ext in extensions)]

def chooseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()

def showFilenamesList():
    extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
    chooseWorkdir()
    filenames = filter(os.listdir(workdir), extensions)

    lw_files.clear()
    lw_files.addItems(filenames)

class ImageProcessor:
    def __init__(self):
        self.image = None
        self.original_image = None  
        self.filename = None
        self.save_dir = "Modified/"

    def loadImage(self, filename):
        self.filename = filename
        fullname = os.path.join(workdir, filename)
        self.image = Image.open(fullname)
        self.original_image = self.image.copy()  

    def reset(self):
        self.image = self.original_image.copy()
        self.saveAndShowImage()

    def saveImage(self):
        path = os.path.join(workdir, self.save_dir)
        os.makedirs(path, exist_ok=True)
        fullname = os.path.join(path, self.filename)
        self.image.save(fullname)

    def do_bw(self):
        self.image = ImageOps.grayscale(self.image)
        self.saveAndShowImage()

    def do_left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveAndShowImage()

    def do_right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveAndShowImage()

    def do_flip(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveAndShowImage()

    def do_sharpen(self):
        self.image = self.image.filter(SHARPEN)
        self.saveAndShowImage()

    def saveAndShowImage(self):
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def showImage(self, path):
        lb_image.hide()
        pixmapimage = QPixmap(path)
        w, h = lb_image.width(), lb_image.height()
        pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
        lb_image.setPixmap(pixmapimage)
        lb_image.show()

def showChosenImage():
    if lw_files.currentRow() >= 0:
        filename = lw_files.currentItem().text()
        workimage.loadImage(filename)
        workimage.showImage(os.path.join(workdir, workimage.filename))


workimage = ImageProcessor()
lw_files.currentRowChanged.connect(showChosenImage)

btn_bw.clicked.connect(workimage.do_bw)
btn_left.clicked.connect(workimage.do_left)
btn_right.clicked.connect(workimage.do_right)
btn_sharp.clicked.connect(workimage.do_sharpen)
btn_flip.clicked.connect(workimage.do_flip)
btn_reset.clicked.connect(workimage.reset)

btn_dir.clicked.connect(showFilenamesList)

app.exec_()
