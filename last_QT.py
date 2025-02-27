import sys
import random
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton, QLineEdit, QListWidget, QFrame, QSizePolicy)
from PyQt6.QtGui import QPalette, QColor, QFont, QIcon, QPixmap
from PyQt6.QtCore import Qt, QSize, QEvent
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
import matplotlib as mpl

# Color scheme constants
LIGHT_LAVENDER = "#DFC5FE"
GRAPE_PURPLE = "#5D1451"
NEON_BLUE = "#04D9FF"

class CloseButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(20, 20)  # Smaller size
        self.setText("✕")  # X symbol
        self.setFont(QFont("Arial", 9, QFont.Weight.Bold))
        self.setStyleSheet("""
            QPushButton {
                background-color: #d32f2f;  /* Darker red */
                color: white;
                border-radius: 10px;
                border: none;
            }
            QPushButton:hover {
                background-color: #ff5252;
            }
        """)

class MinimizeButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(20, 20)  # Smaller size
        self.setText("_")  # Underscore symbol for minimize
        self.setFont(QFont("Arial", 9, QFont.Weight.Bold))
        self.setStyleSheet("""
            QPushButton {
                background-color: #f57f17;  /* Darker yellow */
                color: white;
                border-radius: 10px;
                border: none;
            }
            QPushButton:hover {
                background-color: #ffb300;
            }
        """)

class MaximizeButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(20, 20)  # Smaller size
        self.setText("□")  # Square symbol for maximize
        self.setFont(QFont("Arial", 9, QFont.Weight.Bold))
        self.setStyleSheet("""
            QPushButton {
                background-color: #2e7d32;  /* Darker green */
                color: white;
                border-radius: 10px;
                border: none;
            }
            QPushButton:hover {
                background-color: #4caf50;
            }
        """)

class CustomTitleBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setFixedHeight(40)
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(GRAPE_PURPLE))
        self.setPalette(palette)
        
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(10, 0, 10, 0)
        
        self.title_label = QLabel("Development and Optimization of Vibration-Damped Tool Holders for High Length-to-Diameter Boring Operations")
        self.title_label.setStyleSheet(f"color: {LIGHT_LAVENDER}; font-weight: bold; font-size: 14px;")
        
        self.btn_minimize = MinimizeButton()
        self.btn_maximize = MaximizeButton()
        self.btn_close = CloseButton()
        
        self.btn_minimize.clicked.connect(self.parent.showMinimized)
        self.btn_maximize.clicked.connect(self.toggle_maximize)
        self.btn_close.clicked.connect(self.parent.close)
        
        self.layout.addWidget(self.title_label)
        self.layout.addStretch()
        self.layout.addWidget(self.btn_minimize)
        self.layout.addWidget(self.btn_maximize)
        self.layout.addWidget(self.btn_close)
        
        self.start = None
        
    def toggle_maximize(self):
        if self.parent.isMaximized():
            self.parent.showNormal()
        else:
            self.parent.showMaximized()
    
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.start = event.pos()
        return super().mousePressEvent(event)
    
    def mouseMoveEvent(self, event):
        if self.start is not None and event.buttons() == Qt.MouseButton.LeftButton:
            self.parent.move(self.parent.pos() + event.pos() - self.start)
        return super().mouseMoveEvent(event)
    
    def mouseReleaseEvent(self, event):
        self.start = None
        return super().mouseReleaseEvent(event)
    
    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.toggle_maximize()
        return super().mouseDoubleClickEvent(event)

class GrafikPenceresi(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TD Hesaplama")
        self.setGeometry(100, 100, 800, 500)
        self.setWindowIcon(QIcon("favicon.png"))
        
        # Color scheme for graph
        self.colors = [NEON_BLUE, '#ff7f0e', GRAPE_PURPLE, LIGHT_LAVENDER, '#9467bd', 
                        '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf',
                        '#f58220', '#e6194B', '#3cb44b', '#4363d8', '#911eb4']
        
        # Çerçeve dışında kullanım için flag'leri ayarlama
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # Ana container oluşturma (kenar yuvarlama için)
        self.container = QFrame()
        self.container.setObjectName("MainContainer")
        self.container.setStyleSheet(f"""
            #MainContainer {{
                background-color: {LIGHT_LAVENDER};
                border-radius: 10px;
                border: 2px solid {GRAPE_PURPLE};
            }}
        """)
        
        self.setCentralWidget(self.container)
        
        # Ana düzen
        self.main_layout = QVBoxLayout(self.container)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        # Özel başlık çubuğu ekleme
        self.title_bar = CustomTitleBar(self)
        self.main_layout.addWidget(self.title_bar)
        
        # İçerik konteynerı
        self.content_container = QWidget()
        self.content_layout = QHBoxLayout(self.content_container)
        self.content_layout.setContentsMargins(10, 10, 10, 10)
        
        self.main_layout.addWidget(self.content_container)
        
        # Sol panel (logo için)
        self.left_panel = QVBoxLayout()
        self.left_panel.setContentsMargins(0, 0, 10, 0)
        
        # Left panel should take minimal space
        left_widget = QWidget()
        left_widget.setLayout(self.left_panel)
        left_widget.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        self.content_layout.addWidget(left_widget)

        # Logo ekleme (sol üst köşe)
        self.logo_label = QLabel()
        self.logo_label.setPixmap(QPixmap("logo.png").scaled(80, 80, Qt.AspectRatioMode.KeepAspectRatio))
        self.left_panel.addWidget(self.logo_label, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        self.left_panel.addStretch()

        # Middle panel for graph - this should be the main focus
        self.middle_panel = QVBoxLayout()
        
        # Create a widget for the middle panel and set it to expand
        middle_widget = QWidget()
        middle_widget.setLayout(self.middle_panel)
        middle_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.content_layout.addWidget(middle_widget, 70)  # Graph takes 70% of space
        
        # Grafik alanı - Beyaz arka plan ve kalın kenarlıklar ile
        self.figure = Figure(facecolor="white", figsize=(5, 4), dpi=100)
        self.figure.subplots_adjust(left=0.15, right=0.95, top=0.95, bottom=0.15)
        self.ax = self.figure.add_subplot(111)
        self.ax.set_facecolor("white")  # Grafik arka plan rengi beyaz
        
        # Eksen renklerini grape_purple yap
        self.ax.tick_params(colors=GRAPE_PURPLE, width=2)  # Eksen çizgileri
        self.ax.xaxis.label.set_color(GRAPE_PURPLE)  # X ekseni etiketi
        self.ax.yaxis.label.set_color(GRAPE_PURPLE)  # Y ekseni etiketi
        self.ax.title.set_color(GRAPE_PURPLE)  # Grafik başlığı
        
        # Grafik kenar çizgisini kalınlaştır
        for spine in self.ax.spines.values():
            spine.set_linewidth(2.5)  # Kenar çizgilerini kalınlaştır
            spine.set_color(GRAPE_PURPLE)  # Kenar çizgileri
            
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setStyleSheet(f"background-color: white; border: 2px solid {GRAPE_PURPLE}; border-radius: 5px;")
        self.middle_panel.addWidget(self.canvas)

        # Sağ panel - limited to 30% of space
        self.right_panel = QVBoxLayout()
        self.right_panel.setContentsMargins(10, 0, 0, 0)
        
        # Create a widget for the right panel and limit its width
        right_widget = QWidget()
        right_widget.setLayout(self.right_panel)
        right_widget.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        right_widget.setMaximumWidth(240)  # Set a maximum width
        self.content_layout.addWidget(right_widget, 30)  # Right panel takes 30% of space

        self.label = QLabel("Bir seçenek seç:")
        self.label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.label.setStyleSheet(f"color: {GRAPE_PURPLE};")
        self.right_panel.addWidget(self.label)

        self.combobox = QComboBox()
        self.combobox.addItems(["Seçenek 1", "Seçenek 2", "Seçenek 3"])
        self.combobox.currentIndexChanged.connect(self.secenek_degisti)
        self.combobox.setStyleSheet(f"""
            background-color: {GRAPE_PURPLE}; 
            color: {LIGHT_LAVENDER}; 
            padding: 5px; 
            border-radius: 10px; 
            border: 1px solid {NEON_BLUE};
        """)
        self.right_panel.addWidget(self.combobox)

        self.veri_girisleri = []
        self.veri_paneli = QVBoxLayout()
        self.right_panel.addLayout(self.veri_paneli)

        self.buton_guncelle = QPushButton("Grafiği Güncelle")
        self.buton_guncelle.setStyleSheet(f"""
            background-color: {NEON_BLUE}; 
            color: {GRAPE_PURPLE}; 
            padding: 10px; 
            border-radius: 10px; 
            font-weight: bold;
        """)
        self.buton_guncelle.clicked.connect(self.grafik_guncelle)
        self.right_panel.addWidget(self.buton_guncelle)

        self.listbox_sonuclar = QListWidget()
        self.listbox_sonuclar.setStyleSheet(f"""
            background-color: {GRAPE_PURPLE}; 
            color: {LIGHT_LAVENDER}; 
            border-radius: 10px; 
            border: 1px solid {NEON_BLUE};
        """)
        self.listbox_sonuclar.setMaximumHeight(120)  # Limit the height of the results list
        self.right_panel.addWidget(self.listbox_sonuclar)

        self.buton_kaydet = QPushButton("Grafiği Kaydet")
        self.buton_kaydet.setStyleSheet(f"""
            background-color: {NEON_BLUE}; 
            color: {GRAPE_PURPLE}; 
            padding: 10px; 
            border-radius: 10px; 
            font-weight: bold;
        """)
        self.buton_kaydet.clicked.connect(self.grafik_kaydet)
        self.right_panel.addWidget(self.buton_kaydet)
        
        # Add stretch to push everything up
        self.right_panel.addStretch()

        # Kenar boyutlandırma için event filtresi ekleme
        self.installEventFilter(self)
        
        self.resize_area = 8  # Kenar boyutlandırma için algılama alanı boyutu
        self._resizing = False
        self._resize_direction = None

        self.secenek_degisti()

    def get_random_color(self):
        """Rastgele bir renk döndürür"""
        return random.choice(self.colors)

    def grafik_guncelle(self):
        self.ax.clear()
        self.ax.set_facecolor("white")  # Beyaz arka plan
        
        # Eksen ayarlarını yeniden uygula
        self.ax.tick_params(colors=GRAPE_PURPLE, width=2)
        self.ax.xaxis.label.set_color(GRAPE_PURPLE)
        self.ax.yaxis.label.set_color(GRAPE_PURPLE)
        self.ax.title.set_color(GRAPE_PURPLE)
        
        # Kenar çizgilerini yeniden ayarla
        for spine in self.ax.spines.values():
            spine.set_linewidth(2.5)
            spine.set_color(GRAPE_PURPLE)
            
        self.listbox_sonuclar.clear()
        
        try:
            veriler = [float(entry.text()) for entry in self.veri_girisleri]
            
            # Rastgele renk seç (öncelikle NEON_BLUE'yu kullan)
            line_color = NEON_BLUE if random.random() > 0.5 else self.get_random_color()
            
            # Çizgiyi çiz
            self.ax.plot(range(1, len(veriler) + 1), veriler, 
                         marker='o', 
                         color=line_color, 
                         linestyle='-',
                         linewidth=2.5,
                         markersize=8)
            
            # X ve Y eksen etiketleri
            self.ax.set_xlabel('Veri Noktası', fontweight='bold', fontsize=12)
            self.ax.set_ylabel('Değer', fontweight='bold', fontsize=12)
            self.ax.set_title('Veri Grafiği', fontweight='bold', fontsize=14)
            
            # Izgarayı göster
            self.ax.grid(True, linestyle='--', alpha=0.7, color=LIGHT_LAVENDER)
            
            for i, veri in enumerate(veriler, start=1):
                self.listbox_sonuclar.addItem(f"Veri {i}: {veri} (Renk: {line_color})")
            
            if sum(veriler) > 5:
                self.listbox_sonuclar.addItem("Toplam 5'ten fazla!")
            
        except ValueError:
            self.listbox_sonuclar.addItem("Geçersiz giriş!")
        
        self.canvas.draw()
    
    def grafik_kaydet(self):
        self.figure.savefig("grafik.png", bbox_inches='tight', dpi=300)
        self.listbox_sonuclar.addItem("Grafik 'grafik.png' olarak yüksek kalitede kaydedildi!")
    
    def secenek_degisti(self):
        for i in reversed(range(self.veri_paneli.count())):
            layout_item = self.veri_paneli.itemAt(i)
            if layout_item.layout():
                # Alt layout'ları temizle
                while layout_item.layout().count():
                    child_item = layout_item.layout().takeAt(0)
                    if child_item.widget():
                        child_item.widget().deleteLater()
                # Layout'ı sil
                layout_item.layout().deleteLater()
            elif layout_item.widget():
                layout_item.widget().deleteLater()
                
        self.veri_girisleri.clear()
        
        secim = self.combobox.currentText()
        veri_sayisi = {"Seçenek 1": 2, "Seçenek 2": 3, "Seçenek 3": 4}.get(secim, 2)
        
        for i in range(veri_sayisi):
            hbox = QHBoxLayout()
            label = QLabel(f"Veri {i+1}:")
            label.setStyleSheet(f"color: {GRAPE_PURPLE};")
            entry = QLineEdit()
            entry.setStyleSheet(f"""
                background-color: {GRAPE_PURPLE}; 
                color: {LIGHT_LAVENDER}; 
                padding: 5px; 
                border-radius: 10px; 
                border: 1px solid {NEON_BLUE};
            """)
            self.veri_girisleri.append(entry)
            
            hbox.addWidget(label)
            hbox.addWidget(entry)
            self.veri_paneli.addLayout(hbox)
            
    def eventFilter(self, obj, event):
        if obj is self:
            if event.type() == QEvent.Type.MouseMove:
                if not self.isMaximized() and not self._resizing:
                    x = event.pos().x()
                    y = event.pos().y()
                    w = self.width()
                    h = self.height()
                    
                    # Kenar algılama ve imleç değiştirme
                    left_edge = x < self.resize_area
                    right_edge = x > w - self.resize_area
                    top_edge = y < self.resize_area
                    bottom_edge = y > h - self.resize_area
                    
                    if top_edge and left_edge:
                        self.setCursor(Qt.CursorShape.SizeFDiagCursor)
                    elif top_edge and right_edge:
                        self.setCursor(Qt.CursorShape.SizeBDiagCursor)
                    elif bottom_edge and left_edge:
                        self.setCursor(Qt.CursorShape.SizeBDiagCursor)
                    elif bottom_edge and right_edge:
                        self.setCursor(Qt.CursorShape.SizeFDiagCursor)
                    elif left_edge or right_edge:
                        self.setCursor(Qt.CursorShape.SizeHorCursor)
                    elif top_edge or bottom_edge:
                        self.setCursor(Qt.CursorShape.SizeVerCursor)
                    else:
                        self.setCursor(Qt.CursorShape.ArrowCursor)
                        
            elif event.type() == QEvent.Type.MouseButtonPress:
                if event.button() == Qt.MouseButton.LeftButton and not self.isMaximized():
                    x = event.pos().x()
                    y = event.pos().y()
                    w = self.width()
                    h = self.height()
                    
                    # Kenar algılama
                    left_edge = x < self.resize_area
                    right_edge = x > w - self.resize_area
                    top_edge = y < self.resize_area
                    bottom_edge = y > h - self.resize_area
                    
                    if any([left_edge, right_edge, top_edge, bottom_edge]):
                        self._resizing = True
                        self._resize_direction = {
                            'left': left_edge,
                            'right': right_edge,
                            'top': top_edge,
                            'bottom': bottom_edge
                        }
                        self._resize_start_pos = event.pos()
                        self._resize_start_geometry = self.geometry()
                
            elif event.type() == QEvent.Type.MouseButtonRelease:
                if event.button() == Qt.MouseButton.LeftButton:
                    self._resizing = False
                    self._resize_direction = None
                    
            elif event.type() == QEvent.Type.MouseMove and self._resizing:
                # Boyutlandırma işlemi
                dx = event.pos().x() - self._resize_start_pos.x()
                dy = event.pos().y() - self._resize_start_pos.y()
                
                new_geom = self._resize_start_geometry
                
                if self._resize_direction['left']:
                    new_geom.setLeft(new_geom.left() + dx)
                if self._resize_direction['right']:
                    new_geom.setRight(new_geom.right() + dx)
                if self._resize_direction['top']:
                    new_geom.setTop(new_geom.top() + dy)
                if self._resize_direction['bottom']:
                    new_geom.setBottom(new_geom.bottom() + dy)
                
                # Minimum boyut kontrolü
                if new_geom.width() >= self.minimumWidth() and new_geom.height() >= self.minimumHeight():
                    self.setGeometry(new_geom)
                
        return super().eventFilter(obj, event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    pencere = GrafikPenceresi()
    pencere.show()
    sys.exit(app.exec())