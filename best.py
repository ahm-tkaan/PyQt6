import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QTextEdit)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from math import sqrt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

class GrafikUygulamasi(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tırlamaz")
        self.setGeometry(100, 100, 700, 600)
        self.setStyleSheet("background-color: #2E3440; color: white;")
        
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        
        self.fig = Figure(facecolor='#3B4252')
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvas(self.fig)
        self.layout.addWidget(self.canvas)
        
        self.right_panel = QVBoxLayout()
        self.layout.addLayout(self.right_panel)
        
        self.result_area = QTextEdit()
        self.result_area.setReadOnly(True)
        self.result_area.setStyleSheet("background-color: #4C566A; color: white; padding: 5px; border-radius: 5px;")
        self.right_panel.addWidget(self.result_area)
        
        self.formul_butonlari()
    
    def formul_butonlari(self):
        self.formuller = {
            "Kütle Oranı": ["m1 (Ana kütle)", "m2 (TMD kütlesi)", self.kutle_orani_hesapla],
            "Baranın Rijitliği": ["w1 (Doğal frekans)", "m1 (Ana kütle)", self.bara_rijitlik_hesapla],
            "Optimum TMD Frekansı": ["w1 (Doğal frekans)", "mü (Kütle oranı)", self.optimum_frekans_hesapla],
            "TMD Optimum Rijitliği": ["w2_opt (Optimum frekans)", "m2 (TMD kütlesi)", self.optimum_rijitlik_hesapla],
            "TMD Optimum Sönüm Oranı": ["mü (Kütle oranı)", self.optimum_sonum_orani_hesapla],
            "Optimum TMD Sönüm Katsayısı": ["ksi_2_opt (Sönüm oranı)", "m2 (TMD kütlesi)", "w2_opt (Optimum frekans)", self.optimum_sonum_katsayisi_hesapla]
        }
        
        for formul, degerler in self.formuller.items():
            self.ekle_formul_butonu(formul, degerler)
    
    def ekle_formul_butonu(self, ad, degerler):
        container = QVBoxLayout()
        label = QLabel(ad)
        label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        container.addWidget(label)
        
        entries = []
        for deger in degerler[:-1]:
            hbox = QHBoxLayout()
            lbl = QLabel(deger + ":")
            lbl.setStyleSheet("color: white;")
            entry = QLineEdit()
            entry.setStyleSheet("background-color: #4C566A; color: white; padding: 5px; border-radius: 5px;")
            hbox.addWidget(lbl)
            hbox.addWidget(entry)
            entries.append(entry)
            container.addLayout(hbox)
        
        button = QPushButton("Hesapla")
        button.clicked.connect(lambda: degerler[-1](entries))
        button.setStyleSheet("background-color: #88C0D0; padding: 8px; border-radius: 5px; font-weight: bold;")
        container.addWidget(button)
        
        self.right_panel.addLayout(container)
    
    def kutle_orani_hesapla(self, entries):
        try:
            m1, m2 = map(float, [entry.text() for entry in entries])
            sonuc = f"Kütle Oranı = {m2/m1}"
            self.result_area.append(sonuc)
        except ValueError:
            self.result_area.append("Hatalı giriş!")
    
    def bara_rijitlik_hesapla(self, entries):
        try:
            w1, m1 = map(float, [entry.text() for entry in entries])
            k1 = (w1**2) * m1
            sonuc = f"Baranın Rijitliği = {k1} N/m"
            self.result_area.append(sonuc)
        except ValueError:
            self.result_area.append("Hatalı giriş!")
    
    def optimum_frekans_hesapla(self, entries):
        try:
            w1, mu = map(float, [entry.text() for entry in entries])
            w2_opt = w1 / (1 + mu)
            sonuc = f"Optimum TMD Frekansı = {w2_opt} rad/sn"
            self.result_area.append(sonuc)
        except ValueError:
            self.result_area.append("Hatalı giriş!")
    
    def optimum_rijitlik_hesapla(self, entries):
        try:
            w2_opt, m2 = map(float, [entry.text() for entry in entries])
            k2_opt = (w2_opt ** 2) * m2
            sonuc = f"TMD Optimum Rijitliği = {k2_opt} N/m"
            self.result_area.append(sonuc)
        except ValueError:
            self.result_area.append("Hatalı giriş!")
    
    def optimum_sonum_orani_hesapla(self, entries):
        try:
            mu = float(entries[0].text())
            ksi_2_opt = sqrt((3 * mu) / (8 * (1 + mu)))
            sonuc = f"TMD Optimum Sönüm Oranı = {ksi_2_opt}"
            self.result_area.append(sonuc)
        except ValueError:
            self.result_area.append("Hatalı giriş!")
    
    def optimum_sonum_katsayisi_hesapla(self, entries):
        try:
            ksi_2_opt, m2, w2_opt = map(float, [entry.text() for entry in entries])
            c2_opt = ksi_2_opt * 2 * m2 * w2_opt
            sonuc = f"Optimum TMD Sönüm Katsayısı = {c2_opt} N.s/m"
            self.result_area.append(sonuc)
        except ValueError:
            self.result_area.append("Hatalı giriş!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    pencere = GrafikUygulamasi()
    pencere.show()
    sys.exit(app.exec())
