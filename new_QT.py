import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton, QLineEdit, QListWidget)
from PyQt6.QtGui import QPalette, QColor, QFont, QIcon, QPixmap
from PyQt6.QtCore import Qt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

class GrafikPenceresi(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TD Hesaplama")
        self.setGeometry(100, 100, 800, 500)
        self.setWindowIcon(QIcon("favicon.png"))

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QHBoxLayout()
        self.central_widget.setLayout(self.layout)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#26a9c9"))  # Yeni arka plan rengi
        self.setPalette(palette)

        # Sol panel (logo için)
        self.left_panel = QVBoxLayout()
        self.layout.addLayout(self.left_panel)

        # Logo ekleme (sol üst köşe)
        self.logo_label = QLabel()
        self.logo_label.setPixmap(QPixmap("logo.png").scaled(120, 120, Qt.AspectRatioMode.KeepAspectRatio))
        self.left_panel.addWidget(self.logo_label, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

        # Grafik alanı
        self.figure = Figure(facecolor="#26a9c9")
        self.ax = self.figure.add_subplot(111)
        self.ax.set_facecolor("#26a9c9")  # Grafik alanı arka planı güncellendi
        self.ax.tick_params(colors='white')  # Eksen çizgileri beyaz
        self.ax.xaxis.label.set_color('white')  # X ekseni etiketi beyaz
        self.ax.yaxis.label.set_color('white')  # Y ekseni etiketi beyaz
        self.ax.title.set_color('white')  # Grafik başlığı beyaz
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)

        # Sağ panel
        self.right_panel = QVBoxLayout()
        self.layout.addLayout(self.right_panel)

        self.label = QLabel("Bir seçenek seç:")
        self.label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.label.setStyleSheet("color: white;")
        self.right_panel.addWidget(self.label)

        self.combobox = QComboBox()
        self.combobox.addItems(["Seçenek 1", "Seçenek 2", "Seçenek 3"])
        self.combobox.currentIndexChanged.connect(self.secenek_degisti)
        self.combobox.setStyleSheet("background-color: #003366; color: white; padding: 5px; border-radius: 10px; border: 1px solid white;")
        self.right_panel.addWidget(self.combobox)

        self.veri_girisleri = []
        self.veri_paneli = QVBoxLayout()
        self.right_panel.addLayout(self.veri_paneli)

        self.buton_guncelle = QPushButton("Grafiği Güncelle")
        self.buton_guncelle.setStyleSheet("background-color: #f58220; color: white; padding: 10px; border-radius: 10px; font-weight: bold;")
        self.buton_guncelle.clicked.connect(self.grafik_guncelle)
        self.right_panel.addWidget(self.buton_guncelle)

        self.listbox_sonuclar = QListWidget()
        self.listbox_sonuclar.setStyleSheet("background-color: #003366; color: white; border-radius: 10px; border: 1px solid white;")
        self.right_panel.addWidget(self.listbox_sonuclar)

        self.buton_kaydet = QPushButton("Grafiği Kaydet")
        self.buton_kaydet.setStyleSheet("background-color: #f58220; color: white; padding: 10px; border-radius: 10px; font-weight: bold;")
        self.buton_kaydet.clicked.connect(self.grafik_kaydet)
        self.right_panel.addWidget(self.buton_kaydet)

        self.secenek_degisti()

    def grafik_guncelle(self):
        self.ax.clear()
        self.ax.set_facecolor("#26a9c9")  # Güncellenmiş grafik arka plan rengi
        self.ax.tick_params(colors='white')  # Eksen çizgileri beyaz
        self.ax.xaxis.label.set_color('white')  # X ekseni etiketi beyaz
        self.ax.yaxis.label.set_color('white')  # Y ekseni etiketi beyaz
        self.ax.title.set_color('white')  # Grafik başlığı beyaz
        self.listbox_sonuclar.clear()
        
        try:
            veriler = [float(entry.text()) for entry in self.veri_girisleri]
            self.ax.plot(range(1, len(veriler) + 1), veriler, marker='o', color='white', linestyle='-')
            
            for i, veri in enumerate(veriler, start=1):
                self.listbox_sonuclar.addItem(f"Veri {i}: {veri}")
            
            if sum(veriler) > 5:
                self.listbox_sonuclar.addItem("Toplam 5'ten fazla!")
            
        except ValueError:
            self.listbox_sonuclar.addItem("Geçersiz giriş!")
        
        self.canvas.draw()
    
    def grafik_kaydet(self):
        self.figure.savefig("grafik.png")
        self.listbox_sonuclar.addItem("Grafik 'grafik.png' olarak kaydedildi!")
    
    def secenek_degisti(self):
        for widget in self.veri_girisleri:
            widget.deleteLater()
        self.veri_girisleri.clear()
        
        secim = self.combobox.currentText()
        veri_sayisi = {"Seçenek 1": 2, "Seçenek 2": 3, "Seçenek 3": 4}.get(secim, 2)
        
        for i in range(veri_sayisi):
            hbox = QHBoxLayout()
            label = QLabel(f"Veri {i+1}:")
            label.setStyleSheet("color: white;")
            entry = QLineEdit()
            entry.setStyleSheet("background-color: #003366; color: white; padding: 5px; border-radius: 10px; border: 1px solid white;")
            self.veri_girisleri.append(entry)
            
            hbox.addWidget(label)
            hbox.addWidget(entry)
            self.veri_paneli.addLayout(hbox)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    pencere = GrafikPenceresi()
    pencere.show()
    sys.exit(app.exec())