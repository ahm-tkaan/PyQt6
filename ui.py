import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QComboBox, QLineEdit, QTextEdit)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from math import sqrt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

class GrafikUygulamasi(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt ile Modern Arayüz")
        self.setGeometry(100, 100, 700, 500)
        self.setStyleSheet("background-color: #2E3440; color: white;")
        
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        
        # Grafik Alanı
        self.fig = Figure(facecolor='#3B4252')
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvas(self.fig)
        self.layout.addWidget(self.canvas)
        
        # Sağ Panel
        self.right_panel = QVBoxLayout()
        self.layout.addLayout(self.right_panel)
        
        self.label = QLabel("Bir seçenek seç:")
        self.label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.right_panel.addWidget(self.label)
        
        self.combobox = QComboBox()
        self.combobox.addItems(["1. Kütle Oranı", "2. Baranın Rijitliği", "3. Optimum TMD Frekansı", "4. TMD Optimum Rijitliği", "5. TMD Optimum Sönüm Oranı", "6. Optimum TMD Sönüm Katsayısı"])
        self.combobox.currentIndexChanged.connect(self.secenek_degisti)
        self.combobox.setStyleSheet("background-color: #4C566A; padding: 5px; border-radius: 5px;")
        self.right_panel.addWidget(self.combobox)
        
        self.entry_list = []
        self.entry_container = QVBoxLayout()
        self.right_panel.addLayout(self.entry_container)
        
        self.button_update = QPushButton("Hesapla")
        self.button_update.clicked.connect(self.grafik_guncelle)
        self.button_update.setStyleSheet("background-color: #88C0D0; padding: 8px; border-radius: 5px; font-weight: bold;")
        self.right_panel.addWidget(self.button_update)
        
        self.result_area = QTextEdit()
        self.result_area.setReadOnly(True)
        self.result_area.setStyleSheet("background-color: #4C566A; color: white; padding: 5px; border-radius: 5px;")
        self.right_panel.addWidget(self.result_area)
        
        self.secenek_degisti()
    
    def secenek_degisti(self):
        for i in reversed(range(self.entry_container.count())):
            widget = self.entry_container.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()
        
        self.entry_list = []
        secim = self.combobox.currentText()
        input_labels = {
            "1. Kütle Oranı": ["m1 (Ana kütle)", "m2 (TMD kütlesi)"],
            "2. Baranın Rijitliği": ["w1 (Doğal frekans)", "m1 (Ana kütle)"],
            "3. Optimum TMD Frekansı": ["w1 (Doğal frekans)", "mü (Kütle oranı)"],
            "4. TMD Optimum Rijitliği": ["w2_opt (Optimum frekans)", "m2 (TMD kütlesi)"],
            "5. TMD Optimum Sönüm Oranı": ["mü (Kütle oranı)"],
            "6. Optimum TMD Sönüm Katsayısı": ["ksi_2_opt (Sönüm oranı)", "m2 (TMD kütlesi)", "w2_opt (Optimum frekans)"]
        }
        
        for label_text in input_labels[secim]:
            hbox = QHBoxLayout()
            lbl = QLabel(label_text + ":")
            lbl.setStyleSheet("color: white;")
            entry = QLineEdit()
            entry.setStyleSheet("background-color: #4C566A; color: white; padding: 5px; border-radius: 5px;")
            hbox.addWidget(lbl)
            hbox.addWidget(entry)
            self.entry_list.append(entry)
            self.entry_container.addLayout(hbox)
    
    def grafik_guncelle(self):
        self.ax.clear()
        self.ax.set_facecolor('#4C566A')
        try:
            veriler = [float(entry.text()) for entry in self.entry_list if entry.text()]
            secim = self.combobox.currentText()
            
            sonuc = ""
            if secim == "1. Kütle Oranı" and len(veriler) == 2:
                mü = veriler[1] / veriler[0]
                sonuc = f"Kütle Oranı = {mü:.4f}"
            elif secim == "2. Baranın Rijitliği" and len(veriler) == 2:
                k1 = (veriler[0]**2) * veriler[1]
                sonuc = f"Baranın Rijitliği = {k1:.4f} N/m"
            elif secim == "3. Optimum TMD Frekansı" and len(veriler) == 2:
                w2_opt = veriler[0] / (1 + veriler[1])
                sonuc = f"Optimum TMD Frekansı = {w2_opt:.4f} rad/sn"
            elif secim == "4. TMD Optimum Rijitliği" and len(veriler) == 2:
                k2_opt = (veriler[0] ** 2) * veriler[1]
                sonuc = f"TMD Optimum Rijitliği = {k2_opt:.4f} N/m"
            elif secim == "5. TMD Optimum Sönüm Oranı" and len(veriler) == 1:
                ksi_2_opt = sqrt((3 * veriler[0]) / (8 * (1 + veriler[0])))
                sonuc = f"TMD Optimum Sönüm Oranı = {ksi_2_opt:.4f}"
            elif secim == "6. Optimum TMD Sönüm Katsayısı" and len(veriler) == 3:
                c2_opt = veriler[0] * 2 * veriler[1] * veriler[2]
                sonuc = f"Optimum TMD Sönüm Katsayısı = {c2_opt:.4f} N.s/m"
            
            self.result_area.append(sonuc)
        except ValueError:
            self.result_area.append("Hatalı giriş! Lütfen sayısal değer girin.")
        
        self.canvas.draw()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    pencere = GrafikUygulamasi()
    pencere.show()
    sys.exit(app.exec())
