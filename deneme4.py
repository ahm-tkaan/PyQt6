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
        self.setWindowTitle("PyQt ile Modern Arayüz")
        self.setGeometry(100, 100, 700, 600)
        self.setStyleSheet("background-color: #2E3440; color: white;")
        
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        
        self.result_area = QTextEdit()
        self.result_area.setReadOnly(True)
        self.result_area.setStyleSheet("background-color: #4C566A; color: white; padding: 5px; border-radius: 5px;")
        self.layout.addWidget(self.result_area)
        
        self.entries = {}
        self.formul_butonlari()
    
    def formul_butonlari(self):
        self.formuller = {
            "Kütle Oranı": ["Ana kütle (m1)", "TMD kütlesi (m2)", self.kutle_orani_hesapla],
            "Baranın Rijitliği": ["Doğal frekans (w1)", "Ana kütle (m1)", self.bara_rijitlik_hesapla],
            "Optimum TMD Frekansı": ["Doğal frekans (w1)", "Kütle oranı (mü)", self.optimum_frekans_hesapla],
            "TMD Optimum Rijitliği": ["Optimum frekans (w2_opt)", "TMD kütlesi (m2)", self.optimum_rijitlik_hesapla],
            "TMD Optimum Sönüm Oranı": ["Kütle oranı (mü)", self.optimum_sonum_orani_hesapla],
            "Optimum TMD Sönüm Katsayısı": ["Sönüm oranı (ksi_2_opt)", "TMD kütlesi (m2)", "Optimum frekans (w2_opt)", self.optimum_sonum_katsayisi_hesapla]
        }
        
        for formul, degerler in self.formuller.items():
            self.ekle_formul_butonu(formul, degerler)
    
    def ekle_formul_butonu(self, ad, degerler):
        container = QVBoxLayout()
        label = QLabel(ad)
        label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        container.addWidget(label)
        
        entry_keys = degerler[:-1]
        for key in entry_keys:
            if key not in self.entries:
                hbox = QHBoxLayout()
                lbl = QLabel(key + ":")
                lbl.setStyleSheet("color: white;")
                entry = QLineEdit()
                entry.setStyleSheet("background-color: #4C566A; color: white; padding: 5px; border-radius: 5px;")
                hbox.addWidget(lbl)
                hbox.addWidget(entry)
                self.entries[key] = entry
                self.layout.addLayout(hbox)
        
        button = QPushButton("Hesapla")
        button.clicked.connect(lambda: degerler[-1]())
        button.setStyleSheet("background-color: #88C0D0; padding: 8px; border-radius: 5px; font-weight: bold;")
        container.addWidget(button)
        
        self.layout.addLayout(container)
    
    def get_values(self, keys):
        try:
            return [float(self.entries[key].text()) for key in keys]
        except ValueError:
            self.result_area.append("Hatalı giriş!")
            return None
    
    def kutle_orani_hesapla(self):
        values = self.get_values(["Ana kütle (m1)", "TMD kütlesi (m2)"])
        if values:
            sonuc = f"Kütle Oranı = {values[1]/values[0]:.4f}"
            self.result_area.append(sonuc)
    
    def bara_rijitlik_hesapla(self):
        values = self.get_values(["Doğal frekans (w1)", "Ana kütle (m1)"])
        if values:
            sonuc = f"Baranın Rijitliği = {(values[0]**2) * values[1]:.4f} N/m"
            self.result_area.append(sonuc)
    
    def optimum_frekans_hesapla(self):
        values = self.get_values(["Doğal frekans (w1)", "Kütle oranı (mü)"])
        if values:
            sonuc = f"Optimum TMD Frekansı = {values[0] / (1 + values[1]):.4f} rad/sn"
            self.result_area.append(sonuc)
    
    def optimum_rijitlik_hesapla(self):
        values = self.get_values(["Optimum frekans (w2_opt)", "TMD kütlesi (m2)"])
        if values:
            sonuc = f"TMD Optimum Rijitliği = {(values[0] ** 2) * values[1]:.4f} N/m"
            self.result_area.append(sonuc)
    
    def optimum_sonum_orani_hesapla(self):
        values = self.get_values(["Kütle oranı (mü)"])
        if values:
            sonuc = f"TMD Optimum Sönüm Oranı = {sqrt((3 * values[0]) / (8 * (1 + values[0]))):.4f}"
            self.result_area.append(sonuc)
    
    def optimum_sonum_katsayisi_hesapla(self):
        values = self.get_values(["Sönüm oranı (ksi_2_opt)", "TMD kütlesi (m2)", "Optimum frekans (w2_opt)"])
        if values:
            sonuc = f"Optimum TMD Sönüm Katsayısı = {values[0] * 2 * values[1] * values[2]:.4f} N.s/m"
            self.result_area.append(sonuc)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    pencere = GrafikUygulamasi()
    pencere.show()
    sys.exit(app.exec())
