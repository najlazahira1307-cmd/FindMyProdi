from unittest import result

from pyparsing import col
import streamlit as st
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import streamlit.components.v1 as components
from engine import search_prodi
from data_details import DETAIL_PRODI
from data_keywords import KEYWORD_DATA

# PAGE CONFIG
st.set_page_config(
    page_title="FindMyProdi",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# GLOBAL CSS
st.markdown("""
<link rel="stylesheet"
href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">
""", unsafe_allow_html=True)

st.markdown("""
<style>
@import url('https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css');
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&family=DM+Sans:wght@300;400;500;600&family=Space+Mono:wght@400;700&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    background: #f9ebed !important;
    color: #4f171d !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}
[data-testid="stAppViewContainer"] > .main { background: #f9ebed !important; }
[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stSidebar"] { display: none !important; }
.block-container { padding: 2rem 3rem 1rem !important; max-width: 100% !important; }
[data-testid="stVerticalBlock"] > div { gap: 0 !important; }

::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: #f9ebed; }
::-webkit-scrollbar-thumb { background: #9e2e3b; border-radius: 2px; }
            
// emoticon
.bi {
    font-size: 1em;
    vertical-align: middle;
}

/* Input */
.stTextInput > div > div > input {
    background: rgba(79,23,29,0.1) !important;
    border: 1.5px solid rgba(158,46,59,0.35) !important;
    border-radius: 10px !important;
    color: #4f171d !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 1rem !important;
    padding: 12px 18px !important;
    caret-color: #9e2e3b !important;
}
.stTextInput > div > div > input:focus {
    border-color: #9e2e3b !important;
    box-shadow: 0 0 0 3px rgba(158,46,59,0.15) !important;
    outline: none !important;
}
.stTextInput > div > div > input::placeholder { color: rgba(79,23,29,0.4) !important; }
div[data-testid="stTextInput"] label {
    color: #c6394a !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #c6394a, #77222c) !important;
    color: #f9ebed !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.88rem !important;
    padding: 10px 24px !important;
    letter-spacing: 0.04em !important;
    transition: all 0.2s ease !important;
    width: 100% !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #c6394a, #77222c) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(158,46,59,0.3) !important;
}

/* Metric */
[data-testid="stMetric"] {
    background: rgba(244,215,219,0.6) !important;
    border: 1px solid rgba(158,46,59,0.3) !important;
    border-radius: 10px !important;
    padding: 12px !important;
}
[data-testid="stMetricLabel"] { color: #c6394a !important; font-size: 0.75rem !important; }
[data-testid="stMetricValue"] { color: #77222c !important; font-family: 'Space Mono', monospace !important; font-size: 1.1rem !important; }

/* Hide default streamlit elements */
#MainMenu, footer, header { visibility: hidden; }
            
/* Pills / chip buttons */
[data-testid="stPills"] [role="button"],
[data-testid="stPills"] span[data-testid],
button[kind="pillsButton"],
[data-baseweb="button-group"] button {
    background: transparent !important;
    border: 1.5px solid rgba(158,46,59,0.4) !important;
    color: #c6394a !important;
    border-radius: 100px !important;
}
[data-testid="stPills"] [role="button"]:hover,
[data-baseweb="button-group"] button:hover {
    background: rgba(158,46,59,0.1) !important;
    border-color: #c6394a !important;
}

</style>
""", unsafe_allow_html=True)

# SESSION STATE
if "page" not in st.session_state:       st.session_state.page = 0
if "search_result" not in st.session_state: st.session_state.search_result = None
if "selected_prodi" not in st.session_state: st.session_state.selected_prodi = None
if "keyword_input" not in st.session_state: st.session_state.keyword_input = ""
if "selected_system" not in st.session_state: st.session_state.selected_system = None

def go_to(p):
    st.session_state.page = p
    st.rerun()

# PROGRESS BAR 
def render_progress():
    p = st.session_state.page
    labels = ["Intro","Input","Hasil","Detail","BST","Algoritma","Penutup","Sistem"]
    pct = p / (len(labels)-1) * 100
    dots = ""
    for i, lbl in enumerate(labels):
        cls = "dot-active" if i==p else ("dot-done" if i<p else "dot-idle")
        dots += f'<div class="{cls}" title="{lbl}"></div>'
    st.markdown(f"""
    <style>
    .pb-wrap{{position:fixed;top:0;left:0;right:0;z-index:9999;
        padding:8px 28px 6px;
        background:rgba(249,235,237,0.97);
        border-bottom:1px solid rgba(158,46,59,0.1);
        display:flex;align-items:center;gap:14px;}}
    .pb-logo{{font-family:'Space Mono',monospace;font-size:0.62rem;
        color:rgba(79,23,29,0.7);letter-spacing:0.15em;white-space:nowrap;}}
    .pb-track{{flex:1;height:2px;background:rgba(79,23,29,0.1);border-radius:2px;overflow:hidden;}}
    .pb-fill{{height:100%;background:linear-gradient(90deg,#9e2e3b,#dd8892);
        border-radius:2px;width:{pct:.0f}%;transition:width 0.4s ease;}}
    .dots-row{{display:flex;gap:5px;align-items:center;}}
    .dot-idle{{width:5px;height:5px;border-radius:50%;background:rgba(79,23,29,0.18);}}
    .dot-done{{width:5px;height:5px;border-radius:50%;background:rgba(158,46,59,0.4);}}
    .dot-active{{width:16px;height:5px;border-radius:3px;background:#9e2e3b;}}
    </style>
    <div class="pb-wrap">
        <span class="pb-logo">FINDMYPRODI</span>
        <div class="pb-track"><div class="pb-fill"></div></div>
        <div class="dots-row">{dots}</div>
    </div>
    <div style="height:36px"></div>
    """, unsafe_allow_html=True)

# NAV BUTTONS
def nav_buttons(back_page=None, next_page=None, next_label="Lanjut →", back_label="← Kembali"):
    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1,4,1])
    if back_page is not None:
        with c1:
            if st.button(back_label, key=f"bk_{st.session_state.page}"):
                go_to(back_page)
    if next_page is not None:
        with c3:
            if st.button(next_label, key=f"nx_{st.session_state.page}"):
                go_to(next_page)

# PAGE 0 — SPLASH
def page_logo():
    st.markdown("""
    <style>
    @keyframes fadeUp{from{opacity:0;transform:translateY(24px)}to{opacity:1;transform:translateY(0)}}
    .sp-wrap{
        display:flex;flex-direction:column;align-items:center;justify-content:center;
        padding:40px 20px 0px;
        background:radial-gradient(ellipse at 35% 25%,rgba(158,46,59,0.1) 0%,transparent 55%),#f9ebed;
        position:relative;overflow:hidden;text-align:center;
    }
    .sp-grid{position:absolute;inset:0;
        background-image:linear-gradient(rgba(158,46,59,0.04) 1px,transparent 1px),
        linear-gradient(90deg,rgba(158,46,59,0.04) 1px,transparent 1px);
        background-size:55px 55px;pointer-events:none;}
    .sp-icon{
        width:90px;height:90px;
        background:linear-gradient(135deg,#e8b0b6,#f4d7db);
        border:1px solid rgba(158,46,59,0.4);border-radius:22px;
        display:flex;align-items:center;justify-content:center;font-size:2.4rem;
        margin-bottom:16px;
        box-shadow:0 0 32px rgba(158,46,59,0.18),inset 0 1px 0 rgba(79,23,29,0.08);
        animation:fadeUp 0.7s ease both;position:relative;z-index:1;
    }
    .sp-title{
        font-family:'Plus Jakarta Sans',sans-serif;
        font-size:clamp(3rem,8vw,5rem);font-weight:900;letter-spacing:-0.02em;line-height:1;
        animation:fadeUp 0.7s 0.15s ease both;position:relative;z-index:1;
    }
    .sp-find{color:#4f171d}.sp-my{color:rgba(79,23,29,0.4);font-style:italic;font-weight:400}
    .sp-prodi{color:#9e2e3b}
    .sp-tag{
        font-family:'Space Mono',monospace;font-size:0.7rem;letter-spacing:0.18em;
        color:rgba(209,97,110,0.25);text-transform:uppercase;margin-top:10px;
        animation:fadeUp 0.7s 0.3s ease both;position:relative;z-index:1;
    }
    .sp-desc{
        max-width:480px;color:rgba(79,23,29,0.6);font-size:0.92rem;line-height:1.7;
        margin:12px auto 0;
        animation:fadeUp 0.7s 0.4s ease both;position:relative;z-index:1;
    }
    .sp-chips{
        display:flex;gap:8px;flex-wrap:wrap;justify-content:center;
        margin-top:16px;
        animation:fadeUp 0.7s 0.5s ease both;position:relative;z-index:1;
    }
    .sp-chip{
        background:rgba(158,46,59,0.08);border:1px solid rgba(158,46,59,0.2);
        border-radius:100px;padding:5px 14px;font-size:0.78rem;color:#9e2e3b;
    }
    .sp-line{width:50px;height:2px;background:linear-gradient(90deg,#9e2e3b,transparent);
        margin:16px auto 0;animation:fadeUp 0.7s 0.55s ease both;position:relative;z-index:1;}
    .sp-owner {
        font-family: 'Space Mono', monospace;
        font-size: 0.65rem;
        color: rgba(79,23,29,0.4);
        letter-spacing: 0.12em;
        margin-top: 10px;
        animation: fadeUp 0.7s 0.6s ease both;
        position: relative;
        z-index: 1;
    }
    </style>
    <div class="sp-wrap">
        <div class="sp-grid"></div>
        <div class="sp-icon"><i class="bi bi-mortarboard-fill"></i></div>
        <div class="sp-title">
            <span class="sp-find">Find</span><span class="sp-my">My</span>
            <span class="sp-prodi">Prodi</span>
        </div>
        <div class="sp-tag">Temukan Jurusan Terbaikmu</div>
        <div class="sp-desc">
            Sistem cerdas berbasis <strong style="color:#9e2e3b">Binary Search Tree</strong>
            dan <strong style="color:#c6394a">Regex Engine</strong> untuk menemukan
            program studi yang sesuai dengan minatmu.
        </div>
        <div class="sp-chips">
            <span class="sp-chip"><i class="bi bi-diagram-3-fill"></i> BST</span>
            <span class="sp-chip"><i class="bi bi-lightning-charge-fill"></i> Binary Search</span>
            <span class="sp-chip"><i class="bi bi-search"></i> Regex</span>
        </div>
        <div class="sp-owner">Najla(041) &nbsp;·&nbsp; Alin(068) &nbsp;·&nbsp; Moza(185)</div>
        <div class="sp-line"></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
    st.markdown("""
    <style>
    div[data-testid="column"]:nth-of-type(2) {
        display: flex;
        justify-content: center;
        align-items: center;
    }
    div[data-testid="column"]:nth-of-type(2) .stButton {
        width: auto !important;
    }
    div[data-testid="column"]:nth-of-type(2) .stButton > button {
        width: auto !important;
        padding: 14px 48px !important;
        font-size: 1rem !important;
        border-radius: 12px !important;
    }
    </style>
    """, unsafe_allow_html=True)
    _, col, _ = st.columns([1.66, 1, 1])
    with col:
        if st.button("Mulai →", key="start_btn"):
          go_to(1)

# PAGE 1 — INPUT
def page_input():
    st.markdown("""
    <style>
    @keyframes fadeUp{from{opacity:0;transform:translateY(18px)}to{opacity:1;transform:translateY(0)}}
    .inp-header{text-align:center;margin-bottom:20px;animation:fadeUp 0.5s ease both;}
    .inp-eyebrow{font-family:'Space Mono',monospace;font-size:0.68rem;letter-spacing:0.18em;
        color:#9e2e3b;text-transform:uppercase;margin-bottom:10px;}
    .inp-h1{font-family:'Plus Jakarta Sans',sans-serif;font-size:clamp(1.8rem,4vw,2.8rem);
        font-weight:700;color:#4f171d;line-height:1.2;}
    .inp-h1 em{color:#9e2e3b;font-style:normal;}
    .inp-sub{color:rgba(79,23,29,0.55);font-size:0.88rem;margin-top:8px;line-height:1.5;}
    .feat-label {font-family: 'Space Mono', monospace;font-size: 0.65rem;color: rgba(158,46,59,0.6);letter-spacing: 0.12em;
    text-transform: uppercase;margin-bottom: 8px;margin-top: 16px;}
    .ex-label{font-family:'Space Mono',monospace;font-size:0.65rem;color:rgba(158,46,59,0.6);
        letter-spacing:0.12em;text-transform:uppercase;margin-bottom:8px;}
    .ex-row{display:flex;gap:7px;flex-wrap:wrap;margin-bottom:16px;}
    .ex-tag{background:rgba(158,46,59,0.07);border:1px solid rgba(158,46,59,0.18);
        border-radius:7px;padding:5px 13px;font-size:0.78rem;color:rgba(209,97,110,0.25);}
    .feat-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-top:16px;}
    .feat-card{background:rgba(79,23,29,0.06);border:1px solid rgba(158,46,59,0.1);
        border-radius:12px;padding:14px;text-align:center;}
    .feat-icon{font-size:1.3rem;margin-bottom:6px;}
    .feat-t{font-size:0.78rem;font-weight:600;color:#c6394a;margin-bottom:3px;}
    .feat-d{font-size:0.7rem;color:rgba(79,23,29,0.45);line-height:1.4;}
    </style>
    <div class="inp-header">
        <div class="inp-eyebrow">● Step 01 — Eksplorasi Minat</div>
        <div class="inp-h1">Apa yang <em>kamu</em> minati?</div>
        <div class="inp-sub">Ketikkan kata kunci yang mencerminkan passion atau bidang yang ingin kamu pelajari.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="ex-label">Contoh kata kunci</div>', unsafe_allow_html=True)

    kw_selected = st.pills(
        label="pilih kata kunci",
        options=["ai", "data", "coding", "marketing", "robotik", "keuangan", "bisnis", "game", "website", "machine learning"],
        label_visibility="collapsed",
        key="chip_pills"
    )
    if kw_selected:
        with st.spinner("Mencari..."):
            result = search_prodi(kw_selected)
        st.session_state.search_result = result
        st.session_state.keyword_input = kw_selected
        go_to(2)

    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        keyword = st.text_input(
            "KATA KUNCI MINAT",
            value=st.session_state.keyword_input,
            placeholder="Ketik minatmu di sini...",
            key="kw_field"
        )
        if st.button("⌕ Cari Prodi", key="search_btn"):
            if keyword.strip():
                with st.spinner("Mencari..."):
                    result = search_prodi(keyword.strip())
                st.session_state.search_result = result
                st.session_state.keyword_input = keyword.strip()
                go_to(2)
            else:
                st.warning("Masukkan kata kunci terlebih dahulu.")

    st.markdown("""
    <style>
    .feat-label {
        font-family: 'Space Mono', monospace;
        font-size: 0.65rem;
        color: rgba(158,46,59,0.6);
        letter-spacing: 0.12em;
        text-transform: uppercase;
        margin-bottom: 8px;
        margin-top: 16px;
    }
    </style>
    <div class="feat-label">Detail Struktur Data dan Algoritma</div>
    """, unsafe_allow_html=True)

    fc1, fc2, fc3 = st.columns(3)
    with fc1:
        st.markdown("""
        <div class="feat-card">
            <div class="feat-icon"><i class="bi bi-diagram-3-fill"></i></div>
            <div class="feat-t">BST Indexing</div>
            <div class="feat-d">Data diindeks dengan Binary Search Tree</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Pelajari →", key="feat_bst"):
            st.session_state.selected_system = "bst"
            go_to(7)

    with fc2:
        st.markdown("""
        <div class="feat-card">
            <div class="feat-icon"><i class="bi bi-lightning-charge-fill"></i></div>
            <div class="feat-t">Binary Search</div>
            <div class="feat-d">Exact match O(log n) pada data terurut</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Pelajari →", key="feat_binary"):
            st.session_state.selected_system = "binary"
            go_to(7)

    with fc3:
        st.markdown("""
        <div class="feat-card">
            <div class="feat-icon"><i class="bi bi-search"></i></div>
            <div class="feat-t">Regex Matching</div>
            <div class="feat-d">Pencarian pola fleksibel & partial match</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Pelajari →", key="feat_regex"):
            st.session_state.selected_system = "regex"
            go_to(7)

    nav_buttons(back_page=0)

# PAGE 2 — HASIL PENCARIAN
def page_hasil():
    result = st.session_state.search_result
    if not result:
        st.warning("Belum ada hasil. Kembali ke halaman input.")
        if st.button("← Kembali"): go_to(1)
        return

    keyword    = result["keyword"]
    prodi_list = result["results"]

    binary_names = set(result["binary_results"])
    regex_names  = set(result["regex_results"])

    def get_source(prodi_name):
        if prodi_name in binary_names:
            return "binary"
        return "regex"

    st.markdown(f"""
    <style>
    @keyframes fadeUp{{from{{opacity:0;transform:translateY(16px)}}to{{opacity:1;transform:translateY(0)}}}}
    .hs-header{{text-align:center;margin-bottom:16px;animation:fadeUp 0.5s ease both;}}
    .hs-eyebrow{{font-family:'Space Mono',monospace;font-size:0.68rem;letter-spacing:0.18em;
        color:#9e2e3b;text-transform:uppercase;margin-bottom:8px;}}
    .hs-h1{{font-family:'Plus Jakarta Sans',sans-serif;font-size:clamp(1.6rem,3.5vw,2.4rem);
        font-weight:700;color:#4f171d;}}
    .hs-kw{{display:inline-block;background:rgba(158,46,59,0.1);
        border:1px solid rgba(158,46,59,0.3);border-radius:6px;
        padding:3px 12px;font-family:'Space Mono',monospace;font-size:0.85rem;
        color:#9e2e3b;margin:6px 0 14px;}}

    /* ── Stats pills — tiap algoritma warna berbeda ── */
    .stats-row{{display:flex;gap:10px;justify-content:center;flex-wrap:wrap;margin-bottom:18px;}}

    .stat-pill-binary{{
        background:rgba(119,34,44,0.12);
        border:1.5px solid rgba(119,34,44,0.45);
        border-radius:100px;padding:7px 18px;font-size:0.78rem;
        color:#77222c;font-family:'Plus Jakarta Sans',sans-serif;
        display:flex;align-items:center;gap:6px;
    }}
    .stat-pill-binary strong{{color:#77222c;font-family:'Space Mono',monospace;}}

    .stat-pill-regex{{
        background:rgba(180,90,20,0.10);
        border:1.5px solid rgba(180,90,20,0.40);
        border-radius:100px;padding:7px 18px;font-size:0.78rem;
        color:#a05010;font-family:'Plus Jakarta Sans',sans-serif;
        display:flex;align-items:center;gap:6px;
    }}
    .stat-pill-regex strong{{color:#a05010;font-family:'Space Mono',monospace;}}

    .stat-pill-total{{
        background:rgba(40,100,70,0.10);
        border:1.5px solid rgba(40,100,70,0.35);
        border-radius:100px;padding:7px 18px;font-size:0.78rem;
        color:#285040;font-family:'Plus Jakarta Sans',sans-serif;
        display:flex;align-items:center;gap:6px;
    }}
    .stat-pill-total strong{{color:#285040;font-family:'Space Mono',monospace;}}

    /* ── Prodi cards ── */
    .prodi-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-bottom:8px;}}

    .pd-card-binary{{
        background:linear-gradient(135deg,rgba(119,34,44,0.10),rgba(249,235,237,0.85));
        border:1.5px solid rgba(119,34,44,0.35);border-radius:14px;
        padding:18px 16px;height:170px;
        display:flex;flex-direction:column;justify-content:space-between;
        position:relative;overflow:hidden;
    }}
    .pd-card-binary::before{{
        content:'';position:absolute;top:0;left:0;right:0;height:3px;
        background:linear-gradient(90deg,#77222c,#c6394a);
    }}

    .pd-card-regex{{
        background:linear-gradient(135deg,rgba(180,90,20,0.09),rgba(249,235,237,0.85));
        border:1.5px solid rgba(180,90,20,0.32);border-radius:14px;
        padding:18px 16px;height:170px;
        display:flex;flex-direction:column;justify-content:space-between;
        position:relative;overflow:hidden;
    }}
    .pd-card-regex::before{{
        content:'';position:absolute;top:0;left:0;right:0;height:3px;
        background:linear-gradient(90deg,#a05010,#d4781e);
    }}

    .pd-name{{font-family:'Plus Jakarta Sans',sans-serif;font-size:0.95rem;
        font-weight:600;color:#4f171d;line-height:1.3;}}
    .pd-skills{{display:flex;flex-wrap:wrap;gap:4px;margin-top:8px;}}
    .pd-sk-binary{{background:rgba(119,34,44,0.08);border:1px solid rgba(119,34,44,0.18);
        border-radius:5px;padding:2px 8px;font-size:0.67rem;color:#77222c;}}
    .pd-sk-regex{{background:rgba(180,90,20,0.08);border:1px solid rgba(180,90,20,0.20);
        border-radius:5px;padding:2px 8px;font-size:0.67rem;color:#a05010;}}

    .pd-badge-binary{{
        display:inline-flex;align-items:center;gap:4px;
        background:rgba(119,34,44,0.10);border:1px solid rgba(119,34,44,0.28);
        border-radius:5px;padding:2px 8px;font-size:0.62rem;
        color:#77222c;font-family:'Space Mono',monospace;margin-top:8px;
    }}
    .pd-badge-regex{{
        display:inline-flex;align-items:center;gap:4px;
        background:rgba(180,90,20,0.10);border:1px solid rgba(180,90,20,0.28);
        border-radius:5px;padding:2px 8px;font-size:0.62rem;
        color:#a05010;font-family:'Space Mono',monospace;margin-top:8px;
    }}

    /* tombol detail ikut warna source */
    .pd-card-binary + div > button {{
        background: transparent !important;
        border: 1px solid rgba(119,34,44,0.30) !important;
        color: #77222c !important;
        font-size: 0.75rem !important;
        padding: 6px 14px !important;
        margin-top: 4px !important;
        width: 100% !important;
    }}
    .pd-card-binary + div > button:hover {{
        background: rgba(119,34,44,0.08) !important;
        border-color: #77222c !important;
    }}
    .pd-card-regex + div > button {{
        background: transparent !important;
        border: 1px solid rgba(180,90,20,0.30) !important;
        color: #a05010 !important;
        font-size: 0.75rem !important;
        padding: 6px 14px !important;
        margin-top: 4px !important;
        width: 100% !important;
    }}
    .pd-card-regex + div > button:hover {{
        background: rgba(180,90,20,0.08) !important;
        border-color: #a05010 !important;
    }}
    </style>

    <div class="hs-header">
        <div class="hs-eyebrow">● Step 02 — Hasil Pencarian</div>
        <div class="hs-h1">Prodi yang Cocok Untukmu</div>
        <div class="hs-kw">"{keyword}"</div>
    </div>

    <div class="stats-row">
        <span class="stat-pill-binary">
            <i class="bi bi-lightning-charge-fill"></i>
            Binary &nbsp;<strong>{len(result['binary_results'])} prodi</strong>
        </span>
        <span class="stat-pill-regex">
            <i class="bi bi-search"></i>
            Regex &nbsp;<strong>{len(result['regex_results'])} prodi</strong>
        </span>
        <span class="stat-pill-total">
            <i class="bi bi-check-circle-fill"></i>
            Total &nbsp;<strong>{len(prodi_list)} prodi</strong>
        </span>
    </div>
    """, unsafe_allow_html=True)

    if not prodi_list:
        st.markdown("""
        <div style="text-align:center;padding:40px 20px;color:rgba(79,23,29,0.55);">
            <div style="font-size:2.5rem;margin-bottom:12px"><i class="bi bi-binoculars-fill"></i></div>
            <div style="font-family:'Plus Jakarta Sans',sans-serif;font-size:1.3rem;color:#4f171d;margin-bottom:6px">
                Prodi tidak ditemukan</div>
            <div>Coba kata kunci lain seperti <code style="color:#9e2e3b">ai</code>,
            <code style="color:#9e2e3b">data</code>, atau <code style="color:#9e2e3b">bisnis</code></div>
        </div>""", unsafe_allow_html=True)
    else:
        cols = st.columns(3)
        for i, prodi in enumerate(prodi_list):
            source = get_source(prodi["prodi"])

            if source == "binary":
                card_cls  = "pd-card-binary"
                sk_cls    = "pd-sk-binary"
                badge_html = '<span class="pd-badge-binary"><i class="bi bi-lightning-charge-fill"></i> Binary</span>'
            else:
                card_cls  = "pd-card-regex"
                sk_cls    = "pd-sk-regex"
                badge_html = '<span class="pd-badge-regex"><i class="bi bi-search"></i> Regex</span>'

            skill_tags = "".join(
                [f'<span class="{sk_cls}">{s}</span>' for s in prodi.get("skill", [])[:3]]
            )

            with cols[i % 3]:
                st.markdown(f"""
                <div class="{card_cls}">
                    <div>
                        <div class="pd-name">{prodi['prodi']}</div>
                        <div class="pd-skills">{skill_tags}</div>
                    </div>
                    {badge_html}
                </div>""", unsafe_allow_html=True)
                if st.button("Lihat detail →", key=f"pb_{i}"):
                    st.session_state.selected_prodi = prodi["prodi"]
                    go_to(3)

    nav_buttons(back_page=1, next_page=4 if prodi_list else None, next_label="Lihat BST →")

# PAGE 3 — DETAIL PRODI
def page_detail_prodi():
    prodi_name = st.session_state.selected_prodi
    if not prodi_name:
        st.warning("Pilih prodi terlebih dahulu.")
        if st.button("← Kembali"): go_to(2)
        return

    detail = DETAIL_PRODI.get(prodi_name, {})
    prospek_html = "".join([
        f'<div class="pr-card"><span class="pr-dot">◆</span><span>{p}</span></div>'
        for p in detail.get("prospek", [])
    ])
    skill_html = "".join([f'<span class="sk-badge">{s}</span>' for s in detail.get("skill", [])])

    st.markdown(f"""
    <style>
    @keyframes fadeUp{{from{{opacity:0;transform:translateY(16px)}}to{{opacity:1;transform:translateY(0)}}}}
    .dt-eyebrow{{font-family:'Space Mono',monospace;font-size:0.68rem;letter-spacing:0.18em;
        color:#9e2e3b;text-transform:uppercase;margin-bottom:8px;animation:fadeUp 0.5s ease both;}}
    .dt-title{{font-family:'Plus Jakarta Sans',sans-serif;font-size:clamp(1.8rem,4vw,3rem);
        font-weight:900;color:#4f171d;line-height:1.1;margin-bottom:20px;
        animation:fadeUp 0.5s 0.1s ease both;}}
    .dt-title span{{color:#9e2e3b;}}
    .sec-card{{background:linear-gradient(135deg,rgba(244,215,219,0.8),rgba(249,235,237,0.85));
        border:1px solid rgba(158,46,59,0.12);border-radius:16px;padding:22px;margin-bottom:14px;
        animation:fadeUp 0.5s 0.15s ease both;}}
    .sec-lbl{{font-family:'Space Mono',monospace;font-size:0.65rem;letter-spacing:0.15em;
        color:#9e2e3b;text-transform:uppercase;margin-bottom:10px;}}
    .desc-txt{{color:rgba(79,23,29,0.85);font-size:0.92rem;line-height:1.75;}}
    .pr-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:8px;}}
    .pr-card{{background:rgba(158,46,59,0.06);border:1px solid rgba(158,46,59,0.14);
        border-radius:10px;padding:10px 14px;display:flex;align-items:center;gap:8px;
        color:#4f171d;font-size:0.84rem;}}
    .pr-dot{{color:#9e2e3b;font-size:0.55rem;}}
    .sk-wrap{{display:flex;flex-wrap:wrap;gap:7px;}}
    .sk-badge{{background:rgba(209,97,110,0.25);border:1px solid rgba(209,97,110,0.25);
        border-radius:7px;padding:6px 14px;font-size:0.82rem;color:#c6394a;font-weight:500;}}
    </style>
    <div class="dt-eyebrow">● Step 03 — Detail Program Studi</div>
    <div class="dt-title">{prodi_name}</div>
    <div class="sec-card">
        <div class="sec-lbl">Tentang Program Studi</div>
        <div class="desc-txt">{detail.get('deskripsi', '-')}</div>
    </div>
    <div class="sec-card">
        <div class="sec-lbl">Prospek Karir</div>
        <div class="pr-grid">{prospek_html}</div>
    </div>
    <div class="sec-card">
        <div class="sec-lbl">Skill yang Dipelajari</div>
        <div class="sk-wrap">{skill_html}</div>
    </div>
    """, unsafe_allow_html=True)

    nav_buttons(back_page=2)

# PAGE 4 — BST VISUALIZATION (matplotlib, dari KEYWORD_DATA)

def build_bst():
    from data_keywords import KEYWORD_DATA # import data dilakukan dalam fungsi agar di load hanya saat halaman BST dibuka, bukan saat apk jalan

    class N:
        def __init__(self, k):
            self.k = k
            self.l = None # pointer anak kiri
            self.r = None # pointer anak kanan

    def ins(root, k):
        if root is None: return N(k)
        if k < root.k:  root.l = ins(root.l, k)
        else:            root.r = ins(root.r, k)
        return root

    root = None
    for item in KEYWORD_DATA:
        root = ins(root, item["keyword"]) # keyword pertama yang dimasukkan otomatis menjadi root 
    return root


def assign_positions(root): 
    counter = [0]
    pos = {}
    def inorder(node, depth):
        if node is None: return
        inorder(node.l, depth + 1)
        pos[id(node)] = (counter[0], depth, node.k)
        counter[0] += 1
        inorder(node.r, depth + 1)
    inorder(root, 0)
    return pos


def render_bst_interactive(pos, root):
    """
    pos: {node_id: (x, depth, key)}
    Render BST sebagai HTML interaktif dengan D3.js
    """
    # Build nodes & links dari pos
    id_map = {nid: i for i, nid in enumerate(pos)}
    
    nodes_js = []
    for nid, (x, depth, key) in pos.items():
        nodes_js.append(f'{{"id":{id_map[nid]},"key":"{key}","depth":{depth},"x_order":{x}}}') # format node dikonversi ke format JSON
    
    # Build edges dengan DFS
    links_js = []
    def collect_edges(node):
        if node is None: return
        if node.l:
            links_js.append(f'{{"source":{id_map[id(node)]},"target":{id_map[id(node.l)]}}}')
            collect_edges(node.l)
        if node.r:
            links_js.append(f'{{"source":{id_map[id(node)]},"target":{id_map[id(node.r)]}}}')
            collect_edges(node.r)
    collect_edges(root)

    nodes_str = "[" + ",".join(nodes_js) + "]"
    links_str = "[" + ",".join(links_js) + "]"

    max_x     = max(x for x, _, _ in pos.values())
    max_depth = max(d for _, d, _ in pos.values())

    html = f"""
<!DOCTYPE html>
<html>
<head>
<style>
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{ background:#f9ebed; overflow:hidden; font-family:'Space Mono',monospace; }}
  #canvas {{ width:100%; height:560px; cursor:grab; }}
  #canvas:active {{ cursor:grabbing; }}

  .tooltip {{
    position:absolute; pointer-events:none;
    background:rgba(244,215,219,0.96);
    border:1px solid rgba(158,46,59,0.4);
    border-radius:8px; padding:8px 12px;
    font-family:'Space Mono',monospace;
    font-size:11px; color:#4f171d;
    opacity:0; transition:opacity 0.15s;
    max-width:180px; z-index:10;
  }}
  .tooltip.show {{ opacity:1; }}
  .tooltip .kw  {{ color:#9e2e3b; font-weight:700; font-size:12px; margin-bottom:4px; }}
  .tooltip .dep {{ color:rgba(79,23,29,0.55); font-size:10px; }}

  #controls {{
    position:absolute; bottom:12px; right:14px;
    display:flex; gap:6px;
  }}
  #controls button {{
    background:rgba(79,23,29,0.08);
    border:1px solid rgba(158,46,59,0.25);
    border-radius:6px; color:#9e2e3b;
    font-family:'Space Mono',monospace;
    font-size:10px; padding:5px 10px; cursor:pointer;
    transition:all 0.15s;
  }}
  #controls button:hover {{
    background:rgba(158,46,59,0.12);
    border-color:#9e2e3b;
  }}
  #info {{
    position:absolute; top:10px; left:14px;
    font-family:'Space Mono',monospace;
    font-size:10px; color:rgba(79,23,29,0.35);
  }}
</style>
</head>
<body>
<svg id="canvas"></svg>
<div class="tooltip" id="tip">
  <div class="kw" id="tip-kw"></div>
  <div class="dep" id="tip-dep"></div>
</div>
<div id="info">scroll to zoom · drag to pan · hover node for detail</div>
<div id="controls">
  <button onclick="resetView()">Reset</button>
  <button onclick="zoomIn()">＋</button>
  <button onclick="zoomOut()">－</button>
</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/d3/7.8.5/d3.min.js"></script>
<script>
const nodes = {nodes_str};
const links = {links_str};

const W = document.getElementById('canvas').clientWidth || 900;
const H = 560;
const maxX = {max_x};
const maxD = {max_depth};

const DEPTH_COLORS = [
  {{ fill:'#f4d7db', stroke:'#9e2e3b', text:'#4f171d' }},
  {{ fill:'#c6394a', stroke:'#f9ebed', text:'#f9ebed' }},
  {{ fill:'#e8b0b6', stroke:'#77222c', text:'#4f171d' }},
  {{ fill:'#77222c', stroke:'#dd8892', text:'#f9ebed' }},
  {{ fill:'#9e2e3b', stroke:'#f4d7db', text:'#f9ebed' }},
];
const getColor = d => DEPTH_COLORS[Math.min(d, DEPTH_COLORS.length-1)];

const padX = 60, padY = 50;
const spacingX = Math.max(28, (W - padX*2) / (maxX + 1));
const spacingY = Math.min(80, Math.max(50, (H - padY*2) / (maxD + 1)));

nodes.forEach(n => {{
  n.px = padX + n.x_order * spacingX;
  n.py = padY + n.depth * spacingY;
}});

const svg = d3.select('#canvas')
  .attr('width', W).attr('height', H);

const g = svg.append('g');

// Zoom + pan
const zoom = d3.zoom()
  .scaleExtent([0.25, 3])
  .on('zoom', e => g.attr('transform', e.transform));
svg.call(zoom);

// Edges
g.selectAll('line.edge')
  .data(links).enter()
  .append('line')
  .attr('x1', d => nodes[d.source].px)
  .attr('y1', d => nodes[d.source].py)
  .attr('x2', d => nodes[d.target].px)
  .attr('y2', d => nodes[d.target].py)
  .attr('stroke', 'rgba(209,97,110,0.5)')
  .attr('stroke-width', 1);

// Node groups
const tip   = document.getElementById('tip');
const tipKw = document.getElementById('tip-kw');
const tipDp = document.getElementById('tip-dep');

const nodeG = g.selectAll('g.node')
  .data(nodes).enter()
  .append('g')
  .attr('class','node')
  .attr('transform', d => `translate(${{d.px}},${{d.py}})`)
  .style('cursor','pointer')
  .on('mouseover', function(event, d) {{
    d3.select(this).select('circle.inner')
      .transition().duration(120)
      .attr('r', 18);
    tipKw.textContent = d.key;
    tipDp.textContent = `depth: ${{d.depth}}`;
    tip.classList.add('show');
  }})
  .on('mousemove', function(event) {{
    const rect = document.getElementById('canvas').getBoundingClientRect();
    tip.style.left = (event.clientX - rect.left + 14) + 'px';
    tip.style.top  = (event.clientY - rect.top  - 36) + 'px';
  }})
  .on('mouseout', function(event, d) {{
    d3.select(this).select('circle.inner')
      .transition().duration(120)
      .attr('r', 14);
    tip.classList.remove('show');
  }});

// Outer ring
nodeG.append('circle')
  .attr('r', 20)
  .attr('fill', d => getColor(d.depth).fill)
  .attr('stroke', d => getColor(d.depth).stroke)
  .attr('stroke-width', 1.5)
  .attr('opacity', 0.6);

// Inner circle
nodeG.append('circle')
  .attr('class','inner')
  .attr('r', 14)
  .attr('fill', d => getColor(d.depth).fill)
  .attr('stroke', d => getColor(d.depth).stroke)
  .attr('stroke-width', 1.5);

// Label
nodeG.append('text')
  .attr('text-anchor','middle')
  .attr('dominant-baseline','central')
  .attr('fill', d => getColor(d.depth).text)
  .attr('font-size', d => d.key.length > 7 ? '7px' : '8px')
  .attr('font-family','Space Mono, monospace')
  .attr('font-weight','700')
  .attr('pointer-events','none')
  .text(d => d.key.length > 9 ? d.key.slice(0,8)+'…' : d.key);

// Controls
function resetView() {{
  svg.transition().duration(400)
    .call(zoom.transform, d3.zoomIdentity);
}}
function zoomIn()  {{ svg.transition().duration(250).call(zoom.scaleBy, 1.4); }}
function zoomOut() {{ svg.transition().duration(250).call(zoom.scaleBy, 0.7); }}
</script>
</body>
</html>
"""
    return html


def page_bst():
    st.markdown("""
    <style>
    .bst-eyebrow{font-family:'Space Mono',monospace;font-size:0.68rem;letter-spacing:0.18em;
        color:#9e2e3b;text-transform:uppercase;margin-bottom:8px;}
    .bst-title{font-family:'Plus Jakarta Sans',sans-serif;font-size:clamp(1.8rem,4vw,2.6rem);
        font-weight:700;color:#4f171d;margin-bottom:4px;}
    .bst-sub{color:rgba(79,23,29,0.5);font-size:0.85rem;margin-bottom:14px;}
    .insight-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:10px;margin-top:14px;}
    .ins-card{background:rgba(79,23,29,0.06);border:1px solid rgba(158,46,59,0.1);
        border-radius:12px;padding:16px;}
    .ins-icon{font-size:1.2rem;margin-bottom:6px;}
    .ins-t{font-weight:600;color:#c6394a;font-size:0.82rem;margin-bottom:4px;}
    .ins-d{color:rgba(79,23,29,0.6);font-size:0.77rem;line-height:1.55;}
    .ins-d code{color:#9e2e3b;font-family:'Space Mono',monospace;font-size:0.72rem;}
    </style>
    <div class="bst-eyebrow">● Step 04 — Struktur Data</div>
    <div class="bst-title">Binary Search Tree</div>
    <div class="bst-sub">Visualisasi interaktif BST dari seluruh keyword database — scroll, zoom, hover node</div>
    """, unsafe_allow_html=True)

    root = build_bst()
    pos  = assign_positions(root)

    html_content = render_bst_interactive(pos, root)
    components.html(html_content, height=570, scrolling=False)

    total_nodes = len(pos)
    max_depth   = max(d for _, d, _ in pos.values())
    avg_depth   = sum(d for _, d, _ in pos.values()) / total_nodes
    root_key    = root.k

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Node",      total_nodes)
    c2.metric("Kedalaman Maks",  max_depth)
    c3.metric("Root Node",       f'"{root_key}"')
    c4.metric("Rata-rata Depth", f"{avg_depth:.1f}")

    st.markdown("""
    <div class="insight-grid">
        <div class="ins-card">
            <div class="ins-icon"><i class="bi bi-diagram-3-fill"></i></div>
            <div class="ins-t">Struktur Hierarki</div>
            <div class="ins-d">BST dibangun dari seluruh keyword database secara leksikografis.
            Node kiri lebih kecil dari parent, kanan lebih besar yang dimana ini memungkinkan pencarian <code>O(log n)</code>.</div>
        </div>
        <div class="ins-card">
            <div class="ins-icon"><i class="bi bi-lightning-charge-fill"></i></div>
            <div class="ins-t">Efisiensi Pencarian</div>
            <div class="ins-d">Traversal in-order menghasilkan <code>SORTED_KEYWORDS</code>
            yang digunakan binary search di engine pencarian.</div>
        </div>
        <div class="ins-card">
            <div class="ins-icon"><i class="bi bi-arrow-repeat"></i></div>
            <div class="ins-t">In-Order Traversal</div>
            <div class="ins-d">Pola kiri → parent → kanan menghasilkan semua keyword
            terurut alfabet yang merupakan fondasi dari <code>binary_search()</code>.</div>
        </div>
        <div class="ins-card">
            <div class="ins-icon"><i class="bi bi-bar-chart-fill"></i></div>
            <div class="ins-t">Balanced Insert</div>
        <div class="ins-d">BST ini dibangun dengan teknik <code>balanced insert</code> dimana
            elemen tengah dimasukkan lebih dulu secara rekursif, sehingga pohon
            terbentuk seimbang.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    nav_buttons(back_page=2, next_page=5, next_label="Algoritma →")

# PAGE 5 — ALGORITMA
def page_algoritma():
    result = st.session_state.search_result
    bt  = result["binary_time"] if result else 0.012
    rt  = result["regex_time"]  if result else 0.025
    kw  = result["keyword"]     if result else "-"

    faster     = "Binary Search" if bt <= rt else "Regex Search"
    faster_pct = abs(rt - bt) / max(rt, bt) * 100 if max(rt, bt) > 0 else 0

    st.markdown(f"""
    <style>
    @keyframes fadeUp{{from{{opacity:0;transform:translateY(16px)}}to{{opacity:1;transform:translateY(0)}}}}
    .ag-eyebrow{{font-family:'Space Mono',monospace;font-size:0.68rem;letter-spacing:0.18em;
        color:#9e2e3b;text-transform:uppercase;margin-bottom:8px;}}
    .ag-title{{font-family:'Plus Jakarta Sans',sans-serif;font-size:clamp(1.6rem,3.5vw,2.4rem);
        font-weight:700;color:#4f171d;margin-bottom:14px;}}
    .ag-compare{{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin:14px 0;}}
    .ag-card{{background:linear-gradient(135deg,rgba(244,215,219,0.85),rgba(249,235,237,0.85));
        border:1px solid rgba(158,46,59,0.15);border-radius:14px;padding:20px;position:relative;overflow:hidden;}}
    .ag-card.win{{border-color:rgba(158,46,59,0.45);}}
    .ag-card.win::after{{content:'LEBIH CEPAT';position:absolute;top:12px;right:12px;
        background:rgba(158,46,59,0.12);border:1px solid rgba(158,46,59,0.28);border-radius:5px;
        padding:2px 8px;font-family:'Space Mono',monospace;font-size:0.58rem;color:#9e2e3b;letter-spacing:0.08em;}}
    .ag-card-ico{{font-size:1.6rem;margin-bottom:8px;}}
    .ag-card-name{{font-family:'Plus Jakarta Sans',sans-serif;font-size:1.15rem;color:#4f171d;margin-bottom:4px;}}
    .ag-card-time{{font-family:'Space Mono',monospace;font-size:1.5rem;color:#9e2e3b;font-weight:700;margin:10px 0;}}
    .ag-card-time span{{font-size:0.8rem;color:rgba(158,46,59,0.55);}}
    .ag-card-desc{{font-size:0.78rem;color:rgba(79,23,29,0.6);line-height:1.55;}}
    .ag-tag{{display:inline-block;background:rgba(209,97,110,0.25);border:1px solid rgba(209,97,110,0.25);
        border-radius:5px;padding:3px 9px;font-size:0.68rem;color:#c6394a;margin-top:10px;
        font-family:'Space Mono',monospace;}}
    .bar-wrap{{margin:12px 0;}}
    .bar-lbl{{display:flex;justify-content:space-between;margin-bottom:4px;font-size:0.76rem;}}
    .bar-name{{color:rgba(79,23,29,0.75);font-family:'Space Mono',monospace;}}
    .bar-val{{color:#9e2e3b;font-family:'Space Mono',monospace;}}
    .bar-track{{height:8px;background:rgba(79,23,29,0.08);border-radius:100px;overflow:hidden;margin-bottom:10px;}}
    .bar-fill{{height:100%;border-radius:100px;}}
    .kesimpulan{{background:rgba(158,46,59,0.06);border:1px solid rgba(158,46,59,0.2);
        border-radius:12px;padding:14px 18px;margin:10px 0;font-size:0.84rem;}}
    .ins2-grid{{display:grid;grid-template-columns:repeat(2,1fr);gap:10px;margin-top:12px;}}
    .ins2-card{{background:rgba(79,23,29,0.06);border:1px solid rgba(158,46,59,0.1);
        border-radius:12px;padding:14px;}}
    .i2-ico{{font-size:1.1rem;margin-bottom:6px;}}
    .i2-t{{font-weight:600;color:#c6394a;font-size:0.8rem;margin-bottom:4px;}}
    .i2-d{{color:rgba(79,23,29,0.58);font-size:0.75rem;line-height:1.55;}}
    .i2-d code{{color:#9e2e3b;font-family:'Space Mono',monospace;font-size:0.7rem;}}
    </style>
    <div class="ag-eyebrow">● Step 05 — Analisis Algoritma</div>
    <div class="ag-title">Perbandingan Algoritma Pencarian</div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    c1.metric("Keyword", f'"{kw}"')
    c2.metric("Binary Search", f"{bt:.4f} ms")
    c3.metric("Regex Search",  f"{rt:.4f} ms")

    max_t = max(bt, rt, 0.0001)
    b_pct = int(bt / max_t * 100)
    r_pct = int(rt / max_t * 100)
    b_win = "win" if bt <= rt else ""
    r_win = "win" if rt < bt  else ""

    st.markdown(f"""
    <div class="ag-compare">
        <div class="ag-card {b_win}">
            <div class="ag-card-ico"><i class="bi bi-lightning-charge-fill"></i></div>
            <div class="ag-card-name">Binary Search</div>
            <div class="ag-card-time">{bt:.4f}<span> ms</span></div>
            <div class="ag-card-desc">Memanfaatkan data yang sudah terurut via BST in-order. Kompleksitas <code style="color:#9e2e3b">O(log n)</code> untuk exact match.</div>
            <span class="ag-tag">O(log n)</span>
        </div>
        <div class="ag-card {r_win}">
            <div class="ag-card-ico"><i class="bi bi-search"></i></div>
            <div class="ag-card-name">Regex Search</div>
            <div class="ag-card-time">{rt:.4f}<span> ms</span></div>
            <div class="ag-card-desc">Menelusuri seluruh data dengan pattern matching. Fleksibel untuk partial match, kompleksitas <code style="color:#9e2e3b">O(n)</code>.</div>
            <span class="ag-tag">O(n)</span>
        </div>
    </div>

    <div class="bar-wrap">
        <div class="bar-lbl"><span class="bar-name">Binary Search</span><span class="bar-val">{bt:.6f} ms</span></div>
        <div class="bar-track"><div class="bar-fill" style="width:{b_pct}%;background:linear-gradient(90deg,#c6394a,#77222c)"></div></div>
        <div class="bar-lbl"><span class="bar-name">Regex Search</span><span class="bar-val">{rt:.6f} ms</span></div>
        <div class="bar-track"><div class="bar-fill" style="width:{r_pct}%;background:linear-gradient(90deg,#c6394a,#77222c)"></div></div>
    </div>

    <div class="kesimpulan">
        <span style="font-family:'Space Mono',monospace;font-size:0.7rem;color:#9e2e3b;">KESIMPULAN → </span>
        <strong style="color:#4f171d">{faster}</strong> lebih cepat {faster_pct:.1f}% untuk keyword
        <code style="color:#9e2e3b;font-family:'Space Mono',monospace">"{kw}"</code>.
        <span style="color:rgba(79,23,29,0.7)"> Binary unggul pada exact match, Regex unggul untuk pencarian parsial.</span>
    </div>

    <div class="ins2-grid">
        <div class="ins2-card">
            <div class="i2-ico"><i class="bi bi-bullseye"></i></div>
            <div class="i2-t">Kapan Binary Search Unggul?</div>
            <div class="i2-d">Saat keyword <strong>tepat sama</strong> dengan data. Kompleksitas <code>O(log n)</code>  jauh lebih cepat untuk dataset besar.</div>
        </div>
        <div class="ins2-card">
            <div class="i2-ico"><i class="bi bi-globe"></i></div>
            <div class="i2-t">Kapan Regex Unggul?</div>
            <div class="i2-d">Saat user mengetik <strong>sebagian kata</strong>. Regex menemukan <code>"dig"</code> dalam <code>"digital"</code> sedangkan Binary Search tidak bisa.</div>
        </div>
        <div class="ins2-card">
            <div class="i2-ico"><i class="bi bi-link-45deg"></i></div>
            <div class="i2-t">Sinergi Keduanya</div>
            <div class="i2-d">FindMyProdi menjalankan <strong>keduanya paralel</strong>: Binary untuk akurasi tinggi, Regex untuk jangkauan luas.</div>
        </div>
        <div class="ins2-card">
            <div class="i2-ico"><i class="bi bi-graph-up-arrow"></i></div>
            <div class="i2-t">Skalabilitas</div>
            <div class="i2-d">Pada <code>1000+</code> keyword, Binary makin unggul. Regex tetap <code>O(n)</code>, Binary tetap <code>O(log n)</code>.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    nav_buttons(back_page=4, next_page=6, next_label="Penutup →")

# PAGE 6 — PENUTUP
def page_penutup():
    n_prodi = len(DETAIL_PRODI)
    n_kw    = len(KEYWORD_DATA)

    st.markdown(f"""
    <style>
    @keyframes fadeUp{{from{{opacity:0;transform:translateY(20px)}}to{{opacity:1;transform:translateY(0)}}}}
    @keyframes shimmer{{0%{{background-position:-200% center}}100%{{background-position:200% center}}}}
    @keyframes floatY{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-6px)}}}}
    .pt-wrap{{
        display:flex;flex-direction:column;align-items:center;justify-content:center;
        min-height:85vh;padding:24px 20px;text-align:center;
        background:radial-gradient(ellipse at 30% 30%,rgba(158,46,59,0.1) 0%,transparent 50%),
        radial-gradient(ellipse at 70% 70%,rgba(249,235,237,0.95) 0%,transparent 50%),#f9ebed;
        position:relative;overflow:hidden;
    }}
    .pt-grid{{position:absolute;inset:0;
        background-image:linear-gradient(rgba(158,46,59,0.03) 1px,transparent 1px),
        linear-gradient(90deg,rgba(158,46,59,0.03) 1px,transparent 1px);
        background-size:55px 55px;pointer-events:none;}}
    .pt-icon{{font-size:3.5rem;margin-bottom:16px;position:relative;z-index:1;
        animation:fadeUp 0.6s ease both,floatY 3s 1s ease-in-out infinite;}}
    .pt-title{{
        font-family:'Plus Jakarta Sans',sans-serif;font-size:clamp(2rem,5vw,3.8rem);
        font-weight:900;line-height:1.1;margin-bottom:14px;position:relative;z-index:1;
        background:linear-gradient(135deg,#4f171d 30%,#c6394a 55%,#9e2e3b 80%,#c6394a);
        background-size:200% auto;-webkit-background-clip:text;-webkit-text-fill-color:transparent;
        background-clip:text;
        animation:fadeUp 0.6s 0.2s ease both,shimmer 4s 1.5s linear infinite;
    }}
    .pt-sub{{font-size:0.95rem;color:rgba(79,23,29,0.65);max-width:480px;line-height:1.75;
        margin-bottom:28px;position:relative;z-index:1;
        animation:fadeUp 0.6s 0.35s ease both;}}
    .pt-sub strong{{color:#9e2e3b;}}
    .pt-cards{{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;
        max-width:560px;margin:0 auto 24px;position:relative;z-index:1;
        animation:fadeUp 0.6s 0.5s ease both;}}
    .pt-c{{background:rgba(79,23,29,0.06);border:1px solid rgba(158,46,59,0.12);
        border-radius:12px;padding:16px 12px;transition:all 0.25s;}}
    .pt-c:hover{{background:rgba(158,46,59,0.07);border-color:rgba(158,46,59,0.3);transform:translateY(-2px);}}
    .pt-ci{{font-size:1.5rem;margin-bottom:6px;}}
    .pt-ct{{font-weight:600;color:#c6394a;font-size:0.75rem;margin-bottom:3px;}}
    .pt-cv{{font-family:'Space Mono',monospace;color:#9e2e3b;font-size:1rem;font-weight:700;}}
    .pt-sig{{font-family:'Space Mono',monospace;font-size:0.62rem;
        color:rgba(79,23,29,0.28);letter-spacing:0.1em;margin-top:16px;
        position:relative;z-index:1;animation:fadeUp 0.6s 0.7s ease both;}}
    .pt-btn-wrap{{position:relative;z-index:1;margin-top:20px;
        animation:fadeUp 0.6s 0.6s ease both;}}
    </style>
    <div class="pt-wrap">
        <div class="pt-grid"></div>
        <div class="pt-icon"><i class="bi bi-mortarboard-fill"></i></div>
        <div class="pt-title">Temukan Jalanmu,<br>Raih Impianmu</div>
        <div class="pt-sub">
            <strong>FindMyProdi</strong> hadir untuk membantu kamu menemukan program studi
            yang paling selaras dengan minat dan passion-mu karena pilihan tepat
            adalah awal dari perjalanan luar biasa.
        </div>
        <div class="pt-cards">
            <div class="pt-c"><div class="pt-ci"><i class="bi bi-diagram-3-fill"></i></div><div class="pt-ct">Struktur Data</div><div class="pt-cv">BST</div></div>
            <div class="pt-c"><div class="pt-ci"><i class="bi bi-book-fill"></i></div><div class="pt-ct">Program Studi</div><div class="pt-cv">{n_prodi}+</div></div>
            <div class="pt-c"><div class="pt-ci"><i class="bi bi-key-fill"></i></div><div class="pt-ct">Kata Kunci</div><div class="pt-cv">{n_kw}+</div></div>
        </div>
        <div class="pt-sig">Najla(041) · Alin(068) · Moza(185)</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <style>
    /* Button Kembali — pojok kiri bawah */
    div[data-testid="stButton"]:has(button[kind="secondary"]:contains("Kembali")) {
        position: fixed !important;
        bottom: 28px !important;
        left: 28px !important;
        z-index: 9999 !important;
    }

    /* Button Mulai Ulang — pojok kanan bawah */
    div[data-testid="stButton"]:has(button[kind="secondary"]:contains("Mulai")) {
        position: fixed !important;
        bottom: 28px !important;
        right: 28px !important;
        z-index: 9999 !important;
    }

    div[data-testid="stButton"]:has(button:contains("Kembali")) > button,
    div[data-testid="stButton"]:has(button:contains("Mulai")) > button {
        width: auto !important;
        padding: 10px 22px !important;
        font-size: 0.85rem !important;
        background: rgba(244,215,219,0.92) !important;
        border: 1px solid rgba(158,46,59,0.4) !important;
        color: #9e2e3b !important;
        backdrop-filter: blur(8px) !important;
        border-radius: 10px !important;
    }
    </style>
    """, unsafe_allow_html=True)

    if st.button("← Kembali", key="pt_back"):
        go_to(5)

    if st.button("↻ Mulai Ulang", key="restart_btn"):
        st.session_state.search_result = None
        st.session_state.selected_prodi = None
        st.session_state.keyword_input = ""
        go_to(0)

# PAGE 7 — DESKRIPSI SISTEM
def page_deskripsi_sistem():
    system = st.session_state.selected_system

    CONTENT = {
        "bst": {
            "icon": '<i class="bi bi-diagram-3-fill"></i>',
            "title": "BST Indexing",
            "subtitle": "Binary Search Tree",
            "color": "#9e2e3b",
            "deskripsi": "Binary Search Tree (BST) adalah struktur data pohon di mana setiap node memiliki paling banyak dua anak. Node kiri selalu lebih kecil dari parent dan node kanan selalu lebih besar, sehingga pencarian menjadi sangat efisien.",
            "keunggulan": [
                ("bi-lightning-charge-fill", "Pencarian Cepat", "O(log n) untuk pencarian, insert, dan delete pada pohon seimbang."),
                ("bi-bar-chart-fill", "Data Terurut", "In-order traversal menghasilkan data yang otomatis terurut secara alfabetis."),
                ("bi-arrow-repeat", "Dinamis", "Mudah menambah dan menghapus node tanpa reorganisasi seluruh struktur."),
                ("bi-bullseye", "Efisien", "Lebih efisien dari linear search O(n) untuk dataset besar."),
            ],
            "cara_kerja": [
                "Node root adalah titik awal pencarian.",
                "Bandingkan keyword dengan node saat ini.",
                "Jika lebih kecil, lanjut ke subtree kiri.",
                "Jika lebih besar, lanjut ke subtree kanan.",
                "Ulangi hingga node ditemukan atau NULL.",
            ],
            "kompleksitas": [("Best Case", "O(1)"), ("Average Case", "O(log n)"), ("Worst Case", "O(n)")],
        },
        "binary": {
            "icon": '<i class="bi bi-lightning-charge-fill"></i>',
            "title": "Binary Search",
            "subtitle": "Divide & Conquer Algorithm",
            "color": "#c6394a",
            "deskripsi": "Binary Search adalah algoritma pencarian yang bekerja pada data terurut. Dengan membagi data menjadi dua bagian secara berulang, algoritma ini menemukan target jauh lebih cepat dibanding pencarian linear.",
            "keunggulan": [
                ("bi-rocket-takeoff-fill", "Sangat Cepat", "Hanya butuh log₂(n) langkah yang dimana 1000 data hanya membutuhkan ~10 langkah."),
                ("bi-graph-down", "Efisiensi Tinggi", "Setiap iterasi membuang setengah data yang tidak relevan."),
                ("bi-123", "Presisi", "Cocok untuk exact match, menemukan kata kunci yang persis sama."),
                ("bi-box-fill", "Sederhana", "Implementasi mudah dengan array terurut hasil in-order BST."),
            ],
            "cara_kerja": [
                "Ambil data terurut hasil traversal BST.",
                "Tentukan indeks tengah (mid) dari array.",
                "Bandingkan keyword dengan elemen mid.",
                "Jika sama → ditemukan.",
                "Jika keyword < mid → cari di bagian kiri.",
                "Jika keyword > mid → cari di bagian kanan.",
                "Ulangi hingga ditemukan atau array habis.",
            ],
            "kompleksitas": [("Best Case", "O(1)"), ("Average Case", "O(log n)"), ("Worst Case", "O(log n)")],
        },
        "regex": {
            "icon": '<i class="bi bi-search"></i>',
            "title": "Regex Matching",
            "subtitle": "Regular Expression Engine",
            "color": "#c6394a",
            "deskripsi": "Regular Expression (Regex) adalah pola teks yang digunakan untuk mencocokkan string. Dalam FindMyProdi, Regex memungkinkan pencarian parsial yang dimana user cukup mengetik sebagian kata dan sistem tetap menemukan hasil yang relevan.",
            "keunggulan": [
                ("bi-globe", "Partial Match", "Menemukan 'digital' dari input 'dig' sedangkan Binary Search tidak bisa."),
                ("bi-input-cursor-text", "Fleksibel", "Mendukung pola kompleks, case-insensitive, dan variasi ejaan."),
                ("bi-diagram-3-fill", "Jangkauan Luas", "Menelusuri seluruh dataset untuk hasil yang komprehensif."),
                ("bi-people-fill", "Komplementer", "Melengkapi Binary Search untuk hasil yang lebih lengkap."),
            ],
            "cara_kerja": [
                "Kompilasi pattern dari keyword user (re.compile).",
                "Iterasi seluruh data keyword prodi.",
                "Cocokkan pattern dengan setiap entri (re.search).",
                "Kumpulkan semua entri yang cocok.",
                "Gabungkan dengan hasil Binary Search.",
            ],
            "kompleksitas": [("Best Case", "O(1)"), ("Average Case", "O(n)"), ("Worst Case", "O(n·m)")],
        },
    }

    if not system or system not in CONTENT:
        st.warning("Pilih sistem terlebih dahulu.")
        if st.button("← Kembali"): go_to(1)
        return

    c = CONTENT[system]

    # Render konten
    keunggulan_html = "".join([f"""
    <div class="kg-card">
        <div class="kg-icon">
            <i class="bi {k[0]}"></i>
        </div>
        <div>
            <div class="kg-t">{k[1]}</div>
            <div class="kg-d">{k[2]}</div>
        </div>
    </div>""" for k in c["keunggulan"]])

    komp_html = "".join([f"""
        <div class="kp-pill">
            <div class="kp-lbl">{k[0]}</div>
            <div class="kp-val">{k[1]}</div>
        </div>""" for k in c["kompleksitas"]])

    st.markdown(f"""
    <style>
    @keyframes fadeUp{{from{{opacity:0;transform:translateY(16px)}}to{{opacity:1;transform:translateY(0)}}}}
    .ds-eyebrow{{font-family:'Space Mono',monospace;font-size:0.68rem;letter-spacing:0.18em;
        color:{c['color']};text-transform:uppercase;margin-bottom:8px;}}
    .ds-icon{{font-size:3rem;margin-bottom:8px;}}
    .ds-title{{font-family:'Plus Jakarta Sans',sans-serif;font-size:clamp(2rem,5vw,3.2rem);
        font-weight:900;color:#4f171d;line-height:1.1;}}
    .ds-title span{{color:{c['color']};}}
    .ds-sub{{font-family:'Space Mono',monospace;font-size:0.72rem;color:rgba(79,23,29,0.5);
        letter-spacing:0.1em;margin-bottom:20px;}}
    .sec-card{{background:linear-gradient(135deg,rgba(244,215,219,0.8),rgba(249,235,237,0.85));
        border:1px solid rgba(158,46,59,0.12);border-radius:16px;padding:22px;margin-bottom:14px;}}
    .sec-lbl{{font-family:'Space Mono',monospace;font-size:0.65rem;letter-spacing:0.15em;
        color:{c['color']};text-transform:uppercase;margin-bottom:12px;}}
    .desc-txt{{color:rgba(79,23,29,0.85);font-size:0.92rem;line-height:1.75;}}
    .kg-grid{{display:grid;grid-template-columns:repeat(2,1fr);gap:10px;}}
    .kg-card{{background:rgba(79,23,29,0.06);border:1px solid rgba(158,46,59,0.1);
        border-radius:12px;padding:14px;display:flex;gap:12px;align-items:flex-start;}}
    .kg-icon{{font-size:1.4rem;flex-shrink:0;}}
    .kg-t{{font-weight:600;color:#c6394a;font-size:0.82rem;margin-bottom:3px;}}
    .kg-d{{color:rgba(79,23,29,0.6);font-size:0.75rem;line-height:1.5;}}
    .kp-row{{display:flex;gap:10px;flex-wrap:wrap;}}
    .kp-pill{{background:rgba(158,46,59,0.06);border:1px solid rgba(158,46,59,0.18);
        border-radius:10px;padding:12px 20px;flex:1;text-align:center;}}
    .kp-lbl{{font-size:0.7rem;color:rgba(79,23,29,0.5);font-family:'Space Mono',monospace;
        margin-bottom:4px;}}
    .kp-val{{font-family:'Space Mono',monospace;font-size:1rem;color:{c['color']};font-weight:700;}}
    </style>

    <div class="ds-eyebrow">● Deskripsi Sistem</div>
    <div class="ds-icon">{c['icon']}</div>
    <div class="ds-title">{c['title']}</div>
    <div class="ds-sub">{c['subtitle']}</div>

    <div class="sec-card">
        <div class="sec-lbl">Deskripsi</div>
        <div class="desc-txt">{c['deskripsi']}</div>
    </div>

    <div class="sec-card">
        <div class="sec-lbl">Keunggulan</div>
        <div class="kg-grid">{keunggulan_html}</div>
    </div>

    <div class="sec-card">
        <div class="sec-lbl">Kompleksitas Waktu</div>
        <div class="kp-row">{komp_html}</div>
    </div>
    """, unsafe_allow_html=True)

    nav_buttons(back_page=1)

# ROUTER
render_progress()

p = st.session_state.page
if   p == 0: page_logo()
elif p == 1: page_input()
elif p == 2: page_hasil()
elif p == 3: page_detail_prodi()
elif p == 4: page_bst()
elif p == 5: page_algoritma()
elif p == 6: page_penutup()
elif p == 7: page_deskripsi_sistem()
else: st.error("Halaman tidak ditemukan.")