import ephem
from datetime import datetime, date, timedelta
import math


bulan_names = {
    1: "Muharram",
    2: "Safar",
    3: "Rabiul Awwal",
    4: "Rabiul Akhir",
    5: "Jumadil Awwal",
    6: "Jumadil Akhir",
    7: "Rajab",
    8: "Sya\'ban",
    9: "Ramadhan",
    10: "Syawal",
    11: "Dzulqa\'dah",
    12: "Dzulhijjah"
}


# Titik acuan tanggal (1 Dzulhijjah 1444 H)

tanggal = '2023-7-1'

# Menetapkan posisi observer

# Membuat objek observer
observer = ephem.Observer()

# Mengatur koordinat tempat pengamatan (latitude, longitude)
observer.lat = '-6.690440'  # Latitude Cileungsi
observer.lon = '106.855591'  # Longitude Cileungsi

# Kapan 1 Muharram 1445 H ?

# Konversi tanggal ke objek ephem.Date()



nomorbulan = 1

while True:
    # Bulan Baru Berikutnya :
    tanggalephem = ephem.Date(tanggal)
    bulanbaru = ephem.next_new_moon(tanggalephem) # Tidak spesifik ke Time Zone tertentu

    waktulokal = ephem.localtime(bulanbaru)
    tanggalsaja = waktulokal.date()
    waktusaja = waktulokal.time()      # Diperlukan untuk Menghitung Usia Bulan Saat Maghrib

    
    # Menghitung Waktu Maghrib
    observer.date = ephem.Date(bulanbaru)


    # Menghitung waktu matahari terbenam
    sun = ephem.Sun()
    sunset = observer.next_setting(sun)

    # Mengatur waktu matahari terbenam sebagai waktu maghrib
    
    waktumaghrib = ephem.localtime(sunset)
    waktumaghribjam = waktumaghrib.time()
    
    # Convert the times to datetime objects
    #waktumaghrib_datetime = datetime.combine(date.today(), waktumaghribjam)
    #waktusaja_datetime = datetime.combine(date.today(), waktusaja)

    # Calculate the time difference
    #usiabulan = waktumaghrib_datetime - waktusaja_datetime
    usiabulan = waktumaghrib - waktulokal
    
    
    # Menghitung elongasi bulan pada waktu maghrib
    moon = ephem.Moon()
    observer.date = sunset
    moon.compute(observer)
    elongation = ephem.degrees(moon.elong)
    #moon_azimuth = ephem.degrees(moon.az)
    #moon_altitude = ephem.degrees(moon.alt)
    moon_altitude = math.degrees(moon.alt)
    
    
    #seharisetelahnya = timedelta(days=1) + tanggalsaja
    if (moon_altitude < 1):
        
        print ("Tinggi Bulan kurang dari 1 derajat")
        seharisetelahnya = timedelta(days=2) + tanggalsaja
    else:
        print ("Tinggi Bulan lebih dari 1 derajat")
        seharisetelahnya = timedelta(days=1) + tanggalsaja
    
    if nomorbulan in bulan_names:
        namabulanhijriyah = bulan_names[nomorbulan]
    
    #print(waktumaghrib)
    print("Bulan Baru Berikutnya adalah : ", tanggalsaja, "Pukul : ", waktusaja)
    print("Estimasi 1 ", namabulanhijriyah, " 1445 H : ", seharisetelahnya)
    print("Waktu Maghrib :" ,waktumaghribjam,)
    print("Elongasi Bulan : ", elongation)
    #print(moon_azimuth)
    print("Ketinggian Bulan : ", moon_altitude)
    print("Usia Bulan : ", usiabulan,"\n")
    #print(nomorbulan)

      
    tanggal = str(seharisetelahnya)
    nomorbulan = nomorbulan + 1
    
    # Check if tanggalsaja is equal to July 1st, 2024

    if nomorbulan == 13:
        break



