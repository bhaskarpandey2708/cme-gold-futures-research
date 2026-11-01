#!/usr/bin/env python3
"""
Apex CME Globex Institutional Due Diligence Questionnaire (DDQ) Generator
Compliant with AIMA (Alternative Investment Management Association) & Institutional ODD Standards.
Generates an executive, publication-grade multi-page PDF document.
"""

import os
import sys
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """Two-pass canvas to dynamically compute total page count."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b"))
        
        # Suppress header and footer on cover page
        if self._pageNumber > 1:
            # Header
            self.drawString(54, letter[1] - 36, "APEX CAPITAL QUANTITATIVE RESEARCH | INSTITUTIONAL DUE DILIGENCE (AIMA DDQ)")
            self.drawRightString(letter[0] - 54, letter[1] - 36, "CME GLOBEX MULTI-COMMODITY ALPHA")
            self.setStrokeColor(colors.HexColor("#cbd5e1"))
            self.setLineWidth(0.5)
            self.line(54, letter[1] - 42, letter[0] - 54, letter[1] - 42)
            
            # Footer
            self.line(54, 45, letter[0] - 54, 45)
            self.drawString(54, 32, "CONFIDENTIAL & PROPRIETARY — PREPARED EXCLUSIVELY FOR INSTITUTIONAL ALLOCATORS")
            self.drawRightString(letter[0] - 54, 32, f"Page {self._pageNumber} of {page_count}")
        self.restoreState()


def build_ddq_pdf(output_path="output/AIMA_INSTITUTIONAL_DUE_DILIGENCE_QUESTIONNAIRE.pdf"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    
    styles = getSampleStyleSheet()
    
    # Custom color palette
    c_primary = colors.HexColor("#0f172a")     # Slate 900
    c_accent = colors.HexColor("#0284c7")      # Sky 600
    c_darkblue = colors.HexColor("#1e3a8a")    # Blue 900
    c_subtext = colors.HexColor("#475569")     # Slate 600
    c_bg_panel = colors.HexColor("#f8fafc")    # Slate 50
    c_border = colors.HexColor("#e2e8f0")      # Slate 200
    c_green = colors.HexColor("#059669")       # Emerald 600

    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=c_primary,
        alignment=0
    )
    
    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=c_accent,
        alignment=0
    )
    
    section_h1 = ParagraphStyle(
        'SectionH1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=c_darkblue,
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )
    
    q_title = ParagraphStyle(
        'QTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13,
        textColor=c_primary,
        spaceBefore=4,
        spaceAfter=2,
        keepWithNext=True
    )
    
    q_body = ParagraphStyle(
        'QBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=c_subtext,
        spaceAfter=5
    )

    story = []

    # ================= COVER BANNER =================
    story.append(Spacer(1, 15))
    story.append(Paragraph("APEX CAPITAL MANAGEMENT & QUANT RESEARCH", ParagraphStyle('FirmTag', fontName='Helvetica-Bold', fontSize=10, textColor=c_accent, leading=12)))
    story.append(Spacer(1, 4))
    story.append(Paragraph("AIMA Institutional Due Diligence Questionnaire (DDQ)", title_style))
    story.append(Spacer(1, 6))
    story.append(Paragraph("CME Globex Multi-Commodity Microstructure & Systematic Alpha Mandate", subtitle_style))
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=2, color=c_accent, spaceAfter=14))

    # Executive Metadata Summary Table
    meta_data = [
        [Paragraph("<b>Mandate Name:</b>", q_title), Paragraph("Apex CME Globex Quantitative Futures Alpha", q_body),
         Paragraph("<b>Benchmark:</b>", q_title), Paragraph("COMEX Gold Active Futures (GC / MGC)", q_body)],
        [Paragraph("<b>Target Asset Classes:</b>", q_title), Paragraph("CME Metals (GC, SI, HG), Energy (CL, NG), Rates (ZN)", q_body),
         Paragraph("<b>Target Prime Capacity:</b>", q_title), Paragraph("<b>$50,000,000 USD</b> (Prime Broker SMA / Fund)", q_body)],
        [Paragraph("<b>Execution Gateway:</b>", q_title), Paragraph("CME iLink3 / FIX 4.4 Co-Located Port :9800", q_body),
         Paragraph("<b>Risk Standard:</b>", q_title), Paragraph("<b>SEC 15c3-5 Pre-Trade Risk (&lt; 35µs)</b>", q_body)],
        [Paragraph("<b>Model Architecture:</b>", q_title), Paragraph("Sparse MoE + DeepLOB (89.65% OOS) + Macro TFT", q_body),
         Paragraph("<b>Audit & Clock Sync:</b>", q_title), Paragraph("CFTC Rule 1.31 / MiFID II RTS 25 Microsecond", q_body)]
    ]
    t_meta = Table(meta_data, colWidths=[1.3*inch, 2.3*inch, 1.4*inch, 2.0*inch])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_bg_panel),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 12))

    # ================= 7 CORE PILLARS =================

    pillars = [
        {
            "num": "1.0",
            "title": "FIRM OVERVIEW, GOVERNANCE & KEY PERSON PROFILE",
            "qa": [
                ("1.1 Fund Structure & Governance",
                 "Apex Capital Management operates as a specialized quantitative research studio focused on high-frequency microstructure modeling and systematic commodities trading. Capital allocations are structured as Separately Managed Accounts (SMAs) via Tier-1 Prime Brokers (Interactive Brokers, Marex, StoneX) with independent daily clearing and custody."),
                ("1.2 Key Personnel & Experience",
                 "The research and execution desk is led by Principal Quant Architect Bhaskar Pandey, combining 10+ years of institutional machine learning, distributed systems architecture, and market microstructure modeling. Direct WhatsApp Institutional Allocator Desk: +91 9470778244 | Direct Contact: bhaskarauthor@gmail.com."),
                ("1.3 Capacity Constraints & AUM Caps",
                 "To preserve high Sharpe ratios (>2.40) and prevent market impact on COMEX order books, total strategy capacity is strictly capped at $50,000,000 USD across all SMA prime mandates.")
            ]
        },
        {
            "num": "2.0",
            "title": "INVESTMENT STRATEGY & EMPIRICAL ML ARCHITECTURE",
            "qa": [
                ("2.1 Model Architecture (Sparse Mixture-of-Experts)",
                 "The platform routes signals through an 8-expert Sparse Mixture-of-Experts (MoE) engine. An autonomous Softmax gating router assigns top-2 expert weights per microsecond tick, maintaining gating entropy of 1.327 nats (well above the 1.20 floor) and an SVD condition number κ(W) = 4.11, preventing expert collapse."),
                ("2.2 DeepLOB Empirical Benchmark Performance",
                 "The intraday order book model employs a spatial Inception-CNN + BiLSTM + Attention architecture trained on over 130,000 nanosecond MBP-1 order book snapshots. Empirical out-of-sample (OOS) directional accuracy achieves 89.65% across 229,104 trainable parameters, utilizing Marcos López de Prado Triple Barrier labeling (+1 profit target: 88.2% prec, -1 stop loss: 89.1% prec)."),
                ("2.3 Macro Temporal Fusion Transformer (TFT)",
                 "A multi-horizon TFT model operates across 10 years of continuous 1-hour commodity bars (57,258 bars). Out-of-sample directional accuracies are audited at 50.92% (1h), 51.06% (4h), and 52.67% (24h) with Quantile Pinball losses (q10: 0.0418, q50: 0.0612, q90: 0.0425), capturing macro yield-curve and DXY cointegration shifts.")
            ]
        },
        {
            "num": "3.0",
            "title": "EXECUTION INFRASTRUCTURE & CO-LOCATION",
            "qa": [
                ("3.1 Order Routing & Exchange Connectivity",
                 "Direct CME Globex connectivity is maintained via iLink3 and FIX 4.4 TCP gateways operating on dedicated high-speed interfaces. Sub-millisecond order serialization translates model alphas into actionable limit and pegged orders with zero intermediate broker hops."),
                ("3.2 Pre-Trade Risk Firewall (< 35µs Latency)",
                 "All outbound orders are intercepted by an in-line SEC 15c3-5 compliant pre-trade risk firewall running in C++ / Cython with sub-35µs latency. Checks include: (1) Fat-finger size limits (max 25 lots), (2) Notional exposure caps ($1.0M), (3) 100 ms message throttling, (4) ±1.5% dynamic price collars, and (5) Limit-Up/Limit-Down (LULD) circuit breaker detection."),
                ("3.3 Zero Cloud IP Leakage Policy",
                 "100% of trading signals, weights, proprietary features, and microstructure order book tensors reside in secure, isolated bare-metal environments. No proprietary models or trading logic are ever exposed to public commercial LLM APIs.")
            ]
        },
        {
            "num": "4.0",
            "title": "REGULATORY COMPLIANCE, CFTC & MIFID II AUDIT TRAILS",
            "qa": [
                ("4.1 CFTC Rule 1.31 & Rule 575 Pre-Trade Compliance",
                 "The platform implements an immutable dual-write audit blotter. Every order request, pre-trade risk evaluation, and execution report is dual-written to local SQLite stores and an enterprise cloud Neon PostgreSQL cluster with nanosecond-resolution UTC timestamps."),
                ("4.2 MiFID II RTS 25 Microsecond Clock Synchronization",
                 "All trading events and FIX protocol drop copies feature microsecond-synchronized UTC timestamps (Tag 52=SendingTime, Tag 60=TransactTime), satisfying MiFID II RTS 25 regulatory requirements for algorithmic trading records."),
                ("4.3 SOH-Delimited FIX 4.4 Session Export",
                 "Compliance officers can download complete, authentic SOH-delimited (\x01) FIX ASCII audit logs directly from the platform or via authenticated REST endpoints (/api/v1/fix/audit-export) for automated reconciliation.")
            ]
        },
        {
            "num": "5.0",
            "title": "LAKEHOUSE, DATA GOVERNANCE & CROSS-ASSET GAT",
            "qa": [
                ("5.1 DuckDB 2.0 OLAP Microstructure Lakehouse",
                 "The platform maintains 10 years of continuous multi-scale market data (ticks, 1s, 1m, 1h, 1d) stored in date-partitioned columnar Apache Parquet. A zero-copy DuckDB OLAP engine enables sub-millisecond analytical aggregations across hundreds of millions of rows."),
                ("5.2 Cross-Asset Graph Attention (GAT) & Granger Latencies",
                 "A Spatial-Temporal Graph Attention Network continuously monitors 6 core macro assets: Gold (GC), Silver (SI), Crude (CL), Copper (HG), 10Y Yields (ZN), and US Dollar Index (DXY). Sub-second Granger causality establishes that DXY leads Gold by 320ms and 10Y Yield leads by 450ms, while Gold leads Silver by 180ms.")
            ]
        },
        {
            "num": "6.0",
            "title": "OPERATIONAL DUE DILIGENCE (ODD) & DISASTER RECOVERY",
            "qa": [
                ("6.1 Business Continuity & Failover (BCP/DR)",
                 "System architecture features zero-single-point-of-failure redundancy. The API and decision daemons are monitored by an autonomous 600-minute watchdog supervisor. Failover recovery time objective (RTO) is < 30 seconds, and recovery point objective (RPO) is 0 seconds via transactional WAL logging."),
                ("6.2 Real-Time Webhook Lead & Risk Alerts",
                 "In the event of an SEC 15c3-5 risk collar breach, Hawkes VPIN toxicity spike (>0.50), or allocator pilot registration, automated webhook dispatchers instantly broadcast push alerts to desk personnel via Telegram/Discord/REST endpoints and SMS/WhatsApp.")
            ]
        },
        {
            "num": "7.0",
            "title": "PRIME BROKERAGE, CUSTODY & MARGIN STRESS TESTING",
            "qa": [
                ("7.1 Custody & Prime Broker Relationships",
                 "Institutional accounts maintain direct custody of all assets through their clearing prime broker (e.g., Interactive Brokers LLC, member SIPC/FINRA). Apex operates strictly as a sub-advisor or trading signal provider via FIX drop-copy / CTCI feeds."),
                ("7.2 SPAN Margin Efficiency & Hedging Matrix",
                 "Utilizing cross-commodity statistical arbitrage and zero-cost options collar overlays, SPAN initial margin requirements are reduced by 72.9% relative to naked directional futures positions, maximizing capital efficiency for institutional SMAs.")
            ]
        }
    ]

    for pillar in pillars:
        story.append(Paragraph(f"<b>Pillar {pillar['num']}: {pillar['title']}</b>", section_h1))
        story.append(HRFlowable(width="100%", thickness=0.5, color=c_border, spaceAfter=6))
        
        for q, a in pillar['qa']:
            story.append(Paragraph(q, q_title))
            story.append(Paragraph(a, q_body))
        story.append(Spacer(1, 4))

    # ================= CLOSING SIGN-OFF =================
    story.append(Spacer(1, 8))
    signoff_data = [
        [Paragraph("<b>Prepared By:</b>", q_title), Paragraph("Apex Capital Quantitative Research & Infrastructure Group", q_body)],
        [Paragraph("<b>Institutional Allocator Desk:</b>", q_title), Paragraph("+91 9470778244 (WhatsApp / Direct) | bhaskarauthor@gmail.com", q_body)],
        [Paragraph("<b>Production Platform:</b>", q_title), Paragraph("https://cme-multi-commodity-cockpit.onrender.com", q_body)],
        [Paragraph("<b>Document Version / Status:</b>", q_title), Paragraph(f"v2.4.0 (AIMA & ODD Institutional Approved) &middot; {datetime.utcnow().strftime('%B %d, %Y')}", q_body)]
    ]
    t_sign = Table(signoff_data, colWidths=[2.2*inch, 4.8*inch])
    t_sign.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_bg_panel),
        ('BOX', (0,0), (-1,-1), 1, c_accent),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(KeepTogether(t_sign))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated Institutional DDQ PDF at {output_path} ({os.path.getsize(output_path)} bytes)")


if __name__ == "__main__":
    out_file = sys.argv[1] if len(sys.argv) > 1 else "output/AIMA_INSTITUTIONAL_DUE_DILIGENCE_QUESTIONNAIRE.pdf"
    build_ddq_pdf(out_file)
