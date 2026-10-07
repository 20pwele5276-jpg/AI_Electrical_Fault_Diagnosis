from html import escape

import streamlit as st

from services.fault_detector import predict_fault
from services.llm_service import explain_fault


# ---------------------------------------------------------------------------
# Page configuration
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="AI Electrical Fault Diagnosis",
    page_icon="⚡",
    layout="wide",
)


# ---------------------------------------------------------------------------
# Electric AI theme (CSS)
# ---------------------------------------------------------------------------
THEME_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;600;700&family=Inter:wght@400;500;600&display=swap');

:root {
    --bg-0: #040813;
    --bg-1: #0a1226;
    --panel: rgba(14, 24, 52, 0.72);
    --line: rgba(0, 229, 255, 0.22);
    --cyan: #00e5ff;
    --blue: #2f6bff;
    --violet: #8b5cf6;
    --magenta: #d96bff;
    --text: #e6f1ff;
    --muted: #8da2c7;
    --ok: #3dffb0;
    --glow-cyan: 0 0 18px rgba(0, 229, 255, 0.45);
}

/* ---------- App background ---------- */
.stApp {
    background:
        radial-gradient(900px 500px at 12% -10%, rgba(47, 107, 255, 0.28), transparent 60%),
        radial-gradient(800px 480px at 95% 0%, rgba(139, 92, 246, 0.24), transparent 60%),
        radial-gradient(700px 400px at 50% 110%, rgba(0, 229, 255, 0.14), transparent 60%),
        linear-gradient(180deg, var(--bg-1), var(--bg-0));
    color: var(--text);
    font-family: 'Inter', sans-serif;
}
.stApp::before {
    content: "";
    position: fixed;
    inset: 0;
    pointer-events: none;
    background-image:
        linear-gradient(rgba(0, 229, 255, 0.045) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0, 229, 255, 0.045) 1px, transparent 1px);
    background-size: 44px 44px;
    mask-image: radial-gradient(ellipse at center, #000 30%, transparent 80%);
    -webkit-mask-image: radial-gradient(ellipse at center, #000 30%, transparent 80%);
}

#MainMenu, footer, header[data-testid="stHeader"] { visibility: hidden; height: 0; }

.block-container {
    max-width: 1080px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* ---------- Hero ---------- */
.hero {
    position: relative;
    overflow: hidden;
    padding: 2.2rem 2rem;
    margin-bottom: 1.6rem;
    border-radius: 22px;
    border: 1px solid var(--line);
    background:
        linear-gradient(135deg, rgba(47, 107, 255, 0.18), rgba(139, 92, 246, 0.14)),
        var(--panel);
    box-shadow: 0 0 40px rgba(47, 107, 255, 0.18), inset 0 0 30px rgba(0, 229, 255, 0.05);
    backdrop-filter: blur(10px);
}
.hero::after {
    content: "";
    position: absolute;
    top: 0; left: -40%;
    width: 40%; height: 100%;
    background: linear-gradient(100deg, transparent, rgba(0, 229, 255, 0.16), transparent);
    animation: sweep 5s ease-in-out infinite;
}
@keyframes sweep {
    0%   { left: -40%; }
    60%, 100% { left: 120%; }
}
.hero-row { display: flex; align-items: center; gap: 1.2rem; position: relative; z-index: 1; }
.bolt {
    flex: 0 0 auto;
    width: 64px; height: 64px;
    display: grid; place-items: center;
    font-size: 2rem;
    border-radius: 18px;
    background: radial-gradient(circle at 30% 30%, rgba(0, 229, 255, 0.35), rgba(47, 107, 255, 0.15));
    border: 1px solid var(--cyan);
    box-shadow: var(--glow-cyan), inset 0 0 14px rgba(0, 229, 255, 0.35);
    animation: pulse 2.4s ease-in-out infinite;
}
@keyframes pulse {
    0%, 100% { box-shadow: 0 0 14px rgba(0, 229, 255, 0.35), inset 0 0 12px rgba(0, 229, 255, 0.25); }
    50%      { box-shadow: 0 0 30px rgba(0, 229, 255, 0.75), inset 0 0 18px rgba(0, 229, 255, 0.5); }
}
.hero h1 {
    margin: 0;
    font-family: 'Rajdhani', sans-serif;
    font-weight: 700;
    font-size: clamp(1.8rem, 4.2vw, 2.9rem);
    line-height: 1.05;
    letter-spacing: 0.02em;
    background: linear-gradient(90deg, #ffffff 0%, var(--cyan) 45%, var(--violet) 100%);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
}
.hero p {
    margin: 0.5rem 0 0;
    color: var(--muted);
    max-width: 60ch;
    font-size: 1rem;
}
.chips { display: flex; flex-wrap: wrap; gap: 0.5rem; margin-top: 1rem; }
.chip {
    padding: 0.28rem 0.75rem;
    border-radius: 99px;
    font-size: 0.8rem;
    color: var(--text);
    border: 1px solid var(--line);
    background: rgba(0, 229, 255, 0.07);
}
.chip.ai {
    border-color: rgba(217, 107, 255, 0.5);
    background: rgba(139, 92, 246, 0.14);
}

/* ---------- Panel headings ---------- */
.panel-title {
    font-family: 'Rajdhani', sans-serif;
    font-size: 1.25rem;
    font-weight: 600;
    color: var(--cyan);
    margin: 0 0 0.2rem;
    text-shadow: 0 0 12px rgba(0, 229, 255, 0.5);
}
.panel-sub { color: var(--muted); font-size: 0.88rem; margin-bottom: 0.8rem; }

/* ---------- Panels (bordered containers) ---------- */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: var(--panel);
    border: 1px solid var(--line) !important;
    border-radius: 18px !important;
    box-shadow: 0 0 26px rgba(47, 107, 255, 0.12);
    backdrop-filter: blur(8px);
    transition: border-color 0.25s ease, box-shadow 0.25s ease;
}
div[data-testid="stVerticalBlockBorderWrapper"]:hover {
    border-color: rgba(0, 229, 255, 0.5) !important;
    box-shadow: 0 0 30px rgba(0, 229, 255, 0.18);
}

/* ---------- Inputs ---------- */
label, div[data-testid="stWidgetLabel"] p {
    color: var(--text) !important;
    font-weight: 500;
}
div[data-testid="stNumberInput"] > div > div {
    background: rgba(5, 12, 30, 0.85);
    border: 1px solid rgba(47, 107, 255, 0.45);
    border-radius: 12px;
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
}
div[data-testid="stNumberInput"] > div > div:focus-within {
    border-color: var(--cyan);
    box-shadow: 0 0 0 1px var(--cyan), var(--glow-cyan);
}
div[data-testid="stNumberInput"] input {
    color: var(--text);
    font-family: 'Rajdhani', sans-serif;
    font-size: 1.15rem;
    font-weight: 600;
}
div[data-testid="stNumberInput"] button {
    background: transparent;
    color: var(--cyan);
}
div[data-testid="stNumberInput"] button:hover {
    background: rgba(0, 229, 255, 0.14);
    color: #fff;
}

/* ---------- Primary button ---------- */
div.stButton > button {
    width: 100%;
    padding: 0.85rem 1.2rem;
    border: 1px solid var(--cyan);
    border-radius: 14px;
    color: #031018;
    font-family: 'Rajdhani', sans-serif;
    font-size: 1.2rem;
    font-weight: 700;
    letter-spacing: 0.06em;
    background: linear-gradient(90deg, var(--cyan), var(--blue) 55%, var(--violet));
    background-size: 160% 100%;
    box-shadow: 0 0 22px rgba(0, 229, 255, 0.4);
    transition: transform 0.15s ease, box-shadow 0.25s ease, background-position 0.4s ease;
}
div.stButton > button:hover {
    background-position: 100% 0;
    transform: translateY(-2px);
    box-shadow: 0 0 36px rgba(0, 229, 255, 0.7), 0 0 60px rgba(139, 92, 246, 0.35);
    color: #031018;
    border-color: #fff;
}
div.stButton > button:active { transform: translateY(0) scale(0.99); }
div.stButton > button:focus-visible { outline: 2px solid #fff; outline-offset: 3px; }

/* ---------- Diagnosis result card ---------- */
.result {
    position: relative;
    padding: 1.6rem 1.6rem 1.4rem;
    margin-top: 1.4rem;
    border-radius: 20px;
    border: 1px solid var(--ok);
    background:
        linear-gradient(135deg, rgba(61, 255, 176, 0.10), rgba(0, 229, 255, 0.07)),
        var(--panel);
    box-shadow: 0 0 34px rgba(61, 255, 176, 0.22);
    animation: arrive 0.45s ease-out;
}
@keyframes arrive {
    from { opacity: 0; transform: scale(0.98); filter: brightness(2); }
    to   { opacity: 1; transform: scale(1);    filter: brightness(1); }
}
.result .tag { color: var(--muted); font-size: 0.9rem; }
.result .fault {
    font-family: 'Rajdhani', sans-serif;
    font-size: clamp(1.7rem, 4vw, 2.5rem);
    font-weight: 700;
    color: var(--ok);
    text-shadow: 0 0 18px rgba(61, 255, 176, 0.55);
    margin: 0.1rem 0 1rem;
}
.meter-head {
    display: flex; justify-content: space-between; align-items: baseline;
    color: var(--muted); font-size: 0.9rem; margin-bottom: 0.4rem;
}
.meter-head b {
    font-family: 'Rajdhani', sans-serif;
    font-size: 1.6rem;
    color: var(--cyan);
    text-shadow: 0 0 12px rgba(0, 229, 255, 0.6);
}
.meter {
    height: 12px;
    border-radius: 99px;
    background: rgba(255, 255, 255, 0.07);
    overflow: hidden;
}
.meter span {
    display: block; height: 100%;
    border-radius: 99px;
    background: linear-gradient(90deg, var(--blue), var(--cyan), var(--ok));
    box-shadow: 0 0 14px rgba(0, 229, 255, 0.8);
    animation: fill 0.9s ease-out;
}
@keyframes fill { from { width: 0; } }

/* ---------- AI explanation (the signature element) ---------- */
.ai-head {
    display: flex; align-items: center; gap: 0.9rem;
    margin: 1.6rem 0 0.8rem;
}
.ai-core {
    position: relative;
    flex: 0 0 auto;
    width: 46px; height: 46px;
    border-radius: 50%;
    display: grid; place-items: center;
    font-size: 1.3rem;
    background: radial-gradient(circle at 35% 30%, rgba(217, 107, 255, 0.55), rgba(47, 107, 255, 0.25));
    border: 1px solid var(--magenta);
    box-shadow: 0 0 20px rgba(217, 107, 255, 0.55);
}
.ai-core::before, .ai-core::after {
    content: "";
    position: absolute; inset: -7px;
    border-radius: 50%;
    border: 1px solid rgba(0, 229, 255, 0.45);
    animation: ring 2.6s ease-out infinite;
}
.ai-core::after { animation-delay: 1.3s; }
@keyframes ring {
    from { transform: scale(0.85); opacity: 0.9; }
    to   { transform: scale(1.5);  opacity: 0; }
}
.ai-head h3 {
    margin: 0;
    font-family: 'Rajdhani', sans-serif;
    font-size: 1.5rem;
    font-weight: 700;
    background: linear-gradient(90deg, var(--cyan), var(--magenta));
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
}
.ai-head small { display: block; color: var(--muted); font-size: 0.82rem; }

/* container holding the explanation text */
div[data-testid="stVerticalBlockBorderWrapper"]:has(.ai-marker) {
    border-color: rgba(217, 107, 255, 0.45) !important;
    background:
        linear-gradient(135deg, rgba(139, 92, 246, 0.14), rgba(0, 229, 255, 0.05)),
        var(--panel);
    box-shadow: 0 0 34px rgba(139, 92, 246, 0.25);
    position: relative;
}
div[data-testid="stVerticalBlockBorderWrapper"]:has(.ai-marker):hover {
    border-color: rgba(217, 107, 255, 0.8) !important;
    box-shadow: 0 0 40px rgba(217, 107, 255, 0.35);
}
div[data-testid="stVerticalBlockBorderWrapper"]:has(.ai-marker) p,
div[data-testid="stVerticalBlockBorderWrapper"]:has(.ai-marker) li {
    color: #dbe6ff;
    line-height: 1.7;
    font-size: 1rem;
}
div[data-testid="stVerticalBlockBorderWrapper"]:has(.ai-marker) strong { color: var(--cyan); }
div[data-testid="stVerticalBlockBorderWrapper"]:has(.ai-marker) h1,
div[data-testid="stVerticalBlockBorderWrapper"]:has(.ai-marker) h2,
div[data-testid="stVerticalBlockBorderWrapper"]:has(.ai-marker) h3,
div[data-testid="stVerticalBlockBorderWrapper"]:has(.ai-marker) h4 {
    font-family: 'Rajdhani', sans-serif;
    color: var(--magenta);
}
div[data-testid="stVerticalBlockBorderWrapper"]:has(.ai-marker) code {
    color: var(--cyan);
    background: rgba(0, 229, 255, 0.1);
}

/* spinner */
div[data-testid="stSpinner"] { color: var(--cyan); }
div[data-testid="stSpinner"] i, div[data-testid="stSpinner"] svg { border-top-color: var(--cyan) !important; }

/* ---------- Notices ---------- */
.notice {
    margin-top: 1.1rem;
    padding: 0.85rem 1rem;
    border-radius: 12px;
    border-left: 3px solid var(--violet);
    background: rgba(139, 92, 246, 0.1);
    color: #c9c4ee;
    font-size: 0.9rem;
}
.error-box {
    margin-top: 1.4rem;
    padding: 1rem 1.2rem;
    border-radius: 14px;
    border: 1px solid #ff4d6d;
    background: rgba(255, 77, 109, 0.1);
    color: #ffc2cd;
    box-shadow: 0 0 22px rgba(255, 77, 109, 0.25);
}

/* ---------- Footer ---------- */
.foot { text-align: center; color: var(--muted); font-size: 0.8rem; margin-top: 2rem; }

/* ---------- Accessibility & mobile ---------- */
@media (max-width: 640px) {
    .hero { padding: 1.4rem 1.1rem; }
    .bolt { width: 52px; height: 52px; font-size: 1.6rem; }
}
@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after { animation: none !important; transition: none !important; }
}
</style>
"""

st.markdown(THEME_CSS, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.markdown(
    """
    <div class="hero">
        <div class="hero-row">
            <div class="bolt">⚡</div>
            <div>
                <h1>AI Electrical Fault Diagnosis</h1>
                <p>
                    Enter electrical measurements to identify a possible fault
                    using machine learning and AI.
                </p>
            </div>
        </div>
        <div class="chips">
            <span class="chip">Machine learning detection</span>
            <span class="chip ai">AI explanation</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------------------
# Inputs
# ---------------------------------------------------------------------------
col1, col2 = st.columns(2, gap="large")

with col1:
    with st.container(border=True):
        st.markdown(
            '<div class="panel-title">⚡ Supply Readings</div>'
            '<div class="panel-sub">Voltage, current and frequency</div>',
            unsafe_allow_html=True,
        )

        voltage = st.number_input(
            "Voltage (V)",
            min_value=0.0,
            max_value=500.0,
            value=230.0,
            step=1.0,
        )

        current = st.number_input(
            "Current (A)",
            min_value=0.0,
            max_value=50.0,
            value=5.0,
            step=0.1,
        )

        frequency = st.number_input(
            "Frequency (Hz)",
            min_value=0.0,
            max_value=100.0,
            value=50.0,
            step=0.1,
        )

with col2:
    with st.container(border=True):
        st.markdown(
            '<div class="panel-title">🌡️ Load &amp; Environment</div>'
            '<div class="panel-sub">Power factor and temperature</div>',
            unsafe_allow_html=True,
        )

        power_factor = st.number_input(
            "Power Factor",
            min_value=0.0,
            max_value=1.0,
            value=0.95,
            step=0.01,
        )

        temperature = st.number_input(
            "Temperature (°C)",
            min_value=-50.0,
            max_value=150.0,
            value=35.0,
            step=1.0,
        )


st.write("")


# ---------------------------------------------------------------------------
# Diagnosis
# ---------------------------------------------------------------------------
if st.button(
    "🔍 Diagnose Electrical Fault",
    use_container_width=True,
):

    try:
        fault, confidence = predict_fault(
            voltage,
            current,
            frequency,
            power_factor,
            temperature,
        )

        st.markdown(
            f"""
            <div class="result">
                <div class="tag">Diagnosis Result</div>
                <div class="fault">Detected Fault: {escape(str(fault))}</div>
                <div class="meter-head">
                    <span>Model Confidence</span>
                    <b>{confidence:.2%}</b>
                </div>
                <div class="meter">
                    <span style="width: {max(0.0, min(float(confidence), 1.0)) * 100:.1f}%"></span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="ai-head">
                <div class="ai-core">🤖</div>
                <div>
                    <h3>AI Explanation</h3>
                    <small>Plain-language analysis of the detected fault</small>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        with st.container(border=True):
            st.markdown('<span class="ai-marker"></span>', unsafe_allow_html=True)

            with st.spinner("Generating explanation..."):
                explanation = explain_fault(
                    fault,
                    voltage,
                    current,
                    frequency,
                    power_factor,
                    temperature,
                )

            st.write(explanation)

        st.markdown(
            """
            <div class="notice">
                This system provides decision support only.
                The result should be verified by a qualified electrical professional.
            </div>
            """,
            unsafe_allow_html=True,
        )

    except Exception as error:
        st.markdown(
            f'<div class="error-box">Error: {escape(str(error))}</div>',
            unsafe_allow_html=True,
        )


st.markdown(
    '<div class="foot">⚡ AI Electrical Fault Diagnosis · Decision-support tool</div>',
    unsafe_allow_html=True,
)
