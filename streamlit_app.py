"""
Professional Streamlit Live Object Detection with Distance Alarm
Save as: streamlit_app.py
Run with: streamlit run streamlit_app.py
"""

import streamlit as st
import cv2
from ultralytics import YOLO
import numpy as np
from PIL import Image
import time
import pygame

# Initialize pygame for alarm sound
pygame.mixer.init()

# Page configuration
st.set_page_config(
    page_title="AI Object Detection System",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
    <style>
    /* Main container */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
    }
    
    /* Header styling */
    .header-container {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
        text-align: center;
    }
    
    .main-title {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    .subtitle {
        color: #666;
        font-size: 1.2rem;
        font-weight: 300;
    }
    
    /* Card styling */
    .card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        margin-bottom: 1rem;
        transition: transform 0.3s ease;
    }
    
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.12);
    }
    
    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0.5rem 0;
    }
    
    .metric-label {
        font-size: 0.9rem;
        opacity: 0.9;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Alarm status */
    .alarm-safe {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        color: white;
        font-weight: 600;
        font-size: 1.2rem;
    }
    
    .alarm-active {
        background: linear-gradient(135deg, #eb3349 0%, #f45c43 100%);
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        color: white;
        font-weight: 600;
        font-size: 1.2rem;
        animation: pulse 1s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    
    /* Button styling */
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3rem;
        font-weight: 600;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        border: none;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(0,0,0,0.2);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: white;
    }
    
    /* Info boxes */
    .info-box {
        background: #e3f2fd;
        border-left: 4px solid #2196f3;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    
    .success-box {
        background: #e8f5e9;
        border-left: 4px solid #4caf50;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    
    .warning-box {
        background: #fff3e0;
        border-left: 4px solid #ff9800;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    
    .danger-box {
        background: #ffebee;
        border-left: 4px solid #f44336;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
        animation: pulse 1s infinite;
    }
    
    /* Video container */
    .video-container {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.1);
    }
    
    /* Detection list */
    .detection-item {
        background: #f5f5f5;
        padding: 0.8rem;
        margin: 0.5rem 0;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        font-weight: 500;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main-title {
            font-size: 2rem;
        }
        .metric-value {
            font-size: 1.8rem;
        }
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
    <div class="header-container">
        <h1 class="main-title">🎯 AI Object Detection System</h1>
        <p class="subtitle">Real-time Computer Vision with Distance Monitoring & Smart Alerts</p>
    </div>
""", unsafe_allow_html=True)

# Sidebar with professional styling
with st.sidebar:
    st.markdown("### 🎛️ Control Panel")
    
    # Model selection
    st.markdown("#### 🤖 AI Model")
    model_option = st.selectbox(
        "Select Detection Model",
        ["YOLOv8n (Nano - Fastest)", "YOLOv8s (Small)", "YOLOv8m (Medium)", "YOLOv8l (Large)"],
        label_visibility="collapsed"
    )
    
    model_map = {
        "YOLOv8n (Nano - Fastest)": "yolov8n.pt",
        "YOLOv8s (Small)": "yolov8s.pt",
        "YOLOv8m (Medium)": "yolov8m.pt",
        "YOLOv8l (Large)": "yolov8l.pt"
    }
    
    st.markdown("---")
    
    # Camera settings
    st.markdown("#### 📹 Camera Settings")
    camera_index = st.selectbox("Camera Source", [0, 1, 2], help="Select camera input")
    confidence = st.slider("Detection Confidence", 0.0, 1.0, 0.25, 0.05)
    
    st.markdown("---")
    
    # Alarm settings
    st.markdown("#### 🚨 Proximity Alert System")
    enable_alarm = st.toggle("Enable Alarm", value=True)
    
    if enable_alarm:
        distance_threshold = st.slider(
            "Alert Distance (meters)",
            1.0, 20.0, 10.0, 0.5,
            help="Trigger alarm when objects are closer than this distance"
        )
        
        alarm_type = st.selectbox("Alarm Type", ["Beep", "Siren", "Voice Alert"])
    else:
        distance_threshold = 10.0
        alarm_type = "Beep"
    
    st.markdown("---")
    
    # Calibration
    st.markdown("#### 📏 Distance Calibration")
    focal_length = st.number_input(
        "Focal Length (pixels)",
        100, 2000, 700, 50,
        help="Adjust for accurate distance measurement"
    )
    
    st.markdown("---")
    
    # Object monitoring
    st.markdown("#### 🎯 Object Monitoring")
    monitor_all = st.toggle("Monitor All Objects", value=True)
    
    known_sizes = {
        "person": 1.7, "car": 4.5, "truck": 8.0, "bus": 10.0,
        "bicycle": 1.8, "motorcycle": 2.0, "dog": 0.6, "cat": 0.4,
        "chair": 0.8, "couch": 2.0, "tv": 1.0, "laptop": 0.35,
        "cell phone": 0.15, "bottle": 0.25, "cup": 0.1, "book": 0.25,
        "backpack": 0.5, "umbrella": 0.8, "handbag": 0.4, "suitcase": 0.7
    }
    
    if not monitor_all:
        monitored_objects = st.multiselect(
            "Select Objects",
            list(known_sizes.keys()),
            default=["person", "car"],
            label_visibility="collapsed"
        )
    else:
        monitored_objects = list(known_sizes.keys())
    
    st.markdown("---")
    
    # Display options
    st.markdown("#### 📺 Display Options")
    col1, col2 = st.columns(2)
    with col1:
        show_distance = st.checkbox("Distance", value=True)
        show_labels = st.checkbox("Labels", value=True)
    with col2:
        show_conf = st.checkbox("Confidence", value=True)
        show_fps = st.checkbox("FPS", value=True)

# Load model
@st.cache_resource
def load_model(model_name):
    return YOLO(model_name)

# Initialize session state
if 'run_detection' not in st.session_state:
    st.session_state.run_detection = False
if 'model_loaded' not in st.session_state:
    st.session_state.model_loaded = False
    st.session_state.current_model = None
if 'alarm_cooldown' not in st.session_state:
    st.session_state.alarm_cooldown = 0

# Load model with progress
if not st.session_state.model_loaded or st.session_state.current_model != model_map[model_option]:
    with st.spinner('🔄 Loading AI Model...'):
        model = load_model(model_map[model_option])
        st.session_state.model = model
        st.session_state.model_loaded = True
        st.session_state.current_model = model_map[model_option]
    st.sidebar.success("✅ Model Ready!")

# Distance estimation function
def estimate_distance(bbox_width, known_width, focal_length):
    if bbox_width > 0:
        return (known_width * focal_length) / bbox_width
    return None

# Alarm function
def play_alarm(alarm_type):
    try:
        sample_rate = 44100
        frequency = 1000
        duration = 0.3
        samples = int(sample_rate * duration)
        wave = np.sin(2 * np.pi * frequency * np.linspace(0, duration, samples))
        wave = (wave * 32767).astype(np.int16)
        stereo_wave = np.column_stack((wave, wave))
        sound = pygame.sndarray.make_sound(stereo_wave)
        sound.play()
    except:
        pass

# Control buttons
col1, col2, col3, col4 = st.columns(4)
with col1:
    start_button = st.button("▶️ Start Detection", use_container_width=True, type="primary")
with col2:
    stop_button = st.button("⏹️ Stop", use_container_width=True)
with col3:
    snapshot_button = st.button("📸 Snapshot", use_container_width=True)
with col4:
    if st.button("🔄 Reset", use_container_width=True):
        st.rerun()

if start_button:
    st.session_state.run_detection = True
if stop_button:
    st.session_state.run_detection = False

st.markdown("<br>", unsafe_allow_html=True)

# Main layout
if st.session_state.run_detection:
    # Metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        objects_placeholder = st.empty()
    with col2:
        closest_placeholder = st.empty()
    with col3:
        fps_placeholder = st.empty()
    with col4:
        alarm_placeholder = st.empty()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Video and detection info
    col_video, col_info = st.columns([2, 1])
    
    with col_video:
        st.markdown('<div class="video-container">', unsafe_allow_html=True)
        st.markdown("### 📹 Live Feed")
        video_placeholder = st.empty()
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_info:
        st.markdown("### 📊 Detection Details")
        detection_details = st.empty()
        alert_box = st.empty()
    
    # Open camera
    cap = cv2.VideoCapture(camera_index)
    
    if not cap.isOpened():
        st.error("❌ Cannot access camera. Please check connection.")
        st.session_state.run_detection = False
    else:
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        
        prev_time = time.time()
        frame_count = 0
        
        while st.session_state.run_detection:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Detection
            results = st.session_state.model(frame, conf=confidence, verbose=False)
            annotated_frame = results[0].plot()
            
            # FPS calculation
            current_time = time.time()
            fps = 1 / (current_time - prev_time)
            prev_time = current_time
            
            detections = results[0].boxes
            num_objects = len(detections)
            
            closest_distance = float('inf')
            closest_object = None
            alarm_triggered = False
            detection_list = []
            
            # Process detections
            for box in detections:
                class_id = int(box.cls[0])
                class_name = st.session_state.model.names[class_id]
                conf_score = float(box.conf[0])
                
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                bbox_width = x2 - x1
                
                distance = None
                if class_name in known_sizes:
                    distance = estimate_distance(bbox_width, known_sizes[class_name], focal_length)
                    
                    if distance and show_distance:
                        distance_text = f"{distance:.1f}m"
                        cv2.putText(annotated_frame, distance_text, (int(x1), int(y1) - 10),
                                  cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
                        
                        if class_name in monitored_objects and distance < distance_threshold:
                            cv2.rectangle(annotated_frame, (int(x1), int(y1)), 
                                        (int(x2), int(y2)), (0, 0, 255), 3)
                            
                            if distance < closest_distance:
                                closest_distance = distance
                                closest_object = class_name
                                alarm_triggered = True
                
                if show_labels:
                    if distance:
                        detection_list.append(f"🎯 {class_name.title()}: {distance:.1f}m ({conf_score:.0%})")
                    else:
                        detection_list.append(f"🎯 {class_name.title()} ({conf_score:.0%})")
            
            # Trigger alarm
            if enable_alarm and alarm_triggered:
                if current_time - st.session_state.alarm_cooldown > 1.0:
                    play_alarm(alarm_type)
                    st.session_state.alarm_cooldown = current_time
                    
                    cv2.putText(annotated_frame, "⚠️ PROXIMITY ALERT!", (50, 100),
                              cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)
            
            # Add FPS
            if show_fps:
                cv2.putText(annotated_frame, f"FPS: {fps:.1f}", (10, 30),
                          cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            # Display
            annotated_frame_rgb = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
            video_placeholder.image(annotated_frame_rgb, channels="RGB", use_container_width=True)
            
            # Update metrics
            objects_placeholder.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Objects Detected</div>
                    <div class="metric-value">{num_objects}</div>
                </div>
            """, unsafe_allow_html=True)
            
            if closest_distance < float('inf'):
                closest_placeholder.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-label">Closest Object</div>
                        <div class="metric-value">{closest_distance:.1f}m</div>
                        <div style="font-size: 0.9rem; margin-top: 0.5rem;">{closest_object.title()}</div>
                    </div>
                """, unsafe_allow_html=True)
            else:
                closest_placeholder.markdown("""
                    <div class="metric-card">
                        <div class="metric-label">Closest Object</div>
                        <div class="metric-value">--</div>
                    </div>
                """, unsafe_allow_html=True)
            
            fps_placeholder.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Frame Rate</div>
                    <div class="metric-value">{fps:.0f}</div>
                    <div style="font-size: 0.9rem; margin-top: 0.5rem;">FPS</div>
                </div>
            """, unsafe_allow_html=True)
            
            if alarm_triggered:
                alarm_placeholder.markdown(f"""
                    <div class="alarm-active">
                        🚨 ALERT: {closest_object.upper()}
                    </div>
                """, unsafe_allow_html=True)
                
                alert_box.markdown(f"""
                    <div class="danger-box">
                        <strong>⚠️ PROXIMITY WARNING</strong><br>
                        {closest_object.title()} detected at {closest_distance:.1f}m<br>
                        <small>Alert threshold: {distance_threshold}m</small>
                    </div>
                """, unsafe_allow_html=True)
            else:
                alarm_placeholder.markdown("""
                    <div class="alarm-safe">
                        ✅ All Clear
                    </div>
                """, unsafe_allow_html=True)
                alert_box.empty()
            
            # Detection list
            if detection_list:
                list_html = "<div style='background: #f8f9fa; padding: 1rem; border-radius: 10px;'>"
                for item in detection_list[:10]:
                    list_html += f"<div class='detection-item'>{item}</div>"
                list_html += "</div>"
                detection_details.markdown(list_html, unsafe_allow_html=True)
            
            frame_count += 1
            time.sleep(0.01)
        
        cap.release()
        st.success("✅ Detection stopped successfully")

else:
    # Welcome screen
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
            <div class="info-box" style="text-align: center; padding: 3rem;">
                <h2>👋 Welcome to AI Object Detection</h2>
                <p style="font-size: 1.1rem; margin: 1.5rem 0;">
                    Click <strong>Start Detection</strong> to begin real-time object monitoring
                </p>
                <p style="color: #666;">
                    Configure settings in the left sidebar before starting
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        # Feature cards
        st.markdown("<br>", unsafe_allow_html=True)
        
        feat_col1, feat_col2, feat_col3 = st.columns(3)
        
        with feat_col1:
            st.markdown("""
                <div class="card" style="text-align: center;">
                    <h3>🎯</h3>
                    <h4>Smart Detection</h4>
                    <p>80+ object types</p>
                </div>
            """, unsafe_allow_html=True)
        
        with feat_col2:
            st.markdown("""
                <div class="card" style="text-align: center;">
                    <h3>📏</h3>
                    <h4>Distance Tracking</h4>
                    <p>Real-time measurements</p>
                </div>
            """, unsafe_allow_html=True)
        
        with feat_col3:
            st.markdown("""
                <div class="card" style="text-align: center;">
                    <h3>🚨</h3>
                    <h4>Smart Alerts</h4>
                    <p>Proximity warnings</p>
                </div>
            """, unsafe_allow_html=True)