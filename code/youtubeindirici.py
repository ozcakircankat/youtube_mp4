import os
from PyQt5.QtWidgets import QGridLayout,QLabel,QListWidget,QLineEdit,QPushButton,QMessageBox,\
QApplication,QWidget,QProgressBar
from PyQt5.QtGui import QIcon,QPixmap
from PyQt5.QtCore import QTimer
from youtube_dl import YoutubeDL
#-----------------------------------------------------------------------------------------------------------------------

class Uygulama(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Youtube [HD] MP4 İndirici | Cankat Özçakır")
        self.setWindowIcon(QIcon("C:/Users/AYTEN/Desktop/mp4.ico"))
        self.setMaximumSize(600,500)
        self.resize(600,500)
        self.layout= QGridLayout(self)

        self.liste = QListWidget(self)

        self.yazı2 = QLabel(self)
        self.yazı2.setText("İndirdiğiniz Videolar:")

        self.yazı = QLabel(self)
        self.yazı.setText("İndirme Linki:")

        self.label = QLabel(self)
        self.pixmap = QPixmap('C:/Users/AYTEN/Desktop/youtube-mp4.png')
        self.label.setPixmap(self.pixmap)

        self.veri = QLineEdit(self)

        self.buton = QPushButton(self)
        self.buton.setText("İndir!")

        self.bilgilendirme = QLabel(self)
        self.bilgilendirme.setText("Bilgi: İndirme yaparken url'nin başında 'https:' olmalı.\nBilgi: Videolar, programı"
                                   " hangi dizine koyarsanız oraya kaydedilir.")

        self.yuzde = QProgressBar(self)
        self.yuzde.setValue(0)


        self.layout.addWidget(self.yazı2,0,0,1,1)
        self.layout.addWidget(self.liste,0,1,2,2)
        self.layout.addWidget(self.yazı,1,0,1,1)
        self.layout.addWidget(self.veri,1,1,1,2)
        self.layout.addWidget(self.buton,2,0,1,1)
        self.layout.addWidget(self.bilgilendirme,2,1,1,1)
        self.layout.addWidget(self.label,2,2,1,1)
        self.layout.addWidget(self.yuzde,3,0,1,2)

        self.buton.clicked.connect(self.indir)

#-----------------------------------------------------------------------------------------------------------------------

    def bilgilendirmeYazisi(self):
        self.bilgilendirme.setText("Bilgi: İndirme yaparken url'nin başında 'https:' olmalı.\nBilgi: Videolar, programı"
                                   " hangi dizine koyarsanız oraya kaydedilir.")

    def hook(self,info):

        if info["status"] == "downloading":
            self.buton.setEnabled(False)
            QApplication.processEvents()

        elif info["status"] == "finished":
             QApplication.processEvents()

        else:
            pass



    def bariSekillendir(self):
        self.tamamlanan=0

        while self.tamamlanan < 100:
            self.tamamlanan+=0.00003
            self.yuzde.setValue(self.tamamlanan)
            QApplication.processEvents()


        def bariTemizle(self):
            if self.tamamlanan == 100:
                self.yuzde.setValue(0)
                QApplication.processEvents()

            pass



    def indir(self):

        os.getcwd()
        os.chdir(os.getcwd())  # Videoların programın olduğu dizine kaydetmesini bu iki satır sağlıyor.

        if self.veri.text().startswith("https://www.youtube.com/"):

            ydl_ayarlar = {
                'noplaylist': True,
                'progress_hooks': [self.hook]
            }

            QMessageBox.information(self, "Videonuz işlenmeye hazır",
                                    "İşleme süreci indirdiğiniz videonun boyutuna bağlıdır bekleme süreniz de buna göre "
                                    "değişebilir.İşleme süreci bittiğinde bar dolmaya başlayacak ve video indirilecektir.")

            self.setWindowTitle("Videonuz İşleniyor....")
            ydl = YoutubeDL(ydl_ayarlar)
            ydl.add_default_info_extractors()
            info = ydl.extract_info(self.veri.text(), download=True)
            self.setWindowTitle("Videonuz İndiriliyor....")
            self.buton.setEnabled(False)
            self.bariSekillendir()
            indirilen_oge = info["title"]
            self.liste.insertItem(0, indirilen_oge)
            self.setWindowTitle("Youtube [HD] MP4 İndirici | Cankat Özçakır")
            QMessageBox.information(self, "İndirme Başarılı!", "İndirme işlemini başarıyla gerçekleştirdiniz.")
            self.buton.setEnabled(True)

        elif not self.veri.text():
            self.bilgilendirme.setText("Herhangi bir adres belirtmediniz.")
            QTimer.singleShot(2000,self.bilgilendirmeYazisi)

        else:
            self.bilgilendirme.setText("Yalnızca Youtube'dan video indirebilirsiniz.")
            QTimer.singleShot(2000, self.bilgilendirmeYazisi)


    #-----------------------------------------------------------------------------------------------------------------------

uygulama = QApplication([])
pencere = Uygulama()
pencere.show()
uygulama.exec_()


