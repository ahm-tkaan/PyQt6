# Gerekli kütüphaneleri import et
import tkinter as tk  # Tkinter kütüphanesini arayüz oluşturmak için import et
from tkinter import ttk, simpledialog  # Tkinter'ın gelişmiş bileşenlerini ve diyalog kutularını import et
from matplotlib.figure import Figure  # Matplotlib kütüphanesinden Figure sınıfını grafik oluşturmak için import et
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # Matplotlib grafiklerini Tkinter arayüzüne yerleştirmek için gerekli sınıfı import et

# Ana pencereyi oluştur
pencere = tk.Tk()  # Ana Tkinter penceresini oluştur
pencere.title("Basit Arayüz")  # Pencere başlığını ayarla
pencere.geometry("500x400")   # Pencere boyutunu 500 piksel genişlik ve 400 piksel yükseklik olarak ayarla

# Grafik için bir çerçeve oluştur ve sol tarafa yerleştir
grafik_cerceve = tk.Frame(pencere, width=200, height=200, bg="white")  # Grafik için beyaz bir çerçeve oluştur
grafik_cerceve.pack(side="left", padx=10, pady=10)  # Çerçeveyi sol tarafa, yatayda ve dikeyde 10 piksel boşlukla yerleştir

# Grafik oluşturma fonksiyonu
def grafik_guncelle():
    ax.clear()  # Grafiği temizle
    try:
        veriler = [float(entry.get()) for entry in entry_list]  # Giriş kutularındaki değerleri al ve sayıya dönüştür
        ax.plot(range(1, len(veriler) + 1), veriler, marker='o')  # Verileri grafiğe çiz, 'o' işaretleyicisi ile
        
        if sum(veriler) > 5:  # Verilerin toplamı 5'ten büyükse
            label_sonuc.config(text="Toplam 5'ten fazla!", fg="red")  # Sonuç etiketine kırmızı renkte uyarı yaz
        else:
            label_sonuc.config(text="", fg="black")  # Aksi halde etiketi temizle
    except ValueError:  # Eğer girişlerde sayısal olmayan bir değer varsa
        pass  # Hata oluştuğunda bir şey yapma (uyarı gösterme vb. eklenebilir)
    canvas.draw()  # Grafiği yeniden çiz

# Seçenek değiştiğinde textbox oluşturma fonksiyonu
def secenek_degisti(event):
    for widget in cerceve_veri.winfo_children():  # Önceki giriş kutularını temizle
        widget.destroy()
    global entry_list  # Global bir giriş kutusu listesi oluştur
    entry_list = []
    
    secim = combobox.get()  # Seçilen seçeneği al
    if secim == "Seçenek 1":
        veri_sayisi = 2  # Seçenek 1 için 2 veri girişi
    elif secim == "Seçenek 2":
        veri_sayisi = 3  # Seçenek 2 için 3 veri girişi
    elif secim == "Seçenek 3":
        veri_sayisi = 4  # Seçenek 3 için 4 veri girişi
    else:  # Seçenek 4 (Kullanıcıdan veri sayısı isteme)
        veri_sayisi = simpledialog.askinteger("Veri Sayısı", "Kaç adet veri girmek istiyorsunuz?", minvalue=1, maxvalue=10)  # Kullanıcıdan veri sayısı al
        if veri_sayisi is None:  # Kullanıcı iptal ederse
            return  # Fonksiyondan çık
    
    for i in range(veri_sayisi):  # Gerekli sayıda giriş kutusu oluştur
        entry = tk.Entry(cerceve_veri)  # Yeni bir giriş kutusu oluştur
        entry.pack(pady=2)  # Kutuya çerçevede 2 piksel dikey boşluk ekleyerek yerleştir
        entry_list.append(entry)  # Kutu listesine ekle
    
    buton_guncelle = tk.Button(cerceve_veri, text="Grafiği Güncelle", command=grafik_guncelle)  # Grafiği güncelle butonu
    buton_guncelle.pack(pady=5)  # Butonu 5 piksel dikey boşlukla yerleştir

# Matplotlib figür ve eksenlerini oluştur
fig = Figure(figsize=(2, 2), dpi=100)  # 2x2 inç boyutunda, 100 DPI çözünürlükte bir figür oluştur
ax = fig.add_subplot(111)  # Figüre bir alt grafik ekle (1 satır, 1 sütun, 1. grafik)
canvas = FigureCanvasTkAgg(fig, master=grafik_cerceve)  # Figürü Tkinter çerçevesine yerleştir
canvas.draw()  # Grafiği çiz
canvas.get_tk_widget().pack()  # Grafiği çerçeveye yerleştir

# Sağ taraftaki çerçeveyi oluştur
cerceve_sag = tk.Frame(pencere)  # Sağ taraf için bir çerçeve oluştur
cerceve_sag.pack(side="right", padx=10, pady=10)  # Çerçeveyi sağ tarafa, yatayda ve dikeyde 10 piksel boşlukla yerleştir

etiket = tk.Label(cerceve_sag, text="Bir seçenek seç:")  # Seçenek etiketi
etiket.pack(pady=10)   # Etiketi 10 piksel dikey boşlukla yerleştir

secenekler = ["Seçenek 1", "Seçenek 2", "Seçenek 3", "Seçenek 4"]  # Seçenekler listesi
combobox = ttk.Combobox(cerceve_sag, values=secenekler)  # Seçenekleri içeren bir combobox oluştur
combobox.pack()  # Combobox'ı yerleştir
combobox.set("Seçenek 1")   # Varsayılan olarak ilk seçeneği seç
combobox.bind("<<ComboboxSelected>>", secenek_degisti)  # Seçenek değiştiğinde secenek_degisti fonksiyonunu çağır

cerceve_veri = tk.Frame(cerceve_sag)  # Veri giriş kutularının çerçevesi
cerceve_veri.pack(pady=10)  # Çerçeveyi 10 piksel dikey boşlukla yerleştir

label_sonuc = tk.Label(cerceve_sag, text="", fg="black")  # Sonuç etiketi
label_sonuc.pack()  # Etiketi yerleştir

secenek_degisti(None)   # Başlangıçta varsayılan giriş kutularını oluştur

# Pencereyi çalıştır
pencere.mainloop()  # Tkinter olay döngüsünü başlat ve pencereyi göster