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
        self.setWindowTitle("TMD Hesaplayıcı")
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
        
        self.entries = {}
        self.formul_butonlari()
    
    def formul_butonlari(self):
        self.formuller = {
            "Ana Kütle ve TMD Kütlesi": ["m1 (Ana kütle)", "m2 (TMD kütlesi)"],
            "Doğal Frekans ve Kütle Oranı": ["w1 (Doğal frekans)", "mü (Kütle oranı)", self.kutle_orani_hesapla],
            "Baranın Rijitliği": ["k1 (Ana yapı rijitliği)", self.bara_rijitlik_hesapla],
            "Optimum TMD Frekansı": ["w2_opt (Optimum frekans)", self.optimum_frekans_hesapla],
            "TMD Optimum Rijitliği": ["k2_opt (TMD Rijitliği)", self.optimum_rijitlik_hesapla],
            "TMD Optimum Sönüm Oranı": ["ksi_2_opt (Sönüm oranı)", self.optimum_sonum_orani_hesapla],
            "Optimum TMD Sönüm Katsayısı": ["c2_opt (Sönüm katsayısı)", self.optimum_sonum_katsayisi_hesapla]
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
            self.entries[deger] = entry
            entries.append(entry)
            container.addLayout(hbox)
        
        if callable(degerler[-1]):
            button = QPushButton("Hesapla")
            button.clicked.connect(lambda: degerler[-1]())
            button.setStyleSheet("background-color: #88C0D0; padding: 8px; border-radius: 5px; font-weight: bold;")
            container.addWidget(button)
        
        self.right_panel.addLayout(container)
    
    def kutle_orani_hesapla(self):
        try:
            m1 = float(self.entries["m1 (Ana kütle)"].text())
            m2 = float(self.entries["m2 (TMD kütlesi)"].text())
            mu = m2 / m1
            self.entries["mü (Kütle oranı)"].setText(str(mu))
            self.result_area.append(f"Kütle Oranı = {mu}")
        except ValueError:
            self.result_area.append("Hatalı giriş!")
    
    def bara_rijitlik_hesapla(self):
        try:
            w1 = float(self.entries["w1 (Doğal frekans)"].text())
            m1 = float(self.entries["m1 (Ana kütle)"].text())
            k1 = (w1 ** 2) * m1
            self.entries["k1 (Ana yapı rijitliği)"].setText(str(k1))
            self.result_area.append(f"Baranın Rijitliği = {k1} N/m")
        except ValueError:
            self.result_area.append("Hatalı giriş!")
    
    def optimum_frekans_hesapla(self):
        try:
            w1 = float(self.entries["w1 (Doğal frekans)"].text())
            mu = float(self.entries["mü (Kütle oranı)"].text())
            w2_opt = w1 / (1 + mu)
            self.entries["w2_opt (Optimum frekans)"].setText(str(w2_opt))
            self.result_area.append(f"Optimum TMD Frekansı = {w2_opt} rad/sn")
        except ValueError:
            self.result_area.append("Hatalı giriş!")
    
    def optimum_rijitlik_hesapla(self):
        try:
            w2_opt = float(self.entries["w2_opt (Optimum frekans)"].text())
            m2 = float(self.entries["m2 (TMD kütlesi)"].text())
            k2_opt = (w2_opt ** 2) * m2
            self.entries["k2_opt (TMD Rijitliği)"].setText(str(k2_opt))
            self.result_area.append(f"TMD Optimum Rijitliği = {k2_opt} N/m")
        except ValueError:
            self.result_area.append("Hatalı giriş!")
    
    def optimum_sonum_orani_hesapla(self):
        try:
            mu = float(self.entries["mü (Kütle oranı)"].text())
            ksi_2_opt = sqrt((3 * mu) / (8 * (1 + mu)))
            self.entries["ksi_2_opt (Sönüm oranı)"].setText(str(ksi_2_opt))
            self.result_area.append(f"TMD Optimum Sönüm Oranı = {ksi_2_opt}")
        except ValueError:
            self.result_area.append("Hatalı giriş!")
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    pencere = GrafikUygulamasi()
    pencere.show()
    sys.exit(app.exec())