import streamlit as st
import joblib
import os
import html
from datetime import datetime

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="SpamGuard AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# SESSION STATE
# ============================================================

if "total_scans" not in st.session_state:
    st.session_state.total_scans = 0

if "spam_count" not in st.session_state:
    st.session_state.spam_count = 0

if "legitimate_count" not in st.session_state:
    st.session_state.legitimate_count = 0

if "recent_scans" not in st.session_state:
    st.session_state.recent_scans = []

# ============================================================
# MODEL PATHS
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "spam_model.pkl"
)

VECTORIZER_PATH = os.path.join(
    BASE_DIR,
    "models",
    "tfidf_vectorizer.pkl"
)

# ============================================================
# LOAD MODEL
# ============================================================

@st.cache_resource
def load_model():

    if not os.path.exists(MODEL_PATH):
        return None, None, f"Model not found: {MODEL_PATH}"

    if not os.path.exists(VECTORIZER_PATH):
        return None, None, f"Vectorizer not found: {VECTORIZER_PATH}"

    try:
        model = joblib.load(MODEL_PATH)
        vectorizer = joblib.load(VECTORIZER_PATH)

        return model, vectorizer, None

    except Exception as e:
        return None, None, str(e)


model, vectorizer, model_error = load_model()

# ============================================================
# GLOBAL CSS + JAVASCRIPT
# ============================================================

st.html(
"""
<style>

/* ============================================================
   IMPORT FONT
============================================================ */

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');


/* ============================================================
   GLOBAL
============================================================ */

html {
    scroll-behavior: smooth;
}

body {
    background: #050507;
}

.stApp {

    background:
        radial-gradient(
            circle at 80% 5%,
            rgba(255, 25, 55, 0.13),
            transparent 30%
        ),
        radial-gradient(
            circle at 10% 45%,
            rgba(255, 0, 45, 0.08),
            transparent 30%
        ),
        radial-gradient(
            circle at 90% 85%,
            rgba(180, 0, 40, 0.08),
            transparent 30%
        ),
        #050507;

    color: #f5f5f7;
    font-family: 'Inter', sans-serif;
}


/* ============================================================
   REMOVE STREAMLIT DEFAULT ELEMENTS
============================================================ */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    background: transparent !important;
}


/* ============================================================
   SIDEBAR
============================================================ */

[data-testid="stSidebar"] {

    background:
        linear-gradient(
            180deg,
            rgba(10, 7, 12, 0.98),
            rgba(7, 5, 9, 0.98)
        );

    border-right: 1px solid rgba(255, 40, 70, 0.18);

    min-width: 245px;
}

[data-testid="stSidebar"] > div:first-child {
    padding-top: 25px;
}


/* ============================================================
   SIDEBAR BRAND
============================================================ */

.brand {

    padding: 5px 12px 25px 12px;

    border-bottom:
        1px solid
        rgba(255,255,255,0.06);

}

.brand-icon {

    width: 45px;
    height: 45px;

    border-radius: 13px;

    display: flex;
    align-items: center;
    justify-content: center;

    background:
        linear-gradient(
            145deg,
            rgba(255,35,65,.25),
            rgba(255,0,0,.05)
        );

    border:
        1px solid
        rgba(255,50,70,.65);

    box-shadow:
        0 0 25px
        rgba(255,20,50,.18);

    font-size: 23px;

    margin-bottom: 14px;
}

.brand-title {

    font-size: 20px;
    font-weight: 800;
    letter-spacing: -0.5px;

}

.brand-subtitle {

    margin-top: 5px;

    color: #888;

    font-size: 12px;

}


/* ============================================================
   NAVIGATION
============================================================ */

.nav-title {

    margin-top: 25px;
    margin-bottom: 12px;

    color: #666;

    font-family:
        'JetBrains Mono',
        monospace;

    font-size: 10px;

    letter-spacing: 1.5px;

    text-transform: uppercase;

}

.nav-item {

    padding:
        12px 13px;

    margin:
        5px 0;

    border-radius: 10px;

    color: #9b9b9f;

    font-size: 13px;

    border:
        1px solid
        transparent;

    transition:
        all .25s ease;

}

.nav-item:hover {

    color: white;

    background:
        rgba(255,30,55,.07);

    border-color:
        rgba(255,40,60,.15);

}

.nav-item.active {

    color: white;

    background:
        linear-gradient(
            90deg,
            rgba(255,30,55,.16),
            rgba(255,30,55,.04)
        );

    border:
        1px solid
        rgba(255,40,60,.45);

    box-shadow:
        inset 3px 0 0
        #ff304d,
        0 0 20px
        rgba(255,30,55,.08);

}


/* ============================================================
   MODEL STATUS
============================================================ */

.model-status {

    margin-top: 25px;

    padding:
        15px;

    border-radius: 12px;

    background:
        rgba(255,255,255,.025);

    border:
        1px solid
        rgba(255,255,255,.07);

}

.status-row {

    display: flex;
    align-items: center;
    gap: 8px;

    color: #e9e9e9;

    font-size: 12px;
    font-weight: 600;

}

.status-dot {

    width: 8px;
    height: 8px;

    border-radius: 50%;

    background: #00e59a;

    box-shadow:
        0 0 10px
        rgba(0,229,154,.8);

}

.status-text {

    margin-top: 8px;

    color: #777;

    font-size: 10px;

}


/* ============================================================
   MAIN CONTAINER
============================================================ */

.block-container {

    max-width: 1450px;

    padding-top: 35px !important;
    padding-left: 45px !important;
    padding-right: 45px !important;
}


/* ============================================================
   TOP BAR
============================================================ */

.topbar {
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 14px 4px 24px;
    color: #a9a3a8;
    font-family: "Courier New", monospace;
    font-size: 12px;
    letter-spacing: 1px;
}

.topbar-left {
    display: flex;
    align-items: center;
    gap: 8px;
}

.topbar-brand {
    color: #ff405f;
    font-weight: 700;
}

.topbar-separator {
    color: #5e5559;
}

.topbar-right {
    display: flex;
    align-items: center;
    gap: 28px;
}

.status {
    display: flex;
    align-items: center;
    gap: 8px;
}

.status-dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: #ff405f;
    box-shadow: 0 0 12px #ff405f;
    animation: pulseStatus 1.8s infinite;
}

.version {
    color: #777075;
}

@keyframes pulseStatus {
    0%, 100% {
        opacity: 1;
        transform: scale(1);
    }

    50% {
        opacity: .45;
        transform: scale(.75);
    }
}

/* ============================================================
   HERO
============================================================ */

.hero {

    position: relative;

    overflow: hidden;

    min-height: 205px;

    padding:
        36px 42px;

    border-radius: 18px;

    border:
        1px solid
        rgba(255,45,70,.65);

    background:

        radial-gradient(
            circle at 85% 45%,
            rgba(255,25,55,.20),
            transparent 30%
        ),

        linear-gradient(
            135deg,
            rgba(30,8,15,.95),
            rgba(10,7,12,.90)
        );

    box-shadow:

        0 0 35px
        rgba(255,20,50,.10),

        inset 0 0 40px
        rgba(255,20,50,.03);

}

.hero::before {

    content: "";

    position: absolute;

    width: 450px;
    height: 450px;

    right: -120px;
    top: -180px;

    border-radius: 50%;

    background:
        radial-gradient(
            circle,
            rgba(255,25,50,.20),
            transparent 65%
        );

    filter: blur(20px);

}

.hero::after {

    content: "";

    position: absolute;

    inset: 0;

    background:
        linear-gradient(
            115deg,
            transparent 40%,
            rgba(255,50,70,.06),
            transparent 60%
        );

    animation:
        heroShine 5s
        linear infinite;

}

@keyframes heroShine {

    0% {
        transform: translateX(-100%);
    }

    50% {
        transform: translateX(100%);
    }

    100% {
        transform: translateX(100%);
    }

}

.hero-badge {

    position: relative;

    display: inline-block;

    padding:
        7px 13px;

    border-radius: 30px;

    border:
        1px solid
        rgba(255,40,60,.5);

    background:
        rgba(255,20,40,.07);

    color: #ff667a;

    font-family:
        'JetBrains Mono',
        monospace;

    font-size: 10px;

    letter-spacing: 1.5px;

    z-index: 2;

}

.hero-title {

    position: relative;

    margin-top: 18px;

    font-size: clamp(32px, 4vw, 52px);

    font-weight: 800;

    letter-spacing: -2px;

    line-height: 1;

    z-index: 2;

    background:
        linear-gradient(
            90deg,
            #ffffff,
            #ff526c,
            #ffb0bd,
            #ffffff
        );

    background-size: 300% auto;

    -webkit-background-clip: text;

    -webkit-text-fill-color: transparent;

    animation:
        gradientTitle 5s
        ease infinite;

}

@keyframes gradientTitle {

    0% {
        background-position: 0% center;
    }

    50% {
        background-position: 100% center;
    }

    100% {
        background-position: 0% center;
    }

}

.hero-subtitle {

    position: relative;

    margin-top: 14px;

    color: #999;

    font-size: 14px;

    z-index: 2;

}

.hero-tags {

    position: relative;

    display: flex;

    gap: 8px;

    margin-top: 22px;

    z-index: 2;

}

.hero-tag {

    padding:
        6px 11px;

    border:
        1px solid
        rgba(255,255,255,.10);

    border-radius: 20px;

    color: #aaa;

    background:
        rgba(255,255,255,.025);

    font-size: 10px;

}


/* ============================================================
   KPI
============================================================ */

.kpi-grid {

    display: grid;

    grid-template-columns:
        repeat(4, 1fr);

    gap: 15px;

    margin-top: 18px;

}

.kpi {

    position: relative;

    overflow: hidden;

    padding: 21px;

    min-height: 120px;

    border-radius: 15px;

    background:
        linear-gradient(
            145deg,
            rgba(255,255,255,.045),
            rgba(255,255,255,.015)
        );

    border:
        1px solid
        rgba(255,255,255,.09);

    backdrop-filter:
        blur(18px);

    transition:
        transform .3s ease,
        box-shadow .3s ease,
        border-color .3s ease;

}

.kpi:hover {

    transform:
        translateY(-5px);

    border-color:
        rgba(255,45,70,.55);

    box-shadow:
        0 15px 35px
        rgba(255,20,50,.12);

}

.kpi-label {

    color: #777;

    font-family:
        'JetBrains Mono',
        monospace;

    font-size: 10px;

    letter-spacing: 1px;

}

.kpi-value {

    margin-top: 12px;

    font-size: 31px;

    font-weight: 800;

}

.kpi-description {

    margin-top: 5px;

    color: #666;

    font-size: 10px;

}

.kpi-icon {

    position: absolute;

    right: 18px;
    top: 18px;

    width: 35px;
    height: 35px;

    display: flex;
    align-items: center;
    justify-content: center;

    border-radius: 9px;

    color: #ff405c;

    background:
        rgba(255,30,50,.08);

    border:
        1px solid
        rgba(255,40,60,.18);

}

.kpi-red {

    color: #ff415c;

}

.kpi-green {

    color: #00e5a0;

}

.kpi-model {

    color: #fff;

}


/* ============================================================
   PANELS
============================================================ */

.panel {

    position: relative;

    padding: 25px;

    border-radius: 16px;

    background:
        linear-gradient(
            145deg,
            rgba(255,255,255,.045),
            rgba(255,255,255,.012)
        );

    border:
        1px solid
        rgba(255,255,255,.09);

    backdrop-filter:
        blur(20px);

    box-shadow:
        inset 0 1px 0
        rgba(255,255,255,.03);

    transition:
        transform .35s ease,
        border-color .35s ease,
        box-shadow .35s ease;

}

.panel:hover {

    transform:
        translateY(-3px);

    border-color:
        rgba(255,40,60,.35);

    box-shadow:
        0 15px 35px
        rgba(255,20,50,.08);

}

.panel-title {

    display: flex;

    align-items: center;

    gap: 10px;

    font-size: 17px;

    font-weight: 700;

}

.panel-subtitle {

    margin-top: 7px;

    color: #777;

    font-size: 11px;

}


/* ============================================================
   TEXT AREA
============================================================ */

div[data-testid="stTextArea"] textarea {

    background:
        rgba(5,7,12,.85) !important;

    color: #f5f5f7 !important;

    border:
        1px solid
        rgba(255,255,255,.10) !important;

    border-radius: 12px !important;

    font-family:
        'Inter',
        sans-serif !important;

    font-size: 14px !important;

    padding: 17px !important;

    min-height: 145px !important;

    transition:
        all .25s ease !important;

}

div[data-testid="stTextArea"] textarea:focus {

    border-color:
        rgba(255,45,70,.7) !important;

    box-shadow:
        0 0 25px
        rgba(255,30,50,.10) !important;

}


/* ============================================================
   BUTTON
============================================================ */

.stButton > button {

    border:
        1px solid
        rgba(255,50,70,.75) !important;

    border-radius: 9px !important;

    background:
        linear-gradient(
            135deg,
            #ff1f3d,
            #b50020
        ) !important;

    color: white !important;

    font-weight: 700 !important;

    padding:
        10px 23px !important;

    box-shadow:
        0 0 25px
        rgba(255,25,50,.20) !important;

    transition:
        all .25s ease !important;

}

.stButton > button:hover {

    transform:
        translateY(-2px);

    box-shadow:
        0 0 35px
        rgba(255,25,50,.40) !important;

}


/* ============================================================
   QUICK EXAMPLES
============================================================ */

.example {

    padding:
        12px 13px;

    margin:
        7px 0;

    border-radius: 9px;

    background:
        rgba(255,255,255,.025);

    border:
        1px solid
        rgba(255,255,255,.07);

    color: #bbb;

    font-size: 11px;

    transition:
        all .25s ease;

}

.example:hover {

    border-color:
        rgba(255,40,60,.35);

    background:
        rgba(255,30,50,.06);

    transform:
        translateX(4px);

}


/* ============================================================
   VERDICT
============================================================ */

.verdict {

    margin-top: 18px;

    padding: 25px;

    border-radius: 16px;

    background:
        linear-gradient(
            135deg,
            rgba(0,220,150,.10),
            rgba(0,0,0,.20)
        );

    border:
        1px solid
        rgba(0,230,155,.65);

    box-shadow:
        0 0 35px
        rgba(0,230,155,.08);

}

.verdict.spam {

    background:
        linear-gradient(
            135deg,
            rgba(255,20,50,.12),
            rgba(0,0,0,.20)
        );

    border-color:
        rgba(255,40,65,.65);

    box-shadow:
        0 0 35px
        rgba(255,20,50,.10);

}

.verdict-row {

    display: flex;

    align-items: center;

    justify-content: space-between;

}

.verdict-main {

    display: flex;

    align-items: center;

    gap: 15px;

}

.verdict-icon {

    width: 55px;
    height: 55px;

    display: flex;

    align-items: center;
    justify-content: center;

    border-radius: 50%;

    background:
        rgba(0,230,155,.08);

    border:
        1px solid
        rgba(0,230,155,.35);

    color: #00e59a;

    font-size: 26px;

}

.verdict.spam .verdict-icon {

    background:
        rgba(255,30,50,.08);

    border-color:
        rgba(255,40,60,.4);

    color: #ff405d;

}

.verdict-title {

    font-size: 21px;

    font-weight: 800;

}

.verdict-description {

    margin-top: 5px;

    color: #888;

    font-size: 11px;

}

.confidence {

    text-align: right;

}

.confidence-label {

    color: #777;

    font-family:
        'JetBrains Mono',
        monospace;

    font-size: 9px;

    letter-spacing: 1px;

}

.confidence-value {

    margin-top: 5px;

    font-size: 27px;

    font-weight: 800;

}


/* ============================================================
   PROBABILITY
============================================================ */

.probability {

    margin-top: 25px;

    padding-top: 20px;

    border-top:
        1px solid
        rgba(255,255,255,.07);

}

.prob-title {

    font-size: 12px;

    font-weight: 700;

}

.prob-grid {

    display: grid;

    grid-template-columns:
        1fr 1fr;

    gap: 20px;

    margin-top: 17px;

}

.prob-label {

    display: flex;

    justify-content: space-between;

    margin-bottom: 7px;

    font-size: 10px;

    color: #888;

}

.bar {

    height: 7px;

    overflow: hidden;

    border-radius: 20px;

    background:
        rgba(255,255,255,.07);

}

.bar-fill {

    height: 100%;

    border-radius: 20px;

    transition:
        width 1s ease;

}

.spam-bar {

    background:
        linear-gradient(
            90deg,
            #ff203e,
            #ff7080
        );

}

.safe-bar {

    background:
        linear-gradient(
            90deg,
            #00b879,
            #00f1a3
        );

}


/* ============================================================
   TABLE
============================================================ */

.scan-table {

    width: 100%;

    border-collapse:
        collapse;

    margin-top: 15px;

    font-size: 10px;

}

.scan-table th {

    color: #666;

    font-family:
        'JetBrains Mono',
        monospace;

    font-size: 9px;

    text-align: left;

    padding: 9px;

    border-bottom:
        1px solid
        rgba(255,255,255,.07);

}

.scan-table td {

    color: #aaa;

    padding: 11px 9px;

    border-bottom:
        1px solid
        rgba(255,255,255,.045);

}

.badge {

    display: inline-block;

    padding:
        4px 8px;

    border-radius: 20px;

    font-size: 9px;

}

.badge-spam {

    color: #ff6578;

    background:
        rgba(255,30,50,.10);

    border:
        1px solid
        rgba(255,40,60,.25);

}

.badge-safe {

    color: #00e39b;

    background:
        rgba(0,220,150,.08);

    border:
        1px solid
        rgba(0,230,155,.22);

}


/* ============================================================
   HOW IT WORKS
============================================================ */

.step {

    display: flex;

    align-items: center;

    gap: 12px;

    padding: 10px;

    margin: 7px 0;

    border:
        1px solid
        rgba(255,255,255,.06);

    border-radius: 9px;

    background:
        rgba(255,255,255,.018);

}

.step-number {

    min-width: 29px;
    height: 29px;

    display: flex;

    align-items: center;
    justify-content: center;

    border-radius: 50%;

    background:
        rgba(255,30,50,.10);

    border:
        1px solid
        rgba(255,40,60,.35);

    color: #ff5268;

    font-size: 10px;

    font-weight: 800;

}

.step-title {

    font-size: 11px;

    font-weight: 700;

}

.step-text {

    margin-top: 2px;

    color: #666;

    font-size: 9px;

}


/* ============================================================
   REVEAL ANIMATION
============================================================ */

.reveal {

    opacity: 0;

    filter:
        blur(14px);

    transform:
        translateY(45px)
        scale(.96);

    transition:
        opacity .8s cubic-bezier(.2,.8,.2,1),
        filter .8s cubic-bezier(.2,.8,.2,1),
        transform .8s cubic-bezier(.2,.8,.2,1);

}

.reveal.visible {

    opacity: 1;

    filter:
        blur(0);

    transform:
        translateY(0)
        scale(1);

}


/* KPI stagger */

.kpi:nth-child(1) {
    transition-delay: .05s;
}

.kpi:nth-child(2) {
    transition-delay: .13s;
}

.kpi:nth-child(3) {
    transition-delay: .21s;
}

.kpi:nth-child(4) {
    transition-delay: .29s;
}


/* ============================================================
   FOOTER
============================================================ */

.footer {

    margin-top: 45px;

    padding:
        20px 0;

    border-top:
        1px solid
        rgba(255,255,255,.06);

    display: flex;

    justify-content: space-between;

    color: #555;

    font-family:
        'JetBrains Mono',
        monospace;

    font-size: 9px;

}

.footer strong {

    color: #888;

}


/* ============================================================
   RESPONSIVE
============================================================ */

@media(max-width: 900px) {

    .kpi-grid {

        grid-template-columns:
            repeat(2,1fr);

    }

    .hero-title {

        font-size: 34px;

    }

}

@media(max-width: 600px) {

    .block-container {

        padding-left: 15px !important;
        padding-right: 15px !important;

    }

    .kpi-grid {

        grid-template-columns:
            1fr;

    }

    .hero {

        padding: 25px;

    }

    .prob-grid {

        grid-template-columns:
            1fr;

    }

}


/* ============================================================
   SCROLLBAR
============================================================ */

::-webkit-scrollbar {

    width: 7px;

}

::-webkit-scrollbar-track {

    background: #050507;

}

::-webkit-scrollbar-thumb {

    background:
        linear-gradient(
            #ff304d,
            #660010
        );

    border-radius: 20px;

}

</style>


<script>

(function() {

    function initializeReveal() {

        const elements =
            document.querySelectorAll(
                '.reveal'
            );

        if (!elements.length) {
            return;
        }

        const observer =
            new IntersectionObserver(
                function(entries) {

                    entries.forEach(
                        function(entry) {

                            if (
                                entry.isIntersecting
                            ) {

                                entry.target
                                    .classList
                                    .add(
                                        'visible'
                                    );

                            } else {

                                entry.target
                                    .classList
                                    .remove(
                                        'visible'
                                    );

                            }

                        }
                    );

                },
                {
                    threshold: 0.12,
                    rootMargin:
                        '0px 0px -40px 0px'
                }
            );

        elements.forEach(
            function(element) {

                observer.observe(
                    element
                );

            }
        );

    }


    initializeReveal();


    /*
       Streamlit renders elements dynamically.
       MutationObserver makes sure newly-rendered
       cards also receive the animation.
    */

    const mutationObserver =
        new MutationObserver(
            function() {

                initializeReveal();

            }
        );

    mutationObserver.observe(
        document.body,
        {
            childList: true,
            subtree: true
        }
    );

})();

</script>
""",
unsafe_allow_javascript=True
)

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.html(
        """
        <div class="brand">

            <div class="brand-icon">
                🛡️
            </div>

            <div class="brand-title">
                SpamGuard AI
            </div>

            <div class="brand-subtitle">
                Instagram Comment Security
            </div>

        </div>
        """,
    )

    st.html(
        """
        <div class="nav-title">
            NAVIGATION
        </div>

        <div class="nav-item active">
            ◉ &nbsp; Dashboard
        </div>

        <div class="nav-item">
            ◌ &nbsp; Detection History
        </div>

        <div class="nav-item">
            ◈ &nbsp; Model Insights
        </div>

        <div class="nav-item">
            ▣ &nbsp; Data & Sources
        </div>

        <div class="nav-item">
            ⚙ &nbsp; Settings
        </div>
        """,
        
    )

    status_class = "Model Loaded" if model else "Model Error"

    st.html(
        f"""
        <div class="model-status">

            <div class="status-row">

                <span class="status-dot"></span>

                {status_class}

            </div>

            <div class="status-text">

                TF-IDF + Logistic Regression

            </div>

        </div>
        """,
        
    )

    st.html(
        """
        <div style="
            margin-top:25px;
            color:#777;
            font-size:10px;
            line-height:1.6;
        ">

        <div style="
            color:#666;
            letter-spacing:1px;
            font-size:9px;
            margin-bottom:7px;
        ">
        ABOUT
        </div>

        AI-powered spam detection
        for social media comments.

        <br><br>

        Detect suspicious promotional,
        malicious and bot-like comments.

        </div>
        """,
      
    )

# ============================================================
# TOP BAR
# ============================================================

st.html("""
<div class="topbar">
    <div class="topbar-left">
        <span class="topbar-brand">SPAMGUARD</span>
        <span class="topbar-separator">/</span>
        <span>AI SECURITY CENTER</span>
    </div>

    <div class="topbar-right">
        <div class="status">
            <span class="status-dot"></span>
            SYSTEM ONLINE
        </div>

        <div class="version">
            v1.0.0
        </div>
    </div>
</div>
""", unsafe_allow_javascript=True)

# ============================================================
# HERO
# ============================================================

st.html(
"""
<div class="hero reveal">

    <div class="hero-badge">
        ✦ AI-POWERED CONTENT SECURITY
    </div>

    <div class="hero-title">
        Instagram Spam Detection
    </div>

    <div class="hero-subtitle">
        Analyze comments using Natural Language Processing
        and Machine Learning.
    </div>

    <div class="hero-tags">

        <div class="hero-tag">
            NLP
        </div>

        <div class="hero-tag">
            TF-IDF
        </div>

        <div class="hero-tag">
            Logistic Regression
        </div>

        <div class="hero-tag">
            Social Media Security
        </div>

    </div>

</div>
""",
unsafe_allow_javascript=True
)

# ============================================================
# KPI CARDS
# ============================================================

st.html(
f"""
<div class="kpi-grid">

    <div class="kpi reveal">

        <div class="kpi-icon">
            ◉
        </div>

        <div class="kpi-label">
            TOTAL SCANS
        </div>

        <div class="kpi-value">
            {st.session_state.total_scans}
        </div>

        <div class="kpi-description">
            Comments analyzed
        </div>

    </div>


    <div class="kpi reveal">

        <div class="kpi-icon">
            ⚠
        </div>

        <div class="kpi-label">
            SPAM DETECTED
        </div>

        <div class="kpi-value kpi-red">
            {st.session_state.spam_count}
        </div>

        <div class="kpi-description">
            Potential threats
        </div>

    </div>


    <div class="kpi reveal">

        <div class="kpi-icon">
            ✓
        </div>

        <div class="kpi-label">
            LEGITIMATE
        </div>

        <div class="kpi-value kpi-green">
            {st.session_state.legitimate_count}
        </div>

        <div class="kpi-description">
            Safe comments
        </div>

    </div>


    <div class="kpi reveal">

        <div class="kpi-icon">
            ◈
        </div>

        <div class="kpi-label">
            MODEL
        </div>

        <div class="kpi-value kpi-model">
            TF-IDF
        </div>

        <div class="kpi-description">
            Logistic Regression
        </div>

    </div>

</div>
""",
unsafe_allow_javascript=True
)

st.write("")

# ============================================================
# ANALYSIS AREA
# ============================================================

left, right = st.columns(
    [2.05, 1],
    gap="large"
)

# ============================================================
# LEFT - COMMENT ANALYSIS
# ============================================================

with left:

    st.html(
    """
    <div class="panel reveal">

        <div class="panel-title">
            🔍 &nbsp; Analyze a Comment
        </div>

        <div class="panel-subtitle">
            Enter an Instagram comment below and let the AI model
            determine whether it is spam.
        </div>

    </div>
    """,
    unsafe_allow_javascript=True
    )

    comment = st.text_area(
        "Comment",
        placeholder="Type an Instagram comment here...",
        height=145,
        label_visibility="collapsed"
    )

    col_button, col_space = st.columns(
        [1, 3]
    )

    with col_button:

        analyze = st.button(
            "🔍  Analyze Comment",
            use_container_width=True
        )

    # ========================================================
    # PREDICTION
    # ========================================================

    if analyze:

        if not comment.strip():

            st.warning(
                "Please enter a comment first."
            )

        elif model is None:

            st.error(
                "Model could not be loaded. "
                "Check the models folder."
            )

        else:

            try:

                clean_comment = comment.strip()

                comment_vector = vectorizer.transform(
                        [clean_comment]
                    )

                prediction = model.predict(
                        comment_vector
                    )[0]

                probabilities = None

                if hasattr(
                    model,
                    "predict_proba"
                ):

                    probabilities = model.predict_proba(
                            comment_vector
                        )[0]

                # --------------------------------------------
                # DETERMINE LABEL
                # --------------------------------------------

                try:

                    prediction_int = int(
                        prediction
                    )

                except:

                    prediction_int = None

                if isinstance(
                    prediction,
                    str
                ):

                    label = prediction.lower()

                    is_spam = (
                        "spam" in label
                        or
                        label in [
                            "1",
                            "true"
                        ]
                    )

                else:

                    is_spam = (
                        prediction_int == 1
                    )

                # --------------------------------------------
                # PROBABILITY
                # --------------------------------------------

                if probabilities is not None:

                    classes = list(
                        getattr(
                            model,
                            "classes_",
                            []
                        )
                    )

                    spam_probability = 0.0

                    for i, cls in enumerate(
                        classes
                    ):

                        cls_string = str(
                            cls
                        ).lower()

                        if (
                            cls_string == "1"
                            or
                            "spam" in cls_string
                        ):

                            spam_probability = float(
                                    probabilities[i]
                                )

                    # fallback for your model
                    if (
                        spam_probability == 0
                        and
                        len(probabilities) >= 2
                    ):

                        spam_probability = float(
                            probabilities[1]
                        )

                else:

                    spam_probability = (
                        1.0
                        if is_spam
                        else 0.0
                    )

                legitimate_probability = 1.0 - spam_probability

                confidence = (
                    spam_probability
                    if is_spam
                    else legitimate_probability
                )

                confidence_percent = confidence * 100

                spam_percent = spam_probability * 100

                legitimate_percent = legitimate_probability * 100

                # --------------------------------------------
                # SESSION STATISTICS
                # --------------------------------------------

                st.session_state.total_scans += 1

                if is_spam:

                    st.session_state.spam_count += 1

                    result_label = "SPAM"

                else:

                    st.session_state.legitimate_count += 1

                    result_label = "LEGITIMATE"

                # --------------------------------------------
                # HISTORY
                # --------------------------------------------

                scan_time = datetime.now().strftime(
                        "%H:%M:%S"
                    )

                st.session_state.recent_scans.insert(
                    0,
                    {
                        "comment":
                            clean_comment,
                        "result":
                            result_label,
                        "confidence":
                            confidence_percent,
                        "time":
                            scan_time
                    }
                )

                st.session_state.recent_scans = (
                    st.session_state.recent_scans[:8]
                )

                # --------------------------------------------
                # VERDICT
                # --------------------------------------------

                if is_spam:

                    st.html(
                    f"""
                    <div class="verdict spam reveal visible">

                        <div class="verdict-row">

                            <div class="verdict-main">

                                <div class="verdict-icon">
                                    ⚠
                                </div>

                                <div>

                                    <div class="verdict-title">
                                        Spam Detected
                                    </div>

                                    <div class="verdict-description">
                                        This comment shows characteristics
                                        associated with spam.
                                    </div>

                                </div>

                            </div>


                            <div class="confidence">

                                <div class="confidence-label">
                                    CONFIDENCE
                                </div>

                                <div class="confidence-value">
                                    {confidence_percent:.2f}%
                                </div>

                            </div>

                        </div>


                        <div class="probability">

                            <div class="prob-title">
                                Probability Analysis
                            </div>

                            <div class="prob-grid">

                                <div>

                                    <div class="prob-label">

                                        <span>
                                            Spam Probability
                                        </span>

                                        <strong style="color:#ff5068">
                                            {spam_percent:.2f}%
                                        </strong>

                                    </div>

                                    <div class="bar">

                                        <div
                                            class="bar-fill spam-bar"
                                            style="
                                                width:{spam_percent}%;
                                            "
                                        ></div>

                                    </div>

                                </div>


                                <div>

                                    <div class="prob-label">

                                        <span>
                                            Legitimate Probability
                                        </span>

                                        <strong style="color:#00e59a">
                                            {legitimate_percent:.2f}%
                                        </strong>

                                    </div>

                                    <div class="bar">

                                        <div
                                            class="bar-fill safe-bar"
                                            style="
                                                width:{legitimate_percent}%;
                                            "
                                        ></div>

                                    </div>

                                </div>

                            </div>

                        </div>

                    </div>
                    """,
                    unsafe_allow_javascript=True
                    )

                else:

                    st.html(
                    f"""
                    <div class="verdict reveal visible">

                        <div class="verdict-row">

                            <div class="verdict-main">

                                <div class="verdict-icon">
                                    ✓
                                </div>

                                <div>

                                    <div class="verdict-title">
                                        Legitimate Comment
                                    </div>

                                    <div class="verdict-description">
                                        No strong spam classification
                                        was detected.
                                    </div>

                                </div>

                            </div>


                            <div class="confidence">

                                <div class="confidence-label">
                                    CONFIDENCE
                                </div>

                                <div
                                    class="confidence-value"
                                    style="color:#00e59a"
                                >
                                    {confidence_percent:.2f}%
                                </div>

                            </div>

                        </div>


                        <div class="probability">

                            <div class="prob-title">
                                Probability Analysis
                            </div>

                            <div class="prob-grid">

                                <div>

                                    <div class="prob-label">

                                        <span>
                                            Spam Probability
                                        </span>

                                        <strong style="color:#ff5068">
                                            {spam_percent:.2f}%
                                        </strong>

                                    </div>

                                    <div class="bar">

                                        <div
                                            class="bar-fill spam-bar"
                                            style="
                                                width:{spam_percent}%;
                                            "
                                        ></div>

                                    </div>

                                </div>


                                <div>

                                    <div class="prob-label">

                                        <span>
                                            Legitimate Probability
                                        </span>

                                        <strong style="color:#00e59a">
                                            {legitimate_percent:.2f}%
                                        </strong>

                                    </div>

                                    <div class="bar">

                                        <div
                                            class="bar-fill safe-bar"
                                            style="
                                                width:{legitimate_percent}%;
                                            "
                                        ></div>

                                    </div>

                                </div>

                            </div>

                        </div>

                    </div>
                    """,
                    unsafe_allow_javascript=True
                    )

            except Exception as e:

                st.error(
                    f"Prediction error: {e}"
                )


# ============================================================
# RIGHT SIDE
# ============================================================

with right:

    st.html(
    """
    <div class="panel reveal">

        <div class="panel-title">
            ⚡ &nbsp; Quick Examples
        </div>

        <div class="panel-subtitle">
            Try one of these comments.
        </div>

        <div class="example">
            ✓ &nbsp; Congratulations! You won a free iPhone!
        </div>

        <div class="example">
            ✓ &nbsp; Amazing photo! Keep it up!
        </div>

        <div class="example">
            ✓ &nbsp; DM me to get free followers and likes.
        </div>

        <div class="example">
            ✓ &nbsp; This picture looks beautiful!
        </div>

        <div class="example">
            ⚠ &nbsp; Click the link and claim your prize now!
        </div>

    </div>
    """,
    unsafe_allow_javascript=True
    )

    st.write("")

    # MODEL INFO

    st.html(
    """
    <div class="panel reveal">

        <div class="panel-title">
            ⚙ &nbsp; Model Information
        </div>

        <div class="panel-subtitle">
            Machine learning configuration.
        </div>

        <div style="
            margin-top:18px;
            font-size:11px;
            line-height:2;
            color:#999;
        ">

            <div>
                <span style="color:#555">
                    Algorithm
                </span>

                <span style="float:right;color:#ddd">
                    TF-IDF + Logistic Regression
                </span>
            </div>

            <div>
                <span style="color:#555">
                    Task
                </span>

                <span style="float:right;color:#ddd">
                    Binary Classification
                </span>
            </div>

            <div>
                <span style="color:#555">
                    Language
                </span>

                <span style="float:right;color:#ddd">
                    English
                </span>
            </div>

            <div>
                <span style="color:#555">
                    Training Data
                </span>

                <span style="float:right;color:#ddd">
                    YouTube Spam Collection
                </span>
            </div>

            <div>
                <span style="color:#555">
                    Feature Extraction
                </span>

                <span style="float:right;color:#ddd">
                    TF-IDF
                </span>
            </div>

            <div>
                <span style="color:#555">
                    Status
                </span>

                <span style="float:right;color:#00e59a">
                    ● Loaded Successfully
                </span>
            </div>

        </div>

    </div>
    """,
    unsafe_allow_javascript=True
    )


# ============================================================
# RECENT SCANS
# ============================================================

st.write("")

recent_col, workflow_col = st.columns(
    [1.7, 1],
    gap="large"
)

with recent_col:

    rows = ""

    for item in st.session_state.recent_scans:

        safe_comment = html.escape(
            item["comment"]
        )

        if item["result"] == "SPAM":

            badge = (
                '<span class="badge badge-spam">'
                '● SPAM'
                '</span>'
            )

        else:

            badge = (
                '<span class="badge badge-safe">'
                '● LEGITIMATE'
                '</span>'
            )

        rows += f"""
        <tr>

            <td>
                {safe_comment[:65]}
                {"..." if len(safe_comment) > 65 else ""}
            </td>

            <td>
                {badge}
            </td>

            <td>
                {item["confidence"]:.2f}%
            </td>

            <td>
                {item["time"]}
            </td>

        </tr>
        """

    if not rows:

        rows = """
        <tr>

            <td colspan="4"
                style="
                    text-align:center;
                    color:#555;
                    padding:30px;
                ">

                No scans yet.
                Analyze your first comment above.

            </td>

        </tr>
        """

    st.html(
    f"""
    <div class="panel reveal">

        <div class="panel-title">
            ◷ &nbsp; Recent Scans
        </div>

        <div class="panel-subtitle">
            Latest comment classification activity.
        </div>


        <table class="scan-table">

            <thead>

                <tr>

                    <th>
                        COMMENT
                    </th>

                    <th>
                        RESULT
                    </th>

                    <th>
                        CONFIDENCE
                    </th>

                    <th>
                        TIME
                    </th>

                </tr>

            </thead>

            <tbody>

                {rows}

            </tbody>

        </table>

    </div>
    """,
    unsafe_allow_javascript=True
    )


# ============================================================
# WORKFLOW
# ============================================================

with workflow_col:

    st.html(
    """
    <div class="panel reveal">

        <div class="panel-title">
            ◈ &nbsp; How It Works
        </div>

        <div class="panel-subtitle">
            Detection pipeline.
        </div>


        <div class="step">

            <div class="step-number">
                01
            </div>

            <div>

                <div class="step-title">
                    Text Preprocessing
                </div>

                <div class="step-text">
                    Clean URLs, mentions and special characters.
                </div>

            </div>

        </div>


        <div class="step">

            <div class="step-number">
                02
            </div>

            <div>

                <div class="step-title">
                    TF-IDF
                </div>

                <div class="step-text">
                    Convert text into numerical features.
                </div>

            </div>

        </div>


        <div class="step">

            <div class="step-number">
                03
            </div>

            <div>

                <div class="step-title">
                    Machine Learning
                </div>

                <div class="step-text">
                    Logistic Regression classifier.
                </div>

            </div>

        </div>


        <div class="step">

            <div class="step-number">
                04
            </div>

            <div>

                <div class="step-title">
                    Prediction
                </div>

                <div class="step-text">
                    Classify as Spam or Legitimate.
                </div>

            </div>

        </div>

    </div>
    """,
    unsafe_allow_javascript=True
    )


# ============================================================
# FOOTER
# ============================================================

st.html(
"""
<div class="footer reveal">

    <div>
        <strong>🛡 SpamGuard AI</strong>
        &nbsp; / &nbsp;
        Instagram Spam Detection
    </div>

    <div>
        Detect. Prevent. Protect.
        &nbsp; | &nbsp;
        Built with Streamlit
    </div>

    <div>
        v1.0.0
    </div>

</div>
""",
unsafe_allow_javascript=True
)