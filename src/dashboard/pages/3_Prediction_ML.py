import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
from utils.data import load_market_data
from utils.styles import apply_styles, page_header, section, footer, PLOTLY_THEME

st.markdown("""
<style>
.stRadio div[role="radiogroup"] label {
    color: #0f1923 !important;
}
.stRadio div[role="radiogroup"] label p {
    color: #0f1923 !important;
}
</style>
""", unsafe_allow_html=True)

st.set_page_config(
    page_title="Prédiction Prix — Dar Insight",
    page_icon="🤖",
    layout="wide",
)
apply_styles()

st.markdown("""
<style>
.predict-form {
    background: #ffffff;
    border-radius: 20px;
    padding: 2rem 2.5rem;
    border: 1px solid rgba(0,0,0,0.06);
    box-shadow: 0 4px 20px rgba(0,0,0,0.06);
}
.result-price {
    background: linear-gradient(135deg, #0f1923, #1a3a5c);
    border-radius: 20px;
    padding: 2.5rem;
    text-align: center;
    margin: 1.5rem 0;
    color: white;
}
.result-price .price-label {
    font-size: 0.85rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: rgba(200,220,240,0.8);
    margin-bottom: 0.6rem;
}
.result-price .price-value {
    font-family: 'Playfair Display', serif;
    font-size: 2.8rem;
    font-weight: 700;
    color: #d4af37;
    line-height: 1;
}
.result-price .price-unit {
    font-size: 1rem;
    color: rgba(200,220,240,0.7);
    margin-top: 0.4rem;
}
.result-m2 {
    background: #f7f5f0;
    border-radius: 12px;
    padding: 1rem 1.5rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.8rem;
}
.result-m2 .m2-label { font-size: 0.85rem; color: #6b7c93; }
.result-m2 .m2-value { font-size: 1.1rem; font-weight: 600; color: #0f1923; }
.confidence-bar {
    height: 6px;
    background: #e0e7ef;
    border-radius: 3px;
    overflow: hidden;
    margin-top: 0.4rem;
}
.confidence-fill {
    height: 100%;
    background: linear-gradient(90deg, #1a3a5c, #d4af37);
    border-radius: 3px;
}
.sim-badge {
    display: inline-block;
    background: #e8f4fd;
    color: #1a6fa8;
    font-size: 0.78rem;
    font-weight: 600;
    padding: 0.2rem 0.6rem;
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)

# ── Data & Model ──────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    return load_market_data()

@st.cache_resource
def load_model():
    model = joblib.load("models/model_prix_v3.pkl")
    features = joblib.load("models/features_v3.pkl")
    return model, features

df = load_data()
try:
    model, features = load_model()
    model_ok = True
except Exception as e:
    model_ok = False
    model_err = str(e)

page_header("🤖", "Prédiction du Prix Immobilier", "Estimez la valeur d'un bien grâce au Machine Learning")

# ── Layout ────────────────────────────────────────────────────────────────────
left_col, right_col = st.columns([1, 1], gap="large")

# ── Formulaire ────────────────────────────────────────────────────────────────
with left_col:
    st.markdown("#### <span style='color:#0f1923'>🏠 Caractéristiques du bien</span>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        surface = st.number_input("📐 Surface (m²)", min_value=20, max_value=500, value=80, step=5)
        chambres = st.number_input("🛏️ Chambres", min_value=1, max_value=8, value=2)
    with c2:
        sdb = st.number_input("🚿 Salles de bain", min_value=1, max_value=5, value=1)
        etage = st.number_input("🏢 Étage", min_value=0, max_value=20, value=1)
        ville = st.selectbox(
            "📍 Ville",
            sorted(df["ville"].dropna().unique())
        )

    st.markdown("<span style='color:#0f1923;font-size:0.9rem'>🏪 Type vendeur</span>", unsafe_allow_html=True)
    type_vendeur = st.radio(
        "",
        ["Particulier", "Agence"],
        label_visibility="collapsed"
    )

    st.markdown("<br>", unsafe_allow_html=True)

    if not model_ok:
        st.warning(f"⚠️ Modèle non disponible : `{model_err}`")
    else:
        predict_btn = st.button("🔮 Estimer le prix", type="primary", use_container_width=True)

    # ── Tips ──
    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("💡 Comment utiliser la prédiction ?"):
        st.markdown("""
        - Renseignez les caractéristiques du bien que vous souhaitez estimer
        - Le modèle analyse des milliers d'annonces similaires
        - Le prix estimé est une **fourchette indicative** — les finitions, l'état général et la localisation précise peuvent faire varier le prix réel
        - Consultez les annonces similaires pour valider l'estimation
        """)

# ── Résultats ─────────────────────────────────────────────────────────────────
with right_col:
    st.markdown("#### <span style='color:#0f1923'>📊 Résultat de l'estimation</span>", unsafe_allow_html=True)

    if model_ok and "predict_btn" in dir() and predict_btn:
        try:
            ville_median = df[df["ville"] == ville]["prix"].median()
            if pd.isna(ville_median):
                ville_median = df["prix"].median()

            est_agence = 1 if type_vendeur == "Agence" else 0
            surface_log = np.log1p(surface)
            total_pieces = chambres + sdb
            ratio_chambres_surface = chambres / surface

            ville_map = df.groupby("ville")["prix"].median().to_dict()
            ville_encoded = ville_map.get(ville, df["prix"].median())

            input_data = {
                "surface": surface,
                "surface_log": surface_log,
                "chambres": chambres,
                "salles_de_bain": sdb,
                "etage": etage,
                "total_pieces": total_pieces,
                "ratio_chambres_surface": ratio_chambres_surface,
                "est_agence": est_agence,
                "ville_encoded": ville_encoded,
                "prix_median_ville": ville_median,
            }

            X = pd.DataFrame([input_data])[features]
            prediction = model.predict(X)[0]
            prix_m2 = prediction / surface

            st.markdown(f"""
            <div class="result-price">
              <div class="price-label">Prix estimé</div>
              <div class="price-value">{prediction:,.0f}</div>
              <div class="price-unit">Dirhams Marocains (DH)</div>
            </div>
            """, unsafe_allow_html=True)

            col_m1, col_m2 = st.columns(2)
            with col_m1:
                st.markdown(f"""
                <div class="result-m2">
                  <div class="m2-label">Prix au m²</div>
                  <div class="m2-value">{prix_m2:,.0f} DH/m²</div>
                </div>
                """, unsafe_allow_html=True)
            with col_m2:
                st.markdown(f"""
                <div class="result-m2">
                  <div class="m2-label">Surface analysée</div>
                  <div class="m2-value">{surface} m²</div>
                </div>
                """, unsafe_allow_html=True)

            similaires = df[
                df["surface"].between(surface - 15, surface + 15)
                & (df["chambres"] == chambres)
                & (df["salles_de_bain"] == sdb)
            ].copy()

            if len(similaires) > 0:
                similaires["écart"] = (similaires["prix"] - prediction).abs()
                similaires = similaires.sort_values("écart").head(8)

                st.markdown("---")
                section(f"🏘️ Annonces similaires — {len(similaires)} trouvées")

                fig_sim = px.scatter(
                    similaires,
                    x="surface", y="prix",
                    hover_data=["localisation"],
                    color_discrete_sequence=["#1a3a5c"],
                    labels={"surface": "Surface (m²)", "prix": "Prix (DH)"},
                )
                fig_sim.add_hline(
                    y=prediction,
                    line_dash="dot",
                    line_color="#d4af37",
                    annotation_text=f"Estimation : {prediction:,.0f} DH",
                    annotation_font_color="#d4af37",
                )
                fig_sim.update_layout(**PLOTLY_THEME, height=220)
                fig_sim.update_layout(margin=dict(t=30, b=10, l=0, r=0))
                st.plotly_chart(fig_sim, use_container_width=True, config={"displayModeBar": False})

                cols_affichees = [c for c in ["titre", "prix", "surface", "chambres", "localisation"] if c in similaires.columns]
                st.dataframe(similaires[cols_affichees], use_container_width=True, hide_index=True)
            else:
                st.info("Aucune annonce similaire trouvée dans la base de données.")

        except Exception as e:
            st.error(f"❌ Erreur lors de la prédiction : {e}")

    else:
        st.markdown("""
        <div style="background:#ffffff;border-radius:16px;padding:3rem 2rem;text-align:center;border:2px dashed #dde4ee;color:#8a9ab0">
          <div style="font-size:3rem;margin-bottom:1rem">🏠</div>
          <div style="font-size:1rem;font-weight:500;color:#4a5568;margin-bottom:0.5rem">
            Renseignez les caractéristiques à gauche
          </div>
          <div style="font-size:0.85rem">
            L'estimation apparaîtra ici avec les annonces comparables
          </div>
        </div>
        """, unsafe_allow_html=True)

footer()
