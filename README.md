# 📸 Streamlit Image Processor

โปรเจกต์ตัวอย่าง **Image Processing GUI** ที่สร้างด้วย [Streamlit](https://streamlit.io/) และ [OpenCV](https://opencv.org/) สามารถประมวลผลภาพจาก  

- 📂 อัปโหลดไฟล์  
- 🌐 URL ของรูป  
- 🎥 เว็บแคม (Real-time Video Processing)  

และเลือกใช้เอฟเฟกต์ต่าง ๆ เช่น Grayscale, Blur, Canny Edge Detection และ Brightness & Contrast  

---

## 🚀 คุณสมบัติ (Features)

- รองรับ **การอัปโหลดไฟล์ / URL / เว็บแคม**
- ประมวลผลภาพด้วย OpenCV
- แสดงผล **Histogram ของภาพ**
- เอฟเฟกต์ที่มีให้เลือก:
  - 🖤 Grayscale  
  - 🌫️ Blur (Gaussian)  
  - ✨ Canny Edge Detection  
  - 🌞 Brightness & Contrast  
- ประมวลผลแบบ **Real-time ผ่าน Webcam** ด้วย WebRTC  

---

## 📦 การติดตั้ง (Installation)

1. Clone โปรเจกต์นี้:
   ```bash
   git clone https://github.com/yourusername/streamlit-image-processor.git
   cd streamlit-image-processor
   ```

2. สร้าง virtual environment (แนะนำ):
   ```bash
   python -m venv venv
   source venv/bin/activate   # บน Linux/Mac
   venv\Scripts\activate      # บน Windows
   ```

3. ติดตั้ง dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## ▶️ วิธีการใช้งาน (Usage)

รันแอปด้วยคำสั่ง:
```bash
streamlit run app.py
```

จากนั้นเปิดเบราว์เซอร์ไปที่:
```
http://localhost:8501
```

---

## 📂 โครงสร้างไฟล์ (Project Structure)

```
streamlit-image-processor/
│
├── app.py              # ไฟล์หลักของ Streamlit
├── requirements.txt    # รายการ dependencies
└── README.md           # คำอธิบายโปรเจกต์
```

---

## ⚙️ Dependencies

- streamlit
- streamlit-webrtc
- opencv-python
- numpy
- matplotlib
- requests
- av  

(ทั้งหมดอยู่ใน `requirements.txt`)

---

## 📸 ตัวอย่างหน้าตา (Screenshots)

### 1. อัปโหลดไฟล์ + Histogram  
![Upload Example]([https://storage.googleapis.com/static.streamlit.io/examples/owl.jpg](https://preview.redd.it/gold-ship-training-experience-on-a-normal-day-v0-qecw1blivgcf1.jpeg?width=1080&crop=smart&auto=webp&s=9ec0b6ad60b6bae7844ce533802ed5762324a93e))

### 2. Real-time Webcam Processing  
(สามารถเลือกเอฟเฟกต์ได้ใน sidebar)

---

## 💡 หมายเหตุ
- ถ้าใช้ **Webcam** ต้องอนุญาตให้เบราว์เซอร์เข้าถึงกล้อง  
- หากไม่เห็นภาพจาก webcam ลองใช้ Chrome หรือ Edge  
