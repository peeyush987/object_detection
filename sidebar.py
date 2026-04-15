import streamlit as st  # type: ignore

from config import (
    DEFAULT_CONFIDENCE,
    DEFAULT_DISTANCE_THRESHOLD,
    DEFAULT_FOCAL_LENGTH,
    KNOWN_OBJECT_SIZES,
    MODEL_OPTIONS,
)


def render_sidebar():
    """Render and return all sidebar settings."""
    with st.sidebar:
        st.markdown("## Control Center")
        st.caption("Tune the detection pipeline for live monitoring or uploaded-image analysis.")

        st.markdown("### Input")
        input_source = st.radio(
            "Input source",
            ["Live Camera", "Uploaded Image"],
            help="Use your local webcam for real-time monitoring or upload an image for hosted deployments.",
        )

        st.markdown("### Model")
        model_option = st.selectbox(
            "Detection model",
            list(MODEL_OPTIONS.keys()),
            label_visibility="collapsed",
        )

        uploaded_file = None
        camera_index = 0
        if input_source == "Live Camera":
            st.markdown("### Camera")
            camera_index = st.selectbox(
                "Camera source",
                [0, 1, 2],
                index=0,
                help="Select the connected camera input to use for the live feed.",
            )
        else:
            st.markdown("### Upload")
            uploaded_file = st.file_uploader(
                "Upload image",
                type=["jpg", "jpeg", "png", "webp"],
                help="Upload a single image for detection. This mode works well on Streamlit Cloud.",
            )

        confidence = st.slider(
            "Detection confidence",
            0.0,
            1.0,
            DEFAULT_CONFIDENCE,
            0.05,
            help="Higher values reduce weak detections but may miss distant objects.",
        )

        st.markdown("### Alerts")
        enable_alarm = st.toggle("Enable proximity alarm", value=True)

        if enable_alarm:
            distance_threshold = st.slider(
                "Alert distance (meters)",
                1.0,
                20.0,
                DEFAULT_DISTANCE_THRESHOLD,
                0.5,
                help="Trigger an alert when a monitored object enters this range.",
            )
            alarm_type = st.selectbox("Alarm style", ["Beep", "Siren", "Voice Alert"])
        else:
            distance_threshold = DEFAULT_DISTANCE_THRESHOLD
            alarm_type = "Beep"

        st.markdown("### Calibration")
        focal_length = st.number_input(
            "Focal length (pixels)",
            100,
            2000,
            DEFAULT_FOCAL_LENGTH,
            50,
            help="Adjust this for more accurate distance estimation based on your camera.",
        )

        st.markdown("### Monitoring scope")
        monitor_all = st.toggle("Monitor all supported objects", value=True)

        if not monitor_all:
            monitored_objects = st.multiselect(
                "Tracked object classes",
                list(KNOWN_OBJECT_SIZES.keys()),
                default=["person", "car"],
                help="Choose which known objects should trigger proximity monitoring.",
            )
        else:
            monitored_objects = list(KNOWN_OBJECT_SIZES.keys())

        st.markdown("### Display")
        show_distance = st.checkbox("Show estimated distance", value=True)
        show_labels = st.checkbox("Show labels list", value=True)
        show_conf = st.checkbox("Include confidence scores", value=True)
        show_fps = st.checkbox("Show live FPS", value=True)

        st.markdown("---")
        st.caption(
            f"{len(monitored_objects)} classes monitored • "
            f"threshold {distance_threshold:.1f} m • confidence {confidence:.0%}"
        )

    return {
        "input_source": input_source,
        "model_option": model_option,
        "camera_index": camera_index,
        "uploaded_file": uploaded_file,
        "confidence": confidence,
        "enable_alarm": enable_alarm,
        "distance_threshold": distance_threshold,
        "alarm_type": alarm_type,
        "focal_length": focal_length,
        "monitored_objects": monitored_objects,
        "show_distance": show_distance,
        "show_labels": show_labels,
        "show_conf": show_conf,
        "show_fps": show_fps,
    }
