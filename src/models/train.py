import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

df = pd.read_csv("data/processed/clean_data.csv")
df["ville"] = df["localisation"].str.split(",").str[0].str.strip()

df["surface_log"] = np.log1p(df["surface"])
df["total_pieces"] = df["chambres"] + df["salles_de_bain"]
df["ratio_chambres_surface"] = df["chambres"] / df["surface"]
df["est_agence"] = (df["type_vendeur"] == "STORE").astype(int)
ville_median = df.groupby("ville")["prix"].median()
df["ville_encoded"] = df["ville"].map(ville_median)
df["prix_median_ville"] = df["ville_encoded"]

features = ["surface", "surface_log", "chambres", "salles_de_bain", "etage",
            "total_pieces", "ratio_chambres_surface", "est_agence",
            "ville_encoded", "prix_median_ville"]

X = df[features]
y = df["prix"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestRegressor(n_estimators=300, max_depth=15, random_state=42)
model.fit(X_train, y_train)

joblib.dump(model, "models/model_prix_v2.pkl")
joblib.dump(features, "models/features_v2.pkl")
print("Modele sauvegarde.")