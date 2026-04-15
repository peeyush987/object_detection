def get_custom_css():
    """Returns custom CSS styling for the application."""
    return """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap');

    :root {
        --bg: #081120;
        --bg-soft: #0f1a2f;
        --panel: rgba(10, 18, 33, 0.82);
        --panel-strong: rgba(18, 28, 48, 0.96);
        --card-border: rgba(146, 172, 212, 0.18);
        --text: #ecf3ff;
        --muted: #97a7c3;
        --accent: #5eead4;
        --accent-strong: #20c997;
        --warning: #ffb84d;
        --danger: #ff6b6b;
        --safe: #36d399;
        --shadow: 0 20px 50px rgba(0, 0, 0, 0.25);
        --radius-lg: 24px;
        --radius-md: 18px;
        --radius-sm: 14px;
    }

    html, body, [class*="css"] {
        font-family: "Manrope", sans-serif;
    }

    .stApp {
        background:
            radial-gradient(circle at top left, rgba(32, 201, 151, 0.18), transparent 28%),
            radial-gradient(circle at top right, rgba(94, 234, 212, 0.12), transparent 20%),
            linear-gradient(180deg, #06101d 0%, #091425 45%, #081120 100%);
        color: var(--text);
    }

    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1440px;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(6, 15, 30, 0.97), rgba(10, 20, 38, 0.98));
        border-right: 1px solid rgba(148, 163, 184, 0.12);
    }

    [data-testid="stSidebar"] * {
        color: var(--text);
    }

    .hero-shell,
    .panel-card,
    .metric-card,
    .status-card,
    .video-shell,
    .feed-shell,
    .feature-card,
    .welcome-card,
    .control-strip {
        backdrop-filter: blur(18px);
        background: var(--panel);
        border: 1px solid var(--card-border);
        box-shadow: var(--shadow);
    }

    .hero-shell {
        border-radius: 32px;
        padding: 2rem;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: flex-start;
        justify-content: space-between;
        gap: 1.5rem;
        background:
            linear-gradient(135deg, rgba(18, 28, 48, 0.94), rgba(7, 14, 27, 0.92)),
            linear-gradient(120deg, rgba(94, 234, 212, 0.2), transparent 55%);
    }

    .hero-copy {
        max-width: 760px;
    }

    .eyebrow {
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
        border-radius: 999px;
        padding: 0.45rem 0.8rem;
        margin-bottom: 0.9rem;
        background: rgba(94, 234, 212, 0.12);
        color: var(--accent);
        font-size: 0.82rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }

    .main-title {
        margin: 0;
        font-size: clamp(2.4rem, 4vw, 4rem);
        line-height: 1.02;
        letter-spacing: -0.04em;
        color: var(--text);
    }

    .subtitle {
        margin: 1rem 0 0;
        max-width: 680px;
        color: var(--muted);
        font-size: 1.05rem;
        line-height: 1.7;
    }

    .hero-badge {
        min-width: 230px;
        border-radius: 24px;
        padding: 1rem 1.1rem;
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.08);
    }

    .badge-label {
        display: block;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: var(--muted);
    }

    .badge-value {
        display: block;
        margin-top: 0.4rem;
        font-size: 1rem;
        font-weight: 700;
        color: var(--text);
    }

    .control-strip,
    .panel-card,
    .feature-card,
    .welcome-card,
    .video-shell {
        border-radius: var(--radius-lg);
    }

    .control-strip {
        padding: 0.9rem 1rem;
        margin-bottom: 1rem;
        background: rgba(11, 19, 34, 0.76);
    }

    .metric-card {
        border-radius: 20px;
        padding: 1.25rem;
        min-height: 145px;
        background:
            linear-gradient(180deg, rgba(16, 27, 46, 0.96), rgba(10, 18, 33, 0.96));
    }

    .metric-default {
        border-top: 3px solid rgba(94, 234, 212, 0.9);
    }

    .metric-warning {
        border-top: 3px solid rgba(255, 184, 77, 0.95);
    }

    .metric-danger {
        border-top: 3px solid rgba(255, 107, 107, 0.95);
    }

    .metric-safe {
        border-top: 3px solid rgba(54, 211, 153, 0.95);
    }

    .metric-label {
        color: var(--muted);
        font-size: 0.82rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }

    .metric-value {
        margin-top: 0.75rem;
        font-size: clamp(1.8rem, 3vw, 2.7rem);
        font-weight: 800;
        color: var(--text);
        line-height: 1;
    }

    .metric-subtitle {
        margin-top: 0.65rem;
        color: var(--muted);
        font-size: 0.95rem;
    }

    .status-card {
        border-radius: 20px;
        padding: 1.15rem;
        min-height: 145px;
    }

    .status-safe {
        background: linear-gradient(135deg, rgba(15, 78, 56, 0.9), rgba(22, 102, 72, 0.7));
    }

    .status-alert {
        background: linear-gradient(135deg, rgba(125, 31, 31, 0.94), rgba(174, 50, 50, 0.76));
        animation: pulse 1.4s infinite;
    }

    .status-title {
        font-size: 1.1rem;
        font-weight: 800;
        color: #fff;
    }

    .status-copy {
        margin-top: 0.6rem;
        color: rgba(255, 255, 255, 0.88);
        line-height: 1.55;
    }

    .panel-card {
        padding: 1.2rem;
        background: rgba(10, 18, 33, 0.8);
        margin-bottom: 1rem;
    }

    .panel-muted {
        background: rgba(10, 18, 33, 0.55);
    }

    .panel-title {
        margin-bottom: 0.9rem;
        font-size: 1rem;
        font-weight: 800;
        color: var(--text);
    }

    .panel-copy,
    .panel-footnote {
        color: var(--muted);
        line-height: 1.6;
    }

    .panel-footnote {
        margin-top: 1rem;
        font-size: 0.9rem;
    }

    .kv-grid {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 0.85rem;
    }

    .kv-grid div {
        padding: 0.85rem;
        border-radius: 14px;
        background: rgba(255, 255, 255, 0.03);
    }

    .kv-grid span {
        display: block;
        font-size: 0.78rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: var(--muted);
    }

    .kv-grid strong {
        display: block;
        margin-top: 0.35rem;
        color: var(--text);
        font-size: 0.96rem;
    }

    .video-shell {
        padding: 1.2rem;
        background: rgba(10, 18, 33, 0.76);
    }

    .feed-title {
        margin-bottom: 1rem;
        font-size: 1.05rem;
        font-weight: 800;
        color: var(--text);
    }

    .danger-box {
        border-radius: 18px;
        padding: 1rem 1.1rem;
        background: rgba(176, 44, 44, 0.18);
        border: 1px solid rgba(255, 107, 107, 0.25);
        color: #ffd7d7;
        animation: pulse 1.4s infinite;
    }

    .detection-list {
        display: grid;
        gap: 0.65rem;
    }

    .detection-item,
    .timeline-item,
    .snapshot-item {
        border-radius: 16px;
        padding: 0.9rem 1rem;
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.06);
    }

    .detection-item {
        border-left: 3px solid var(--accent);
        color: var(--text);
        font-weight: 600;
    }

    .timeline-list,
    .snapshot-grid {
        display: grid;
        gap: 0.75rem;
    }

    .timeline-item {
        display: grid;
        grid-template-columns: 88px minmax(0, 1fr);
        gap: 0.8rem;
    }

    .timeline-time,
    .snapshot-meta {
        color: var(--muted);
        font-size: 0.86rem;
    }

    .timeline-content {
        display: grid;
        gap: 0.25rem;
    }

    .timeline-content strong,
    .snapshot-name {
        color: var(--text);
        font-size: 0.95rem;
    }

    .timeline-content span {
        color: var(--muted);
        line-height: 1.55;
    }

    .snapshot-grid {
        grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
    }

    .welcome-shell {
        margin: 0.5rem 0 1rem;
    }

    .welcome-primary {
        padding: 1.7rem;
        background:
            linear-gradient(135deg, rgba(15, 24, 41, 0.95), rgba(9, 16, 29, 0.88)),
            linear-gradient(120deg, rgba(94, 234, 212, 0.16), transparent 60%);
    }

    .welcome-card h2,
    .feature-card h3 {
        color: var(--text);
        margin-bottom: 0.5rem;
    }

    .welcome-card p,
    .feature-card p,
    .feature-kicker {
        color: var(--muted);
        line-height: 1.65;
    }

    .feature-card {
        padding: 1.35rem;
        min-height: 195px;
        background: rgba(10, 18, 33, 0.72);
    }

    .feature-kicker {
        font-size: 0.78rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: var(--accent);
    }

    .stButton > button,
    .stDownloadButton > button {
        width: 100%;
        min-height: 3rem;
        border: 1px solid rgba(94, 234, 212, 0.16);
        border-radius: 14px;
        background: linear-gradient(180deg, rgba(17, 28, 47, 0.96), rgba(10, 18, 33, 0.96));
        color: var(--text);
        font-weight: 700;
        transition: transform 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease;
    }

    .stButton > button:hover,
    .stDownloadButton > button:hover {
        transform: translateY(-1px);
        border-color: rgba(94, 234, 212, 0.4);
        box-shadow: 0 12px 30px rgba(6, 182, 212, 0.16);
        color: var(--text);
    }

    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #14b8a6, #0f766e);
        border-color: rgba(94, 234, 212, 0.4);
    }

    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div,
    .stSlider [data-baseweb="slider"] {
        background-color: rgba(255, 255, 255, 0.03) !important;
    }

    [data-testid="stMetric"] {
        background: transparent;
    }

    [data-testid="stImage"] img {
        border-radius: 18px;
        border: 1px solid rgba(255, 255, 255, 0.08);
    }

    #MainMenu,
    footer {
        visibility: hidden;
    }

    @keyframes pulse {
        0%, 100% { transform: scale(1); opacity: 1; }
        50% { transform: scale(0.995); opacity: 0.88; }
    }

    @media (max-width: 1100px) {
        .hero-shell {
            flex-direction: column;
        }

        .hero-badge {
            width: 100%;
        }
    }

    @media (max-width: 768px) {
        .main .block-container {
            padding-top: 1.2rem;
            padding-left: 1rem;
            padding-right: 1rem;
        }

        .kv-grid,
        .timeline-item {
            grid-template-columns: 1fr;
        }

        .metric-card,
        .status-card {
            min-height: auto;
        }
    }
    </style>
    """
