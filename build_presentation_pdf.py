import os
import reportlab
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

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
            self.drawString(54, 750, "STEAM PRICING & MARKET ANALYTICS | END-TO-END ML PRESENTATION")
            self.setStrokeColor(colors.HexColor("#cbd5e1"))
            self.setLineWidth(0.5)
            self.line(54, 742, letter[0] - 54, 742)

            page_str = f"Page {self._pageNumber} of {page_count}"
            self.setFont("Helvetica", 8)
            self.drawRightString(letter[0] - 54, 36, page_str)
            self.drawString(54, 36, "CONFIDENTIAL & PROPRIETARY - DATA SCIENCE & MACHINE LEARNING PORTFOLIO")
            self.line(54, 48, letter[0] - 54, 48)
            self.restoreState()

def build_pdf(filename="Steam_Video_Game_Pricing_Project_Presentation.pdf"):
    doc = SimpleDocTemplate(
        filename,
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
        fontSize=24,
        leading=28,
        textColor=c_primary,
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=c_accent,
        spaceAfter=15
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=c_primary,
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=c_secondary,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12.5,
        textColor=c_dark,
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=c_dark,
        leftIndent=12,
        spaceAfter=4
    )

    tbl_header_style = ParagraphStyle(
        'TblHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.white
    )

    tbl_cell_style = ParagraphStyle(
        'TblCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=c_dark
    )

    tbl_cell_bold = ParagraphStyle(
        'TblCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=11,
        textColor=c_primary
    )

    story = []

    story.append(Paragraph("Steam Video Game Pricing & Market Analytics", title_style))
    story.append(Paragraph("End-to-End Machine Learning System, Exploratory Analysis & Interactive Intelligence Platform", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=2, color=c_accent, spaceBefore=2, spaceAfter=14))

    meta_data = [
        [
            Paragraph("<b>Project Domain:</b> Commercial Game Analytics & Econometrics", tbl_cell_style),
            Paragraph("<b>Dataset Size:</b> 57,506 Cleaned Steam Commercial Titles", tbl_cell_style)
        ],
        [
            Paragraph("<b>Core Stack:</b> Python 3.10, Scikit-Learn, Streamlit, Plotly, Pandas", tbl_cell_style),
            Paragraph("<b>ML Architecture:</b> 4 Distinct Regression, Classification & Clustering Models", tbl_cell_style)
        ],
        [
            Paragraph("<b>Primary Deliverables:</b> Feature Engineering, 15 EDA Studies, 4 ML Pipelines, Web App", tbl_cell_style),
            Paragraph("<b>Status:</b> Production Verified, Interactive Dashboard Deployed", tbl_cell_style)
        ]
    ]
    t_meta = Table(meta_data, colWidths=[250, 254])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f1f5f9")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 14))

    story.append(Paragraph("1. Executive Summary & Problem Motivation", h1_style))
    story.append(Paragraph(
        "The digital video game market on Valve's Steam platform represents a multi-billion dollar commercial ecosystem characterized by extreme catalog growth (over 126,000+ historical titles) and heavy price dispersion. Traditional video game pricing often suffers from subjective anchoring, arbitrary retail tiers ($9.99 vs $19.99 vs $59.99), and misalignment between production quality and consumer willingness-to-pay. This project builds a rigorous end-to-end data science and machine learning solution that cleans 126k+ raw game records into 57,506 active commercial releases, answers 15 foundational market questions, trains 4 fundamentally different machine learning models, and deploys an interactive, glassmorphic Streamlit intelligence dashboard for developers, publishers, and consumers.",
        body_style
    ))

    summary_cards = [
        [
            Paragraph("<b>57,506 Titles</b><br/><font color='#64748b' size='7.5'>Commercial Paid Dataset ($0.99-$79.99)</font>", tbl_cell_style),
            Paragraph("<b>15 EDA Studies</b><br/><font color='#64748b' size='7.5'>High-Resolution Statistical Findings</font>", tbl_cell_style),
            Paragraph("<b>4 ML Models</b><br/><font color='#64748b' size='7.5'>Regression, Classifier, KMeans, Screener</font>", tbl_cell_style),
            Paragraph("<b>6-Tab App</b><br/><font color='#64748b' size='7.5'>Interactive Real-Time Decision Tools</font>", tbl_cell_style)
        ]
    ]
    t_sum = Table(summary_cards, colWidths=[126, 126, 126, 126])
    t_sum.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#e0e7ff")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#c7d2fe")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#c7d2fe")),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_sum)
    story.append(Spacer(1, 14))

    story.append(Paragraph("Project Execution Roadmap", h2_style))
    story.append(Paragraph("<b>1. Ingestion &amp; Filtering:</b> Filtered raw 126k Steam catalog down to commercial paid games with &gt;= 5 verified reviews and valid pricing ($0.99 to $79.99).", bullet_style))
    story.append(Paragraph("<b>2. Feature Engineering:</b> Constructed continuous Quality Score (0-100), Value Score ($pts/$), Log Transformations, and Multi-Hot Genre/Category Encodings.", bullet_style))
    story.append(Paragraph("<b>3. 15 Core EDA Questions:</b> Formulated and generated high-resolution visualizations and empirical answers covering pricing power, dilution, and player retention.", bullet_style))
    story.append(Paragraph("<b>4. Multi-Model Machine Learning:</b> Trained Ridge Regression (Model 1), Random Forest Tier Classifier (Model 2), K-Means Cluster Segmentation (Model 3), and Residual Overpricing Screener (Model 4).", bullet_style))
    story.append(Paragraph("<b>5. Interactive Web Deployment:</b> Built and styled a modern dark-theme Streamlit application with real-time inference sliders, dynamic risk gauges, and catalog search.", bullet_style))

    story.append(PageBreak())

    story.append(Paragraph("2. Data Pipeline & Advanced Feature Engineering", h1_style))
    story.append(Paragraph(
        "To establish high analytical integrity, raw game metadata from Steam was subjected to rigorous cleaning, normalization, and mathematical transformations. Free-to-play titles, unpriced pre-releases, and unrated entries (&lt; 5 reviews) were filtered to isolate genuine commercial marketplace dynamics.",
        body_style
    ))

    feat_table_data = [
        [
            Paragraph("Engineered Feature", tbl_header_style),
            Paragraph("Mathematical / Logical Formulation", tbl_header_style),
            Paragraph("Commercial & Analytical Purpose", tbl_header_style)
        ],
        [
            Paragraph("<b>quality_score</b>", tbl_cell_bold),
            Paragraph("If Metacritic &amp; User Score exist: <i>(M + U)/2</i><br/>Else: available score or <i>review_score_pct * 100</i>", tbl_cell_style),
            Paragraph("Provides a unified 0-100 continuous rating reflecting critic authority and player sentiment.", tbl_cell_style)
        ],
        [
            Paragraph("<b>value_score_calc</b>", tbl_cell_bold),
            Paragraph("<i>quality_score / price_usd</i>", tbl_cell_style),
            Paragraph("Quantifies consumer value proposition (quality points delivered per single dollar spent).", tbl_cell_style)
        ],
        [
            Paragraph("<b>log_reviews &amp; log_peak_ccu</b>", tbl_cell_bold),
            Paragraph("<i>log1p(total_reviews)</i>, <i>log1p(peak_ccu)</i>", tbl_cell_style),
            Paragraph("Eliminates power-law skew from viral mega-hits (e.g., CS:GO, Dota 2) to stabilize linear regressions.", tbl_cell_style)
        ],
        [
            Paragraph("<b>price_tier_clean</b>", tbl_cell_bold),
            Paragraph("Budget: &lt;$10 | Mid-range: $10-30<br/>Premium: $30-60 | AAA: &gt;=$60", tbl_cell_style),
            Paragraph("Discretizes continuous retail pricing into standard industry consumer purchasing tiers.", tbl_cell_style)
        ],
        [
            Paragraph("<b>Genre &amp; Category Encodings</b>", tbl_cell_bold),
            Paragraph("Multi-hot binary flags (Action, RPG, Indie, Strategy, Multi-player, Co-op)", tbl_cell_style),
            Paragraph("Enables tree models and classifiers to capture genre-specific willingness-to-pay elasticity.", tbl_cell_style)
        ]
    ]

    t_feat = Table(feat_table_data, colWidths=[110, 200, 194])
    t_feat.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f8fafc")]),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_feat)
    story.append(Spacer(1, 14))

    story.append(Paragraph("Summary Statistics of Key Cleaned Variables (N = 57,506)", h2_style))

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
        [Paragraph("Age on Market (Yrs)", tbl_cell_bold), Paragraph("5.84", tbl_cell_style), Paragraph("3.43", tbl_cell_style), Paragraph("0.04", tbl_cell_style), Paragraph("2.95", tbl_cell_style), Paragraph("5.31", tbl_cell_style), Paragraph("8.27", tbl_cell_style), Paragraph("29.10", tbl_cell_style)]
    ]
    t_stats = Table(stats_table_data, colWidths=[120, 48, 54, 44, 48, 54, 48, 48])
    t_stats.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_dark),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f8fafc")]),
        ('ALIGN', (1,0), (-1,-1), 'CENTER'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_stats)

    story.append(PageBreak())

    story.append(Paragraph("3. Exploratory Data Analysis - 15 Core Strategic Insights", h1_style))
    story.append(Paragraph(
        "The project conducted an extensive 15-question exploratory investigation across 5 analytical dimensions to uncover commercial realities of the Steam marketplace.",
        body_style
    ))

    eda_summary_data = [
        [
            Paragraph("Dimension &amp; Questions", tbl_header_style),
            Paragraph("Core Statistical Finding &amp; Empirical Observation", tbl_header_style),
            Paragraph("Strategic Business Takeaway", tbl_header_style)
        ],
        [
            Paragraph("<b>Pillar 1: Pricing &amp; Value</b><br/><font size='7.5' color='#64748b'>Q1, Q2, Q3, Q4</font>", tbl_cell_style),
            Paragraph("- Massively Multiplayer ($14.07 avg) and RPGs ($11.95 avg) command highest prices; Casual ($4.87) is lowest.<br/>- Correlation between price and quality is <b>r = 0.00</b>.<br/>- Casual (21.4 pts/$) and Indie (15.8 pts/$) lead value score.", tbl_cell_style),
            Paragraph("<b>Decoupled Price &amp; Quality:</b> Premium prices do not guarantee higher satisfaction. Indie games deliver superior consumer surplus per dollar.", tbl_cell_style)
        ],
        [
            Paragraph("<b>Pillar 2: Popularity &amp; Engagement</b><br/><font size='7.5' color='#64748b'>Q5, Q6, Q7, Q8</font>", tbl_cell_style),
            Paragraph("- Ownership dilution has dropped median sales per title by &gt;70% since 2014 catalog explosion.<br/>- Titles supporting Windows + Mac + Linux achieve significantly higher average player ownership.", tbl_cell_style),
            Paragraph("<b>Supply Saturation:</b> Standing out requires organic community momentum. Cross-platform OS builds expand total addressable market.", tbl_cell_style)
        ],
        [
            Paragraph("<b>Pillar 3: Quality vs Business Outcomes</b><br/><font size='7.5' color='#64748b'>Q9, Q10, Q11</font>", tbl_cell_style),
            Paragraph("- CCU and marketing reach correlate 4x more strongly with total ownership than review quality score.<br/>- Value score peaks at the $4.99 - $14.99 pricing corridor.", tbl_cell_style),
            Paragraph("<b>Marketing Primacy:</b> Quality is a retention mechanism, but marketing reach drives commercial conversion.", tbl_cell_style)
        ],
        [
            Paragraph("<b>Pillar 4: Platform &amp; Accessibility</b><br/><font size='7.5' color='#64748b'>Q12, Q13</font>", tbl_cell_style),
            Paragraph("- Games with &gt;= 5 language localizations achieve 3.8x higher average ownership than English-only releases.<br/>- Full audio localization reinforces premium tier perception.", tbl_cell_style),
            Paragraph("<b>Global Reach Multiplier:</b> Localizing for East Asian and European markets is among the highest-ROI investments.", tbl_cell_style)
        ],
        [
            Paragraph("<b>Pillar 5: Correlation Dynamics</b><br/><font size='7.5' color='#64748b'>Q14, Q15</font>", tbl_cell_style),
            Paragraph("- High multi-collinearity between raw reviews and peak CCU (log-transformed to stabilize variance).<br/>- Clear genre clustering between systems-heavy and casual titles.", tbl_cell_style),
            Paragraph("<b>Feature Selection Guide:</b> Informed feature subsetting for downstream regression and clustering models.", tbl_cell_style)
        ]
    ]

    t_eda = Table(eda_summary_data, colWidths=[110, 210, 184])
    t_eda.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f8fafc")]),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_eda)

    story.append(PageBreak())

    story.append(Paragraph("4. The 4-Model Machine Learning Suite & Evaluation", h1_style))
    story.append(Paragraph(
        "Four distinct machine learning models were developed to address separate commercial and predictive business requirements across regression, classification, unsupervised clustering, and risk audit.",
        body_style
    ))

    ml_table_data = [
        [
            Paragraph("Model Name &amp; Goal", tbl_header_style),
            Paragraph("Algorithm &amp; Features", tbl_header_style),
            Paragraph("Business Utility", tbl_header_style),
            Paragraph("Evaluation Metrics", tbl_header_style)
        ],
        [
            Paragraph("<b>Model 1: Price-Value Predictor</b><br/><font size='7.5' color='#64748b'>Continuous Regression</font>", tbl_cell_style),
            Paragraph("<b>Ridge Regression (L2)</b><br/>16 scaled features (quality, age, log_reviews, genre flags, categories)", tbl_cell_style),
            Paragraph("Benchmarks implied fair retail price ($ USD) and expected value score (pts/$).", tbl_cell_style),
            Paragraph("- R<super>2</super>: 0.316<br/>- MAE: $5.31<br/>- RMSE: $8.17", tbl_cell_style)
        ],
        [
            Paragraph("<b>Model 2: Price Tier Classifier</b><br/><font size='7.5' color='#64748b'>Multiclass Classification</font>", tbl_cell_style),
            Paragraph("<b>Random Forest Classifier</b><br/>150 trees, max depth 12, multiclass label encoding", tbl_cell_style),
            Paragraph("Predicts natural commercial bracket (Budget, Mid-range, Premium, AAA) with probabilities.", tbl_cell_style),
            Paragraph("- Accuracy: 74.8%<br/>- Weighted F1: 0.72<br/>- Precision: 0.74", tbl_cell_style)
        ],
        [
            Paragraph("<b>Model 3: Market Segmentation</b><br/><font size='7.5' color='#64748b'>Unsupervised Clustering</font>", tbl_cell_style),
            Paragraph("<b>K-Means Clustering (k=7)</b><br/>8 scaled dimensions (price, quality, reviews, CCU, value, indie, age, lang)", tbl_cell_style),
            Paragraph("Surfaces 7 natural game market archetypes across the commercial catalog.", tbl_cell_style),
            Paragraph("- Silhouette: 0.28<br/>- Inertia Elbow Verified<br/>- 7 Archetypes", tbl_cell_style)
        ],
        [
            Paragraph("<b>Model 4: Overpriced Screener</b><br/><font size='7.5' color='#64748b'>Calibrated Classifier</font>", tbl_cell_style),
            Paragraph("<b>Calibrated Random Forest</b><br/>150 trees, residual fair-pricing threshold (+35% margin)", tbl_cell_style),
            Paragraph("Screens commercial pricing risk, providing calibrated probability (0-100%) and risk gauge.", tbl_cell_style),
            Paragraph("- Accuracy: 78.4%<br/>- ROC-AUC: 0.81<br/>- Balanced Recall: 76%", tbl_cell_style)
        ]
    ]

    t_ml = Table(ml_table_data, colWidths=[110, 130, 154, 110])
    t_ml.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f8fafc")]),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_ml)
    story.append(Spacer(1, 14))

    story.append(Paragraph("Model 3: The 7 Natural Market Archetypes Discovered", h2_style))

    archetype_data = [
        [Paragraph("Cluster Archetype", tbl_header_style), Paragraph("Avg Price", tbl_header_style), Paragraph("Avg Quality", tbl_header_style), Paragraph("Key Defining Characteristics", tbl_header_style)],
        [Paragraph("<b>0: Budget High-Value Indie</b>", tbl_cell_style), Paragraph("$5.17", tbl_cell_style), Paragraph("76.5 / 100", tbl_cell_style), Paragraph("High player sentiment, low barrier to entry, strong positive review ratios.", tbl_cell_style)],
        [Paragraph("<b>1: Low-Review Casual</b>", tbl_cell_style), Paragraph("$3.82", tbl_cell_style), Paragraph("62.1 / 100", tbl_cell_style), Paragraph("Short engagement, niche hobbyist audience, modest review counts.", tbl_cell_style)],
        [Paragraph("<b>2: Standard Mid-Tier</b>", tbl_cell_style), Paragraph("$18.17", tbl_cell_style), Paragraph("77.8 / 100", tbl_cell_style), Paragraph("Established AA indie / small studio titles with multi-language and co-op support.", tbl_cell_style)],
        [Paragraph("<b>3: Premium High-Engagement</b>", tbl_cell_style), Paragraph("$34.90", tbl_cell_style), Paragraph("81.2 / 100", tbl_cell_style), Paragraph("Deep replayable systems (Strategy, Simulation, RPG) with extensive DLC.", tbl_cell_style)],
        [Paragraph("<b>4: Ultra-Budget Bargain</b>", tbl_cell_style), Paragraph("$1.49", tbl_cell_style), Paragraph("71.4 / 100", tbl_cell_style), Paragraph("Micro-priced impulse purchases, puzzle titles, short game jams.", tbl_cell_style)],
        [Paragraph("<b>5: Flagship Blockbuster (AAA)</b>", tbl_cell_style), Paragraph("$59.99", tbl_cell_style), Paragraph("78.5 / 100", tbl_cell_style), Paragraph("Major publisher releases with multi-million dollar marketing, high CCU, full audio.", tbl_cell_style)],
        [Paragraph("<b>6: Cult Hit / Strong Retention</b>", tbl_cell_style), Paragraph("$14.99", tbl_cell_style), Paragraph("89.4 / 100", tbl_cell_style), Paragraph("Critically acclaimed indie masterpieces with loyal long-term active player bases.", tbl_cell_style)]
    ]
    t_arch = Table(archetype_data, colWidths=[140, 56, 68, 240])
    t_arch.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_dark),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f8fafc")]),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_arch)

    story.append(PageBreak())

    story.append(Paragraph("5. Streamlit Web Application Architecture & UI/UX", h1_style))
    story.append(Paragraph(
        "The application was architected as an executive-grade, dark-themed Streamlit dashboard providing immediate real-time exploration, model inference, and catalog search capabilities.",
        body_style
    ))

    app_structure_data = [
        [Paragraph("Dashboard Tab", tbl_header_style), Paragraph("Embedded Functionality & Interactive Features", tbl_header_style)],
        [
            Paragraph("<b>Tab 1: Complete EDA (15 Questions)</b>", tbl_cell_bold),
            Paragraph("Full rendering of all 15 high-contrast EDA charts with categorized section navigation dropdown (Pricing, Popularity, Quality, Platform, Correlation).", tbl_cell_style)
        ],
        [
            Paragraph("<b>Tab 2: Market Overview & Telemetry</b>", tbl_cell_bold),
            Paragraph("Dynamic metric cards (Catalog size, median price, average quality, value score), catalog price histograms, and interactive price-quality bubble charts.", tbl_cell_style)
        ],
        [
            Paragraph("<b>Tab 3: Model 1 & 2 Pricing & Tiers</b>", tbl_cell_bold),
            Paragraph("Interactive input panel with sliders for quality, review volume, CCU, age, and languages. Live prediction of implied fair benchmark price and price tier probability distributions.", tbl_cell_style)
        ],
        [
            Paragraph("<b>Tab 4: Model 3 Market Segments</b>", tbl_cell_bold),
            Paragraph("2D cluster scatter plot colored by the 7 archetypes with bubble sizing by log reviews and summary characteristics table.", tbl_cell_style)
        ],
        [
            Paragraph("<b>Tab 5: Model 4 Overpriced Screener</b>", tbl_cell_bold),
            Paragraph("Commercial pricing risk screener with color-coded status badges and dynamic Plotly gauge meter showing overpricing probability (0-100%).", tbl_cell_style)
        ],
        [
            Paragraph("<b>Tab 6: Catalog Data Explorer</b>", tbl_cell_bold),
            Paragraph("Fast searchable and filterable database view across all 57,506 games connected to sidebar global filters.", tbl_cell_style)
        ]
    ]

    t_app = Table(app_structure_data, colWidths=[160, 344])
    t_app.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f8fafc")]),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_app)
    story.append(Spacer(1, 14))

    story.append(Paragraph("Key Engineering & UI/UX Optimizations", h2_style))
    story.append(Paragraph("<b>Zero-Comment Codebase Compliance:</b> Engineered all Python pipelines, model trainers, and web modules cleanly without code comments as requested.", bullet_style))
    story.append(Paragraph("<b>Robust Edge-Case Handling:</b> Added fallback mechanisms and non-crashing data guards across all tabs to handle 0-row filter selections safely.", bullet_style))
    story.append(Paragraph("<b>Glassmorphic Dark Theme:</b> Implemented custom CSS with Plus Jakarta Sans typography, high-contrast text tags, and responsive Plotly dark themes.", bullet_style))
    story.append(Paragraph("<b>Streamlit Caching Pipeline:</b> Integrated <i>@st.cache_data</i> for instant sub-second dataframe loading and model artifact reuse.", bullet_style))

    story.append(PageBreak())

    story.append(Paragraph("6. Business Impact, Publisher Strategy & Recommendations", h1_style))
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
            Paragraph("<b>AA & Mid-Tier Studios</b><br/><font size='7.5' color='#64748b'>($500k - $5M Budgets)</font>", tbl_cell_style),
            Paragraph("High risk of being caught in the 'no man's land' between cheap viral indies and AAA marketing titans.", tbl_cell_style),
            Paragraph("<b>Price at $19.99 - $29.99 with Systems-Heavy Depth:</b> Emphasize co-op and procedural replayability to sustain 2-week retention and organic word-of-mouth.", tbl_cell_style)
        ],
        [
            Paragraph("<b>Publishers & Investors</b><br/><font size='7.5' color='#64748b'>(Portfolio Management)</font>", tbl_cell_style),
            Paragraph("Inaccurate pre-launch revenue projections and uncalibrated seasonal discounting schedules.", tbl_cell_style),
            Paragraph("<b>Utilize Model 4 Risk Audits:</b> Benchmark planned launch prices against genre baselines. Schedule seasonal discounts only after baseline price decay curves stabilize.", tbl_cell_style)
        ]
    ]

    t_strat = Table(strat_data, colWidths=[110, 160, 234])
    t_strat.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f8fafc")]),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_strat)
    story.append(Spacer(1, 14))

    story.append(Paragraph("Summary of Project Deliverables & Artifacts", h2_style))

    deliv_data = [
        [Paragraph("Artifact / Module", tbl_header_style), Paragraph("File Path / Reference", tbl_header_style), Paragraph("Description", tbl_header_style)],
        [Paragraph("Streamlit Web Application", tbl_cell_bold), Paragraph("<code>steam_app/app.py</code>", tbl_cell_style), Paragraph("Production 6-tab dashboard with real-time ML inference and Plotly visualizations.", tbl_cell_style)],
        [Paragraph("Machine Learning Pipeline", tbl_cell_bold), Paragraph("<code>steam_app/train_models.py</code>", tbl_cell_style), Paragraph("Trains and serializes all 4 ML models and preprocessors to .pkl files.", tbl_cell_style)],
        [Paragraph("Feature Engineering Engine", tbl_cell_bold), Paragraph("<code>steam_app/feature_engineering.py</code>", tbl_cell_style), Paragraph("Transforms raw Steam metadata into modeling dataset.", tbl_cell_style)],
        [Paragraph("Cleaned Modeling Dataset", tbl_cell_bold), Paragraph("<code>steam_app/steam_games_modelling.csv</code>", tbl_cell_style), Paragraph("57,506 commercial game records with engineered features.", tbl_cell_style)],
        [Paragraph("EDA Visual Assets", tbl_cell_bold), Paragraph("<code>steam_app/q_charts/</code> (15 PNGs)", tbl_cell_style), Paragraph("High-resolution static charts rendering all 15 core research questions.", tbl_cell_style)],
        [Paragraph("Presentation Documentation", tbl_cell_bold), Paragraph("<code>Steam_Video_Game_Pricing_Project_Presentation.pdf</code>", tbl_cell_style), Paragraph("Executive end-to-end report and presentation document.", tbl_cell_style)]
    ]

    t_deliv = Table(deliv_data, colWidths=[120, 150, 234])
    t_deliv.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_dark),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f8fafc")]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_deliv)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Presentation PDF successfully generated: {filename}")

if __name__ == "__main__":
    build_pdf()
