from datetime import datetime

import streamlit as st  # type: ignore


def render_header():
    """Render the primary application hero section."""
    st.markdown(
        """
        <section class="hero-shell">
            <div class="hero-copy">
                <div class="eyebrow">Vision Operations Console</div>
                <h1 class="main-title">AI Object Detection Command Center</h1>
                <p class="subtitle">
                    Real-time object monitoring, proximity intelligence, incident snapshots,
                    and session analytics in one operational workspace.
                </p>
            </div>
            <div class="hero-badge">
                <span class="badge-label">Live readiness</span>
                <span class="badge-value">Model + Camera Workflow</span>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_metric_card(label, value, subtitle="", tone="default"):
    """Render a metric card."""
    return f"""
        <div class="metric-card metric-{tone}">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            {f'<div class="metric-subtitle">{subtitle}</div>' if subtitle else ""}
        </div>
    """


def render_alarm_status(is_active, object_name=""):
    """Render alert status card."""
    if is_active:
        return f"""
            <div class="status-card status-alert">
                <div class="status-title">Alert Active</div>
                <div class="status-copy">{object_name.title()} inside threshold zone</div>
            </div>
        """
    return """
        <div class="status-card status-safe">
            <div class="status-title">System Safe</div>
            <div class="status-copy">No monitored object is inside the alert boundary</div>
        </div>
    """


def render_detection_list(detections):
    """Render list of detected objects."""
    if not detections:
        return """
            <div class="panel-card panel-muted">
                <div class="panel-title">Current detections</div>
                <p class="panel-copy">No objects detected in the current frame.</p>
            </div>
        """

    items = "".join(
        f"<div class='detection-item'><span>{item}</span></div>" for item in detections[:10]
    )
    return f"""
        <div class="panel-card">
            <div class="panel-title">Current detections</div>
            <div class="detection-list">{items}</div>
        </div>
    """


def render_system_overview(settings, model_name):
    """Render compact system configuration details."""
    monitored_count = len(settings["monitored_objects"])
    source_value = (
        f"Camera {settings['camera_index']}"
        if settings["input_source"] == "Live Camera"
        else "Uploaded image"
    )
    return f"""
        <div class="panel-card">
            <div class="panel-title">Monitoring profile</div>
            <div class="kv-grid">
                <div><span>Source</span><strong>{source_value}</strong></div>
                <div><span>Model</span><strong>{settings["model_option"]}</strong></div>
                <div><span>Confidence</span><strong>{settings["confidence"]:.0%}</strong></div>
                <div><span>Alert range</span><strong>{settings["distance_threshold"]:.1f} m</strong></div>
                <div><span>Alarm</span><strong>{'Enabled' if settings["enable_alarm"] else 'Disabled'}</strong></div>
                <div><span>Tracked classes</span><strong>{monitored_count}</strong></div>
            </div>
            <div class="panel-footnote">Loaded model file: {model_name}</div>
        </div>
    """


def render_activity_timeline(events):
    """Render recent activity timeline."""
    if not events:
        return (
            "### Activity timeline\n"
            "_Events will appear here when detection starts._"
        )

    rows = ["### Activity timeline"]
    for event in events[:8]:
        timestamp = event.get("timestamp")
        if isinstance(timestamp, datetime):
            stamp = timestamp.strftime("%H:%M:%S")
        else:
            stamp = str(timestamp)
        title = event.get("title", "Event")
        detail = event.get("detail", "")
        rows.append(f"- `{stamp}` **{title}**  ")
        rows.append(f"  {detail}")

    return "\n".join(rows)


def render_snapshot_gallery(snapshots):
    """Render recent snapshots."""
    if not snapshots:
        return """
            <div class="panel-card panel-muted">
                <div class="panel-title">Snapshot archive</div>
                <p class="panel-copy">Save a snapshot during detection to build an incident record.</p>
            </div>
        """

    cards = []
    for snapshot in snapshots[:6]:
        cards.append(
            f"""
            <div class="snapshot-item">
                <div class="snapshot-name">{snapshot["name"]}</div>
                <div class="snapshot-meta">{snapshot["timestamp"]}</div>
                <div class="snapshot-meta">{snapshot["summary"]}</div>
            </div>
            """
        )

    return f"""
        <div class="panel-card">
            <div class="panel-title">Snapshot archive</div>
            <div class="snapshot-grid">{''.join(cards)}</div>
        </div>
    """


def render_welcome_screen():
    """Render welcome screen when detection is not running."""
    st.markdown(
        """
        <section class="welcome-shell">
            <div class="welcome-card welcome-primary">
                <div class="eyebrow">Ready to monitor</div>
                <h2>Launch a polished live detection workflow</h2>
                <p>
                    Tune your camera, choose the right model, and start a session when you're
                    ready. The app now keeps a timeline of alerts, preserves snapshots, and
                    surfaces live operational metrics.
                </p>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-kicker">Live Vision</div>
                <h3>Operational monitoring</h3>
                <p>Real-time object detection with FPS, class summaries, and distance overlays.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-kicker">Alerting</div>
                <h3>Actionable proximity warnings</h3>
                <p>Threshold-aware alerts with audio feedback and incident history for review.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col3:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-kicker">Evidence</div>
                <h3>Snapshot archive</h3>
                <p>Capture annotated frames and retain a lightweight visual log of key moments.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
