import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.data import load_market_data
from utils.styles import apply_styles, page_header, section, footer, PLOTLY_THEME

st.set_page_config(
    page_title="Insights — Dar Insight",
    page_icon="💡",
    layout="wide",
)
apply_styles()

st.markdown("""
<style>
.insight-card {
    background: #ffffff;
    border-radius: 16px;
    padding: 1.6rem 2rem;
    border: 1px solid rgba(0,0,0,0.06);
    box-shadow: 0 2px 12px rgba(0,0,0,0.04);
    margin-bottom: 1rem;
    display: flex;
    align-items: flex-start;
    gap: 1.2rem;
}
.insight-icon {
    font-size: 1.8rem;
    width: 56px; height: 56px;
    border-radius: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
}
.insight-title { font-weight: 600; color: #0f1923; font-size: 0.9rem; margin-bottom: 0.2rem; }
.insight-value { font-size: 1.5rem; font-weight: 700; color: #0f1923; line-height: 1.2; }
.insight-sub { font-size: 0.8rem; color: #8a9ab0; margin-top: 0.3rem; }
</style>
""", unsafe_allow_html=True)

# ── Data ──────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    return load_market_data()

df = load_data()

page_header("💡", "Insights & Tendances", "Les faits marquants du marché immobilier marocain")

# ── Calculs clés ──────────────────────────────────────────────────────────────
ville_prix = df.groupby("ville")["prix"].mean()
ville_vol = df.groupby("ville").size()
ville_m2 = (df.groupby("ville")["prix"].mean() / df.groupby("ville")["surface"].mean())

ville_chere = ville_prix.idxmax()
ville_accessible = ville_prix.idxmin()
ville_active = ville_vol.idxmax()
prix_max_moy = ville_prix.max()
prix_min_moy = ville_prix.min()
meilleur_rapport = ville_m2.idxmin()

# ── Insight Cards ─────────────────────────────────────────────────────────────
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="insight-card">
      <div class="insight-icon" style="background:#fff3e0">🏆</div>
      <div>
        <div class="insight-title">Ville la plus chère</div>
        <div class="insight-value">{ville_chere}</div>
        <div class="insight-sub">Prix moy. {prix_max_moy:,.0f} DH</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="insight-card">
      <div class="insight-icon" style="background:#e8f5e9">💚</div>
      <div>
        <div class="insight-title">Ville la plus accessible</div>
        <div class="insight-value">{ville_accessible}</div>
        <div class="insight-sub">Prix moy. {prix_min_moy:,.0f} DH</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="insight-card">
      <div class="insight-icon" style="background:#e3f2fd">📊</div>
      <div>
        <div class="insight-title">Marché le plus actif</div>
        <div class="insight-value">{ville_active}</div>
        <div class="insight-sub">{ville_vol[ville_active]:,} annonces</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ── Row charts ────────────────────────────────────────────────────────────────
col_a, col_b = st.columns(2)

with col_a:
    section("Volume d'annonces par ville (Top 12)")
    top_vol = ville_vol.sort_values(ascending=False).head(12).reset_index()
    top_vol.columns = ["Ville", "Annonces"]
    fig_vol = px.bar(
        top_vol,
        x="Annonces", y="Ville",
        orientation="h",
        color="Annonces",
        color_continuous_scale=["#e3f2fd", "#1a3a5c"],
        text="Annonces",
    )
    fig_vol.update_traces(
        texttemplate="%{text:,}",
        textposition="outside",
        marker_line_width=0,
        hovertemplate="<b>%{y}</b><br>%{x:,} annonces<extra></extra>",
    )
    fig_vol.update_layout(**PLOTLY_THEME, height=380, coloraxis_showscale=False, xaxis_title="Nombre d'annonces")
    fig_vol.update_yaxes(autorange="reversed", title="")
    st.plotly_chart(fig_vol, use_container_width=True, config={"displayModeBar": False})

with col_b:
    section("Prix moyen au m² (Top 10 villes)")
    top_m2 = ville_m2.sort_values(ascending=False).head(10).reset_index()
    top_m2.columns = ["Ville", "DH/m²"]
    fig_m2 = px.bar(
        top_m2,
        x="Ville", y="DH/m²",
        color="DH/m²",
        color_continuous_scale=["#f8f0da", "#d4af37"],
        text="DH/m²",
    )
    fig_m2.update_traces(
        texttemplate="%{text:,.0f}",
        textposition="outside",
        marker_line_width=0,
        hovertemplate="<b>%{x}</b><br>%{y:,.0f} DH/m²<extra></extra>",
    )
    fig_m2.update_layout(
        **PLOTLY_THEME,
        height=380,
        coloraxis_showscale=False,
        yaxis_tickformat=",.0f",
        xaxis_title="",
    )
    st.plotly_chart(fig_m2, use_container_width=True, config={"displayModeBar": False})

# ── Corrélation heatmap (si features numériques) ──────────────────────────────
num_cols = df[["prix", "surface", "chambres"]].dropna()
if len(num_cols) > 0:
    st.markdown("---")
    col_c, col_d = st.columns(2)

    with col_c:
        section("Matrice de corrélation")
        corr = num_cols.corr()
        fig_corr = go.Figure(data=go.Heatmap(
            z=corr.values,
            x=corr.columns,
            y=corr.columns,
            colorscale=[[0, "#e3edf7"], [0.5, "#5d9cc8"], [1, "#0f1923"]],
            zmin=-1, zmax=1,
            text=corr.values.round(2),
            texttemplate="%{text}",
            hovertemplate="%{x} / %{y}<br>Corrélation : %{z:.2f}<extra></extra>",
        ))
        fig_corr.update_layout(**PLOTLY_THEME, height=280)
        fig_corr.update_layout(margin=dict(t=20, b=10, l=0, r=0))
        st.plotly_chart(fig_corr, use_container_width=True, config={"displayModeBar": False})

    with col_d:
        section("Résumé global")
        stats_data = {
            "Indicateur": [
                "Annonces totales",
                "Prix moyen",
                "Prix médian",
                "Surface moyenne",
                "Nb de villes",
                "Fourchette de prix",
            ],
            "Valeur": [
                f"{len(df):,}",
                f"{int(df['prix'].mean()):,} DH",
                f"{int(df['prix'].median()):,} DH",
                f"{df['surface'].mean():.1f} m²",
                str(df['ville'].nunique()),
                f"{int(df['prix'].min()):,} – {int(df['prix'].max()):,} DH",
            ],
        }
        st.dataframe(
            pd.DataFrame(stats_data),
            use_container_width=True,
            hide_index=True,
        )

footer()
