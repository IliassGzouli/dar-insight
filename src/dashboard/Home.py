import streamlit as st
import plotly.express as px
from utils.data import load_market_data

st.set_page_config(
    page_title="Dar Insight — Immobilier Maroc",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f1923 0%, #162232 100%);
    border-right: 1px solid rgba(255,255,255,0.06);
}
[data-testid="stSidebar"] * {
    color: #c9d8e8 !important;
}
[data-testid="stSidebar"] .stRadio label {
    font-size: 0.88rem;
}

/* ── Main background ── */
[data-testid="stAppViewContainer"] {
    background: #f7f5f0;
}

/* ── Hide default header ── */
header[data-testid="stHeader"] { display: none; }

/* ── Hero banner ── */
.hero {
    background: linear-gradient(135deg, #0f1923 0%, #1a3a5c 60%, #0f1923 100%);
    border-radius: 20px;
    padding: 3rem 3.5rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 320px; height: 320px;
    background: radial-gradient(circle, rgba(212,175,55,0.15) 0%, transparent 70%);
    border-radius: 50%;
}
.hero::after {
    content: '';
    position: absolute;
    bottom: -40px; left: 30%;
    width: 200px; height: 200px;
    background: radial-gradient(circle, rgba(52,152,219,0.1) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-tag {
    display: inline-block;
    background: rgba(212,175,55,0.15);
    border: 1px solid rgba(212,175,55,0.4);
    color: #d4af37 !important;
    font-size: 0.72rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    padding: 0.3rem 0.9rem;
    border-radius: 20px;
    margin-bottom: 1.2rem;
}
.hero h1 {
    font-family: 'Playfair Display', serif;
    font-size: 3rem;
    color: #ffffff !important;
    line-height: 1.15;
    margin: 0 0 1rem;
}
.hero h1 span { color: #d4af37; }
.hero p {
    color: rgba(200,215,230,0.85) !important;
    font-size: 1.05rem;
    font-weight: 300;
    max-width: 520px;
    line-height: 1.7;
    margin: 0;
}

/* ── KPI cards ── */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
    margin-bottom: 2rem;
}
.kpi-card {
    background: #ffffff;
    border-radius: 16px;
    padding: 1.5rem 1.8rem;
    border: 1px solid rgba(0,0,0,0.06);
    box-shadow: 0 2px 12px rgba(0,0,0,0.05);
    transition: transform 0.2s, box-shadow 0.2s;
    position: relative;
    overflow: hidden;
}
.kpi-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 24px rgba(0,0,0,0.1);
}
.kpi-card::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 3px;
    background: var(--accent, #1a3a5c);
    border-radius: 0 0 16px 16px;
}
.kpi-icon {
    font-size: 1.6rem;
    margin-bottom: 0.6rem;
    display: block;
}
.kpi-label {
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #8a9ab0;
    font-weight: 500;
    margin-bottom: 0.3rem;
}
.kpi-value {
    font-size: 1.8rem;
    font-weight: 700;
    color: #0f1923;
    font-family: 'DM Sans', sans-serif;
    line-height: 1;
}
.kpi-sub {
    font-size: 0.78rem;
    color: #8a9ab0;
    margin-top: 0.3rem;
}

/* ── Section title ── */
.section-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.5rem;
    color: #0f1923;
    margin-bottom: 0.3rem;
}
.section-divider {
    width: 40px;
    height: 3px;
    background: #d4af37;
    border-radius: 2px;
    margin-bottom: 1.5rem;
}

/* ── Feature cards ── */
.feature-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
    margin-bottom: 2rem;
}
.feature-card {
    background: #ffffff;
    border-radius: 16px;
    padding: 1.6rem 2rem;
    border: 1px solid rgba(0,0,0,0.06);
    display: flex;
    align-items: flex-start;
    gap: 1.2rem;
    transition: transform 0.2s, box-shadow 0.2s;
}
.feature-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(0,0,0,0.08);
}
.feature-icon {
    font-size: 1.8rem;
    flex-shrink: 0;
    width: 52px; height: 52px;
    background: #f0f4f8;
    border-radius: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
}
.feature-title {
    font-weight: 600;
    color: #0f1923;
    font-size: 0.95rem;
    margin-bottom: 0.35rem;
}
.feature-desc {
    font-size: 0.83rem;
    color: #6b7c93;
    line-height: 1.6;
}

/* ── Mini chart card ── */
.chart-card {
    background: #ffffff;
    border-radius: 16px;
    padding: 1.6rem;
    border: 1px solid rgba(0,0,0,0.06);
    box-shadow: 0 2px 12px rgba(0,0,0,0.04);
    margin-bottom: 2rem;
}

/* ── Footer ── */
.footer {
    text-align: center;
    color: #8a9ab0;
    font-size: 0.8rem;
    padding: 1.5rem 0 0.5rem;
    border-top: 1px solid rgba(0,0,0,0.07);
}
</style>
""", unsafe_allow_html=True)

# ── Data ──────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    return load_market_data()

df = load_data()

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-tag">🇲🇦 Marché Immobilier Maroc</div>
  <h1>Dar <span>Insight</span></h1>
  <p>Explorez, analysez et prédisez les prix immobiliers au Maroc grâce à la Data Science et au Machine Learning.</p>
</div>
""", unsafe_allow_html=True)

# ── KPI Cards ─────────────────────────────────────────────────────────────────
prix_median = int(df['prix'].median())
surface_moy = df['surface'].mean()

st.markdown(f"""
<div class="kpi-grid">
  <div class="kpi-card" style="--accent:#1a3a5c">
    <span class="kpi-icon">📊</span>
    <div class="kpi-label">Annonces analysées</div>
    <div class="kpi-value">{len(df):,}</div>
    <div class="kpi-sub">Base de données active</div>
  </div>
  <div class="kpi-card" style="--accent:#d4af37">
    <span class="kpi-icon">💰</span>
    <div class="kpi-label">Prix moyen</div>
    <div class="kpi-value">{int(df['prix'].mean()):,}</div>
    <div class="kpi-sub">DH · médiane {prix_median:,} DH</div>
  </div>
  <div class="kpi-card" style="--accent:#27ae60">
    <span class="kpi-icon">📐</span>
    <div class="kpi-label">Surface moyenne</div>
    <div class="kpi-value">{surface_moy:.0f} m²</div>
    <div class="kpi-sub">Toutes typologies</div>
  </div>
  <div class="kpi-card" style="--accent:#e74c3c">
    <span class="kpi-icon">🏙️</span>
    <div class="kpi-label">Villes couvertes</div>
    <div class="kpi-value">{df['ville'].nunique()}</div>
    <div class="kpi-sub">Principales agglomérations</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Features ──────────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">Ce que vous pouvez faire</div>', unsafe_allow_html=True)
st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

st.markdown("""
<div class="feature-grid">
  <div class="feature-card">
    <div class="feature-icon">📈</div>
    <div>
      <div class="feature-title">Analyse du Marché</div>
      <div class="feature-desc">Distribution des prix, tendances par ville, corrélations entre surface et prix.</div>
    </div>
  </div>
  <div class="feature-card">
    <div class="feature-icon">🤖</div>
    <div>
      <div class="feature-title">Prédiction ML</div>
      <div class="feature-desc">Estimez le prix d'un bien en quelques secondes grâce à notre modèle entraîné.</div>
    </div>
  </div>
  <div class="feature-card">
    <div class="feature-icon">⚖️</div>
    <div>
      <div class="feature-title">Comparaison Avito / Mubawab</div>
      <div class="feature-desc">Comparez les deux plateformes principales sur les prix, volumes et typologies.</div>
    </div>
  </div>
  <div class="feature-card">
    <div class="feature-icon">💡</div>
    <div>
      <div class="feature-title">Insights Clés</div>
      <div class="feature-desc">Les villes les plus chères, les meilleures affaires, et les tendances cachées.</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Quick Chart ───────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">Aperçu rapide</div>', unsafe_allow_html=True)
st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

ville_top = (
    df.groupby("ville")["prix"]
    .median()
    .sort_values(ascending=False)
    .head(8)
    .reset_index()
)
ville_top.columns = ["Ville", "Prix médian (DH)"]

fig = px.bar(
    ville_top,
    x="Ville",
    y="Prix médian (DH)",
    color="Prix médian (DH)",
    color_continuous_scale=["#1a3a5c", "#d4af37"],
    text="Prix médian (DH)",
)
fig.update_traces(
    texttemplate="%{text:,.0f} DH",
    textposition="outside",
    marker_line_width=0,
    hovertemplate="<b>%{x}</b><br>Prix médian : %{y:,.0f} DH<extra></extra>",
)
fig.update_layout(
    plot_bgcolor="white",
    paper_bgcolor="white",
    font=dict(family="DM Sans", color="#0f1923"),
    coloraxis_showscale=False,
    xaxis=dict(title="", tickfont=dict(size=11)),
    yaxis=dict(title="Prix médian (DH)", tickformat=",.0f", gridcolor="#f0f0f0"),
    margin=dict(t=20, b=10, l=0, r=0),
    height=320,
)

st.markdown('<div class="chart-card">', unsafe_allow_html=True)
st.markdown("**Prix médian par ville (Top 8)**")
st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
st.markdown('</div>', unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
  Dar Insight &nbsp;·&nbsp; Data Science & Machine Learning &nbsp;·&nbsp; Marché Immobilier Maroc
</div>
""", unsafe_allow_html=True)
