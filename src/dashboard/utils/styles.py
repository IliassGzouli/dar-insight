"""
Shared styling utilities for Dar Insight pages.
"""
import streamlit as st

GLOBAL_CSS = """

<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=DM+Sans:wght@300;400;500;600&display=swap');

html, body { font-family: 'DM Sans', sans-serif; color: #0f1923; }

[data-testid="stWidgetLabel"] p,
[data-testid="stWidgetLabel"],
label,
.stNumberInput label,
.stSelectbox label,
.stRadio label { color: #0f1923 !important; }

.stRadio div[role="radiogroup"] label,
.stRadio div[role="radiogroup"] label p { color: #0f1923 !important; }

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f1923 0%, #162232 100%);
    border-right: 1px solid rgba(255,255,255,0.06);
}
[data-testid="stSidebar"] a,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] li { color: #c9d8e8 !important; }

[data-testid="stAppViewContainer"] { background: #f7f5f0; }
header[data-testid="stHeader"] { display: none; }

.page-header {
    display: flex; align-items: center; gap: 1rem;
    background: #ffffff; border-radius: 16px;
    padding: 1.4rem 2rem; margin-bottom: 1.8rem;
    border: 1px solid rgba(0,0,0,0.06);
    box-shadow: 0 2px 12px rgba(0,0,0,0.04);
}
.page-header-icon {
    font-size: 2rem; width: 60px; height: 60px;
    background: #f0f4f8; border-radius: 16px;
    display: flex; align-items: center;
    justify-content: center; flex-shrink: 0;
}
.page-header-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.7rem; color: #0f1923; margin: 0;
}
.page-header-subtitle { font-size: 0.88rem; color: #6b7c93; margin: 0; }
.accent-bar {
    width: 40px; height: 3px; background: #d4af37;
    border-radius: 2px; margin: 0.4rem 0 1.5rem;
}
.card {
    background: #ffffff; border-radius: 16px; padding: 1.6rem;
    border: 1px solid rgba(0,0,0,0.06);
    box-shadow: 0 2px 12px rgba(0,0,0,0.04); margin-bottom: 1.2rem;
}
.footer {
    text-align: center; color: #8a9ab0; font-size: 0.8rem;
    padding: 1.5rem 0 0.5rem;
    border-top: 1px solid rgba(0,0,0,0.07); margin-top: 2rem;
}

.hoverlayer .hovertext rect { fill: white !important; stroke: #e0e0e0 !important; }
.hoverlayer .hovertext text { fill: #0f1923 !important; }
.hoverlayer path { fill: white !important; stroke: #e0e0e0 !important; }


</style>
"""

PLOTLY_THEME = dict(
    plot_bgcolor="white",
    paper_bgcolor="white",
    font=dict(family="DM Sans", color="#0f1923", size=12),
    margin=dict(t=30, b=10, l=0, r=0),
    xaxis=dict(gridcolor="#f0f0f0", linecolor="#e0e0e0", color="#0f1923"),
    yaxis=dict(gridcolor="#f0f0f0", linecolor="#e0e0e0", color="#0f1923"),
)

def apply_styles():
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

def page_header(icon: str, title: str, subtitle: str = ""):
    st.markdown(f"""
    <div class="page-header">
      <div class="page-header-icon">{icon}</div>
      <div>
        <div class="page-header-title">{title}</div>
        <div class="page-header-subtitle">{subtitle}</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

def section(title: str):
    st.markdown(f"<p style='font-weight:600;color:#0f1923;font-size:1rem;margin-bottom:0'>{title}</p>", unsafe_allow_html=True)
    st.markdown('<div class="accent-bar"></div>', unsafe_allow_html=True)

def footer():
    st.markdown("""
    <div class="footer">
      Dar Insight &nbsp;·&nbsp; Data Science & ML &nbsp;·&nbsp; Marché Immobilier Maroc
    </div>
    """, unsafe_allow_html=True)