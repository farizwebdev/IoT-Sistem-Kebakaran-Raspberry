# Fire Alarm System (Raspberry Pi Pico W)

**Penyusun:** Fariz Husain Albar  
**Jurusan:** Informatika - UIN Sunan Kalijaga Yogyakarta    
**Hardware:** Raspberry Pi Pico W  

## Deskripsi Proyek
Sistem deteksi kebakaran berbasis IoT yang menggunakan **Raspberry Pi Pico W**. Proyek ini memanfaatkan **Sensor Api (Flame Sensor)** dalam mode **Digital** untuk mendeteksi keberadaan api secara cepat.

Berbeda dengan versi analog, sistem ini bekerja secara biner:
1.  **AMAN (Hijau):** Sensor tidak mendeteksi api.
2.  **BAHAYA (Merah):** Sensor mendeteksi api, Buzzer berbunyi, dan notifikasi dikirim.

Sistem terhubung ke cloud **Blynk IoT** menggunakan metode **HTTP REST API** untuk pengiriman data yang efisien tanpa membebani memori mikrokontroler.

## Fitur Utama
* **Digital Monitoring:** Deteksi instan menggunakan sinyal High/Low dari sensor.
* **HTTP API Integration:** Mengirim data ke Blynk menggunakan protokol HTTP Request standar.
* **Batch Update:** Mengupdate status LED, Grafik, dan Teks sekaligus dalam satu request untuk mengurangi delay.
* **Warna Dinamis:** Teks status di aplikasi berubah warna (Hijau saat aman, Merah saat bahaya).
* **Critical Alert:** Mengirim notifikasi *"Fire Alert"* ke Smartphone hanya sekali saat api terdeteksi (mencegah spam notifikasi).

## Kebutuhan Hardware
1.  **Raspberry Pi Pico W** (Fitur WiFi).
2.  **Flame Sensor** (Pin DO / Digital Output digunakan).
3.  **Active Buzzer**.
4.  Kabel Jumper & Breadboard.
5.  Kabel Micro USB (Data).

## Konfigurasi Wiring (Pinout)
Berdasarkan kode `main.py`:

| Komponen | Pin Device | Pin Pico W | Keterangan |
| :--- | :--- | :--- | :--- |
| **Flame Sensor** | **DO** (Digital Out) | **GP16** | Input Sensor (Pin 21) |
| | VCC | 3V3 (OUT) | Power (Pin 36) |
| | GND | GND | Ground |
| **Buzzer** | Positif (+) | **GP15** | Output Suara (Pin 20) |
| | Negatif (-) | GND | Ground |

> **Penting:** Pastikan menghubungkan kaki **DO** (Digital Output) pada sensor api ke GP16, bukan kaki AO.

## Konfigurasi Blynk Dashboard
Buat Datastreams dengan konfigurasi berikut:

| Nama Stream | Virtual Pin | Tipe Data | Min/Max | Fungsi |
| :--- | :--- | :--- | :--- | :--- |
| **Status LED** | `V0` | Integer | 0 / 1 | Indikator visual |
| **Gauge Api** | `V1` | Integer | 0 / 100 | Visualisasi status (0=Aman, 100=Api) |
| **Pesan Teks** | `V2` | String | - | Menampilkan "Ruangan Aman" / "KEBAKARAN!!" |

**Event Setup:**
* Buat event baru dengan kode: `fire_alert`
* Type: **Critical**
* Centang: **Send Loop to Notifications**

## Logika Program
Sistem menggunakan logika **Active LOW** (Umum pada sensor modul China):

1.  **Kondisi Bahaya (Api Terdeteksi)**
    * **Input Sensor:** `0` (Low)
    * **Aksi:** Buzzer Bunyi, Kirim Data ke Blynk (Warna Merah), Kirim Notifikasi.
2.  **Kondisi Aman**
    * **Input Sensor:** `1` (High)
    * **Aksi:** Buzzer Mati, Kirim Data ke Blynk (Warna Hijau).

## Cara Instalasi (Thonny IDE)
1.  **Flash Firmware:** Install firmware **MicroPython for Pico W** terbaru pada board.
2.  **IDE:** Buka aplikasi **Thonny IDE**.
3.  **Koding:**
    * Buat file baru, paste kodingan Python.
    * Simpan file di dalam Raspberry Pi Pico dengan nama `main.py` (agar jalan otomatis saat dinyalakan).
4.  **Konfigurasi:**
    * Ubah bagian `SSID` dan `PASSWORD` dengan WiFi hotspot Anda.
    * Masukkan `BLYNK_AUTH` token Anda.
5.  **Run:** Tekan tombol Play atau cabut-colok USB untuk memulai.

---
*Dibuat untuk Tugas Mata Kuliah Organisasi & Arsitektur Komputer.*
