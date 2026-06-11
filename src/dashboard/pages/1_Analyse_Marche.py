import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from utils.data import load_market_data
from utils.styles import apply_styles, page_header, section, footer, PLOTLY_THEME

st.set_page_config(page_title="Analyse du Marché — Dar Insight", page_icon="📈", layout="wide")
apply_styles()

st.markdown("""
<style>
svg text { fill: #0f1923 !important; }
.js-plotly-plot .plotly text { fill: #0f1923 !important; }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    return load_market_data()

df = load_data()

page_header("📈", "Analyse du Marché", "Distribution des prix, comparaisons par ville et corrélations")


st.markdown("<p style='color:#0f1923;font-weight:600;font-size:0.95rem;margin-bottom:0.5rem'>Filtres</p>", unsafe_allow_html=True)
col_f1, col_f2, col_f3 = st.columns(3)
with col_f1:
    villes_dispo = sorted(df["ville"].dropna().unique())
    villes_sel = st.multiselect("Villes", villes_dispo, default=villes_dispo[:10])
with col_f2:
    prix_min, prix_max = int(df["prix"].min()), int(df["prix"].max())
    prix_range = st.slider("Plage de prix (DH)", prix_min, prix_max, (prix_min, prix_max), step=10_000)
with col_f3:
    surf_min, surf_max = int(df["surface"].min()), int(df["surface"].max())
    surf_range = st.slider("Surface (m2)", surf_min, surf_max, (surf_min, surf_max))

mask = (
    df["ville"].isin(villes_sel if villes_sel else villes_dispo)
    & df["prix"].between(*prix_range)
    & df["surface"].between(*surf_range)
)
dff = df[mask].copy()

st.markdown(f"<p style='color:#0f1923;font-size:0.9rem'><b>{len(dff):,}</b> annonces correspondent a vos criteres</p>", unsafe_allow_html=True)
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    section("Distribution des prix")
    fig_hist = px.histogram(dff, x="prix", nbins=60, color_discrete_sequence=["#1a3a5c"], labels={"prix": "Prix (DH)", "count": "Annonces"})
    fig_hist.update_traces(hovertemplate="Prix : %{x:,.0f} DH<br>Annonces : %{y}<extra></extra>", marker_line_width=0)
    fig_hist.update_layout(**PLOTLY_THEME, height=340, bargap=0.05, xaxis_tickformat=",.0f")
    st.plotly_chart(fig_hist, use_container_width=True, config={"displayModeBar": False})
    
with col2:
    section("Prix median par ville (Top 10)")
    top_villes = dff.groupby("ville")["prix"].median().sort_values(ascending=False).head(10).reset_index()
    top_villes.columns = ["Ville", "Prix median"]
    fig_bar = px.bar(top_villes, x="Ville", y="Prix median", color="Prix median", color_continuous_scale=["#1a3a5c", "#d4af37"], text="Prix median")
    fig_bar.update_traces(texttemplate="%{text:,.0f}", textposition="outside", marker_line_width=0)
    fig_bar.update_layout(**PLOTLY_THEME, height=340, coloraxis_showscale=False, yaxis_tickformat=",.0f")
    st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})

col3, col4 = st.columns(2)

with col3:
    section("Surface vs Prix")
    fig_scatter = px.scatter(dff, x="surface", y="prix", color="chambres", color_continuous_scale=px.colors.sequential.Blues, opacity=0.65, labels={"surface": "Surface (m2)", "prix": "Prix (DH)", "chambres": "Chambres"})
    fig_scatter.update_traces(marker=dict(size=5))
    fig_scatter.update_layout(**PLOTLY_THEME, height=340, yaxis_tickformat=",.0f")
    valid = dff[["surface", "prix"]].dropna()
    if len(valid) > 5:
        z = np.polyfit(valid["surface"], valid["prix"], 1)
        p = np.poly1d(z)
        xs = np.linspace(valid["surface"].min(), valid["surface"].max(), 100)
        fig_scatter.add_trace(go.Scatter(x=xs, y=p(xs), mode="lines", line=dict(color="#d4af37", width=2, dash="dot"), name="Tendance"))
    st.plotly_chart(fig_scatter, use_container_width=True, config={"displayModeBar": False})

with col4:
    section("Repartition par nombre de chambres")
    chambre_counts = dff["chambres"].value_counts().sort_index()
    fig_pie = px.pie(values=chambre_counts.values, names=[f"{c} chambre(s)" for c in chambre_counts.index], color_discrete_sequence=px.colors.sequential.Blues_r, hole=0.4)
    fig_pie.update_traces(textposition="inside", textinfo="percent+label")
    fig_pie.update_layout(**PLOTLY_THEME, height=340, showlegend=False)
    st.plotly_chart(fig_pie, use_container_width=True, config={"displayModeBar": False})

st.markdown("---")
section("Statistiques descriptives")
stats = dff[["prix", "surface", "chambres"]].describe().T
stats.columns = ["Nb", "Moyenne", "Ecart-type", "Min", "Q25", "Mediane", "Q75", "Max"]
stats = stats.applymap(lambda x: f"{x:,.1f}")
st.dataframe(stats, use_container_width=True)

footer()
