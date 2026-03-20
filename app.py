"""
DSP Break Time Tracker
Generic / Template Version  ·  Powered by Streamlit
"""

import re
from datetime import date

import pandas as pd
import streamlit as st

from analysis import (
    run_analysis,
    build_script,
    export_excel,
    detect_station,
)

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────

st.set_page_config(
    page_title="DSP Break Time Tracker",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# GLOBAL CSS
# ─────────────────────────────────────────────

st.markdown("""
<style>
/* ── Google Font ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* ── App background ── */
[data-testid="stAppViewContainer"] {
    background: #F0F4F8;
}
[data-testid="stHeader"] {
    background: transparent;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0F2447 0%, #1B3A6B 60%, #1B4F8A 100%);
    border-right: none;
    box-shadow: 3px 0 15px rgba(0,0,0,0.2);
}
[data-testid="stSidebar"] * {
    color: #E8F0FE !important;
}
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p {
    color: #FFFFFF !important;
}
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stDateInput label,
[data-testid="stSidebar"] .stFileUploader label {
    color: #BDD4F5 !important;
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}
[data-testid="stSidebar"] hr {
    border-color: rgba(255,255,255,0.2) !important;
}

/* ── Selectbox & inputs in sidebar ── */
[data-testid="stSidebar"] .stSelectbox > div > div {
    background: rgba(255,255,255,0.12) !important;
    border: 1px solid rgba(255,255,255,0.25) !important;
    color: #FFFFFF !important;
    border-radius: 8px;
}
[data-testid="stSidebar"] .stSelectbox svg {
    fill: #FFFFFF !important;
}

/* ── File uploader in sidebar ── */
[data-testid="stSidebar"] [data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.08) !important;
    border: 1px dashed rgba(255,255,255,0.35) !important;
    border-radius: 10px;
    padding: 8px;
}
[data-testid="stSidebar"] [data-testid="stFileUploader"] button {
    background: rgba(255,255,255,0.15) !important;
    color: #FFFFFF !important;
    border: 1px solid rgba(255,255,255,0.4) !important;
    border-radius: 6px;
}
[data-testid="stSidebar"] [data-testid="stFileUploader"] button:hover {
    background: rgba(255,255,255,0.25) !important;
}

/* ── Date input in sidebar ── */
[data-testid="stSidebar"] .stDateInput input {
    background: rgba(255,255,255,0.12) !important;
    border: 1px solid rgba(255,255,255,0.25) !important;
    color: #FFFFFF !important;
    border-radius: 8px;
}

/* ── Metric cards ── */
.metric-card {
    background: #FFFFFF;
    border-radius: 16px;
    padding: 24px 20px;
    box-shadow: 0 2px 12px rgba(15,36,71,0.08);
    border-top: 4px solid #1B3A6B;
    text-align: center;
    transition: transform 0.15s ease, box-shadow 0.15s ease;
}
.metric-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 6px 20px rgba(15,36,71,0.14);
}
.metric-card .metric-value {
    font-size: 2.4rem;
    font-weight: 700;
    color: #0F2447;
    line-height: 1.1;
}
.metric-card .metric-label {
    font-size: 0.78rem;
    font-weight: 600;
    color: #6B7A99;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    margin-top: 6px;
}
.metric-card.ok    { border-top-color: #22C55E; }
.metric-card.warn  { border-top-color: #F59E0B; }
.metric-card.error { border-top-color: #EF4444; }
.metric-card.ok    .metric-value { color: #16A34A; }
.metric-card.warn  .metric-value { color: #D97706; }
.metric-card.error .metric-value { color: #DC2626; }

/* ── Section headers ── */
.section-header {
    font-size: 1.05rem;
    font-weight: 700;
    color: #0F2447;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    border-left: 4px solid #FF9900;
    padding-left: 12px;
    margin: 24px 0 16px 0;
}

/* ── Page hero banner ── */
.hero-banner {
    background: linear-gradient(135deg, #0F2447 0%, #1B4F8A 50%, #1E6CB5 100%);
    border-radius: 18px;
    padding: 36px 40px;
    color: #FFFFFF;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
}
.hero-banner::before {
    content: "🚚";
    position: absolute;
    right: 40px;
    top: 50%;
    transform: translateY(-50%);
    font-size: 5rem;
    opacity: 0.15;
}
.hero-banner h1 {
    margin: 0;
    font-size: 2rem;
    font-weight: 700;
    color: #FFFFFF !important;
    letter-spacing: -0.01em;
}
.hero-banner p {
    margin: 8px 0 0 0;
    font-size: 1rem;
    color: rgba(255,255,255,0.8) !important;
}
.hero-badge {
    display: inline-block;
    background: #FF9900;
    color: #FFFFFF;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    padding: 4px 12px;
    border-radius: 20px;
    margin-bottom: 12px;
}

/* ── Status badges ── */
.badge-ok    { background: #DCFCE7; color: #15803D; padding: 3px 10px; border-radius: 12px; font-weight: 600; font-size: 0.82rem; }
.badge-warn  { background: #FEF3C7; color: #B45309; padding: 3px 10px; border-radius: 12px; font-weight: 600; font-size: 0.82rem; }
.badge-error { background: #FEE2E2; color: #B91C1C; padding: 3px 10px; border-radius: 12px; font-weight: 600; font-size: 0.82rem; }

/* ── Table styling ── */
[data-testid="stDataFrame"] {
    border-radius: 12px !important;
    overflow: hidden;
    box-shadow: 0 2px 10px rgba(15,36,71,0.07);
}

/* ── Script card ── */
.script-card {
    background: #FFFFFF;
    border-radius: 14px;
    padding: 20px 24px;
    border-left: 5px solid #1B3A6B;
    box-shadow: 0 2px 10px rgba(15,36,71,0.07);
    margin-bottom: 12px;
    font-size: 0.93rem;
    line-height: 1.65;
    color: #1E293B;
}
.script-name {
    font-weight: 700;
    font-size: 0.85rem;
    color: #1B3A6B;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-bottom: 8px;
}
.script-status-over  { border-left-color: #F59E0B; }
.script-status-under { border-left-color: #EF4444; }
.script-status-ok    { border-left-color: #22C55E; }

/* ── Upload area ── */
.upload-prompt {
    background: #FFFFFF;
    border: 2px dashed #CBD5E1;
    border-radius: 16px;
    padding: 48px 32px;
    text-align: center;
    color: #64748B;
}
.upload-prompt h2 {
    color: #1E293B;
    font-size: 1.4rem;
    margin-bottom: 8px;
}
.upload-prompt p {
    color: #64748B;
    font-size: 0.9rem;
}

/* ── Tab styling ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 6px;
    background: transparent;
    border-bottom: 2px solid #E2E8F0;
    padding-bottom: 0;
}
.stTabs [data-baseweb="tab"] {
    background: transparent;
    border-radius: 8px 8px 0 0;
    padding: 10px 20px;
    font-weight: 600;
    font-size: 0.88rem;
    color: #64748B;
    border: none;
}
.stTabs [aria-selected="true"] {
    background: #FFFFFF;
    color: #0F2447 !important;
    border-bottom: 3px solid #FF9900;
}

/* ── Download button ── */
[data-testid="stDownloadButton"] > button {
    background: linear-gradient(135deg, #FF9900, #E68A00);
    color: #FFFFFF;
    border: none;
    border-radius: 10px;
    font-weight: 700;
    font-size: 0.9rem;
    padding: 10px 24px;
    box-shadow: 0 3px 10px rgba(255,153,0,0.35);
    transition: all 0.15s ease;
}
[data-testid="stDownloadButton"] > button:hover {
    background: linear-gradient(135deg, #E68A00, #CC7A00);
    box-shadow: 0 5px 15px rgba(255,153,0,0.45);
    transform: translateY(-1px);
}

/* ── Run button ── */
.stButton > button {
    background: linear-gradient(135deg, #1B3A6B, #1B4F8A);
    color: #FFFFFF;
    border: none;
    border-radius: 10px;
    font-weight: 700;
    font-size: 0.95rem;
    padding: 12px 28px;
    width: 100%;
    box-shadow: 0 3px 10px rgba(27,58,107,0.35);
    transition: all 0.15s ease;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #0F2447, #1B3A6B);
    box-shadow: 0 5px 18px rgba(15,36,71,0.45);
    transform: translateY(-1px);
}

/* ── Progress bar ── */
.progress-bar-outer {
    background: #E2E8F0;
    border-radius: 99px;
    height: 8px;
    width: 100%;
    margin-top: 6px;
}
.progress-bar-inner {
    background: linear-gradient(90deg, #22C55E, #16A34A);
    border-radius: 99px;
    height: 8px;
    transition: width 0.4s ease;
}
.progress-bar-inner.warn {
    background: linear-gradient(90deg, #F59E0B, #D97706);
}
.progress-bar-inner.error {
    background: linear-gradient(90deg, #EF4444, #DC2626);
}

/* ── Info boxes ── */
.info-box {
    background: #EFF6FF;
    border: 1px solid #BFDBFE;
    border-radius: 10px;
    padding: 14px 18px;
    color: #1E40AF;
    font-size: 0.88rem;
}

/* ── Footer ── */
.app-footer {
    margin-top: 40px;
    padding: 16px 0;
    border-top: 1px solid #E2E8F0;
    text-align: center;
    color: #94A3B8;
    font-size: 0.78rem;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────

ALL_STATIONS = [
    "DAB4","DAB5","DAB8","DAE1","DAE3","DAE7","DAE8","DAL9","DAS7","DAS8",
    "DAS9","DAT9","DAU1","DAU2","DAU5","DAU7","DAX3","DAX5","DAX7","DAX8",
    "DAZ2","DAZ4","DBA5","DBA7","DBA8","DBC3","DBK1","DBK4","DBK6","DBL1",
    "DBL8","DBM5","DBO3","DBO6","DBO7","DBO9","DBU1","DBU2","DBU3","DBU7",
    "DBU9","DCB4","DCB8","DCD6","DCG2","DCG4","DCH6","DCH8","DCK1","DCK6",
    "DCL3","DCL4","DCL5","DCL7","DCL9","DCM2","DCM3","DCM5","DCM6","DCN2",
    "DCS3","DCS6","DCW8","DCX2","DCX5","DCX7","DCX8","DCY1","DCY2","DCY9",
    "DDA9","DDC3","DDC4","DDC9","DDE8","DDE9","DDF1","DDF2","DDF4","DDF5",
    "DDM5","DDO6","DDP1","DDP3","DDP5","DDP9","DDT1","DDT3","DDT4","DDT6",
    "DDT9","DDV2","DDV3","DDV4","DDV5","DDW1","DDW7","DDX2","DDX6","DDX7",
    "DEB2","DEW5","DEW8","DFA5","DFB1","DFH1","DFH3","DFH7","DFL3","DFL4",
    "DFL5","DFL7","DFL8","DFM3","DFM4","DFM5","DFO2","DFO3","DFO9","DFT4",
    "DFX3","DFX4","DFX9","DGE4","DGE7","DGE9","DGF1","DGI3","DGR3","DGR6",
    "DGR8","DGS2","DGT2","DGT8","DHI2","DHO3","DHO4","DHO7","DHO8","DHT1",
    "DHT4","DHX1","DHX4","DIA3","DIA4","DIA5","DIA6","DIB5","DIB6","DIB7",
    "DID2","DID3","DII3","DII4","DII5","DIL5","DIL7","DIN4","DIN6","DIN8",
    "DJC5","DJE1","DJE2","DJE3","DJE5","DJE9","DJR1","DJR3","DJR5","DJT6",
    "DJW8","DJX2","DJX3","DJX4","DJZ2","DJZ3","DJZ4","DJZ5","DJZ6","DJZ8",
    "DKC3","DKO1","DKO9","DKS3","DKY4","DKY5","DKY6","DKY8","DKY9","DLB2",
    "DLD1","DLD7","DLF1","DLI3","DLI4","DLI5","DLI6","DLI8","DLI9","DLN2",
    "DLN3","DLN4","DLN8","DLR2","DLT2","DLT3","DLT6","DLT7","DLT8","DLV2",
    "DLV3","DLV4","DLV7","DLX1","DLX2","DLX5","DLX7","DLX8","DLX9","DMC2",
    "DMC3","DMC4","DMD2","DMD4","DMD5","DMD6","DMD8","DMD9","DMF1","DMF3",
    "DMF5","DMF8","DMH4","DMH9","DMI7","DMI9","DML3","DML4","DML6","DML8",
    "DMO3","DMO4","DMO6","DMP1","DMS2","DMS6","DMW2","DNA4","DNA6","DNH2",
    "DNJ2","DNJ4","DNJ7","DNK2","DNK5","DNK7","DNO2","DNO3","DNY2","DOB2",
    "DOB4","DOB7","DOK2","DOK3","DOK4","DOK6","DOM2","DOM3","DOR2","DOR3",
    "DOT4","DPD2","DPD4","DPD6","DPD7","DPD8","DPH7","DPH8","DPH9","DPL2",
    "DPL7","DPP1","DPP7","DPS2","DPS5","DPS6","DPX4","DPX7","DRC1","DRC6",
    "DRI1","DRO2","DRT3","DRT4","DRT7","DRT8","DRT9","DSC3","DSC4","DSD1",
    "DSD4","DSD5","DSD8","DSE1","DSE8","DSF5","DSF7","DSF8","DSJ5","DSJ9",
    "DSK4","DSM4","DSR2","DSR4","DSR6","DSR8","DSW2","DSW3","DSW5","DSX5",
    "DSX8","DSX9","DTB4","DTB9","DTG5","DTN6","DTN7","DTN8","DTP3","DTP7",
    "DTP9","DTU2","DTU3","DTU6","DTU7","DTU8","DTU9","DUR1","DUR3","DUR9",
    "DUT2","DUT4","DUT5","DUT7","DVA2","DVA3","DVA5","DVB4","DVB5","DVB7",
    "DVB8","DVC4","DVV2","DVV5","DVY2","DVY7","DWA2","DWA5","DWA6","DWA7",
    "DWA9","DWD6","DWI4","DWO1","DWO6","DWS4","DXC3","DXC5","DXC8","DXH1",
    "DXH5","DXH6","DXT4","DXT6","DXT8","DXX4","DXX5","DXY4","DYB2","DYB3",
    "DYH1","DYN3","DYN5","DYN7","DYN9","DYO1","DYO2","DYO5","DYR3","DYR7",
    "DYT6","DYV1","DYY3","DYY4","DYY5","DYY6","DYY8","DYY9","DZU1",
    "HAL1","HAT2","HAU1","HAU2","HBA2","HBA3","HBD1","HBF4","HBF5","HBI2",
    "HBN2","HBO1","HBO2","HCE2","HCH4","HCH5","HCI1","HCL2","HCN1","HCO1",
    "HCT2","HDA1","HDA3","HDC1","HDE2","HDS2","HDT3","HDY1","HEU1","HEW2",
    "HEW4","HFA2","HGE2","HGR1","HHO3","HHS4","HIN2","HIN3","HJX1","HJX2",
    "HKX1","HLA2","HLA4","HLO3","HLR1","HLU2","HLV1","HLX1","HMB1","HMC3",
    "HME3","HMI3","HMK4","HMO2","HMS2","HMY1","HNY1","HNY2","HNY3","HNY5",
    "HNY8","HOK2","HOM1","HPB2","HPD1","HPH2","HPH4","HPT1","HPX3","HRC1",
    "HRD2","HRN1","HRN2","HRO1","HRS1","HSA1","HSD2","HSF2","HSF3","HSF5",
    "HSL1","HSM1","HSY1","HTC2","HTP2","HVB2","HVP1","HYC2","HYE1","HYV1",
    "JFK7","LGB5","MKE5",
    "WBM3","WBM4","WBY1","WCH2","WCI1","WCO8","WDE1","WEE1","WET1","WFB1",
    "WFG1","WFL2","WFL3","WFL6","WGE2","WGL1","WGR1","WGR2","WGR3","WGR7",
    "WID1","WID3","WID8","WIL1","WIL3","WIL4","WIL5","WIL6","WIN1","WIN2",
    "WIN5","WIO2","WIO3","WIO4","WIO9","WKN1","WKN3","WKN5","WKS1","WKS3",
    "WKS4","WKY3","WKY5","WLF2","WLN2","WLN3","WLN6","WMD1","WMG1","WMH1",
    "WMI1","WMI2","WML1","WMN2","WMN3","WMN4","WMN7","WMO1","WMO2","WMO3",
    "WMO4","WMS1","WMS2","WMS4","WMT1","WMT2","WMT3","WMT4","WNB2","WNB5",
    "WNC3","WNC4","WNC5","WNC6","WNC8","WNC9","WND1","WND4","WNG1","WNM2",
    "WNM4","WNY1","WNY2","WNY3","WNY4","WOH1","WOH2","WOI5","WOL1","WOM5",
    "WOO1","WOR1","WOR4","WPR1","WPT2","WPY1","WQQ1","WQQ2","WRD9","WRK1",
    "WRT3","WSC2","WSC7","WSD1","WSD2","WSM9","WSP1","WSP9","WSV1","WTH1",
    "WTN1","WTN2","WTN4","WTX1","WTX2","WTX3","WTX4","WTX5","WTX7","WTX8",
    "WTX9","WTY1","WUS5","WUT1","WVC1","WWG1","WWG2","WWG4","WWG5","WWG6",
    "WWI2","WWI3","WWI4","WWI6","WWS1","WWV8","WWV9","WZN1","WZN2","WZN4",
    "WZN6",
    "XJZ4","XNJ7","XVV2","XVV3","XYC1",
]


# ─────────────────────────────────────────────
# PASSWORD GATE
# ─────────────────────────────────────────────

def check_password() -> bool:
    """Show a password gate; return True once authenticated."""
    correct = st.secrets.get("APP_PASSWORD", "dsp2026")

    if st.session_state.get("authenticated"):
        return True

    # Center the login card
    col1, col2, col3 = st.columns([1, 1.6, 1])
    with col2:
        st.markdown("<div style='height:60px'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div style='background:#FFFFFF;border-radius:20px;padding:48px 40px;
                    box-shadow:0 8px 40px rgba(15,36,71,0.15);text-align:center;'>
            <div style='font-size:3.5rem;margin-bottom:4px'>🚚</div>
            <h1 style='color:#0F2447;font-size:1.6rem;font-weight:700;margin:0 0 6px'>
                DSP Break Time Tracker
            </h1>
            <p style='color:#64748B;font-size:0.92rem;margin:0 0 28px'>
                Enter your access code to continue
            </p>
        </div>
        """, unsafe_allow_html=True)

        with st.form("login_form"):
            pwd = st.text_input("Access Code", type="password", placeholder="••••••••",
                                label_visibility="collapsed")
            st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
            submitted = st.form_submit_button("🔓  Sign In", use_container_width=True)

        if submitted:
            if pwd == correct:
                st.session_state["authenticated"] = True
                st.rerun()
            else:
                st.error("Incorrect access code. Please try again.")

    return False


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────

def render_sidebar() -> tuple:
    """Render sidebar controls; return (adp_file, amz_file, station, report_date)."""
    with st.sidebar:
        # Logo / Brand
        st.markdown("""
        <div style='text-align:center;padding:20px 0 24px'>
            <div style='font-size:2.8rem'>🚚</div>
            <div style='font-size:1.1rem;font-weight:700;color:#FFFFFF;letter-spacing:-0.01em'>
                Break Time Tracker
            </div>
            <div style='font-size:0.72rem;color:#BDD4F5;margin-top:2px;letter-spacing:0.06em;
                        text-transform:uppercase'>Amazon DSP Tool</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<hr style='margin:0 0 20px;border-color:rgba(255,255,255,0.15)'>",
                    unsafe_allow_html=True)

        # Station selector
        st.markdown("**📍 Station**")
        auto_station = st.session_state.get("auto_station", "")
        station_options = ["— Select Station —"] + ALL_STATIONS
        default_idx = 0
        if auto_station and auto_station in ALL_STATIONS:
            default_idx = ALL_STATIONS.index(auto_station) + 1

        station = st.selectbox(
            "Station", station_options, index=default_idx,
            label_visibility="collapsed"
        )
        if station == "— Select Station —":
            station = ""

        st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

        # Report date
        st.markdown("**📅 Report Date**")
        report_date = st.date_input("Report Date", value=date.today(),
                                    label_visibility="collapsed")

        st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
        st.markdown("<hr style='margin:0 0 18px;border-color:rgba(255,255,255,0.15)'>",
                    unsafe_allow_html=True)

        # File uploads
        st.markdown("**📂 Upload Files**")
        st.markdown("""
        <div style='font-size:0.75rem;color:#BDD4F5;margin-bottom:12px'>
            Upload both ADP & Amazon exports to begin analysis
        </div>
        """, unsafe_allow_html=True)

        st.markdown("**ADP Timecard Export**")
        adp_file = st.file_uploader(
            "ADP", type=["xlsx", "csv"],
            key="adp_upload", label_visibility="collapsed"
        )

        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
        st.markdown("**Amazon Time Export**")
        amz_file = st.file_uploader(
            "Amazon", type=["xlsx", "csv"],
            key="amz_upload", label_visibility="collapsed"
        )

        # Auto-detect station from filenames
        if adp_file or amz_file:
            adp_name = adp_file.name if adp_file else ""
            amz_name = amz_file.name if amz_file else ""
            detected = detect_station(adp_name, amz_name)
            if detected and detected != st.session_state.get("auto_station"):
                st.session_state["auto_station"] = detected
                st.rerun()

        st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
        st.markdown("<hr style='margin:0 0 18px;border-color:rgba(255,255,255,0.15)'>",
                    unsafe_allow_html=True)

        # Break policy reference
        with st.expander("📋 Break Policy Reference", expanded=False):
            st.markdown("""
            <div style='font-size:0.82rem;color:#E8F0FE;line-height:1.7'>
            <b>Unpaid Break Requirements:</b><br>
            • Under 6 hrs → No break required<br>
            • 6–10 hrs → 30-min unpaid break<br>
            • 10+ hrs → 60-min unpaid break<br><br>
            <b>Discrepancy Thresholds:</b><br>
            • ✅ OK: within ±5 min<br>
            • ⚠️ Over: Amazon &gt; expected<br>
            • 🔴 Under: Amazon &lt; expected
            </div>
            """, unsafe_allow_html=True)

        # Footer
        st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div style='text-align:center;font-size:0.70rem;color:rgba(255,255,255,0.35);
                    padding-bottom:12px'>
            DSP Break Time Tracker v2.0
        </div>
        """, unsafe_allow_html=True)

    return adp_file, amz_file, station, report_date


# ─────────────────────────────────────────────
# METRIC HELPERS
# ─────────────────────────────────────────────

def metric_card(value, label, card_class="", icon=""):
    return f"""
    <div class="metric-card {card_class}">
        <div class="metric-value">{icon} {value}</div>
        <div class="metric-label">{label}</div>
    </div>
    """


def progress_bar(pct: float, cls: str = "") -> str:
    w = min(max(pct, 0), 100)
    return f"""
    <div class="progress-bar-outer">
        <div class="progress-bar-inner {cls}" style="width:{w:.1f}%"></div>
    </div>
    """


# ─────────────────────────────────────────────
# RENDER: METRICS DASHBOARD
# ─────────────────────────────────────────────

def render_metrics(df: pd.DataFrame):
    total   = len(df)
    ok      = len(df[df["status"].str.contains("OK",    na=False)])
    over    = len(df[df["status"].str.contains("Over",  na=False)])
    under   = len(df[df["status"].str.contains("Under", na=False)])
    issues  = over + under
    pct_ok  = (ok / total * 100) if total > 0 else 0

    st.markdown('<div class="section-header">📊 Summary Dashboard</div>', unsafe_allow_html=True)

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        st.markdown(metric_card(total, "Total Associates", "", "👥"), unsafe_allow_html=True)
    with c2:
        st.markdown(metric_card(ok, "No Issues", "ok", "✅"), unsafe_allow_html=True)
    with c3:
        st.markdown(metric_card(over, "Over (Amazon)", "warn", "⚠️"), unsafe_allow_html=True)
    with c4:
        st.markdown(metric_card(under, "Under (Amazon)", "error", "🔴"), unsafe_allow_html=True)
    with c5:
        cls = "ok" if pct_ok >= 80 else ("warn" if pct_ok >= 50 else "error")
        st.markdown(metric_card(f"{pct_ok:.0f}%", "Compliance Rate", cls, "📈"), unsafe_allow_html=True)

    # Visual compliance bar
    if total > 0:
        bar_cls = "ok" if pct_ok >= 80 else ("warn" if pct_ok >= 50 else "error")
        st.markdown(f"""
        <div style='background:#FFFFFF;border-radius:14px;padding:20px 24px;
                    box-shadow:0 2px 10px rgba(15,36,71,0.07);margin:16px 0'>
            <div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:8px'>
                <span style='font-weight:600;color:#1E293B;font-size:0.88rem'>Overall Compliance</span>
                <span style='font-weight:700;color:#0F2447;font-size:0.9rem'>{ok}/{total} associates on target</span>
            </div>
            {progress_bar(pct_ok, bar_cls)}
            <div style='display:flex;justify-content:space-between;margin-top:8px;font-size:0.78rem;color:#94A3B8'>
                <span>0%</span><span>50%</span><span>100%</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if issues > 0:
            st.markdown(f"""
            <div class='info-box'>
                🔍 <strong>{issues} associate{'' if issues == 1 else 's'}</strong> have time discrepancies
                that may require review — {over} over-recorded and {under} under-recorded.
            </div>
            """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# RENDER: TABLE
# ─────────────────────────────────────────────

def render_table(df: pd.DataFrame):
    st.markdown('<div class="section-header">📋 Discrepancy Details</div>', unsafe_allow_html=True)

    # Filter controls
    col_f1, col_f2, col_f3 = st.columns([2, 1, 1])
    with col_f1:
        search = st.text_input("🔍 Search by name", placeholder="Type a name…",
                               label_visibility="visible")
    with col_f2:
        status_filter = st.multiselect("Filter by Status",
                                       ["✅ OK", "⚠️ Over", "🔴 Under"],
                                       default=["✅ OK", "⚠️ Over", "🔴 Under"])
    with col_f3:
        sort_by = st.selectbox("Sort by",
                               ["Discrepancy (abs)", "Employee Name", "ADP Hours"],
                               label_visibility="visible")

    view = df.copy()

    # Apply filters
    if search:
        name_col = "employee_name" if "employee_name" in view.columns else "associate_name"
        view = view[view[name_col].str.contains(search, case=False, na=False)]

    if status_filter:
        view = view[view["status"].isin(status_filter)]

    if sort_by == "Discrepancy (abs)" and "discrepancy_min" in view.columns:
        view = view.assign(_abs=view["discrepancy_min"].abs()).sort_values("_abs", ascending=False).drop(columns=["_abs"])
    elif sort_by == "Employee Name":
        name_col = "employee_name" if "employee_name" in view.columns else "associate_name"
        view = view.sort_values(name_col)
    elif sort_by == "ADP Hours" and "adp_duration_hrs" in view.columns:
        view = view.sort_values("adp_duration_hrs", ascending=False)

    # Select display columns
    display_map = {
        "employee_name":      "Employee",
        "file_number":        "File #",
        "adp_duration_hrs":   "ADP Hrs",
        "amz_duration_hrs":   "Amazon Hrs",
        "required_break_min": "Req. Break (min)",
        "expected_amz_hrs":   "Expected Hrs",
        "discrepancy_hrs":    "Discrepancy (hrs)",
        "discrepancy_min":    "Discrepancy (min)",
        "status":             "Status",
    }
    cols_available = {k: v for k, v in display_map.items() if k in view.columns}
    display_df = view[list(cols_available.keys())].rename(columns=cols_available)

    st.dataframe(
        display_df,
        use_container_width=True,
        height=min(600, 56 + len(display_df) * 36),
        hide_index=True,
        column_config={
            "ADP Hrs":             st.column_config.NumberColumn(format="%.2f"),
            "Amazon Hrs":          st.column_config.NumberColumn(format="%.2f"),
            "Expected Hrs":        st.column_config.NumberColumn(format="%.2f"),
            "Discrepancy (hrs)":   st.column_config.NumberColumn(format="%.2f"),
            "Discrepancy (min)":   st.column_config.NumberColumn(format="%.1f"),
            "Req. Break (min)":    st.column_config.NumberColumn(format="%d"),
        }
    )
    st.caption(f"Showing {len(display_df)} of {len(df)} records")


# ─────────────────────────────────────────────
# RENDER: CALL SCRIPTS
# ─────────────────────────────────────────────

def render_scripts(df: pd.DataFrame):
    st.markdown('<div class="section-header">🎙️ Conversation Scripts</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class='info-box' style='margin-bottom:16px'>
        💡 These scripts are ready-to-use for conversations with associates about their time records.
        Focus on discrepancies first — associates marked ✅ are included for completeness.
    </div>
    """, unsafe_allow_html=True)

    # Sort: issues first
    issues = df[~df["status"].str.contains("OK", na=False)].copy()
    ok_df  = df[df["status"].str.contains("OK",  na=False)].copy()
    ordered = pd.concat([issues, ok_df], ignore_index=True)

    show_ok = st.checkbox("Also show scripts for associates with no issues", value=False)

    name_col = "employee_name" if "employee_name" in ordered.columns else "associate_name"

    for _, row in ordered.iterrows():
        status = str(row.get("status", ""))
        if "OK" in status and not show_ok:
            continue

        name    = row.get(name_col, "Associate")
        script  = build_script(row)
        disc    = row.get("discrepancy_min", 0)

        if "OK" in status:
            card_cls, icon = "script-status-ok",    "✅"
        elif "Over" in status:
            card_cls, icon = "script-status-over",  "⚠️"
        else:
            card_cls, icon = "script-status-under", "🔴"

        disc_txt = f"{abs(disc):.0f} min {'over' if disc > 0 else 'under'}" if abs(disc) > 5 else "on target"

        st.markdown(f"""
        <div class="script-card {card_cls}">
            <div class="script-name">{icon} {name} &nbsp;·&nbsp; {disc_txt}</div>
            {script}
        </div>
        """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# RENDER: EXPORT
# ─────────────────────────────────────────────

def render_export(df: pd.DataFrame, report_date: date, station: str):
    st.markdown('<div class="section-header">💾 Export Report</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        <div style='background:#FFFFFF;border-radius:14px;padding:24px;
                    box-shadow:0 2px 10px rgba(15,36,71,0.07)'>
            <div style='font-weight:700;color:#0F2447;margin-bottom:8px'>📊 Excel Report</div>
            <div style='font-size:0.88rem;color:#64748B;line-height:1.6'>
                Download a fully formatted Excel workbook with:<br>
                • Color-coded discrepancy table<br>
                • Break compliance summary<br>
                • Report metadata sheet
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        xlsx_bytes = export_excel(df, report_date, station or "Unknown")
        fname = f"break_report_{station}_{report_date.strftime('%Y%m%d')}.xlsx"
        st.download_button(
            label="⬇️  Download Excel Report",
            data=xlsx_bytes,
            file_name=fname,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
        )


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

def main():
    if not check_password():
        return

    adp_file, amz_file, station, report_date = render_sidebar()

    # ── Hero banner ──────────────────────────────────────────────────────────
    station_label = station if station else "All Stations"
    st.markdown(f"""
    <div class="hero-banner">
        <div class="hero-badge">Amazon DSP</div>
        <h1>Break Time Tracker</h1>
        <p>Station <strong>{station_label}</strong> · Report Date: {report_date.strftime('%B %d, %Y')}</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Upload prompt when no files yet ─────────────────────────────────────
    if not adp_file or not amz_file:
        st.markdown("""
        <div class='upload-prompt'>
            <h2>📂 Upload Your Files to Begin</h2>
            <p>Use the sidebar to upload both your <strong>ADP Timecard Export</strong>
               and <strong>Amazon Time Export</strong>.<br>
               Then hit <strong>Run Analysis</strong> to see discrepancies instantly.</p>
        </div>

        <div style='display:grid;grid-template-columns:repeat(3,1fr);gap:20px;margin-top:24px'>
            <div style='background:#FFFFFF;border-radius:14px;padding:24px;
                        box-shadow:0 2px 10px rgba(15,36,71,0.07);text-align:center'>
                <div style='font-size:2rem;margin-bottom:8px'>📤</div>
                <div style='font-weight:700;color:#0F2447;font-size:0.95rem'>1. Upload Files</div>
                <div style='font-size:0.82rem;color:#64748B;margin-top:6px'>
                    Upload ADP & Amazon exports from the sidebar
                </div>
            </div>
            <div style='background:#FFFFFF;border-radius:14px;padding:24px;
                        box-shadow:0 2px 10px rgba(15,36,71,0.07);text-align:center'>
                <div style='font-size:2rem;margin-bottom:8px'>⚡</div>
                <div style='font-weight:700;color:#0F2447;font-size:0.95rem'>2. Run Analysis</div>
                <div style='font-size:0.82rem;color:#64748B;margin-top:6px'>
                    Click the button to match employees and calculate discrepancies
                </div>
            </div>
            <div style='background:#FFFFFF;border-radius:14px;padding:24px;
                        box-shadow:0 2px 10px rgba(15,36,71,0.07);text-align:center'>
                <div style='font-size:2rem;margin-bottom:8px'>📊</div>
                <div style='font-weight:700;color:#0F2447;font-size:0.95rem'>3. Review & Export</div>
                <div style='font-size:0.82rem;color:#64748B;margin-top:6px'>
                    Review flagged records, read scripts, download Excel report
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Footer
        st.markdown("""
        <div class='app-footer'>
            DSP Break Time Tracker &nbsp;·&nbsp; Built for Amazon Delivery Service Partners
        </div>
        """, unsafe_allow_html=True)
        return

    # ── Run Analysis button ──────────────────────────────────────────────────
    run_col, _ = st.columns([1, 3])
    with run_col:
        run_clicked = st.button("⚡  Run Analysis")

    if not run_clicked and "results_df" not in st.session_state:
        st.markdown("""
        <div class='info-box' style='margin-top:12px'>
            📁 Both files uploaded! Hit <strong>Run Analysis</strong> to process the data.
        </div>
        """, unsafe_allow_html=True)
        return

    if run_clicked:
        with st.spinner("Analysing records…"):
            try:
                df = run_analysis(adp_file, amz_file)
                st.session_state["results_df"] = df
                st.session_state["result_station"] = station
                st.session_state["result_date"]    = report_date
            except Exception as e:
                st.error(f"❌ Analysis failed: {e}")
                return

    df           = st.session_state.get("results_df")
    use_station  = st.session_state.get("result_station", station)
    use_date     = st.session_state.get("result_date", report_date)

    if df is None or df.empty:
        st.warning("No data returned. Check that your files contain the expected columns.")
        return

    # ── Metrics ──────────────────────────────────────────────────────────────
    render_metrics(df)

    # ── Tabs ─────────────────────────────────────────────────────────────────
    tab1, tab2, tab3 = st.tabs(["📋  Discrepancy Table", "🎙️  Call Scripts", "💾  Export"])

    with tab1:
        render_table(df)

    with tab2:
        render_scripts(df)

    with tab3:
        render_export(df, use_date, use_station)

    # ── Footer ───────────────────────────────────────────────────────────────
    st.markdown("""
    <div class='app-footer'>
        DSP Break Time Tracker &nbsp;·&nbsp; Built for Amazon Delivery Service Partners
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
