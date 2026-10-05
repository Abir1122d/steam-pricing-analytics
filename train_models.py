import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import Ridge
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.cluster import KMeans
import warnings
warnings.filterwarnings("ignore")

DATA = r"C:\Users\joysa\Documents\C\steam_app\steam_games_modelling.csv"
OUT = r"C:\Users\joysa\Documents\C\steam_app"

df = pd.read_csv(DATA)

REG_FEATURES = [
    "quality_score", "age_by_years", "log_reviews", "log_peak_ccu",
    "genre_count", "languages_count", "is_indie",
    "genre_action", "genre_casual", "genre_adventure", "genre_rpg",
    "genre_simulation", "genre_strategy",
    "cat_single_player", "cat_multi_player", "cat_co_op"
]
REG_FEATURES = [c for c in REG_FEATURES if c in df.columns]

CLF_FEATURES = REG_FEATURES.copy()

CLUSTER_FEATURES = [
    "price_usd", "quality_score", "log_reviews",
    "log_peak_ccu", "value_score_calc", "is_indie",
    "age_by_years", "languages_count"
]
CLUSTER_FEATURES = [c for c in CLUSTER_FEATURES if c in df.columns]

X_reg = df[REG_FEATURES]
y_reg = df["price_usd"]

le = LabelEncoder()
y_clf = le.fit_transform(df["price_tier_clean"])
joblib.dump(le, f"{OUT}/label_encoder.pkl")

X_clf = df[CLF_FEATURES]

X_tr, X_te, y_tr, y_te = train_test_split(X_reg, y_reg, test_size=0.2, random_state=42)
scaler1 = StandardScaler()
X_tr_s = scaler1.fit_transform(X_tr)
X_te_s = scaler1.transform(X_te)
m1 = Ridge(alpha=10.0)
m1.fit(X_tr_s, y_tr)
joblib.dump(m1, f"{OUT}/model1_ridge.pkl")
joblib.dump(scaler1, f"{OUT}/scaler1.pkl")
joblib.dump(REG_FEATURES, f"{OUT}/reg_features.pkl")

X_tr2, X_te2, y_tr2, y_te2 = train_test_split(X_clf, y_clf, test_size=0.2, random_state=42)
m2 = RandomForestClassifier(n_estimators=150, max_depth=12, random_state=42, n_jobs=-1)
m2.fit(X_tr2, y_tr2)
joblib.dump(m2, f"{OUT}/model2_rf_classifier.pkl")
joblib.dump(CLF_FEATURES, f"{OUT}/clf_features.pkl")

X_cl = df[CLUSTER_FEATURES].dropna()
scaler3 = StandardScaler()
X_cl_s = scaler3.fit_transform(X_cl)
m3 = KMeans(n_clusters=7, random_state=42, n_init=10)
m3.fit(X_cl_s)
joblib.dump(m3, f"{OUT}/model3_kmeans.pkl")
joblib.dump(scaler3, f"{OUT}/scaler3.pkl")
joblib.dump(CLUSTER_FEATURES, f"{OUT}/cluster_features.pkl")
joblib.dump(7, f"{OUT}/best_k.pkl")

fair_features = ['quality_score', 'log_reviews', 'age_by_years', 'languages_count', 'is_indie', 'genre_action', 'genre_rpg', 'cat_multi_player']
rf_fair = RandomForestRegressor(n_estimators=50, max_depth=8, random_state=42, n_jobs=-1)
rf_fair.fit(df[fair_features], df['price_usd'])
df['fair_price_pred'] = rf_fair.predict(df[fair_features])
df['is_overpriced'] = (df['price_usd'] > df['fair_price_pred'] * 1.35).astype(int)

OVER_FEATURES = [
    'price_usd', 'quality_score', 'log_reviews', 'age_by_years',
    'languages_count', 'is_indie', 'genre_action', 'genre_casual',
    'cat_single_player', 'cat_multi_player', 'genre_rpg', 'genre_simulation'
]
OVER_FEATURES = [c for c in OVER_FEATURES if c in df.columns]

X_ov = df[OVER_FEATURES]
y_ov = df["is_overpriced"]
X_tr4, X_te4, y_tr4, y_te4 = train_test_split(X_ov, y_ov, test_size=0.2, random_state=42)
m4 = RandomForestClassifier(n_estimators=150, max_depth=7, random_state=42, n_jobs=-1)
m4.fit(X_tr4, y_tr4)
joblib.dump(m4, f"{OUT}/model4_gbm.pkl")
joblib.dump(OVER_FEATURES, f"{OUT}/over_features.pkl")

df.to_csv(f"{OUT}/steam_games_modelling.csv", index=False)
