import streamlit as st
import cv2
import numpy as np
import matplotlib.pyplot as plt
# 1. Import RTCConfiguration เพิ่มเข้ามา
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase, RTCConfiguration
import requests
import av  # ต้องมีเพราะเราจะใช้ av.VideoFrame

# ฟังก์ชันสำหรับดาวน์โหลดรูปภาพจาก URL
def load_image_from_url(url):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        image_array = np.asarray(bytearray(response.content), dtype=np.uint8)
        image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
        return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    except requests.exceptions.RequestException as e:
        st.error(f"ไม่สามารถโหลดรูปจาก URL ได้: {e}")
        return None

# ฟังก์ชันสำหรับประมวลผลภาพ
def process_image(image, effect, params):
    processed_image = image.copy()
    if effect == 'Grayscale':
        processed_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    elif effect == 'Blur':
        ksize = params['ksize']
        if ksize % 2 == 0: ksize += 1 # Kernel size must be odd
        processed_image = cv2.GaussianBlur(image, (ksize, ksize), 0)
    elif effect == 'Canny Edge Detection':
        threshold1 = params['threshold1']
        threshold2 = params['threshold2']
        gray_img = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        processed_image = cv2.Canny(gray_img, threshold1, threshold2)
    elif effect == 'Brightness & Contrast':
        alpha = params['alpha'] # Contrast
        beta = params['beta']   # Brightness
        processed_image = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
        
    return processed_image

# ฟังก์ชันสำหรับสร้างและแสดงกราฟ Histogram
def plot_histogram(image):
    fig, ax = plt.subplots()
    if len(image.shape) == 2: # Grayscale image
        color = ('black',)
        ax.hist(image.ravel(), 256, [0, 256], color='black')
    else: # Color image
        color = ('r', 'g', 'b')
        for i, col in enumerate(color):
            hist = cv2.calcHist([image], [i], None, [256], [0, 256])
            ax.plot(hist, color=col)
    
    ax.set_title("Image Histogram")
    ax.set_xlabel("Pixel Intensity")
    ax.set_ylabel("Number of Pixels")
    st.pyplot(fig)

# คลาสสำหรับจัดการ Video Stream จาก Webcam
class VideoProcessor(VideoTransformerBase):
    def __init__(self):
        self.effect = 'None'
        self.params = {}

    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        if self.effect != 'None':
            processed_img = process_image(img_rgb, self.effect, self.params)
        else:
            processed_img = img_rgb

        if len(processed_img.shape) == 2:
            processed_img = cv2.cvtColor(processed_img, cv2.COLOR_GRAY2RGB)

        # ✅ คืนค่าเป็น av.VideoFrame เพื่อให้ WebRTC แสดงผลได้
        return av.VideoFrame.from_ndarray(processed_img, format="rgb24")

# --- หน้าตาของแอปพลิเคชัน (GUI) ---
st.set_page_config(page_title="Streamlit Image Processor", layout="wide")
st.title("📸 Streamlit Image Processor")
st.info("โปรเจ็คสาธิตการทำ Image Processing แบบง่ายๆ ผ่าน GUI ด้วย Streamlit และ OpenCV")

# --- Sidebar สำหรับตั้งค่า ---
with st.sidebar:
    st.header("🖼️ เลือกแหล่งที่มาของรูป")
    source_type = st.radio("เลือก Input:", ("อัปโหลดไฟล์", "URL", "เว็บแคม"))

    st.header("⚙️ ตั้งค่าการประมวลผล")
    processing_effect = st.selectbox(
        "เลือกเอฟเฟกต์:",
        ['None', 'Grayscale', 'Blur', 'Canny Edge Detection', 'Brightness & Contrast']
    )

    params = {}
    if processing_effect == 'Blur':
        params['ksize'] = st.slider("Kernel Size", 1, 51, 5, step=2)
    elif processing_effect == 'Canny Edge Detection':
        params['threshold1'] = st.slider("Threshold 1", 0, 255, 100)
        params['threshold2'] = st.slider("Threshold 2", 0, 255, 200)
    elif processing_effect == 'Brightness & Contrast':
        st.write("Contrast (alpha)")
        params['alpha'] = st.slider(" ", 1.0, 3.0, 1.0, 0.1, key='alpha')
        st.write("Brightness (beta)")
        params['beta'] = st.slider(" ", -100, 100, 0, key='beta')
        
    if source_type != "เว็บแคม":
        show_graph = st.checkbox("📊 แสดงกราฟ Histogram")

# --- ส่วนแสดงผลหลัก ---

if source_type == "เว็บแคม":
    st.header("📷 Real-time Webcam Processing")
    st.info("เลือกเอฟเฟกต์และปรับค่าในแถบด้านข้าง แล้วกด START เพื่อดูผลแบบ Real-time")

    RTC_CONFIGURATION = RTCConfiguration(
        {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
    )

    ctx = webrtc_streamer(
        key="webcam",
        video_processor_factory=VideoProcessor,
        rtc_configuration=RTC_CONFIGURATION,
        media_stream_constraints={"video": True, "audio": False}
    )

    if ctx.video_processor:
        ctx.video_processor.effect = processing_effect
        ctx.video_processor.params = params
    
else: # จัดการส่วนของ "อัปโหลดไฟล์" และ "URL"
    original_image = None
    if source_type == "อัปโหลดไฟล์":
        uploaded_file = st.file_uploader("เลือกไฟล์รูปภาพ...", type=["jpg", "jpeg", "png"])
        if uploaded_file is not None:
            file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
            image = cv2.imdecode(file_bytes, 1)
            original_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    elif source_type == "URL":
        url = st.text_input("กรอก URL ของรูปภาพ:", "https://storage.googleapis.com/static.streamlit.io/examples/owl.jpg")
        if url:
            original_image = load_image_from_url(url)
    
    if original_image is not None:
        st.header("🖼️ ผลการประมวลผล")
        col1, col2 = st.columns(2)
        with col1:
            st.image(original_image, caption="🖼️ รูปต้นฉบับ", use_column_width=True)
            if show_graph:
                plot_histogram(original_image)

        with col2:
            if processing_effect != 'None':
                processed_image = process_image(original_image, processing_effect, params)
                st.image(processed_image, caption=f"✨ รูปที่ผ่านการประมวลผล ({processing_effect})", use_column_width=True)
                if show_graph:
                    plot_histogram(processed_image)
            else:
                st.image(original_image, caption="✨ ไม่มีเอฟเฟกต์", use_column_width=True)