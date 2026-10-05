import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import joblib
import os

st.set_page_config(
    page_title="Steam Video Game Pricing & Market Analytics",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    * { font-family: 'Plus Jakarta Sans', sans-serif; }
    .main { background: #0b0f19; color: #f1f5f9; }
    .stApp { background: #0b0f19; }

    section[data-testid="stSidebar"] {
        background-color: #0f172a !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08);
    }
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #ffffff !important;
    }
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] label {
        color: #cbd5e1 !important;
    }

    h1, h2, h3 {
        color: #ffffff !important;
        font-weight: 700 !important;
        letter-spacing: -0.02em !important;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: rgba(15, 23, 42, 0.6);
        padding: 6px;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        color: #94a3b8 !important;
        font-weight: 600;
        padding: 8px 16px;
    }

    .stTabs [aria-selected="true"] {
        background-color: #6366f1 !important;
        color: #ffffff !important;
    }

    .metric-card {
        background: linear-gradient(135deg, rgba(30,41,59,0.85), rgba(15,23,42,0.95));
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 10px 25px -5px rgba(0,0,0,0.4);
        backdrop-filter: blur(10px);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-3px);
        border-color: rgba(99,102,241,0.45);
    }
    .metric-title {
        color: #94a3b8;
        font-size: 0.82rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 6px;
    }
    .metric-value {
        color: #ffffff;
        font-size: 1.9rem;
        font-weight: 800;
        letter-spacing: -0.02em;
    }
    .metric-subtitle {
        color: #64748b;
        font-size: 0.78rem;
        margin-top: 4px;
    }

    .badge-budget { background: #059669; color: white; padding: 4px 12px; border-radius: 9999px; font-weight: 600; font-size: 0.85rem; }
    .badge-mid-range { background: #2563eb; color: white; padding: 4px 12px; border-radius: 9999px; font-weight: 600; font-size: 0.85rem; }
    .badge-premium { background: #7c3aed; color: white; padding: 4px 12px; border-radius: 9999px; font-weight: 600; font-size: 0.85rem; }
    .badge-aaa { background: #db2777; color: white; padding: 4px 12px; border-radius: 9999px; font-weight: 600; font-size: 0.85rem; }

    .status-fair { background: rgba(16,185,129,0.15); border: 1px solid #10b981; color: #34d399; padding: 14px 20px; border-radius: 12px; font-weight: 700; font-size: 1.15rem; text-align: center; }
    .status-over { background: rgba(239,68,68,0.15); border: 1px solid #ef4444; color: #f87171; padding: 14px 20px; border-radius: 12px; font-weight: 700; font-size: 1.15rem; text-align: center; }

    .question-box {
        background: linear-gradient(135deg, rgba(30,41,59,0.92), rgba(15,23,42,0.98));
        border: 1px solid rgba(255,255,255,0.1);
        border-left: 5px solid #6366f1;
        padding: 18px 22px;
        border-radius: 0 14px 14px 0;
        margin-bottom: 20px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.3);
    }
    .question-box h4 {
        color: #38bdf8 !important;
        font-size: 1.15rem !important;
        font-weight: 700 !important;
        margin-top: 0 !important;
        margin-bottom: 12px !important;
        letter-spacing: -0.01em;
    }
    .question-box p {
        color: #e2e8f0 !important;
        font-size: 0.95rem !important;
        line-height: 1.6 !important;
        margin-bottom: 8px !important;
    }
    .question-box b {
        color: #ffffff !important;
        font-weight: 700 !important;
    }
</style>
""", unsafe_allow_html=True)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHART_DIR = os.path.join(BASE_DIR, "q_charts")

@st.cache_data
def load_data():
    return pd.read_csv(os.path.join(BASE_DIR, "steam_games_modelling.csv"))

def load_models():
    m1 = joblib.load(os.path.join(BASE_DIR, "model1_ridge.pkl"))
    scaler1 = joblib.load(os.path.join(BASE_DIR, "scaler1.pkl"))
    reg_features = joblib.load(os.path.join(BASE_DIR, "reg_features.pkl"))

    m2 = joblib.load(os.path.join(BASE_DIR, "model2_rf_classifier.pkl"))
    clf_features = joblib.load(os.path.join(BASE_DIR, "clf_features.pkl"))
    le = joblib.load(os.path.join(BASE_DIR, "label_encoder.pkl"))

    m3 = joblib.load(os.path.join(BASE_DIR, "model3_kmeans.pkl"))
    scaler3 = joblib.load(os.path.join(BASE_DIR, "scaler3.pkl"))
    cluster_features = joblib.load(os.path.join(BASE_DIR, "cluster_features.pkl"))

    m4 = joblib.load(os.path.join(BASE_DIR, "model4_gbm.pkl"))
    over_features = joblib.load(os.path.join(BASE_DIR, "over_features.pkl"))

    return {
        "m1": m1, "scaler1": scaler1, "reg_features": reg_features,
        "m2": m2, "clf_features": clf_features, "le": le,
        "m3": m3, "scaler3": scaler3, "cluster_features": cluster_features,
        "m4": m4, "over_features": over_features
    }

df = load_data()
models = load_models()

with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/8/83/Steam_icon_logo.svg", width=50)
    st.title("Steam Pricing Lab")
    st.caption("Commercial Video Game Pricing Intelligence")

    st.markdown("---")
    st.subheader("Global Catalog Filter")

    selected_tier = st.multiselect(
        "Price Tier",
        options=["Budget", "Mid-range", "Premium", "AAA"],
        default=["Budget", "Mid-range", "Premium", "AAA"]
    )

    price_range = st.slider(
        "Price Range ($ USD)",
        min_value=float(df["price_usd"].min()),
        max_value=float(df["price_usd"].max()),
        value=(0.99, 79.99)
    )

    is_indie_filter = st.selectbox(
        "Studio Classification",
        options=["All Games", "Indie Titles Only", "Non-Indie (Major Studios)"]
    )

    st.markdown("---")
    st.markdown("### Model Suite")
    st.markdown("• **Model 1**: Value Score Predictor *(Ridge)*")
    st.markdown("• **Model 2**: Price Tier Classifier *(Random Forest)*")
    st.markdown("• **Model 3**: Market Segmentation *(K-Means)*")
    st.markdown("• **Model 4**: Overpriced Screener *(Calibrated Classifier)*")

filtered_df = df[
    (df["price_tier_clean"].isin(selected_tier)) &
    (df["price_usd"] >= price_range[0]) &
    (df["price_usd"] <= price_range[1])
]

if is_indie_filter == "Indie Titles Only":
    filtered_df = filtered_df[filtered_df["is_indie"] == 1]
elif is_indie_filter == "Non-Indie (Major Studios)":
    filtered_df = filtered_df[filtered_df["is_indie"] == 0]

tab_eda, tab_overview, tab_m12, tab_m3, tab_m4, tab_data = st.tabs([
    "📊 Complete EDA (15 Questions)",
    "📈 Market Overview",
    "🎯 Model 1 & 2: Pricing & Tiers",
    "🧩 Model 3: Market Segments",
    "⚖️ Model 4: Overpriced Screener",
    "📁 Catalog Data Explorer"
])

with tab_eda:
    st.markdown("## Exploratory Data Analysis: 15 Core Questions")
    st.caption("Comprehensive analysis from the EDA Notebook covering 126,000+ Steam titles")

    eda_sections = [
        "All 15 Questions",
        "Section 1: Pricing & Value Patterns (Q1 - Q4)",
        "Section 2: Popularity & Engagement Patterns (Q5 - Q8)",
        "Section 3: Quality vs Business Outcomes (Q9 - Q11)",
        "Section 4: Platform & Accessibility (Q12 - Q13)",
        "Section 5: Correlation Matrix & Summary Tables (Q14 - Q15)"
    ]

    selected_section = st.selectbox("Navigate EDA Section:", eda_sections)

    if selected_section in ["All 15 Questions", "Section 1: Pricing & Value Patterns (Q1 - Q4)"]:
        st.markdown("### Section 1: Pricing & Value Patterns")

        q1_c1, q1_c2 = st.columns([1.2, 1])
        with q1_c1:
            st.image(os.path.join(CHART_DIR, "q1_pricing.png"), use_container_width=True)
        with q1_c2:
            st.markdown("""
            <div class="question-box">
                <h4>Q1: Which genres have the highest and lowest average prices?</h4>
                <p><b>Finding:</b> Massively Multiplayer ($14.07 avg) and RPGs ($11.95 avg) command the highest price tags on Steam, driven by expansive content scope and production budgets. Casual ($4.87) and Indie ($6.25) games are the most affordable.</p>
                <p><b>Key Takeaway:</b> Heavy median skew across every genre proves the bulk of Steam titles are entry-priced budget releases ($3.99 - $9.99).</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        q2_c1, q2_c2 = st.columns([1.2, 1])
        with q2_c1:
            st.image(os.path.join(CHART_DIR, "q2_price_vs_quality.png"), use_container_width=True)
        with q2_c2:
            st.markdown("""
            <div class="question-box">
                <h4>Q2: Does game price correlate with quality score?</h4>
                <p><b>Finding:</b> Statistical correlation between price and review rating is virtually <b>0.00</b>. Expensive games ($40 - $70) do not reliably score higher than $5 indie titles.</p>
                <p><b>Key Takeaway:</b> Player satisfaction on Steam is driven by fun, polish, and gameplay loops rather than development budget.</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        q3_c1, q3_c2 = st.columns([1.2, 1])
        with q3_c1:
            st.image(os.path.join(CHART_DIR, "q3_value_by_genre.png"), use_container_width=True)
        with q3_c2:
            st.markdown("""
            <div class="question-box">
                <h4>Q3: Which genres deliver the highest value per dollar?</h4>
                <p><b>Finding:</b> Casual (21.4 pts/$) and Indie (15.8 pts/$) offer the best quality-per-dollar ratio on the platform.</p>
                <p><b>Key Takeaway:</b> High-budget genres (MMO, RPG) have lower value scores per dollar due to higher baseline price points.</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        q4_c1, q4_c2 = st.columns([1.2, 1])
        with q4_c1:
            st.image(os.path.join(CHART_DIR, "q4_price_trends.png"), use_container_width=True)
        with q4_c2:
            st.markdown("""
            <div class="question-box">
                <h4>Q4: How have average game prices trended by release year?</h4>
                <p><b>Finding:</b> The golden era of PC gaming (2000-2012) had high average prices ($15 - $22) due to curated retail pricing. Following Steam Greenlight and Direct, the influx of indie games reduced the platform median price to ~$4.99.</p>
                <p><b>Key Takeaway:</b> Commercial democratization lowered median price while total catalog volume expanded by over 2,000%.</p>
            </div>
            """, unsafe_allow_html=True)

    if selected_section in ["All 15 Questions", "Section 2: Popularity & Engagement Patterns (Q5 - Q8)"]:
        st.markdown("### Section 2: Popularity & Engagement Patterns")

        q5_c1, q5_c2 = st.columns([1.2, 1])
        with q5_c1:
            st.image(os.path.join(CHART_DIR, "q5_ownership_dilution.png"), use_container_width=True)
        with q5_c2:
            st.markdown("""
            <div class="question-box">
                <h4>Q5: Which genres have highest owners and how has dilution evolved?</h4>
                <p><b>Finding:</b> Action and RPGs historically led ownership volumes. However, average owners per game have dropped sharply across all genres as catalog supply outpaced player base growth.</p>
                <p><b>Key Takeaway:</b> Standing out requires targeted marketing and strong community engagement rather than relying on store browsing.</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        q6_c1, q6_c2 = st.columns([1.2, 1])
        with q6_c1:
            st.image(os.path.join(CHART_DIR, "q6_platforms.png"), use_container_width=True)
        with q6_c2:
            st.markdown("""
            <div class="question-box">
                <h4>Q6: Does cross-platform OS support increase ownership?</h4>
                <p><b>Finding:</b> Titles supporting Windows + Mac + Linux achieve significantly higher average player ownership compared to Windows-only releases.</p>
                <p><b>Key Takeaway:</b> Supporting multiple operating systems expands total addressable market and correlates with professional development standards.</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        q7_c1, q7_c2 = st.columns([1.2, 1])
        with q7_c1:
            st.image(os.path.join(CHART_DIR, "q7_retention.png"), use_container_width=True)
        with q7_c2:
            st.markdown("""
            <div class="question-box">
                <h4>Q7: How does long-term player retention differ by genre?</h4>
                <p><b>Finding:</b> Strategy and Simulation games lead in 2-week active playtime retention, while story-driven Adventure titles see sharp post-launch drop-offs.</p>
                <p><b>Key Takeaway:</b> Systems-driven gameplay and procedural generation drive multi-year player engagement.</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        q8_c1, q8_c2 = st.columns([1.2, 1])
        with q8_c1:
            st.image(os.path.join(CHART_DIR, "q8_indie_vs_non_indie.png"), use_container_width=True)
        with q8_c2:
            st.markdown("""
            <div class="question-box">
                <h4>Q8: How do Indie titles compare to Major Studio games in price and rating?</h4>
                <p><b>Finding:</b> Indie titles average $6.25 vs $14.80 for non-indie, yet achieve comparable or superior average review satisfaction rates (77.4% vs 75.1%).</p>
                <p><b>Key Takeaway:</b> Indie developers outperform on player sentiment and value satisfaction despite operating on smaller budgets.</p>
            </div>
            """, unsafe_allow_html=True)

    if selected_section in ["All 15 Questions", "Section 3: Quality vs Business Outcomes (Q9 - Q11)"]:
        st.markdown("### Section 3: Quality vs Business Outcomes")

        q9_c1, q9_c2 = st.columns([1.2, 1])
        with q9_c1:
            st.image(os.path.join(CHART_DIR, "q9_drivers.png"), use_container_width=True)
        with q9_c2:
            st.markdown("""
            <div class="question-box">
                <h4>Q9: Does review quality or player count better predict ownership?</h4>
                <p><b>Finding:</b> Peak concurrent users (CCU) and recommendation volume are 5x stronger predictors of commercial success than raw review percentage.</p>
                <p><b>Key Takeaway:</b> Network effects, virality, and streaming presence drive commercial scale more than critical rating alone.</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        q10_c1, q10_c2 = st.columns([1.2, 1])
        with q10_c1:
            st.image(os.path.join(CHART_DIR, "q10_price_tiers.png"), use_container_width=True)
        with q10_c2:
            st.markdown("""
            <div class="question-box">
                <h4>Q10: Which price tier has the highest average review ratings?</h4>
                <p><b>Finding:</b> Mid-range ($10-$30) and Premium ($30-$60) games achieve the highest median positive review percentages (~82%), while budget games under $5 suffer higher review dispersion.</p>
                <p><b>Key Takeaway:</b> Players evaluate games relative to their price expectations.</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        q11_c1, q11_c2 = st.columns([1.2, 1])
        with q11_c1:
            st.image(os.path.join(CHART_DIR, "q11_sweet_spot.png"), use_container_width=True)
        with q11_c2:
            st.markdown("""
            <div class="question-box">
                <h4>Q11: Where is the commercial 'sweet spot' for pricing?</h4>
                <p><b>Finding:</b> The $9.99 to $19.99 window provides the optimal balance of perceived quality, consumer willingness-to-pay, and high value scores.</p>
                <p><b>Key Takeaway:</b> Games in this bracket maximize gross revenue while retaining strong positive sentiment.</p>
            </div>
            """, unsafe_allow_html=True)

    if selected_section in ["All 15 Questions", "Section 4: Platform & Accessibility (Q12 - Q13)"]:
        st.markdown("### Section 4: Platform & Accessibility")

        q12_c1, q12_c2 = st.columns([1.2, 1])
        with q12_c1:
            st.image(os.path.join(CHART_DIR, "q12_languages.png"), use_container_width=True)
        with q12_c2:
            st.markdown("""
            <div class="question-box">
                <h4>Q12: Does multi-language localization increase player reach?</h4>
                <p><b>Finding:</b> Titles localized into 5+ languages (specifically Simplified Chinese, German, Russian, Japanese, Spanish) achieve 3.8x higher median ownership.</p>
                <p><b>Key Takeaway:</b> Localization is one of the highest ROI investments for indie developers looking to scale globally.</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        q13_c1, q13_c2 = st.columns([1.2, 1])
        with q13_c1:
            st.image(os.path.join(CHART_DIR, "q13_os_support.png"), use_container_width=True)
        with q13_c2:
            st.markdown("""
            <div class="question-box">
                <h4>Q13: What is the impact of Linux & macOS platform support?</h4>
                <p><b>Finding:</b> Cross-platform games have higher average ratings (79.2% vs 74.8%) and 2.4x higher player retention.</p>
                <p><b>Key Takeaway:</b> Cross-platform releases signal technical maturity and developer support.</p>
            </div>
            """, unsafe_allow_html=True)

    if selected_section in ["All 15 Questions", "Section 5: Correlation Matrix & Summary Tables (Q14 - Q15)"]:
        st.markdown("### Section 5: Matrix & Multi-Metric Synthesis")

        q14_c1, q14_c2 = st.columns([1.2, 1])
        with q14_c1:
            st.image(os.path.join(CHART_DIR, "q14_heatmap.png"), use_container_width=True)
        with q14_c2:
            st.markdown("""
            <div class="question-box">
                <h4>Q14: Correlation Heatmap Across Features</h4>
                <p><b>Finding:</b> High correlation between total reviews, peak CCU, and ownership. Very low correlation between price and review ratings.</p>
                <p><b>Key Takeaway:</b> Features are well-conditioned for machine learning models with no extreme collinearity bottlenecks.</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        st.image(os.path.join(CHART_DIR, "q15_genre_matrix.png"), use_container_width=True)
        st.markdown("""
        <div class="question-box">
            <h4>Q15: Multi-Metric Genre Comparison Matrix</h4>
            <p>Comprehensive overview of pricing, ownership, ratings, and value scores across all major genres on Steam.</p>
        </div>
        """, unsafe_allow_html=True)

with tab_overview:
    st.markdown("## Steam Market Overview & Telemetry")
    st.caption("Live statistical breakdown of the filtered dataset")

    if len(filtered_df) == 0:
        st.warning("No games match the current filter selection. Showing overall catalog statistics.")
        display_df = df
    else:
        display_df = filtered_df

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Catalog Size</div>
            <div class="metric-value">{len(display_df):,}</div>
            <div class="metric-subtitle">Active Commercial Titles</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Median Price</div>
            <div class="metric-value">${display_df['price_usd'].median():.2f}</div>
            <div class="metric-subtitle">Mean: ${display_df['price_usd'].mean():.2f}</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Average Quality</div>
            <div class="metric-value">{display_df['quality_score'].mean():.1f}/100</div>
            <div class="metric-subtitle">Player Sentiment Rating</div>
        </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Value Score</div>
            <div class="metric-value">{display_df['value_score_calc'].mean():.1f}</div>
            <div class="metric-subtitle">Quality Points / $1 Spent</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    with col_a:
        fig_price = px.histogram(
            display_df,
            x="price_usd",
            nbins=35,
            title="Price Distribution Across Catalog",
            color_discrete_sequence=["#6366f1"],
            template="plotly_dark"
        )
        fig_price.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(15,23,42,0.6)",
            font=dict(family="Plus Jakarta Sans", color="#94a3b8"),
            xaxis_title="Price ($ USD)",
            yaxis_title="Title Count"
        )
        st.plotly_chart(fig_price, use_container_width=True)

    with col_b:
        fig_val = px.scatter(
            display_df.sample(min(2000, len(display_df))),
            x="price_usd",
            y="quality_score",
            color="price_tier_clean",
            size="log_reviews",
            title="Price vs Quality Score (Bubble Size = Review Volume)",
            color_discrete_map={
                "Budget": "#059669",
                "Mid-range": "#2563eb",
                "Premium": "#7c3aed",
                "AAA": "#db2777"
            },
            template="plotly_dark"
        )
        fig_val.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(15,23,42,0.6)",
            font=dict(family="Plus Jakarta Sans", color="#94a3b8"),
            xaxis_title="Price ($ USD)",
            yaxis_title="Quality Score (% Positive)"
        )
        st.plotly_chart(fig_val, use_container_width=True)

with tab_m12:
    st.markdown("## Interactive Pricing & Tier Predictor")
    st.caption("Deploying **Model 1 (Ridge Regression)** for Value Prediction & **Model 2 (Random Forest)** for Tier Classification")

    col_in, col_out = st.columns([1.2, 1])

    with col_in:
        st.markdown("### Game Attributes Configuration")

        c_in1, c_in2 = st.columns(2)
        with c_in1:
            in_quality = st.slider("Expected Quality Score (0-100)", 10.0, 100.0, 80.0, 1.0)
            in_reviews = st.number_input("Estimated Review Volume", min_value=5, max_value=1000000, value=350)
            in_ccu = st.number_input("Peak Concurrent Players (CCU)", min_value=0, max_value=500000, value=65)
            in_age = st.slider("Years on Market", 0.0, 15.0, 1.0, 0.5)
            in_lang = st.slider("Supported Languages Count", 1, 30, 5)
            in_audio = st.slider("Full Audio Localization Count", 0, 15, 2)

        with c_in2:
            in_achieve = st.number_input("Total Achievements", min_value=0, max_value=1000, value=20)
            in_indie = st.checkbox("Indie Development Studio", value=True)
            in_single = st.checkbox("Single Player Support", value=True)
            in_multi = st.checkbox("Multiplayer Support", value=False)
            in_coop = st.checkbox("Co-op Campaign", value=False)

        selected_genre = st.selectbox(
            "Primary Game Genre Focus",
            ["Action", "Adventure", "Casual", "RPG", "Simulation", "Strategy"]
        )

    with col_out:
        st.markdown("### Prediction Results")

        feature_dict = {
            "quality_score": in_quality,
            "age_by_years": in_age,
            "log_reviews": np.log1p(in_reviews),
            "log_peak_ccu": np.log1p(in_ccu),
            "genre_count": 2,
            "languages_count": in_lang,
            "full_audio_languages_count": in_audio,
            "is_indie": 1 if in_indie else 0,
            "genre_action": 1 if selected_genre == "Action" else 0,
            "genre_casual": 1 if selected_genre == "Casual" else 0,
            "genre_adventure": 1 if selected_genre == "Adventure" else 0,
            "genre_rpg": 1 if selected_genre == "RPG" else 0,
            "genre_simulation": 1 if selected_genre == "Simulation" else 0,
            "genre_strategy": 1 if selected_genre == "Strategy" else 0,
            "cat_single_player": 1 if in_single else 0,
            "cat_multi_player": 1 if in_multi else 0,
            "cat_co_op": 1 if in_coop else 0,
            "cat_steam_achievements": 1 if in_achieve > 0 else 0,
            "achievements_count": in_achieve
        }

        input_df = pd.DataFrame([feature_dict])

        for col in models["reg_features"]:
            if col not in input_df.columns:
                input_df[col] = 0
        input_reg = input_df[models["reg_features"]]

        input_reg_scaled = models["scaler1"].transform(input_reg)
        pred_price = float(np.clip(models["m1"].predict(input_reg_scaled)[0], 0.99, 79.99))
        pred_value = in_quality / pred_price if pred_price > 0 else 0

        for col in models["clf_features"]:
            if col not in input_df.columns:
                input_df[col] = 0
        input_clf = input_df[models["clf_features"]]

        pred_tier_code = models["m2"].predict(input_clf)[0]
        pred_tier_label = models["le"].inverse_transform([pred_tier_code])[0]
        pred_tier_probs = models["m2"].predict_proba(input_clf)[0]

        st.markdown(f"""
        <div class="metric-card" style="margin-bottom: 16px;">
            <div class="metric-title">Model 1: Implied Fair Benchmark Price</div>
            <div class="metric-value" style="color: #6366f1;">${pred_price:.2f} USD</div>
            <div class="metric-subtitle">Predicted Value Score: {pred_value:.2f} pts/$</div>
        </div>
        """, unsafe_allow_html=True)

        badge_class = f"badge-{pred_tier_label.lower().replace('-','-').replace(' ','-')}"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Model 2: Predicted Price Tier</div>
            <div class="metric-value"><span class="{badge_class}">{pred_tier_label}</span></div>
            <div class="metric-subtitle">Classification Confidence: {np.max(pred_tier_probs)*100:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("#### Price Tier Probability Distribution")
        prob_df = pd.DataFrame({
            "Tier": models["le"].classes_,
            "Probability (%)": pred_tier_probs * 100
        })
        fig_prob = px.bar(
            prob_df,
            x="Tier",
            y="Probability (%)",
            color="Tier",
            color_discrete_map={
                "Budget": "#059669",
                "Mid-range": "#2563eb",
                "Premium": "#7c3aed",
                "AAA": "#db2777"
            },
            template="plotly_dark"
        )
        fig_prob.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(15,23,42,0.6)",
            font=dict(family="Plus Jakarta Sans", color="#94a3b8"),
            showlegend=False,
            height=200,
            margin=dict(l=20, r=20, t=20, b=20)
        )
        st.plotly_chart(fig_prob, use_container_width=True)

with tab_m3:
    st.markdown("## Market Archetypes & Segmentation")
    st.caption("Deploying **Model 3 (K-Means Clustering)** to discover natural game personas across Steam")

    target_df = filtered_df if len(filtered_df) > 0 else df
    if len(filtered_df) == 0:
        st.warning("No games match the current filter selection. Displaying clusters across the full catalog.")

    df_sample = target_df.sample(min(3000, len(target_df))).copy()

    c_cl1, c_cl2 = st.columns([1.5, 1])

    with c_cl1:
        X_cl_input = df_sample[models["cluster_features"]].fillna(0)
        X_cl_scaled = models["scaler3"].transform(X_cl_input)
        df_sample["cluster"] = models["m3"].predict(X_cl_scaled)

        cluster_names = {
            0: "Budget High-Value Indie",
            1: "Low-Review Casual",
            2: "Standard Mid-Tier",
            3: "Premium High-Engagement",
            4: "Ultra-Budget Bargain",
            5: "AAA / Flagship Blockbuster",
            6: "Cult Hit / Strong Retention"
        }
        df_sample["cluster_name"] = df_sample["cluster"].map(cluster_names)

        fig_cluster = px.scatter(
            df_sample,
            x="price_usd",
            y="quality_score",
            color="cluster_name",
            size="log_reviews",
            title="K-Means Market Cluster Distribution",
            hover_data=["name", "price_usd", "quality_score"],
            template="plotly_dark"
        )
        fig_cluster.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(15,23,42,0.6)",
            font=dict(family="Plus Jakarta Sans", color="#94a3b8"),
            xaxis_title="Price ($ USD)",
            yaxis_title="Quality Score",
            height=480
        )
        st.plotly_chart(fig_cluster, use_container_width=True)

    with c_cl2:
        st.markdown("### Cluster Characteristics")
        summary_table = df.groupby("price_tier_clean")[["price_usd", "quality_score", "value_score_calc"]].mean().round(2)
        st.dataframe(summary_table, use_container_width=True)

        st.markdown("#### Strategic Positioning")
        st.markdown("""
        - **Budget High-Value Indie**: Maximum player goodwill, great for studio launch.
        - **Premium High-Engagement**: High price with deep systems (Strategy, Simulation, RPG).
        - **Flagship Blockbuster**: Highest production scale and marketing reach.
        """)

with tab_m4:
    st.markdown("## Commercial Pricing Health & Overpriced Screener")
    st.caption("Deploying **Model 4 (Calibrated Classifier)** to screen commercial pricing risk")

    c_aud1, c_aud2 = st.columns([1, 1])

    with c_aud1:
        st.markdown("### Title Pricing & Quality Parameters")
        aud_price = st.slider("Listed Price ($ USD)", 0.99, 79.99, 14.99, 0.50)
        aud_qual = st.slider("Player Review Quality Rating (0-100)", 10.0, 100.0, 75.0, 1.0)
        aud_rev = st.number_input("Total Steam Reviews", min_value=5, max_value=500000, value=300)
        aud_age = st.slider("Years on Market", 0.0, 15.0, 1.5, 0.5)
        aud_lang = st.slider("Supported Languages", 1, 25, 4)
        aud_indie = st.checkbox("Is Indie Title", value=True, key="aud_indie")
        aud_genre = st.selectbox("Game Genre", ["Action", "Adventure", "Casual", "RPG", "Simulation", "Strategy"], key="aud_genre")

        audit_dict = {
            "price_usd": aud_price,
            "quality_score": aud_qual,
            "log_reviews": np.log1p(aud_rev),
            "age_by_years": aud_age,
            "languages_count": aud_lang,
            "is_indie": 1 if aud_indie else 0,
            "genre_action": 1 if aud_genre == "Action" else 0,
            "genre_casual": 1 if aud_genre == "Casual" else 0,
            "cat_single_player": 1,
            "cat_multi_player": 0,
            "genre_rpg": 1 if aud_genre == "RPG" else 0,
            "genre_simulation": 1 if aud_genre == "Simulation" else 0
        }

    with c_aud2:
        st.markdown("### Risk Analysis Verdict")

        aud_df = pd.DataFrame([audit_dict])
        for col in models["over_features"]:
            if col not in aud_df.columns:
                aud_df[col] = 0
        aud_input = aud_df[models["over_features"]]

        over_prob = models["m4"].predict_proba(aud_input)[0][1]
        is_over = 1 if over_prob >= 0.50 else 0

        if is_over == 1:
            st.markdown(f"""
            <div class="status-over">
                ⚠️ OVERPRICING RISK DETECTED<br>
                <span style="font-size: 0.9rem; font-weight: 500;">Risk Probability: {over_prob*100:.1f}%</span>
            </div>
            """, unsafe_allow_html=True)
            st.warning("Recommendation: The listed price is significantly above comparable titles for this quality bracket. Consider a promotional discount or bundling.")
        else:
            st.markdown(f"""
            <div class="status-fair">
                ✅ FAIR VALUE PRICING<br>
                <span style="font-size: 0.9rem; font-weight: 500;">Risk Probability: {over_prob*100:.1f}%</span>
            </div>
            """, unsafe_allow_html=True)
            st.success("This title is competitively priced relative to its genre competitors and expected player sentiment.")

        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=over_prob * 100,
            title={'text': "Overpricing Risk Level (%)", 'font': {'size': 16, 'color': '#94a3b8'}},
            gauge={
                'axis': {'range': [None, 100], 'tickcolor': "#94a3b8"},
                'bar': {'color': "#ef4444" if is_over == 1 else "#10b981"},
                'steps': [
                    {'range': [0, 40], 'color': "rgba(16,185,129,0.2)"},
                    {'range': [40, 60], 'color': "rgba(245,158,11,0.2)"},
                    {'range': [60, 100], 'color': "rgba(239,68,68,0.2)"}
                ]
            }
        ))
        fig_gauge.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Plus Jakarta Sans", color="#ffffff"),
            height=270,
            margin=dict(l=20, r=20, t=30, b=20)
        )
        st.plotly_chart(fig_gauge, use_container_width=True)

with tab_data:
    st.markdown("## Searchable Steam Catalog Dataset")
    if len(filtered_df) == 0:
        st.warning("No games match the current filter selection. Displaying full catalog.")
        data_to_show = df
    else:
        data_to_show = filtered_df

    st.caption(f"Showing {len(data_to_show):,} titles")

    st.dataframe(
        data_to_show[[
            "name", "price_usd", "price_tier_clean", "quality_score",
            "value_score_calc", "total_review", "primary_genre", "is_indie"
        ]].sort_values(by="total_review", ascending=False).head(200),
        use_container_width=True
    )
