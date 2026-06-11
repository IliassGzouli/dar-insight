import pandas as pd
import numpy as np
import joblib
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split

df = pd.read_csv("data/processed/clean_data.csv")
df["ville"] = df["localisation"].str.split(",").str[0].str.strip()

df["surface_log"] = np.log1p(df["surface"])
df["total_pieces"] = df["chambres"] + df["salles_de_bain"]
df["ratio_chambres_surface"] = df["chambres"] / df["surface"]
df["est_agence"] = (df["type_vendeur"] == "STORE").astype(int)
ville_median = df.groupby("ville")["prix"].median()
df["ville_encoded"] = df["ville"].map(ville_median)
df["prix_median_ville"] = df["ville_encoded"]

features = joblib.load("models/features_v2.pkl")
model = joblib.load("models/model_prix_v2.pkl")

X = df[features]
y = df["prix"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

y_pred = model.predict(X_test)
print("MAE:", round(mean_absolute_error(y_test, y_pred), 0), "DH")
print("R2 Score:", round(r2_score(y_test, y_pred), 3))