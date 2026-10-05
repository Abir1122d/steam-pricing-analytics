import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder

def load_and_engineer(path=r"C:\Users\joysa\Documents\C\steam_games_EDA_ready.csv"):
    df = pd.read_csv(path)

    df = df[df["price_status"] == "paid"].copy()
    df = df[df["total_review"] >= 5].copy()

    df["price_usd"] = np.expm1(df["price"])
    df = df[(df["price_usd"] >= 0.99) & (df["price_usd"] <= 79.99)].copy()

    df["is_indie"] = df["genres"].str.contains("Indie", na=False).astype(int)

    def get_quality(row):
        m = row["metacritic_score"]
        u = row["user_score"]
        if m > 0 and u > 0:
            return (m + u) / 2
        if m > 0:
            return m
        if u > 0:
            return u
        return row["review_score_pct"] * 100

    df["quality_score"] = df.apply(get_quality, axis=1)

    df["value_score_calc"] = np.where(
        df["price_usd"] > 0,
        df["quality_score"] / df["price_usd"],
        0
    )

    df["log_reviews"] = np.log1p(df["total_review"])
    df["log_peak_ccu"] = np.log1p(df["peak_ccu"])
    df["log_recommendations"] = np.log1p(df["recommendations"])

    top_genres = ["Action", "Adventure", "Casual", "RPG", "Simulation", "Strategy", "Sports", "Racing", "Indie"]
    for g in top_genres:
        df[f"genre_{g.lower()}"] = df["genres"].str.contains(g, na=False).astype(int)

    top_cats = ["Single-player", "Multi-player", "Co-op", "Steam Achievements", "Steam Cloud", "Family Sharing"]
    for c in top_cats:
        col = "cat_" + c.lower().replace("-", "_").replace(" ", "_")
        df[col] = df["categories"].str.contains(c, na=False).astype(int)

    def assign_tier(p):
        if p == 0:
            return "Free"
        if p < 10:
            return "Budget"
        if p < 30:
            return "Mid-range"
        if p < 60:
            return "Premium"
        return "AAA"

    df["price_tier_clean"] = df["price_usd"].apply(assign_tier)

    le = LabelEncoder()
    df["price_tier_encoded"] = le.fit_transform(df["price_tier_clean"])

    df = df.dropna(subset=["quality_score", "value_score_calc", "price_usd"])
    df = df[np.isfinite(df["value_score_calc"])].copy()
    df = df[df["value_score_calc"] > 0].copy()

    return df

if __name__ == "__main__":
    df = load_and_engineer()
    df.to_csv(r"C:\Users\joysa\Documents\C\steam_app\steam_games_modelling.csv", index=False)
    print("Rows saved:", len(df))
    print(df[["price_usd", "quality_score", "value_score_calc", "price_tier_clean", "is_indie"]].describe())
