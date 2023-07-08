import ephem
from datetime import datetime, date, timedelta
import math

namabulan = {
    1: 'Muharram',
    2: 'Safar',
    3: 'Rabiul Awwal',
    4: 'Rabiul Akhir',
    5: 'Jumadil Awwal',
    6: 'Jumadil Akhir',
    7: 'Rajab',
    8: 'Sya\'ban',
    9: 'Ramadhan',
    10: 'Syawal',
    11: 'Dzulqa\'dah',
    12: 'Dzulhijjah'
 
}

# Titik acuan tanggal (1 Dzulhijjah 1444 H)

tanggal = '2023-7-1'

# Posisi Pengamat

observer = ephem.Observer()

# Posisi Latitude dan Longitude (Cileungsi)

observer.lat = '-6.690440'  # Latitude Cileungsi
observer.lon = '106.855591'  # Longitude Cileungsi

#observer.lat = '0'  # Latitude Cileungsi
#observer.lon = '150'  # Longitude Cileungsi

# Kapan 1 Muharram 1445 H ?
nomorbulan = 1
# Konversi tanggal ke objek ephem.Date()
while True:
    tanggalephem = ephem.Date(tanggal)

    # Bulan Baru Berikutnya :

    bulanbaru = ephem.next_new_moon(tanggalephem) # Tidak spesifik ke Time Zone tertentu
    waktulokal = ephem.localtime(bulanbaru) # Objek mencakup tanggal dan waktu
    tanggalsaja = waktulokal.date()
    waktusaja = waktulokal.time()      # Diperlukan untuk Menghitung Usia Bulan Saat Maghrib

    observer.date = ephem.Date(bulanbaru)

    # Menghitung Waktu Matahari Terbenam (Waktu Maghrib)
    sun = ephem.Sun()
    sunset = observer.next_setting(sun)  # Tidak spesifik ke Time Zone tertentu

    waktumaghrib = ephem.localtime(sunset)  # Objek mencakup tanggal dan waktu
    waktumaghribjam = waktumaghrib.time()

    # Menghitung Usia Bulan
    bulan = ephem.Moon()
    observer.date = sunset                # sunset = ephem.Date
    bulan.compute(observer)
    ketinggianbulan = math.degrees(bulan.alt) # konversi radian ke derajat
    elongasi = math.degrees(bulan.elong)

    if (waktumaghribjam < waktusaja):
        print("Waktu Maghrib lebih dulu daripada Waktu Bulan Baru")
        usiabulan = waktulokal - waktumaghrib
    else:      
        usiabulan = waktumaghrib - waktulokal # waktulokal = waktu bulan baru
    

    
    
    # Bahwa standar yang kita gunakan adalah minimal hilal terlihat itu jika elongasinya
    # >= 6.4 derajat atau jika usia bulan kurang dari 1 jam
    # (Standar ini hanyalah ujicoba, tidak mengacu kepada standar manapun)
      
    
    if (elongasi <= 6.4) or (usiabulan < timedelta(hours=1)):
        awalbulanhijriyah = timedelta(days=2) + tanggalsaja
        hilalkelihatan = "tidak"
    else:
        awalbulanhijriyah = timedelta(days=1) + tanggalsaja
        hilalkelihatan = "kelihatan"


    if nomorbulan in namabulan:
        bulanhijriyah = namabulan[nomorbulan]
    
    print("Bulan Baru Berikutnya adalah : ", tanggalsaja, "Pukul : ", waktusaja)
    print("Waktu Maghrib : ", waktumaghribjam)
    print("Usia Bulan : ", usiabulan)
    print("Ketinggian Bulan Saat Maghrib :",ketinggianbulan)
    print("Elongasi Bulan saat Maghrib : ", elongasi)
    print("Apakah Hilal Kelihatan Saat Maghrib di Indonesia tanggal", tanggalsaja, ": ", hilalkelihatan)
    print("Estimasi 1 ", bulanhijriyah, "1445 H : ", awalbulanhijriyah, "\n")
    
    tanggal = str(awalbulanhijriyah)
    nomorbulan = nomorbulan + 1
    
    if (nomorbulan == 13):
        break
