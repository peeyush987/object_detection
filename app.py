from datetime import datetime
import time

import cv2
import numpy as np
import pygame
import streamlit as st
from ultralytics import YOLO

from components import (
    render_activity_timeline,
    render_alarm_status,
    render_detection_list,
    render_header,
    render_metric_card,
    render_snapshot_gallery,
    render_system_overview,
    render_welcome_screen,
)
from config import KNOWN_OBJECT_SIZES, MODEL_OPTIONS
from sidebar import render_sidebar
from styles import get_custom_css
from utils import (
    add_text_to_frame,
    estimate_distance,
    play_alarm_sound,
    save_snapshot,
    summarize_detected_classes,
)

pygame.mixer.init()

st.set_page_config(
    page_title="AI Object Detection System",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_resource
def load_model(model_name):
    """Load YOLO model (cached for performance)."""
    return YOLO(model_name)


def initialize_state():
    """Initialize session state for the app."""
    defaults = {
        "run_detection": False,
        "model_loaded": False,
        "current_model": None,
        "alarm_cooldown": 0.0,
        "auto_snapshot_cooldown": 0.0,
        "snapshot_requested": False,
        "detection_history": [],
        "alert_history": [],
        "snapshots": [],
        "last_processed_upload_token": None,
        "session_stats": {
            "processed_frames": 0,
            "peak_objects": 0,
            "alerts": 0,
            "last_classes": "No detections",
            "last_snapshot": "None",
            "session_started_at": None,
        },
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def register_event(title, detail, target="detection_history"):
    """Store a timestamped event with capped history."""
    st.session_state[target].insert(
        0,
        {"timestamp": datetime.now(), "title": title, "detail": detail},
    )
    st.session_state[target] = st.session_state[target][:20]


def reset_session():
    """Reset transient session data."""
    st.session_state.run_detection = False
    st.session_state.alarm_cooldown = 0.0
    st.session_state.auto_snapshot_cooldown = 0.0
    st.session_state.snapshot_requested = False
    st.session_state.detection_history = []
    st.session_state.alert_history = []
    st.session_state.snapshots = []
    st.session_state.last_processed_upload_token = None
    st.session_state.session_stats = {
        "processed_frames": 0,
        "peak_objects": 0,
        "alerts": 0,
        "last_classes": "No detections",
        "last_snapshot": "None",
        "session_started_at": None,
    }


def process_frame(frame, settings):
    """Run detection and enrich a single frame."""
    results = st.session_state.model(frame, conf=settings["confidence"], verbose=False)
    annotated_frame = results[0].plot(
        conf=settings["show_conf"],
        labels=settings["show_labels"],
    )

    detections = results[0].boxes
    closest_distance = float("inf")
    closest_object = None
    alarm_triggered = False
    class_names = []
    detection_list = []

    for box in detections:
        class_id = int(box.cls[0])
        class_name = st.session_state.model.names[class_id]
        class_names.append(class_name)
        conf_score = float(box.conf[0])

        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
        bbox_width = x2 - x1
        distance = None

        if class_name in KNOWN_OBJECT_SIZES:
            distance = estimate_distance(
                bbox_width,
                KNOWN_OBJECT_SIZES[class_name],
                settings["focal_length"],
            )

            if distance and settings["show_distance"]:
                add_text_to_frame(
                    annotated_frame,
                    f"{distance:.1f}m",
                    (int(x1), int(y1) - 10),
                    (0, 255, 255),
                )

            if (
                distance
                and class_name in settings["monitored_objects"]
                and distance < settings["distance_threshold"]
            ):
                cv2.rectangle(
                    annotated_frame,
                    (int(x1), int(y1)),
                    (int(x2), int(y2)),
                    (0, 0, 255),
                    3,
                )
                if distance < closest_distance:
                    closest_distance = distance
                    closest_object = class_name
                alarm_triggered = True

        if settings["show_labels"]:
            label = class_name.title()
            if distance:
                label += f" • {distance:.1f}m"
            if settings["show_conf"]:
                label += f" • {conf_score:.0%}"
            detection_list.append(label)

    return {
        "annotated_frame": annotated_frame,
        "num_objects": len(detections),
        "closest_distance": closest_distance,
        "closest_object": closest_object,
        "alarm_triggered": alarm_triggered,
        "class_names": class_names,
        "detection_list": detection_list,
    }


def update_session_stats(num_objects, class_names):
    """Update session analytics."""
    st.session_state.session_stats["processed_frames"] += 1
    st.session_state.session_stats["peak_objects"] = max(
        st.session_state.session_stats["peak_objects"],
        num_objects,
    )
    st.session_state.session_stats["last_classes"] = summarize_detected_classes(class_names)


def render_live_metrics(
    objects_placeholder,
    closest_placeholder,
    fps_placeholder,
    alert_count_placeholder,
    num_objects,
    closest_distance,
    closest_object,
    frame_rate,
    settings,
):
    """Render the dashboard metric cards."""
    objects_placeholder.markdown(
        render_metric_card("Objects detected", num_objects, "Current frame", "default"),
        unsafe_allow_html=True,
    )

    if closest_distance < float("inf") and closest_object:
        closest_placeholder.markdown(
            render_metric_card(
                "Closest object",
                f"{closest_distance:.1f}m",
                closest_object.title(),
                "warning" if closest_distance > settings["distance_threshold"] / 2 else "danger",
            ),
            unsafe_allow_html=True,
        )
    else:
        closest_placeholder.markdown(
            render_metric_card("Closest object", "--", "No tracked object nearby", "safe"),
            unsafe_allow_html=True,
        )

    fps_placeholder.markdown(
        render_metric_card("Frame rate", frame_rate, "Frames per second", "default"),
        unsafe_allow_html=True,
    )
    alert_count_placeholder.markdown(
        render_metric_card(
            "Alerts raised",
            st.session_state.session_stats["alerts"],
            "Session total",
            "danger" if st.session_state.session_stats["alerts"] else "safe",
        ),
        unsafe_allow_html=True,
    )


def render_result_panels(
    detection_details,
    alert_box,
    live_timeline,
    session_panel,
    processed,
    settings,
):
    """Render the right-side detail panels."""
    if processed["alarm_triggered"] and processed["closest_object"]:
        alert_box.markdown(
            render_alarm_status(True, processed["closest_object"])
            + f"""
                <div class="danger-box">
                    <strong>Proximity warning</strong><br>
                    {processed['closest_object'].title()} detected at {processed['closest_distance']:.1f}m.<br>
                    <small>Configured threshold: {settings['distance_threshold']:.1f}m</small>
                </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        alert_box.markdown(render_alarm_status(False), unsafe_allow_html=True)

    detection_details.markdown(
        render_detection_list(processed["detection_list"]),
        unsafe_allow_html=True,
    )
    live_timeline.markdown(
        render_activity_timeline(
            st.session_state.alert_history or st.session_state.detection_history
        )
    )
    session_panel.markdown(
        render_snapshot_gallery(st.session_state.snapshots),
        unsafe_allow_html=True,
    )


def handle_snapshot(frame, summary):
    """Persist a snapshot from the current result."""
    snapshot_path = save_snapshot(frame)
    st.session_state.snapshots.insert(
        0,
        {
            "name": snapshot_path.name,
            "path": str(snapshot_path),
            "timestamp": datetime.now().strftime("%d %b %Y • %H:%M:%S"),
            "summary": summary,
        },
    )
    st.session_state.snapshots = st.session_state.snapshots[:12]
    st.session_state.session_stats["last_snapshot"] = snapshot_path.name
    st.session_state.snapshot_requested = False
    register_event("Snapshot saved", f"Stored {snapshot_path.name}.")


initialize_state()

st.markdown(get_custom_css(), unsafe_allow_html=True)
render_header()

settings = render_sidebar()

model_name = MODEL_OPTIONS[settings["model_option"]]
if not st.session_state.model_loaded or st.session_state.current_model != model_name:
    with st.spinner("Loading AI model..."):
        st.session_state.model = load_model(model_name)
        st.session_state.model_loaded = True
        st.session_state.current_model = model_name
    st.sidebar.success("Model loaded and ready.")

primary_label = "Start Detection" if settings["input_source"] == "Live Camera" else "Analyze Image"
secondary_label = "Stop Session" if settings["input_source"] == "Live Camera" else "Clear Analysis"
capture_label = "Capture Next Frame" if settings["input_source"] == "Live Camera" else "Save Result Snapshot"

col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button(primary_label, use_container_width=True, type="primary"):
        st.session_state.run_detection = True
        if not st.session_state.session_stats["session_started_at"]:
            st.session_state.session_stats["session_started_at"] = datetime.now()
        start_detail = (
            f"Monitoring on camera {settings['camera_index']}."
            if settings["input_source"] == "Live Camera"
            else "Uploaded image queued for analysis."
        )
        register_event("Session started", start_detail)
with col2:
    if st.button(secondary_label, use_container_width=True):
        st.session_state.run_detection = False
        if settings["input_source"] == "Uploaded Image":
            st.session_state.last_processed_upload_token = None
        register_event("Session stopped", "Detection was paused by the operator.")
with col3:
    if st.button(capture_label, use_container_width=True):
        st.session_state.snapshot_requested = True
with col4:
    if st.button("Reset Dashboard", use_container_width=True):
        reset_session()
        st.rerun()

summary_col1, summary_col2 = st.columns([1.15, 0.85])
with summary_col1:
    st.markdown(render_system_overview(settings, model_name), unsafe_allow_html=True)
with summary_col2:
    st.markdown(
        render_activity_timeline(
            st.session_state.alert_history or st.session_state.detection_history
        )
    )

if st.session_state.run_detection:
    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
    objects_placeholder = metric_col1.empty()
    closest_placeholder = metric_col2.empty()
    fps_placeholder = metric_col3.empty()
    alert_count_placeholder = metric_col4.empty()

    col_video, col_info = st.columns([1.8, 1])
    with col_video:
        title = "Live camera feed" if settings["input_source"] == "Live Camera" else "Uploaded image analysis"
        st.markdown(f'<div class="feed-title">{title}</div>', unsafe_allow_html=True)
        video_placeholder = st.empty()
    with col_info:
        detection_details = st.empty()
        alert_box = st.empty()
        live_timeline = st.empty()
        session_panel = st.empty()

    if settings["input_source"] == "Live Camera":
        cap = cv2.VideoCapture(settings["camera_index"])

        if not cap.isOpened():
            st.error("Cannot access the selected camera. Check the connection and try again.")
            st.session_state.run_detection = False
            register_event("Camera unavailable", "The selected camera could not be opened.", "alert_history")
        else:
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
            prev_time = time.time()

            while st.session_state.run_detection:
                ret, frame = cap.read()
                if not ret:
                    st.error("Failed to read a frame from the camera.")
                    register_event(
                        "Camera read failure",
                        "The feed stopped returning frames unexpectedly.",
                        "alert_history",
                    )
                    break

                processed = process_frame(frame, settings)
                current_time = time.time()
                fps_value = f"{1 / max(current_time - prev_time, 1e-6):.0f}"
                prev_time = current_time

                update_session_stats(processed["num_objects"], processed["class_names"])

                if processed["alarm_triggered"] and processed["closest_object"]:
                    if current_time - st.session_state.alarm_cooldown > 1.0:
                        if settings["enable_alarm"]:
                            play_alarm_sound(settings["alarm_type"])
                        st.session_state.alarm_cooldown = current_time
                        st.session_state.session_stats["alerts"] += 1
                        register_event(
                            "Proximity alert",
                            f"{processed['closest_object'].title()} at {processed['closest_distance']:.1f}m.",
                            "alert_history",
                        )
                        add_text_to_frame(
                            processed["annotated_frame"],
                            "PROXIMITY ALERT",
                            (50, 100),
                            (0, 0, 255),
                            1.3,
                            3,
                        )

                    if current_time - st.session_state.auto_snapshot_cooldown > 4.0:
                        handle_snapshot(
                            processed["annotated_frame"],
                            f"Auto-captured alert: {processed['closest_object'].title()} at {processed['closest_distance']:.1f}m",
                        )
                        st.session_state.auto_snapshot_cooldown = current_time

                if st.session_state.snapshot_requested:
                    handle_snapshot(
                        processed["annotated_frame"],
                        st.session_state.session_stats["last_classes"],
                    )

                if settings["show_fps"]:
                    add_text_to_frame(processed["annotated_frame"], f"FPS: {fps_value}", (10, 30))

                video_placeholder.image(
                    cv2.cvtColor(processed["annotated_frame"], cv2.COLOR_BGR2RGB),
                    channels="RGB",
                    use_container_width=True,
                )
                render_live_metrics(
                    objects_placeholder,
                    closest_placeholder,
                    fps_placeholder,
                    alert_count_placeholder,
                    processed["num_objects"],
                    processed["closest_distance"],
                    processed["closest_object"],
                    fps_value,
                    settings,
                )
                render_result_panels(
                    detection_details,
                    alert_box,
                    live_timeline,
                    session_panel,
                    processed,
                    settings,
                )
                time.sleep(0.01)

            cap.release()
            if not st.session_state.run_detection:
                st.success("Detection session stopped successfully.")
    else:
        uploaded_file = settings["uploaded_file"]
        if uploaded_file is None:
            st.info("Upload an image from the sidebar, then click Analyze Image.")
            render_live_metrics(
                objects_placeholder,
                closest_placeholder,
                fps_placeholder,
                alert_count_placeholder,
                0,
                float("inf"),
                None,
                "--",
                settings,
            )
            render_result_panels(
                detection_details,
                alert_box,
                live_timeline,
                session_panel,
                {
                    "alarm_triggered": False,
                    "closest_object": None,
                    "closest_distance": float("inf"),
                    "detection_list": [],
                },
                settings,
            )
        else:
            upload_bytes = uploaded_file.getvalue()
            upload_token = f"{uploaded_file.name}:{len(upload_bytes)}"
            frame = cv2.imdecode(np.frombuffer(upload_bytes, np.uint8), cv2.IMREAD_COLOR)

            if frame is None:
                st.error("The uploaded image could not be read. Please try another file.")
                st.session_state.run_detection = False
            else:
                processed = process_frame(frame, settings)

                if st.session_state.last_processed_upload_token != upload_token:
                    update_session_stats(processed["num_objects"], processed["class_names"])
                    st.session_state.last_processed_upload_token = upload_token

                    if processed["alarm_triggered"] and processed["closest_object"]:
                        st.session_state.session_stats["alerts"] += 1
                        register_event(
                            "Uploaded image alert",
                            f"{processed['closest_object'].title()} at {processed['closest_distance']:.1f}m.",
                            "alert_history",
                        )
                    else:
                        register_event("Image analyzed", f"Processed {uploaded_file.name}.")

                if st.session_state.snapshot_requested:
                    handle_snapshot(processed["annotated_frame"], uploaded_file.name)

                video_placeholder.image(
                    cv2.cvtColor(processed["annotated_frame"], cv2.COLOR_BGR2RGB),
                    channels="RGB",
                    use_container_width=True,
                )
                render_live_metrics(
                    objects_placeholder,
                    closest_placeholder,
                    fps_placeholder,
                    alert_count_placeholder,
                    processed["num_objects"],
                    processed["closest_distance"],
                    processed["closest_object"],
                    "Static",
                    settings,
                )
                render_result_panels(
                    detection_details,
                    alert_box,
                    live_timeline,
                    session_panel,
                    processed,
                    settings,
                )
                st.success("Image analyzed successfully.")
                st.session_state.run_detection = False
else:
    render_welcome_screen()

    if settings["input_source"] == "Uploaded Image" and settings["uploaded_file"] is not None:
        st.info("Image uploaded and ready. Click Analyze Image to run detection.")

    stats = st.session_state.session_stats
    started_at = (
        stats["session_started_at"].strftime("%d %b %Y • %H:%M:%S")
        if stats["session_started_at"]
        else "Not started yet"
    )

    analytics_col1, analytics_col2, analytics_col3 = st.columns(3)
    analytics_col1.markdown(
        render_metric_card("Frames processed", stats["processed_frames"], started_at, "default"),
        unsafe_allow_html=True,
    )
    analytics_col2.markdown(
        render_metric_card("Peak detections", stats["peak_objects"], stats["last_classes"], "warning"),
        unsafe_allow_html=True,
    )
    analytics_col3.markdown(
        render_metric_card("Last snapshot", stats["last_snapshot"], "Archive status", "safe"),
        unsafe_allow_html=True,
    )

    lower_col1, lower_col2 = st.columns([1.1, 0.9])
    with lower_col1:
        st.markdown(
            render_snapshot_gallery(st.session_state.snapshots),
            unsafe_allow_html=True,
        )
    with lower_col2:
        st.markdown(
            render_activity_timeline(
                st.session_state.alert_history or st.session_state.detection_history
            )
        )
