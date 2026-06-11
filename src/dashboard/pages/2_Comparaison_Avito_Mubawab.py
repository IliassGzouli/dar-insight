import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
from utils.styles import apply_styles, page_header, footer

st.set_page_config(
    page_title="Comparaison Plateformes — Dar Insight",
    page_icon="⚖️",
    layout="wide",
)
apply_styles()

st.markdown("""
<style>
.status-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    background: rgba(212,175,55,0.12);
    border: 1px solid rgba(212,175,55,0.35);
    color: #b8950a;
    font-size: 0.82rem;
    font-weight: 500;
    padding: 0.4rem 1rem;
    border-radius: 20px;
    margin-bottom: 1.5rem;
}
.platform-card {
    background: #ffffff;
    border-radius: 16px;
    padding: 2rem;
    border: 1px solid rgba(0,0,0,0.06);
    box-shadow: 0 2px 12px rgba(0,0,0,0.04);
    text-align: center;
    transition: transform 0.2s;
}
.platform-card:hover { transform: translateY(-3px); }
.platform-card .p-name {
    font-size: 1.3rem;
    font-weight: 700;
    color: #0f1923;
    margin: 1rem 0 0.4rem;
}
.platform-card .p-status {
    font-size: 0.82rem;
    padding: 0.25rem 0.75rem;
    border-radius: 12px;
    font-weight: 500;
}
.active { background: #e8f5e9; color: #2e7d32; }
.pending { background: #fff8e1; color: #f57f17; }
.roadmap-item {
    display: flex;
    align-items: flex-start;
    gap: 1rem;
    padding: 1rem 0;
    border-bottom: 1px solid #f0f0f0;
}
.roadmap-item:last-child { border-bottom: none; }
.roadmap-dot {
    width: 10px; height: 10px;
    border-radius: 50%;
    margin-top: 0.35rem;
    flex-shrink: 0;
}
.dot-done { background: #27ae60; }
.dot-todo { background: #d4af37; }
.dot-later { background: #bdc3c7; }
.roadmap-label { font-size: 0.9rem; color: #0f1923; font-weight: 500; }
.roadmap-sub { font-size: 0.78rem; color: #8a9ab0; }
</style>
""", unsafe_allow_html=True)

page_header("⚖️", "Comparaison Avito vs Mubawab", "Analyse comparative des deux principales plateformes immobilières au Maroc")

st.markdown('<span class="status-badge">⏳ En cours d\'intégration — données Mubawab à venir</span>', unsafe_allow_html=True)

# ── Platform cards ────────────────────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="platform-card">
      <div style="font-size:3rem">🏪</div>
      <div class="p-name">Avito.ma</div>
      <span class="p-status active">✅ Données intégrées</span>
      <div style="margin-top:1.2rem; text-align:left; font-size:0.85rem; color:#6b7c93; line-height:1.8">
        ✔ Scraping effectué<br>
        ✔ Nettoyage et normalisation<br>
        ✔ Modèle ML entraîné<br>
        ✔ Analyses disponibles
      </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="platform-card">
      <div style="font-size:3rem">🏠</div>
      <div class="p-name">Mubawab.ma</div>
      <span class="p-status pending">🔄 Scraping en cours</span>
      <div style="margin-top:1.2rem; text-align:left; font-size:0.85rem; color:#6b7c93; line-height:1.8">
        ○ Scraping en développement<br>
        ○ Nettoyage à faire<br>
        ○ Fusion des datasets<br>
        ○ Analyse comparative
      </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ── Roadmap ───────────────────────────────────────────────────────────────────
col_r, col_p = st.columns([1, 1])

with col_r:
    st.markdown("**Roadmap d'intégration**")
    st.markdown('<div class="accent-bar" style="width:40px;height:3px;background:#d4af37;border-radius:2px;margin-bottom:1rem"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="roadmap-item">
      <div class="roadmap-dot dot-done"></div>
      <div>
        <div class="roadmap-label">Scraping Avito.ma</div>
        <div class="roadmap-sub">Collecte automatisée des annonces</div>
      </div>
    </div>
    <div class="roadmap-item">
      <div class="roadmap-dot dot-done"></div>
      <div>
        <div class="roadmap-label">Nettoyage & Feature Engineering</div>
        <div class="roadmap-sub">Normalisation, gestion des valeurs manquantes</div>
      </div>
    </div>
    <div class="roadmap-item">
      <div class="roadmap-dot dot-todo"></div>
      <div>
        <div class="roadmap-label">Scraping Mubawab.ma</div>
        <div class="roadmap-sub">En cours de développement</div>
      </div>
    </div>
    <div class="roadmap-item">
      <div class="roadmap-dot dot-todo"></div>
      <div>
        <div class="roadmap-label">Fusion des datasets</div>
        <div class="roadmap-sub">Alignement des colonnes et déduplication</div>
      </div>
    </div>
    <div class="roadmap-item">
      <div class="roadmap-dot dot-later"></div>
      <div>
        <div class="roadmap-label">Dashboard comparatif</div>
        <div class="roadmap-sub">Prix, volume, typologies par plateforme</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

with col_p:
    st.markdown("**Ce que cette page affichera**")
    st.markdown('<div class="accent-bar" style="width:40px;height:3px;background:#d4af37;border-radius:2px;margin-bottom:1rem"></div>', unsafe_allow_html=True)
    preview_items = [
        ("📊", "Comparaison des prix moyens/médians par plateforme"),
        ("📍", "Répartition géographique des annonces"),
        ("🏷️", "Différence de prix pour des biens similaires"),
        ("📈", "Volume d'annonces par ville et par plateforme"),
        ("🛏️", "Typologies (studios, F2, F3…) par source"),
        ("💡", "Indicateur de confiance des prix"),
    ]
    for icon, label in preview_items:
        st.markdown(f"""
        <div style="display:flex;gap:0.8rem;align-items:center;padding:0.6rem 0;border-bottom:1px solid #f0f0f0;font-size:0.88rem;color:#0f1923">
          <span style="font-size:1.1rem">{icon}</span> {label}
        </div>
        """, unsafe_allow_html=True)

footer()
