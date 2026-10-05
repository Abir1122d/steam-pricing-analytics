import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

os.makedirs(r"C:\Users\joysa\Documents\C\steam_app\diagrams", exist_ok=True)
OUT_DIR = r"C:\Users\joysa\Documents\C\steam_app\diagrams"

plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['font.family'] = 'sans-serif'

def create_system_architecture_diagram():
    fig, ax = plt.subplots(figsize=(10, 5), dpi=300)
    fig.patch.set_facecolor('#0f172a')
    ax.set_facecolor('#0f172a')

    ax.axis('off')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 50)

    def draw_box(x, y, w, h, title, subtitle, bg_color, border_color, text_color='#ffffff'):
        rect = patches.FancyBboxPatch(
            (x, y), w, h,
            boxstyle="round,pad=0.5,rounding_size=1.5",
            facecolor=bg_color,
            edgecolor=border_color,
            linewidth=1.5
        )
        ax.add_patch(rect)
        ax.text(x + w/2, y + h*0.62, title, color=text_color, weight='bold', fontsize=9.5, ha='center', va='center')
        ax.text(x + w/2, y + h*0.32, subtitle, color='#94a3b8', fontsize=7.5, ha='center', va='center')

    def draw_arrow(x1, y1, x2, y2, label=''):
        ax.annotate(
            '', xy=(x2, y2), xytext=(x1, y1),
            arrowprops=dict(facecolor='#6366f1', edgecolor='#6366f1', width=1.5, headwidth=6, headlength=6)
        )
        if label:
            ax.text((x1+x2)/2, (y1+y2)/2 + 1.5, label, color='#38bdf8', fontsize=7, ha='center', weight='bold')

    draw_box(2, 28, 18, 14, "Raw Steam Data", "126k+ Raw Catalog Records\nPrice, Reviews, CCU, Tags", "#1e293b", "#334155")
    draw_arrow(20.5, 35, 26.5, 35, "Filtering")

    draw_box(27, 28, 20, 14, "Feature Engineering", "Quality (0-100), Value (pts/$)\nLog Transforms, Multi-Hot Tags", "#1e293b", "#4f46e5")
    draw_arrow(47.5, 35, 53.5, 35, "Clean Matrix")

    draw_box(54, 28, 20, 14, "4 ML Model Trainers", "Ridge, Random Forest,\nK-Means, Calibrated Screener", "#1e293b", "#0284c7")
    draw_arrow(74.5, 35, 80.5, 35, "Serialization")

    draw_box(81, 28, 17, 14, "12 .pkl Artifacts", "Models, Scalers,\nEncoders, Feature Lists", "#312e81", "#6366f1")

    draw_arrow(89.5, 27.5, 89.5, 18, "Instant Load")

    draw_box(54, 4, 44, 14, "Streamlit Web App + Gemini Copilot (7 Tabs)", "Real-Time Sliders | Plotly Charts | 15 EDA Studies | Gemini AI Copilot", "#1e293b", "#10b981")

    draw_arrow(53.5, 11, 41.5, 11, "Empowers")

    draw_box(2, 4, 39, 14, "Strategic Decision Makers", "Indie Developers | AA Studios | Game Publishers | Analysts", "#1e293b", "#f59e0b")

    plt.tight_layout()
    path = os.path.join(OUT_DIR, "diagram1_sys_arch.png")
    plt.savefig(path, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
    plt.close()
    print(f"Saved: {path}")

def create_pkl_inference_pipeline_diagram():
    fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300)
    fig.patch.set_facecolor('#0f172a')
    ax.set_facecolor('#0f172a')

    ax.axis('off')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 60)

    def draw_box(x, y, w, h, title, subtitle, bg_color, border_color, text_color='#ffffff'):
        rect = patches.FancyBboxPatch(
            (x, y), w, h,
            boxstyle="round,pad=0.5,rounding_size=1.2",
            facecolor=bg_color,
            edgecolor=border_color,
            linewidth=1.2
        )
        ax.add_patch(rect)
        ax.text(x + w/2, y + h*0.62, title, color=text_color, weight='bold', fontsize=8.5, ha='center', va='center')
        ax.text(x + w/2, y + h*0.32, subtitle, color='#94a3b8', fontsize=7, ha='center', va='center')

    def draw_arrow(x1, y1, x2, y2, color='#6366f1'):
        ax.annotate(
            '', xy=(x2, y2), xytext=(x1, y1),
            arrowprops=dict(facecolor=color, edgecolor=color, width=1.2, headwidth=5, headlength=5)
        )

    draw_box(2, 22, 16, 16, "User UI Input", "Quality, CCU, Reviews,\nAge, Genres, Studio", "#1e293b", "#6366f1")

    draw_box(22, 22, 18, 16, "Feature Aligners", "reg_features.pkl\nclf_features.pkl\nover_features.pkl", "#1e1e38", "#818cf8")
    draw_arrow(18.5, 30, 21.5, 30)

    draw_box(44, 46, 15, 11, "scaler1.pkl", "StandardScaler (M1)\nMean & Variance", "#0f2b48", "#38bdf8")
    draw_arrow(40.5, 33, 43.5, 49)

    draw_box(63, 46, 17, 11, "model1_ridge.pkl", "Ridge Regression\nPredicts Fair Price", "#1e293b", "#38bdf8")
    draw_arrow(59.5, 51.5, 62.5, 51.5)

    draw_box(83, 46, 15, 11, "Fair Price ($)", "$28.87 USD\nValue: 2.8 pts/$", "#064e3b", "#10b981")
    draw_arrow(80.5, 51.5, 82.5, 51.5)

    draw_box(44, 32, 18, 11, "model2_rf_classifier.pkl", "RandomForest (150 trees)\nPredicts Tier Probs", "#1e293b", "#a855f7")
    draw_arrow(40.5, 30, 43.5, 37.5)

    draw_box(65, 32, 15, 11, "label_encoder.pkl", "Decodes Class Index\n0,1,2,3 -> Tier Name", "#2e1065", "#c084fc")
    draw_arrow(62.5, 37.5, 64.5, 37.5)

    draw_box(83, 32, 15, 11, "Predicted Tier", "Mid-range Tier\n(82% Confidence)", "#064e3b", "#10b981")
    draw_arrow(80.5, 37.5, 82.5, 37.5)

    draw_box(44, 18, 16, 11, "scaler3.pkl", "StandardScaler (M3)\n8 Cluster Dims", "#0f2b48", "#0284c7")
    draw_arrow(40.5, 27, 43.5, 23.5)

    draw_box(63, 18, 17, 11, "model3_kmeans.pkl", "KMeans (k=7, best_k.pkl)\nEuclidean Centroids", "#1e293b", "#0284c7")
    draw_arrow(60.5, 23.5, 62.5, 23.5)

    draw_box(83, 18, 15, 11, "Market Segment", "Archetype 2:\nStandard Mid-Tier", "#064e3b", "#10b981")
    draw_arrow(80.5, 23.5, 82.5, 23.5)

    draw_box(44, 4, 18, 11, "model4_gbm.pkl", "Calibrated RandomForest\nResidual Overprice Risk", "#1e293b", "#f43f5e")
    draw_arrow(40.5, 24, 43.5, 9.5)

    draw_box(65, 4, 15, 11, "Risk Estimator", "Predicts Probability\n0.0% to 100.0%", "#4c0519", "#fb7185")
    draw_arrow(62.5, 9.5, 64.5, 9.5)

    draw_box(83, 4, 15, 11, "Risk Verdict", "24.2% Risk\nCompetitive / Healthy", "#064e3b", "#10b981")
    draw_arrow(80.5, 9.5, 82.5, 9.5)

    plt.tight_layout()
    path = os.path.join(OUT_DIR, "diagram2_pkl_pipeline.png")
    plt.savefig(path, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
    plt.close()
    print(f"Saved: {path}")

def create_model_comparison_diagram():
    fig, ax = plt.subplots(figsize=(10, 4.5), dpi=300)
    fig.patch.set_facecolor('#0f172a')
    ax.set_facecolor('#0f172a')

    ax.axis('off')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 40)

    def draw_card(x, y, w, h, model_num, title, alg, goal, metric, color_border, color_badge):
        rect = patches.FancyBboxPatch(
            (x, y), w, h,
            boxstyle="round,pad=0.5,rounding_size=1.2",
            facecolor="#1e293b",
            edgecolor=color_border,
            linewidth=1.5
        )
        ax.add_patch(rect)

        badge = patches.FancyBboxPatch(
            (x+2, y+h-7), 19, 5,
            boxstyle="round,pad=0.2,rounding_size=0.8",
            facecolor=color_badge,
            edgecolor='none'
        )
        ax.add_patch(badge)
        ax.text(x+11.5, y+h-4.5, model_num, color='#ffffff', weight='bold', fontsize=7.5, ha='center', va='center')

        ax.text(x+w/2, y+h-9.5, title, color='#ffffff', weight='bold', fontsize=8.5, ha='center')
        ax.text(x+w/2, y+h-14.5, f"Algorithm: {alg}", color='#38bdf8', fontsize=7, ha='center')
        ax.text(x+w/2, y+h-20, goal, color='#94a3b8', fontsize=6.8, ha='center')
        ax.text(x+w/2, y+4.5, f"Key Metric: {metric}", color='#10b981', weight='bold', fontsize=7.2, ha='center')

    draw_card(2, 2, 22.5, 36, "MODEL 1", "Price-Value Predictor", "Ridge Regression", "Predicts continuous fair\nbenchmark retail price in USD\nand consumer value score.", "R² = 0.316 | MAE: $5.31", "#6366f1", "#4f46e5")
    draw_card(26.5, 2, 22.5, 36, "MODEL 2", "Price Tier Classifier", "Random Forest (150t)", "Predicts discrete market\ntier (Budget, Mid, Premium, AAA)\nwith probability breakdown.", "Accuracy: 74.8% | F1: 0.72", "#a855f7", "#9333ea")
    draw_card(51, 2, 22.5, 36, "MODEL 3", "Market Segmentation", "K-Means (k=7)", "Discovers 7 natural market\narchetypes across multi-scale\ncommercial dimensions.", "Silhouette: 0.28 | k=7", "#0284c7", "#0369a1")
    draw_card(75.5, 2, 22.5, 36, "MODEL 4", "Overpriced Screener", "Calibrated Classifier", "Screens commercial pricing\nrisk relative to fair residual\nbenchmark baseline.", "Accuracy: 78.4% | AUC: 0.81", "#f43f5e", "#e11d48")

    plt.tight_layout()
    path = os.path.join(OUT_DIR, "diagram3_models_overview.png")
    plt.savefig(path, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
    plt.close()
    print(f"Saved: {path}")

if __name__ == "__main__":
    create_system_architecture_diagram()
    create_pkl_inference_pipeline_diagram()
    create_model_comparison_diagram()
