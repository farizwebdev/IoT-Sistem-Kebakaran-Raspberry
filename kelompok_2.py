"""
Project : Fire Alarm System
Hardware: Raspberry Pi Pico W, Flame Sensor, Buzzer
Penyusun: Fariz Husain Albar
"""

import network
import time
from machine import Pin
import urequests as requests 

# --- KONFIGURASI WIFI & BLYNK ---
SSID = 'yeay'
PASSWORD = 'hehehehe'
BLYNK_AUTH = '_SRNbHVGll7zvuy41FN8f1CEqZIw0Hyg'
BLYNK_SERVER = "blynk.cloud" 

# --- KONFIGURASI PIN ---
# Sensor Api di GP16 (Mode INPUT)
sensor_api = Pin(16, Pin.IN)   

# Buzzer di GP15 (Mode OUTPUT)
buzzer = Pin(15, Pin.OUT)

# Variabel
is_notified = False

# --- KONEK WIFI ---
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    print("Menghubungkan WiFi...", end="")
    while not wlan.isconnected():
        print(".", end="")
        time.sleep(1)
    print("\nTerhubung! IP:", wlan.ifconfig()[0])

# --- KIRIM NOTIFIKASI (Hanya Sekali) ---
def blynk_alert():
    try:
        print("Mengirim Notifikasi ke HP...")
        url = f"https://{BLYNK_SERVER}/external/api/logEvent?token={BLYNK_AUTH}&code=fire_alert"
        req = requests.get(url)
        req.close()
        print("Notifikasi Terkirim!")
    except Exception as e:
        print("Gagal kirim notif:", e)

# --- FUNGSI UPDATE BLYNK (BATCH) ---
def update_blynk_all(led_status, gauge_value, pesan_teks, warna_hex):
    try:
        # 1. Encoding URL
        pesan_url = pesan_teks.replace(" ", "%20")
        warna_url = warna_hex.replace("#", "%23")
        
        # 2. BATCH UPDATE
        url_data = f"https://{BLYNK_SERVER}/external/api/batch/update?token={BLYNK_AUTH}&v0={led_status}&v1={gauge_value}&v2={pesan_url}"
        
        req1 = requests.get(url_data)
        req1.close()
        
        # 3. UPDATE PROPERTY WARNA
        url_color = f"https://{BLYNK_SERVER}/external/api/update/property?token={BLYNK_AUTH}&pin=v2&color={warna_url}"
        
        req2 = requests.get(url_color)
        req2.close()
        
    except Exception as e:
        # Pass error agar tidak spamming serial monitor
        pass

# --- SETUP ---
connect_wifi()
buzzer.value(0) 
print("SISTEM PICO SIAP! MONITORING DIGITAL...")

# --- LOOP UTAMA ---
while True:
    # 1. Baca Sensor (0 = Api, 1 = Aman)
    status_sensor = sensor_api.value()
    
    print(f"Status Sensor: {status_sensor}") 

    # 2. LOGIKA ALARM (Active LOW)
    if status_sensor == 0:
        # --- KONDISI BAHAYA ---
        print("!!! API TERDETEKSI !!!")
        
        buzzer.value(1) 
        
        # Kirim semua data
        update_blynk_all(1, 100, "KEBAKARAN!!", "#D3435C") 
        
        if not is_notified:
            blynk_alert()
            is_notified = True
            
    else:
        # --- KONDISI AMAN ---
        buzzer.value(0)
        
        # Kirim semua data
        update_blynk_all(0, 0, "Ruangan Aman", "#23C48E")
        
        is_notified = False

    time.sleep(1)