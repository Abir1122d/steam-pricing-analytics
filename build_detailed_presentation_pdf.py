import os
import reportlab
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image, HRFlowable, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

BASE_DIR = r"C:\Users\joysa\Documents\C\steam_app"
DIAG_DIR = os.path.join(BASE_DIR, "diagrams")

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        if self._pageNumber > 1:
            self.saveState()
            self.setFont("Helvetica-Bold", 8)
            self.setFillColor(colors.HexColor("#64748b"))
            self.drawString(54, 750, "STEAM PRICING & MARKET ANALYTICS | SYSTEM ARCHITECTURE & ML REPORT")
            self.setStrokeColor(colors.HexColor("#cbd5e1"))
            self.setLineWidth(0.5)
            self.line(54, 742, letter[0] - 54, 742)

            page_str = f"Page {self._pageNumber} of {page_count}"
            self.setFont("Helvetica", 8)
            self.drawRightString(letter[0] - 54, 36, page_str)
            self.drawString(54, 36, "CONFIDENTIAL & PROPRIETARY - DATA SCIENCE & MACHINE LEARNING PORTFOLIO")
            self.line(54, 48, letter[0] - 54, 48)
            self.restoreState()

def build_pdf(filename="Steam_Video_Game_Pricing_Detailed_Architecture_Presentation.pdf"):
    pdf_path = os.path.join(BASE_DIR, filename)
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    c_primary = colors.HexColor("#0f172a")
    c_accent = colors.HexColor("#4f46e5")
    c_secondary = colors.HexColor("#0284c7")
    c_dark = colors.HexColor("#1e293b")
    c_muted = colors.HexColor("#64748b")
    c_light = colors.HexColor("#f8fafc")

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=c_primary,
        spaceAfter=4
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=15,
        textColor=c_accent,
        spaceAfter=10
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=c_primary,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13.5,
        textColor=c_secondary,
        spaceBefore=7,
        spaceAfter=3,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.2,
        leading=11.8,
        textColor=c_dark,
        spaceAfter=4
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11.5,
        textColor=c_dark,
        leftIndent=10,
        spaceAfter=3
    )

    tbl_header_style = ParagraphStyle(
        'TblHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10.5,
        textColor=colors.white
    )

    tbl_cell_style = ParagraphStyle(
        'TblCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=10.5,
        textColor=c_dark
    )

    tbl_cell_bold = ParagraphStyle(
        'TblCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=10.5,
        textColor=c_primary
    )

    story = []

    story.append(Paragraph("Steam Video Game Pricing & Market Analytics", title_style))
    story.append(Paragraph("End-to-End Machine Learning System, .pkl Pipeline Deep-Dive & Interactive Platform", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_accent, spaceBefore=2, spaceAfter=8))

    meta_data = [
        [
            Paragraph("<b>Domain:</b> Commercial Video Game Econometrics", tbl_cell_style),
            Paragraph("<b>Dataset:</b> 57,506 Cleaned Steam Commercial Paid Games", tbl_cell_style)
        ],
        [
            Paragraph("<b>Tech Stack:</b> Python 3.10, Scikit-Learn, Streamlit, Plotly, Pandas, Joblib", tbl_cell_style),
            Paragraph("<b>ML Models:</b> 4 Models (Ridge, Random Forest, K-Means, Calibrated Screener)", tbl_cell_style)
        ],
        [
            Paragraph("<b>Artifacts:</b> 12 Serialized .pkl Files, 15 EDA Studies, 7-Tab Streamlit App", tbl_cell_style),
            Paragraph("<b>Status:</b> Production Verified, Zero-Comment Codebase Compliance", tbl_cell_style)
        ]
    ]
    t_meta = Table(meta_data, colWidths=[250, 254])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f1f5f9")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 6))

    story.append(Paragraph("1. Executive Summary & End-to-End System Architecture", h1_style))
    story.append(Paragraph(
        "The digital video game market on Valve's Steam platform is characterized by rapid supply expansion (over 126,000+ historical titles) and extreme price dispersion. Setting an optimal retail price is among the highest-leverage commercial decisions a game studio makes. This project develops an end-to-end data science and machine learning platform that cleans raw catalog data, engineers multi-scale signals, extracts 15 core empirical findings, trains 4 complementary machine learning models, serializes pipelines into 12 optimized .pkl artifacts, and serves real-time pricing intelligence via a modern Streamlit web application.",
        body_style
    ))
    story.append(Spacer(1, 4))

    diag1_path = os.path.join(DIAG_DIR, "diagram1_sys_arch.png")
    if os.path.exists(diag1_path):
        img1 = Image(diag1_path, width=504, height=210)
        story.append(img1)
        story.append(Spacer(1, 4))

    story.append(Paragraph("<b>End-to-End Engineering Lifecycle:</b>", h2_style))
    story.append(Paragraph("<b>Phase 1: Ingestion &amp; Quality Filtering</b> - Filtered 126k+ raw titles to 57,506 commercial paid releases ($0.99-$79.99, &gt;=5 reviews).", bullet_style))
    story.append(Paragraph("<b>Phase 2: Mathematical Feature Engineering</b> - Engineered continuous Quality Score (0-100), Value Score ($pts/$), log transformations, and multi-hot tags.", bullet_style))
    story.append(Paragraph("<b>Phase 3: 15 Core EDA Research Studies</b> - Answered 15 foundational commercial questions across pricing, quality, engagement, and platform factors.", bullet_style))
    story.append(Paragraph("<b>Phase 4: Multi-Model Machine Learning</b> - Trained 4 production pipelines and serialized models, scalers, and feature schemas into 12 .pkl files.", bullet_style))
    story.append(Paragraph("<b>Phase 5: Interactive Web Application</b> - Deployed a 6-tab glassmorphic dark Streamlit dashboard with sub-second real-time inference.", bullet_style))

    story.append(PageBreak())

    story.append(Paragraph("2. Data Ingestion & Advanced Feature Engineering Pipeline", h1_style))
    story.append(Paragraph(
        "To establish empirical reliability, raw Steam metadata underwent comprehensive filtering and mathematical transformations. Non-commercial entities (free-to-play demos, unpriced pre-releases, DLC packages, and unrated hobbyist uploads with &lt; 5 reviews) were filtered out to isolate genuine marketplace transactions.",
        body_style
    ))

    feat_table_data = [
        [
            Paragraph("Engineered Feature", tbl_header_style),
            Paragraph("Mathematical / Logical Formulation", tbl_header_style),
            Paragraph("Commercial &amp; Analytical Purpose", tbl_header_style)
        ],
        [
            Paragraph("<b>quality_score</b>", tbl_cell_bold),
            Paragraph("If Metacritic &amp; User Score exist: <i>(M + U)/2</i><br/>Else: available score or <i>review_score_pct * 100</i>", tbl_cell_style),
            Paragraph("Harmonizes critic authority and crowd-sourced user sentiment into a unified continuous 0-100 rating.", tbl_cell_style)
        ],
        [
            Paragraph("<b>value_score_calc</b>", tbl_cell_bold),
            Paragraph("<i>quality_score / price_usd</i>", tbl_cell_style),
            Paragraph("Quantifies consumer surplus: quality points delivered per single dollar of retail purchase price.", tbl_cell_style)
        ],
        [
            Paragraph("<b>log_reviews &amp; log_peak_ccu</b>", tbl_cell_bold),
            Paragraph("<i>log1p(total_reviews)</i>, <i>log1p(peak_ccu)</i>", tbl_cell_style),
            Paragraph("Compresses heavy right-tail power-law distributions to prevent mega-hits from distorting linear weights.", tbl_cell_style)
        ],
        [
            Paragraph("<b>price_tier_clean</b>", tbl_cell_bold),
            Paragraph("Budget: &lt;$10 | Mid-range: $10-30<br/>Premium: $30-60 | AAA: &gt;=$60", tbl_cell_style),
            Paragraph("Discretizes continuous retail pricing into standard industry consumer purchasing brackets.", tbl_cell_style)
        ],
        [
            Paragraph("<b>Multi-Hot Genre &amp; Category Flags</b>", tbl_cell_bold),
            Paragraph("Binary indicators: Action, RPG, Indie, Strategy, Simulation, Single-player, Multi-player, Co-op", tbl_cell_style),
            Paragraph("Allows tree-based and linear models to learn genre-specific pricing elasticity and feature interactions.", tbl_cell_style)
        ]
    ]

    t_feat = Table(feat_table_data, colWidths=[110, 200, 194])
    t_feat.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f8fafc")]),
        ('TOPPADDING', (0,0), (-1,-1), 4.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4.5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_feat)
    story.append(Spacer(1, 8))

    story.append(Paragraph("Cleaned Dataset Statistical Baseline (N = 57,506 Commercial Games)", h2_style))

    stats_table_data = [
        [
            Paragraph("Metric", tbl_header_style),
            Paragraph("Mean", tbl_header_style),
            Paragraph("Std Dev", tbl_header_style),
            Paragraph("Min", tbl_header_style),
            Paragraph("25%", tbl_header_style),
            Paragraph("Median", tbl_header_style),
            Paragraph("75%", tbl_header_style),
            Paragraph("Max", tbl_header_style)
        ],
        [Paragraph("Price ($ USD)", tbl_cell_bold), Paragraph("$9.74", tbl_cell_style), Paragraph("$9.88", tbl_cell_style), Paragraph("$0.99", tbl_cell_style), Paragraph("$2.99", tbl_cell_style), Paragraph("$6.99", tbl_cell_style), Paragraph("$12.99", tbl_cell_style), Paragraph("$79.99", tbl_cell_style)],
        [Paragraph("Quality Score (0-100)", tbl_cell_bold), Paragraph("76.80", tbl_cell_style), Paragraph("19.00", tbl_cell_style), Paragraph("3.57", tbl_cell_style), Paragraph("66.67", tbl_cell_style), Paragraph("80.56", tbl_cell_style), Paragraph("91.36", tbl_cell_style), Paragraph("100.0", tbl_cell_style)],
        [Paragraph("Value Score (pts/$)", tbl_cell_bold), Paragraph("18.58", tbl_cell_style), Paragraph("21.04", tbl_cell_style), Paragraph("0.14", tbl_cell_style), Paragraph("5.60", tbl_cell_style), Paragraph("10.43", tbl_cell_style), Paragraph("20.79", tbl_cell_style), Paragraph("101.0", tbl_cell_style)],
        [Paragraph("Age on Market (Yrs)", tbl_cell_bold), Paragraph("5.84", tbl_cell_style), Paragraph("3.43", tbl_cell_style), Paragraph("0.04", tbl_cell_style), Paragraph("2.95", tbl_cell_style), Paragraph("5.31", tbl_cell_style), Paragraph("8.27", tbl_cell_style), Paragraph("29.10", tbl_cell_style)],
        [Paragraph("Supported Languages", tbl_cell_bold), Paragraph("4.35", tbl_cell_style), Paragraph("4.78", tbl_cell_style), Paragraph("1.00", tbl_cell_style), Paragraph("1.00", tbl_cell_style), Paragraph("2.00", tbl_cell_style), Paragraph("6.00", tbl_cell_style), Paragraph("34.00", tbl_cell_style)]
    ]
    t_stats = Table(stats_table_data, colWidths=[120, 48, 54, 44, 48, 54, 48, 48])
    t_stats.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_dark),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f8fafc")]),
        ('ALIGN', (1,0), (-1,-1), 'CENTER'),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_stats)

    story.append(PageBreak())

    story.append(Paragraph("3. Exploratory Data Analysis - 15 Core Strategic Insights", h1_style))
    story.append(Paragraph(
        "A rigorous exploratory data analysis investigated 15 specific market questions across 5 commercial pillars, informing the mathematical feature design and downstream model selection.",
        body_style
    ))

    eda_summary_data = [
        [
            Paragraph("Dimension &amp; Questions", tbl_header_style),
            Paragraph("Core Statistical Finding &amp; Empirical Observation", tbl_header_style),
            Paragraph("Strategic Business Takeaway", tbl_header_style)
        ],
        [
            Paragraph("<b>Pillar 1: Pricing &amp; Value</b><br/><font size='7.5' color='#64748b'>Q1: Price by Genre<br/>Q2: Price vs Quality<br/>Q3: Value Score Ranking<br/>Q4: Free vs Paid Quality</font>", tbl_cell_style),
            Paragraph("- Massively Multiplayer ($14.07 avg) and RPGs ($11.95 avg) command highest prices; Casual ($4.87) is lowest.<br/>- Correlation between price and quality is virtually zero (<b>r = 0.00</b>).<br/>- Casual (21.4 pts/$) and Indie (15.8 pts/$) deliver peak consumer value scores.", tbl_cell_style),
            Paragraph("<b>Decoupled Price &amp; Quality:</b> Price reflects production scale and genre conventions rather than consumer satisfaction. Indie titles generate massive consumer surplus.", tbl_cell_style)
        ],
        [
            Paragraph("<b>Pillar 2: Popularity &amp; Retention</b><br/><font size='7.5' color='#64748b'>Q5: Peak CCU vs Price<br/>Q6: Reviews Distribution<br/>Q7: Catalog Dilution<br/>Q8: Multi-OS Ownership</font>", tbl_cell_style),
            Paragraph("- Annual Steam game releases grew &gt;1200% since 2014, causing median ownership per game to drop by &gt;70%.<br/>- Titles supporting Windows + Mac + Linux achieve significantly higher average player ownership than Windows-only releases.", tbl_cell_style),
            Paragraph("<b>Marketplace Saturation:</b> Discoverability is the primary bottleneck. Multi-platform OS support expands total addressable market with minimal porting friction.", tbl_cell_style)
        ],
        [
            Paragraph("<b>Pillar 3: Commercial Outcomes</b><br/><font size='7.5' color='#64748b'>Q9: Revenue by Price Tier<br/>Q10: Value vs Ownership<br/>Q11: Age Price Decay</font>", tbl_cell_style),
            Paragraph("- The $10-$30 Mid-range corridor accounts for the largest aggregate share of commercial Steam revenue.<br/>- Back-catalog titles experience steady price decay of ~5-8% annually through seasonal discount events.", tbl_cell_style),
            Paragraph("<b>The $14.99 Sweet Spot:</b> Mid-range pricing maximizes gross revenue by balancing unit conversion volume against per-copy revenue.", tbl_cell_style)
        ],
        [
            Paragraph("<b>Pillar 4: Platform &amp; Localization</b><br/><font size='7.5' color='#64748b'>Q12: Language Multiplier<br/>Q13: Audio vs Text Local</font>", tbl_cell_style),
            Paragraph("- Games with &gt;= 5 language localizations achieve 3.8x higher average ownership than English-only releases.<br/>- Full audio localization reinforces premium pricing perception ($30+).", tbl_cell_style),
            Paragraph("<b>Localization ROI:</b> Translating text for East Asian (Simplified Chinese, Japanese) and European markets provides the highest return per dollar spent.", tbl_cell_style)
        ],
        [
            Paragraph("<b>Pillar 5: Correlation Matrix</b><br/><font size='7.5' color='#64748b'>Q14: Feature Correlation<br/>Q15: Genre Clustering</font>", tbl_cell_style),
            Paragraph("- High collinearity between raw reviews and CCU confirmed the need for log transformations (<i>log_reviews</i>, <i>log_peak_ccu</i>).<br/>- Clean separation between systems-heavy and casual genres.", tbl_cell_style),
            Paragraph("<b>Feature Selection Guidance:</b> Guided subset selection for downstream regression, classification, and clustering models.", tbl_cell_style)
        ]
    ]

    t_eda = Table(eda_summary_data, colWidths=[110, 210, 184])
    t_eda.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f8fafc")]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_eda)

    story.append(PageBreak())

    story.append(Paragraph("4. The 4-Model Machine Learning Suite & Evaluation", h1_style))
    story.append(Paragraph(
        "To deliver multifaceted pricing intelligence, four distinct machine learning architectures were trained on 57,506 games, each addressing a unique commercial decision dimension.",
        body_style
    ))
    story.append(Spacer(1, 4))

    diag3_path = os.path.join(DIAG_DIR, "diagram3_models_overview.png")
    if os.path.exists(diag3_path):
        img3 = Image(diag3_path, width=504, height=180)
        story.append(img3)
        story.append(Spacer(1, 6))

    ml_table_data = [
        [
            Paragraph("Model &amp; Objective", tbl_header_style),
            Paragraph("Algorithm &amp; Pipeline", tbl_header_style),
            Paragraph("Evaluation Metrics", tbl_header_style),
            Paragraph("Operational Output in App", tbl_header_style)
        ],
        [
            Paragraph("<b>Model 1: Price Predictor</b><br/><font size='7' color='#64748b'>Continuous Regression</font>", tbl_cell_style),
            Paragraph("<b>Ridge Regression (L2)</b><br/>StandardScaler + 16 features", tbl_cell_style),
            Paragraph("- R<super>2</super>: 0.316<br/>- MAE: $5.31<br/>- RMSE: $8.17", tbl_cell_style),
            Paragraph("Implied benchmark retail price ($ USD) &amp; expected value score ($pts/$).", tbl_cell_style)
        ],
        [
            Paragraph("<b>Model 2: Tier Classifier</b><br/><font size='7' color='#64748b'>Multiclass Classification</font>", tbl_cell_style),
            Paragraph("<b>Random Forest Classifier</b><br/>150 trees, max depth 12", tbl_cell_style),
            Paragraph("- Accuracy: 74.8%<br/>- Weighted F1: 0.72<br/>- Precision: 0.74", tbl_cell_style),
            Paragraph("Recommended price tier badge &amp; multiclass probability distribution.", tbl_cell_style)
        ],
        [
            Paragraph("<b>Model 3: Segmentation</b><br/><font size='7' color='#64748b'>Unsupervised Clustering</font>", tbl_cell_style),
            Paragraph("<b>K-Means Clustering</b><br/>k=7, 8 scaled dimensions", tbl_cell_style),
            Paragraph("- Silhouette: 0.28<br/>- Elbow Inertia Verified<br/>- 7 Archetypes", tbl_cell_style),
            Paragraph("2D market segment scatter plot &amp; archetype profile description.", tbl_cell_style)
        ],
        [
            Paragraph("<b>Model 4: Overprice Screener</b><br/><font size='7' color='#64748b'>Calibrated Classifier</font>", tbl_cell_style),
            Paragraph("<b>Calibrated Random Forest</b><br/>150 trees, residual threshold", tbl_cell_style),
            Paragraph("- Accuracy: 78.4%<br/>- ROC-AUC: 0.81<br/>- Recall: 76.2%", tbl_cell_style),
            Paragraph("Commercial risk probability (0-100%) &amp; dynamic color-coded gauge meter.", tbl_cell_style)
        ]
    ]

    t_ml = Table(ml_table_data, colWidths=[110, 130, 110, 154])
    t_ml.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f8fafc")]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_ml)
    story.append(Spacer(1, 6))

    story.append(Paragraph("Model 3: The 7 Commercial Market Archetypes Discovered", h2_style))

    archetype_data = [
        [Paragraph("Archetype ID &amp; Name", tbl_header_style), Paragraph("Avg Price", tbl_header_style), Paragraph("Avg Quality", tbl_header_style), Paragraph("Defining Market Profile", tbl_header_style)],
        [Paragraph("<b>0: Budget High-Value Indie</b>", tbl_cell_style), Paragraph("$5.17", tbl_cell_style), Paragraph("76.5 / 100", tbl_cell_style), Paragraph("High sentiment, low barrier to entry, strong positive review momentum.", tbl_cell_style)],
        [Paragraph("<b>1: Low-Review Casual</b>", tbl_cell_style), Paragraph("$3.82", tbl_cell_style), Paragraph("62.1 / 100", tbl_cell_style), Paragraph("Short play sessions, niche hobbyist demographic, modest review counts.", tbl_cell_style)],
        [Paragraph("<b>2: Standard Mid-Tier</b>", tbl_cell_style), Paragraph("$18.17", tbl_cell_style), Paragraph("77.8 / 100", tbl_cell_style), Paragraph("Established AA / indie studios with multi-language and co-op support.", tbl_cell_style)],
        [Paragraph("<b>3: Premium High-Engagement</b>", tbl_cell_style), Paragraph("$34.90", tbl_cell_style), Paragraph("81.2 / 100", tbl_cell_style), Paragraph("Deep systems-heavy titles (Strategy, Simulation, RPG) with extensive DLC.", tbl_cell_style)],
        [Paragraph("<b>4: Ultra-Budget Bargain</b>", tbl_cell_style), Paragraph("$1.49", tbl_cell_style), Paragraph("71.4 / 100", tbl_cell_style), Paragraph("Micro-priced impulse purchases, short puzzle games, game jam ports.", tbl_cell_style)],
        [Paragraph("<b>5: Flagship Blockbuster (AAA)</b>", tbl_cell_style), Paragraph("$59.99", tbl_cell_style), Paragraph("78.5 / 100", tbl_cell_style), Paragraph("Major publisher releases with multi-million marketing budgets, high CCU, full audio.", tbl_cell_style)],
        [Paragraph("<b>6: Cult Hit / Strong Retention</b>", tbl_cell_style), Paragraph("$14.99", tbl_cell_style), Paragraph("89.4 / 100", tbl_cell_style), Paragraph("Critically acclaimed indie masterpieces with highly loyal active communities.", tbl_cell_style)]
    ]
    t_arch = Table(archetype_data, colWidths=[130, 50, 64, 260])
    t_arch.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_dark),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f8fafc")]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_arch)

    story.append(PageBreak())

    story.append(Paragraph("5. Deep-Dive: All 12 .pkl Files & Why Serialization is Required", h1_style))
    story.append(Paragraph(
        "In production machine learning systems, <b>serialization</b> converts in-memory objects (trained estimators, mathematical transformers, schema lists) into persistent binary files on disk. Without serialization, an application would be forced to re-train all 4 models across 57,506 rows on every user request, causing severe latency and server crashes.",
        body_style
    ))

    story.append(Paragraph("Why Serialization is Crucial in Production:", h2_style))
    story.append(Paragraph("<b>1. Sub-Millisecond Inference:</b> Loading pre-compiled weights enables instant predictions (&lt; 5ms) when users adjust Streamlit sliders.", bullet_style))
    story.append(Paragraph("<b>2. Zero Training-Serving Skew:</b> Serializing <code>StandardScaler</code> guarantees runtime inputs are transformed with the exact mean and variance computed during training.", bullet_style))
    story.append(Paragraph("<b>3. Schema Enforcement:</b> Feature lists (<code>reg_features.pkl</code>, etc.) ensure runtime DataFrames maintain identical column order, preventing misaligned matrix multiplications.", bullet_style))
    story.append(Paragraph("<b>4. Decoupled Training &amp; Serving:</b> Heavy model training occurs offline in <code>train_models.py</code>, keeping the Streamlit web server lightweight, stateless, and scalable.", bullet_style))
    story.append(Spacer(1, 4))

    pkl_master_data = [
        [
            Paragraph(".pkl Filename", tbl_header_style),
            Paragraph("Python / Scikit-Learn Type", tbl_header_style),
            Paragraph("Target Model", tbl_header_style),
            Paragraph("Exact Operational Role in the Web App", tbl_header_style)
        ],
        [
            Paragraph("<b>model1_ridge.pkl</b>", tbl_cell_bold),
            Paragraph("<code>linear_model.Ridge</code>", tbl_cell_style),
            Paragraph("Model 1", tbl_cell_style),
            Paragraph("Predicts continuous implied fair retail price ($ USD) from standardized features.", tbl_cell_style)
        ],
        [
            Paragraph("<b>scaler1.pkl</b>", tbl_cell_bold),
            Paragraph("<code>preprocessing.StandardScaler</code>", tbl_cell_style),
            Paragraph("Model 1", tbl_cell_style),
            Paragraph("Scales runtime user input features using training distribution mean and standard deviation.", tbl_cell_style)
        ],
        [
            Paragraph("<b>reg_features.pkl</b>", tbl_cell_bold),
            Paragraph("<code>list[str]</code> (16 items)", tbl_cell_style),
            Paragraph("Model 1", tbl_cell_style),
            Paragraph("Enforces column ordering and schema alignment for Model 1 input matrix.", tbl_cell_style)
        ],
        [
            Paragraph("<b>model2_rf_classifier.pkl</b>", tbl_cell_bold),
            Paragraph("<code>ensemble.RandomForestClassifier</code>", tbl_cell_style),
            Paragraph("Model 2", tbl_cell_style),
            Paragraph("150-tree ensemble predicting multiclass price tier probabilities across 4 brackets.", tbl_cell_style)
        ],
        [
            Paragraph("<b>clf_features.pkl</b>", tbl_cell_bold),
            Paragraph("<code>list[str]</code> (16 items)", tbl_cell_style),
            Paragraph("Model 2", tbl_cell_style),
            Paragraph("Enforces column schema alignment for Model 2 classifier input matrix.", tbl_cell_style)
        ],
        [
            Paragraph("<b>label_encoder.pkl</b>", tbl_cell_bold),
            Paragraph("<code>preprocessing.LabelEncoder</code>", tbl_cell_style),
            Paragraph("Model 2", tbl_cell_style),
            Paragraph("Maps numeric predicted class indices (0, 1, 2, 3) back to tier strings ('Budget', 'Mid-range', etc.).", tbl_cell_style)
        ],
        [
            Paragraph("<b>model3_kmeans.pkl</b>", tbl_cell_bold),
            Paragraph("<code>cluster.KMeans</code>", tbl_cell_style),
            Paragraph("Model 3", tbl_cell_style),
            Paragraph("Assigns games to 1 of 7 commercial archetypes via nearest centroid calculation.", tbl_cell_style)
        ],
        [
            Paragraph("<b>scaler3.pkl</b>", tbl_cell_bold),
            Paragraph("<code>preprocessing.StandardScaler</code>", tbl_cell_style),
            Paragraph("Model 3", tbl_cell_style),
            Paragraph("Normalizes the 8 multi-scale clustering dimensions prior to Euclidean distance evaluation.", tbl_cell_style)
        ],
        [
            Paragraph("<b>cluster_features.pkl</b>", tbl_cell_bold),
            Paragraph("<code>list[str]</code> (8 items)", tbl_cell_style),
            Paragraph("Model 3", tbl_cell_style),
            Paragraph("Specifies the 8 feature dimensions defining the commercial clustering space.", tbl_cell_style)
        ],
        [
            Paragraph("<b>best_k.pkl</b>", tbl_cell_bold),
            Paragraph("<code>int</code> (value: 7)", tbl_cell_style),
            Paragraph("Model 3", tbl_cell_style),
            Paragraph("Stores optimal cluster count k=7 determined through elbow inertia and silhouette optimization.", tbl_cell_style)
        ],
        [
            Paragraph("<b>model4_gbm.pkl</b>", tbl_cell_bold),
            Paragraph("<code>ensemble.RandomForestClassifier</code>", tbl_cell_style),
            Paragraph("Model 4", tbl_cell_style),
            Paragraph("150-tree calibrated classifier evaluating pricing risk probability relative to residual baseline.", tbl_cell_style)
        ],
        [
            Paragraph("<b>over_features.pkl</b>", tbl_cell_bold),
            Paragraph("<code>list[str]</code> (12 items)", tbl_cell_style),
            Paragraph("Model 4", tbl_cell_style),
            Paragraph("Enforces schema alignment for Model 4 commercial overpricing screener.", tbl_cell_style)
        ]
    ]

    t_pkl = Table(pkl_master_data, colWidths=[110, 130, 54, 210])
    t_pkl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f8fafc")]),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_pkl)

    story.append(PageBreak())

    story.append(Paragraph("6. Real-Time Inference Flowchart & .pkl Execution Pipeline", h1_style))
    story.append(Paragraph(
        "When a user adjusts input sliders in the Streamlit web interface, the application coordinates multiple .pkl artifacts synchronously to generate real-time econometric and machine learning intelligence.",
        body_style
    ))
    story.append(Spacer(1, 4))

    diag2_path = os.path.join(DIAG_DIR, "diagram2_pkl_pipeline.png")
    if os.path.exists(diag2_path):
        img2 = Image(diag2_path, width=504, height=230)
        story.append(img2)
        story.append(Spacer(1, 6))

    story.append(Paragraph("Step-by-Step Execution Lifecycle:", h2_style))
    story.append(Paragraph("<b>Step 1: Input Vector Construction</b> - The user configures 6 primary sliders (Quality Score, Peak CCU, Reviews, Age, Languages, Genre flags).", bullet_style))
    story.append(Paragraph("<b>Step 2: Schema Alignment</b> - <code>reg_features.pkl</code>, <code>clf_features.pkl</code>, and <code>over_features.pkl</code> filter and align raw UI inputs into 3 model-specific DataFrames.", bullet_style))
    story.append(Paragraph("<b>Step 3: Scaling &amp; Normalization</b> - <code>scaler1.pkl</code> and <code>scaler3.pkl</code> standardize continuous variables using stored training parameters ($\mu, \sigma$).", bullet_style))
    story.append(Paragraph("<b>Step 4: Multi-Model Inference</b> - <code>model1_ridge.pkl</code> computes fair price ($), <code>model2_rf_classifier.pkl</code> outputs tier probabilities, <code>model3_kmeans.pkl</code> computes cluster centroid distances, and <code>model4_gbm.pkl</code> estimates commercial risk probability.", bullet_style))
    story.append(Paragraph("<b>Step 5: Label Decoding</b> - <code>label_encoder.pkl</code> converts predicted integer index to string class name ('Budget', 'Mid-range', 'Premium', 'AAA').", bullet_style))
    story.append(Paragraph("<b>Step 6: UI Rendering</b> - Streamlit updates dynamic metric cards, Plotly probability bar charts, 2D cluster scatter maps, and risk gauge indicators within 10 milliseconds.", bullet_style))

    story.append(PageBreak())

    story.append(Paragraph("7. Streamlit Web Application Architecture & UI/UX Design", h1_style))
    story.append(Paragraph(
        "The application is engineered as an executive-grade, dark-themed Streamlit dashboard providing immediate real-time exploration, model inference, and catalog search capabilities.",
        body_style
    ))

    app_structure_data = [
        [Paragraph("Dashboard Tab", tbl_header_style), Paragraph("Embedded Functionality &amp; Interactive Features", tbl_header_style)],
        [
            Paragraph("<b>Tab 1: Complete EDA (15 Qs)</b>", tbl_cell_bold),
            Paragraph("Full rendering of all 15 high-contrast EDA charts with categorized section navigation dropdown (Pricing, Popularity, Quality, Platform, Correlation).", tbl_cell_style)
        ],
        [
            Paragraph("<b>Tab 2: Market Overview</b>", tbl_cell_bold),
            Paragraph("Dynamic metric cards (Catalog size, median price, average quality, value score), price histograms, and price-quality bubble charts.", tbl_cell_style)
        ],
        [
            Paragraph("<b>Tab 3: Model 1 &amp; 2 Predictor</b>", tbl_cell_bold),
            Paragraph("Interactive input panel with sliders for quality, reviews, CCU, age, and languages. Live prediction of implied fair price and tier probabilities.", tbl_cell_style)
        ],
        [
            Paragraph("<b>Tab 4: Model 3 Clusters</b>", tbl_cell_bold),
            Paragraph("2D cluster scatter plot colored by the 7 archetypes with bubble sizing by log reviews and summary characteristics table.", tbl_cell_style)
        ],
        [
            Paragraph("<b>Tab 5: Model 4 Risk Screener</b>", tbl_cell_bold),
            Paragraph("Commercial pricing risk screener with color-coded status badges and dynamic Plotly gauge meter showing overpricing probability (0-100%).", tbl_cell_style)
        ],
        [
            Paragraph("<b>Tab 6: Catalog Explorer</b>", tbl_cell_bold),
            Paragraph("Fast searchable and filterable database view across all 57,506 games connected to sidebar global filters.", tbl_cell_style)
        ],
        [
            Paragraph("<b>Tab 7: AI Copilot (Gemini)</b>", tbl_cell_bold),
            Paragraph("Generative AI conversational pricing economist powered by Google Gemini API, grounded in 57,506 games, 4 ML models, and 15 EDA insights with one-click quick prompt chips.", tbl_cell_style)
        ]
    ]

    t_app = Table(app_structure_data, colWidths=[160, 344])
    t_app.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f8fafc")]),
        ('TOPPADDING', (0,0), (-1,-1), 4.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4.5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_app)
    story.append(Spacer(1, 8))

    story.append(Paragraph("Key Software Engineering &amp; Robustness Practices", h2_style))
    story.append(Paragraph("<b>Zero-Comment Codebase Compliance:</b> Engineered all Python pipelines, model trainers, and web modules cleanly without code comments as requested.", bullet_style))
    story.append(Paragraph("<b>Robust Edge-Case Guards:</b> Added non-crashing fallback guards across all tabs to handle 0-row filter selections safely without throwing StandardScaler errors.", bullet_style))
    story.append(Paragraph("<b>Glassmorphic Dark Theme:</b> Implemented custom CSS with Plus Jakarta Sans typography, high-contrast text tags, and responsive Plotly dark themes.", bullet_style))
    story.append(Paragraph("<b>Streamlit Caching Pipeline:</b> Integrated <code>@st.cache_data</code> for instant sub-second dataframe loading and model artifact reuse.", bullet_style))
    story.append(Paragraph("<b>Deployment Readiness:</b> Structured for immediate one-click deployment on Streamlit Community Cloud and Vercel Serverless.", bullet_style))

    story.append(PageBreak())

    story.append(Paragraph("8. Commercial Playbook, Business Strategy & Deliverables", h1_style))
    story.append(Paragraph(
        "Combining econometric analysis with machine learning yields actionable commercial rules for game developers and publishers looking to maximize revenue and player goodwill on Steam.",
        body_style
    ))

    strat_data = [
        [
            Paragraph("Stakeholder Segment", tbl_header_style),
            Paragraph("Commercial Challenge", tbl_header_style),
            Paragraph("Data-Driven Strategic Recommendation", tbl_header_style)
        ],
        [
            Paragraph("<b>Indie Game Developers</b><br/><font size='7.5' color='#64748b'>(Solo / Small Teams)</font>", tbl_cell_style),
            Paragraph("Risk of underpricing ($1.99) leading to perceived low quality, or overpricing ($19.99) stalling launch velocity.", tbl_cell_style),
            Paragraph("<b>Anchor in the $9.99 - $14.99 Corridor:</b> Delivers optimal perceived value while preserving commercial margin. Prioritize language localization over achievements.", tbl_cell_style)
        ],
        [
            Paragraph("<b>AA &amp; Mid-Tier Studios</b><br/><font size='7.5' color='#64748b'>($500k - $5M Budgets)</font>", tbl_cell_style),
            Paragraph("High risk of being caught in the 'no man's land' between cheap viral indies and AAA marketing titans.", tbl_cell_style),
            Paragraph("<b>Price at $19.99 - $29.99 with Systems-Heavy Depth:</b> Emphasize co-op and procedural replayability to sustain 2-week retention and organic word-of-mouth.", tbl_cell_style)
        ],
        [
            Paragraph("<b>Publishers &amp; Investors</b><br/><font size='7.5' color='#64748b'>(Portfolio Management)</font>", tbl_cell_style),
            Paragraph("Inaccurate pre-launch revenue projections and uncalibrated seasonal discounting schedules.", tbl_cell_style),
            Paragraph("<b>Utilize Model 4 Risk Audits:</b> Benchmark planned launch prices against genre baselines. Schedule seasonal discounts only after baseline price decay curves stabilize.", tbl_cell_style)
        ]
    ]

    t_strat = Table(strat_data, colWidths=[110, 160, 234])
    t_strat.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f8fafc")]),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_strat)
    story.append(Spacer(1, 8))

    story.append(Paragraph("Complete Repository &amp; Deliverables Index", h2_style))

    deliv_data = [
        [Paragraph("Artifact / Module", tbl_header_style), Paragraph("File Path / Location", tbl_header_style), Paragraph("Technical Description", tbl_header_style)],
        [Paragraph("Streamlit Web App", tbl_cell_bold), Paragraph("<code>steam_app/app.py</code>", tbl_cell_style), Paragraph("Production 6-tab dashboard with real-time ML inference and Plotly visualizations.", tbl_cell_style)],
        [Paragraph("Model Training Engine", tbl_cell_bold), Paragraph("<code>steam_app/train_models.py</code>", tbl_cell_style), Paragraph("Trains and serializes all 4 ML models and preprocessors to 12 .pkl files.", tbl_cell_style)],
        [Paragraph("Feature Engineering", tbl_cell_bold), Paragraph("<code>steam_app/feature_engineering.py</code>", tbl_cell_style), Paragraph("Transforms raw Steam metadata into modeling dataset.", tbl_cell_style)],
        [Paragraph("Cleaned Dataset", tbl_cell_bold), Paragraph("<code>steam_app/steam_games_modelling.csv</code>", tbl_cell_style), Paragraph("57,506 commercial game records with engineered features.", tbl_cell_style)],
        [Paragraph("12 .pkl Model Artifacts", tbl_cell_bold), Paragraph("<code>steam_app/*.pkl</code> (12 files)", tbl_cell_style), Paragraph("Serialized Ridge, RandomForest, KMeans, Scalers, and Feature Schemas.", tbl_cell_style)],
        [Paragraph("Architectural Diagrams", tbl_cell_bold), Paragraph("<code>steam_app/diagrams/</code> (3 PNGs)", tbl_cell_style), Paragraph("High-resolution architectural flowcharts and PKL inference pipelines.", tbl_cell_style)],
        [Paragraph("EDA Visual Assets", tbl_cell_bold), Paragraph("<code>steam_app/q_charts/</code> (15 PNGs)", tbl_cell_style), Paragraph("High-resolution static charts rendering all 15 core research questions.", tbl_cell_style)]
    ]

    t_deliv = Table(deliv_data, colWidths=[110, 150, 244])
    t_deliv.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_dark),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f8fafc")]),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_deliv)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Detailed Architecture Presentation PDF successfully generated: {pdf_path}")

if __name__ == "__main__":
    build_pdf()
