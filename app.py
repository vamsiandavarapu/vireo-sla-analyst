"""
Vireo Audio — Support SLA Analyst Web Application
=================================================
Interactive Analytical Dashboard & AI Operations Assistant for Support Operations.
Built with Streamlit & Plotly (Session State Persistent Results & Dynamic API Key Support).
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from sla_engine import SLAEngine, SLA_CREDIT_PER_BREACH_INR
from ai_analyst import AIAnalyst

# Page configuration
st.set_page_config(
    page_title="Vireo Audio — Support SLA Analyst",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Comprehensive Light Theme CSS
st.markdown("""
<style>
    /* Global App Background & Main Canvas */
    .stApp, [data-testid="stAppViewContainer"] {
        background-color: #f8fafc !important;
        color: #0f172a !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
    }
    
    /* Main Header Titles */
    .main-header {
        font-size: 38px !important;
        font-weight: 800 !important;
        color: #0f172a !important;
        margin-bottom: 6px !important;
        letter-spacing: -0.5px;
    }
    
    .sub-header {
        font-size: 18px !important;
        color: #475569 !important;
        margin-bottom: 28px !important;
        font-weight: 500 !important;
    }

    /* SIDEBAR CONTAINER STYLING */
    [data-testid="stSidebar"], [data-testid="stSidebarNav"] {
        background-color: #ffffff !important;
        border-right: 2px solid #e2e8f0 !important;
    }
    
    .sidebar-title {
        font-size: 22px !important;
        font-weight: 800 !important;
        color: #0f172a !important;
        margin-bottom: 20px !important;
        padding-bottom: 10px !important;
        border-bottom: 2px solid #cbd5e1 !important;
    }

    /* FILTER WIDGET LABELS */
    label[data-testid="stWidgetLabel"], .stSelectbox label, .stMultiSelect label, .stFileUploader label, .stTextInput label {
        font-size: 17px !important;
        font-weight: 700 !important;
        color: #0f172a !important;
        margin-bottom: 8px !important;
    }

    /* MULTISELECT & DROPDOWN CONTAINER */
    div[data-baseweb="select"] {
        border-radius: 12px !important;
        border: 2px solid #cbd5e1 !important;
        background-color: #ffffff !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04) !important;
    }
    
    div[data-baseweb="select"] * {
        background-color: transparent !important;
        color: #0f172a !important;
    }

    /* MULTISELECT DROPDOWN MENU POPOVER */
    div[data-baseweb="popover"], div[data-baseweb="menu"], ul[role="listbox"] {
        background-color: #ffffff !important;
        border: 2px solid #cbd5e1 !important;
        border-radius: 12px !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.12) !important;
    }

    /* DROPDOWN OPTION LIST ITEMS */
    li[role="option"], div[role="option"], [data-baseweb="menu"] li, [data-baseweb="menu"] div {
        background-color: #ffffff !important;
        color: #0f172a !important;
        font-size: 16px !important;
        font-weight: 600 !important;
        padding: 10px 14px !important;
    }

    /* HOVERED / SELECTED OPTION ITEM */
    li[role="option"]:hover, div[role="option"]:hover, [aria-selected="true"] {
        background-color: #f1f5f9 !important;
        color: #ff4b4b !important;
    }

    /* MULTISELECT TAG PILLS */
    span[data-baseweb="tag"] {
        background-color: #ffe4e6 !important;
        border: 1px solid #fecdd3 !important;
        border-radius: 8px !important;
        padding: 4px 10px !important;
    }
    
    span[data-baseweb="tag"] span {
        color: #9f1239 !important;
        font-weight: 700 !important;
        font-size: 14px !important;
    }

    /* STREAMLIT RED/ORANGE CUSTOM ACTION & DOWNLOAD BUTTONS */
    button[kind="primary"], .stDownloadButton button, div.stButton > button {
        background-color: #ff4b4b !important;
        color: #0f172a !important;
        font-size: 16px !important;
        font-weight: 800 !important;
        border-radius: 12px !important;
        border: 1px solid #e2e8f0 !important;
        padding: 12px 24px !important;
        box-shadow: 0 4px 12px rgba(255, 75, 75, 0.25) !important;
        transition: all 0.2s ease !important;
    }

    button[kind="primary"]:hover, .stDownloadButton button:hover, div.stButton > button:hover {
        background-color: #e03e3e !important;
        color: #0f172a !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 16px rgba(255, 75, 75, 0.35) !important;
    }

    /* TOP KPI METRIC CARDS */
    .metric-card {
        background: #ffffff !important;
        border: 1.5px solid #cbd5e1 !important;
        border-radius: 16px !important;
        padding: 24px 28px !important;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.05) !important;
        margin-bottom: 16px !important;
    }
    
    .metric-label {
        font-size: 14px !important;
        font-weight: 800 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
        color: #475569 !important;
        margin-bottom: 8px !important;
    }
    
    .metric-value {
        font-size: 36px !important;
        font-weight: 800 !important;
        color: #0f172a !important;
        line-height: 1.1 !important;
    }
    
    .metric-subtitle {
        font-size: 14px !important;
        color: #64748b !important;
        margin-top: 10px !important;
        font-weight: 600 !important;
    }

    /* CALLOUT ALERT BOXES */
    .highlight-card {
        background: #fef2f2 !important;
        border: 1.5px solid #fecaca !important;
        border-left: 6px solid #dc2626 !important;
        border-radius: 14px !important;
        padding: 24px 28px !important;
        margin-bottom: 24px !important;
    }
    
    .highlight-title {
        font-size: 20px !important;
        font-weight: 800 !important;
        color: #991b1b !important;
        margin-bottom: 10px !important;
    }

    .highlight-body {
        font-size: 16px !important;
        color: #7f1d1d !important;
        line-height: 1.6 !important;
    }

    /* ENLARGED PROMINENT TABS */
    button[data-baseweb="tab"] {
        font-size: 19px !important;
        font-weight: 700 !important;
        padding: 16px 28px !important;
        color: #475569 !important;
        border-radius: 12px 12px 0px 0px !important;
        background-color: transparent !important;
    }
    
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #ff4b4b !important;
        border-bottom: 4px solid #ff4b4b !important;
        background-color: #ffffff !important;
        box-shadow: 0 -2px 12px rgba(0, 0, 0, 0.04) !important;
    }

    /* SECTION TITLES & PARAGRAPHS */
    .section-title {
        font-size: 24px !important;
        font-weight: 800 !important;
        color: #0f172a !important;
        margin-top: 16px !important;
        margin-bottom: 20px !important;
    }
    
    p, li, span {
        font-size: 16px !important;
        color: #1e293b !important;
        line-height: 1.6 !important;
    }
    
    /* TABLE CONTAINER */
    .stDataFrame {
        border-radius: 12px !important;
        overflow: hidden !important;
        border: 1.5px solid #cbd5e1 !important;
        background-color: #ffffff !important;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_and_process_data(uploaded_tickets_file=None):
    engine = SLAEngine()
    engine.load_data()
    
    # If user uploads a new tickets CSV dynamically
    if uploaded_tickets_file is not None:
        engine.tickets_raw = pd.read_csv(uploaded_tickets_file)
        
    engine.process_tickets()
    engine.map_historical_roster()
    kpis = engine.get_summary_kpis()
    return engine, kpis

def main():
    st.markdown('<div class="main-header">⚡ Vireo Audio — Support SLA Analyst</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Weekly First-Response SLA Analytics, Financial Impact & Operational Root Cause Diagnostics</div>', unsafe_allow_html=True)
    
    # Sidebar: Data Source Upload Config
    st.sidebar.markdown('<div class="sidebar-title">📁 Data Source & Settings</div>', unsafe_allow_html=True)
    uploaded_file = st.sidebar.file_uploader(
        "Upload Support Tickets (CSV):",
        type=["csv"],
        help="Upload a new tickets.csv export to run analytics on new support data dynamically."
    )

    # Load data dynamically
    with st.spinner("Processing support tickets dataset & historical roster mapping..."):
        engine, kpis = load_and_process_data(uploaded_tickets_file=uploaded_file)
        
    df_clean = engine.tickets_clean
    df_rostered = engine.tickets_rostered

    # Sidebar Filters
    st.sidebar.markdown('<div class="sidebar-title">🔍 Filter Dashboard</div>', unsafe_allow_html=True)
    
    selected_tier = st.sidebar.multiselect(
        "Agent Tier:",
        options=[1, 2],
        default=[1]
    )
    
    available_shifts = df_rostered['shift'].dropna().unique().tolist()
    selected_shifts = st.sidebar.multiselect(
        "Roster Shift:",
        options=available_shifts,
        default=available_shifts
    )
    
    available_channels = df_clean['channel'].unique().tolist()
    selected_channels = st.sidebar.multiselect(
        "Support Channel:",
        options=available_channels,
        default=available_channels
    )

    # Filtered dataset
    filtered_df = df_rostered[
        (df_rostered['tier'].isin(selected_tier)) &
        (df_rostered['shift'].isin(selected_shifts)) &
        (df_rostered['channel'].isin(selected_channels))
    ].copy()

    # Top KPI Metrics Row
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Total Clean Tickets</div>
            <div class="metric-value">{kpis['unique_tickets']:,}</div>
            <div class="metric-subtitle">Raw: {kpis['raw_ticket_rows']:,} (-{kpis['duplicate_rows_removed']} dupes)</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Overall Breach Rate</div>
            <div class="metric-value" style="color: #dc2626;">{kpis['overall_breach_rate']:.2f}%</div>
            <div class="metric-subtitle">{kpis['total_breaches']:,} breached tickets</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">SLA Credit Loss</div>
            <div class="metric-value" style="color: #d97706;">₹{kpis['sla_credit_exposure_inr']:,}</div>
            <div class="metric-subtitle">₹350 credit per breach</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Morning Shift Breach Rate</div>
            <div class="metric-value" style="color: #ff4b4b;">{kpis['t1_morning_breach_rate']:.2f}%</div>
            <div class="metric-subtitle">{kpis['t1_morning_breaches']:,} Morning breaches</div>
        </div>
        """, unsafe_allow_html=True)

    with col5:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Overnight Creation Share</div>
            <div class="metric-value" style="color: #7c3aed;">{kpis['morning_overnight_breach_share']:.1f}%</div>
            <div class="metric-subtitle">{kpis['morning_overnight_breaches']:,} created 22:00-06:00</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Main Navigation Tabs - RENAME TAB 5 TO "🤖 AI Intelligence"
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📈 Executive Overview",
        "🌅 Morning & Overnight Deep Dive",
        "👥 Agent Performance Leaderboard",
        "📱 Channel Breakdown",
        "🤖 AI Intelligence",
        "📥 Export Reports"
    ])

    # -------------------------------------------------------------
    # TAB 1: EXECUTIVE OVERVIEW
    # -------------------------------------------------------------
    with tab1:
        st.markdown('<div class="section-title">Weekly SLA Breach Trend & Financial Loss Overview</div>', unsafe_allow_html=True)
        
        weekly_df = engine.get_weekly_trends()
        
        # Enlarge chart height to 600px
        fig_weekly = px.line(
            weekly_df,
            x='created_week_ist',
            y='breach_rate',
            title="Weekly SLA Breach Rate (%) Over 18 Months",
            labels={'created_week_ist': 'Week Starting (IST)', 'breach_rate': 'Breach Rate (%)'},
            markers=True
        )
        fig_weekly.add_hline(
            y=15.0,
            line_dash="dash",
            line_color="#059669",
            line_width=3,
            annotation_text="Proposed Target (15.0%)",
            annotation_position="bottom right",
            annotation_font=dict(color="#059669", size=15, family="Inter, sans-serif")
        )
        fig_weekly.update_traces(line_color="#dc2626", line_width=3.5, marker=dict(size=9, color="#991b1b"))
        fig_weekly.update_layout(
            template="plotly_white",
            height=600,
            paper_bgcolor='#ffffff',
            plot_bgcolor='#f8fafc',
            font=dict(family="Inter, sans-serif", size=15, color="#0f172a"),
            title=dict(font=dict(size=22, color="#0f172a", family="Inter, sans-serif")),
            xaxis=dict(title_font=dict(size=16, color="#0f172a"), tickfont=dict(size=14, color="#0f172a"), gridcolor="#e2e8f0"),
            yaxis=dict(title_font=dict(size=16, color="#0f172a"), tickfont=dict(size=14, color="#0f172a"), gridcolor="#e2e8f0"),
            margin=dict(l=30, r=30, t=60, b=30)
        )
        st.plotly_chart(fig_weekly, use_container_width=True)

        col_w1, col_w2 = st.columns(2)
        with col_w1:
            st.markdown('<div class="section-title" style="font-size: 21px !important;">Shift Breach Rate Comparison (Tier 1)</div>', unsafe_allow_html=True)
            shift_df = engine.get_shift_breakdown()
            
            # Enlarge chart height to 540px
            fig_shift = px.bar(
                shift_df,
                x='shift',
                y='breach_rate',
                text='breach_rate',
                color='shift',
                title="Breach Rate by Roster Shift",
                labels={'breach_rate': 'Breach Rate (%)', 'shift': 'Roster Shift'},
                color_discrete_sequence=['#dc2626', '#2563eb', '#059669']
            )
            fig_shift.update_traces(texttemplate='%{text:.2f}%', textposition='outside', textfont=dict(size=16, color='#0f172a', family="Inter, sans-serif"))
            fig_shift.update_layout(
                template="plotly_white",
                height=540,
                showlegend=False,
                paper_bgcolor='#ffffff',
                plot_bgcolor='#f8fafc',
                font=dict(family="Inter, sans-serif", size=15, color="#0f172a"),
                title=dict(font=dict(size=20, color="#0f172a")),
                xaxis=dict(title_font=dict(size=16, color="#0f172a"), tickfont=dict(size=15, color="#0f172a")),
                yaxis=dict(title_font=dict(size=16, color="#0f172a"), tickfont=dict(size=14, color="#0f172a"), gridcolor="#e2e8f0")
            )
            st.plotly_chart(fig_shift, use_container_width=True)
            
        with col_w2:
            st.markdown('<div class="section-title" style="font-size: 21px !important;">SLA Credit Exposure by Support Channel</div>', unsafe_allow_html=True)
            channel_df = engine.get_channel_breakdown()
            
            # Enlarge chart height to 540px
            fig_chan = px.bar(
                channel_df,
                x='channel',
                y='sla_credit_inr',
                text='sla_credit_inr',
                color='channel',
                title="SLA Credit Financial Loss (₹) by Channel",
                labels={'sla_credit_inr': 'Total SLA Credit Loss (INR)', 'channel': 'Channel'},
                color_discrete_sequence=['#ff4b4b', '#d97706', '#0284c7', '#059669']
            )
            fig_chan.update_traces(texttemplate='₹%{text:,.0f}', textposition='outside', textfont=dict(size=16, color='#0f172a', family="Inter, sans-serif"))
            fig_chan.update_layout(
                template="plotly_white",
                height=540,
                showlegend=False,
                paper_bgcolor='#ffffff',
                plot_bgcolor='#f8fafc',
                font=dict(family="Inter, sans-serif", size=15, color="#0f172a"),
                title=dict(font=dict(size=20, color="#0f172a")),
                xaxis=dict(title_font=dict(size=16, color="#0f172a"), tickfont=dict(size=15, color="#0f172a")),
                yaxis=dict(title_font=dict(size=16, color="#0f172a"), tickfont=dict(size=14, color="#0f172a"), gridcolor="#e2e8f0")
            )
            st.plotly_chart(fig_chan, use_container_width=True)

    # -------------------------------------------------------------
    # TAB 2: MORNING SHIFT & OVERNIGHT DEEP DIVE
    # -------------------------------------------------------------
    with tab2:
        st.markdown('<div class="section-title">🌅 Root Cause Analysis: Morning Shift & Overnight Carryover Queue</div>', unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="highlight-card">
            <div class="highlight-title">🔍 Critical Operational Discovery:</div>
            <div class="highlight-body">
                While <b>Tier 1 Morning Shift (06:00 – 14:00 IST)</b> shows the highest breach rate at <b>32.16%</b>, data analysis proves that <b>77.81% of these breaches</b> (1,452 out of 1,866) originated from tickets submitted <b>overnight (22:00 – 06:00 IST)</b>.<br><br>
                Morning agents are <b>not underperforming during their shift</b>. Instead, they inherit a massive unassigned backlog at 06:00 AM IST that has already breached its SLA deadline!
            </div>
        </div>
        """, unsafe_allow_html=True)

        col_m1, col_m2 = st.columns(2)
        with col_m1:
            st.markdown('<div class="section-title" style="font-size: 21px !important;">Morning Shift: In-Shift Creation vs Overnight Carryover</div>', unsafe_allow_html=True)
            m_comp = pd.DataFrame({
                'Ticket Creation Window': ['Normal Hours (06:00-22:00 IST)', 'Overnight (22:00-06:00 IST)'],
                'Breach Rate (%)': [kpis['morning_normal_breach_rate'], kpis['morning_overnight_breach_rate']]
            })
            
            # Enlarge chart height to 560px
            fig_m = px.bar(
                m_comp,
                x='Ticket Creation Window',
                y='Breach Rate (%)',
                text='Breach Rate (%)',
                color='Ticket Creation Window',
                color_discrete_map={
                    'Normal Hours (06:00-22:00 IST)': '#059669',
                    'Overnight (22:00-06:00 IST)': '#dc2626'
                },
                title="Morning Shift Breach Rate Comparison"
            )
            fig_m.update_traces(texttemplate='%{text:.2f}%', textposition='outside', textfont=dict(size=16, color='#0f172a', family="Inter, sans-serif"))
            fig_m.update_layout(
                template="plotly_white",
                height=560,
                showlegend=False,
                paper_bgcolor='#ffffff',
                plot_bgcolor='#f8fafc',
                font=dict(family="Inter, sans-serif", size=15, color="#0f172a"),
                title=dict(font=dict(size=20, color="#0f172a")),
                xaxis=dict(title_font=dict(size=16, color="#0f172a"), tickfont=dict(size=15, color="#0f172a")),
                yaxis=dict(title_font=dict(size=16, color="#0f172a"), tickfont=dict(size=14, color="#0f172a"), gridcolor="#e2e8f0")
            )
            st.plotly_chart(fig_m, use_container_width=True)
            
        with col_m2:
            st.markdown('<div class="section-title" style="font-size: 21px !important;">Hourly Ticket Creation Distribution (IST)</div>', unsafe_allow_html=True)
            t1_df = df_rostered[df_rostered['tier'] == 1].copy()
            hourly = t1_df.groupby(['created_hour_ist', 'is_breach']).size().reset_index(name='count')
            hourly['Status'] = hourly['is_breach'].map({True: 'Breached', False: 'Within SLA'})
            
            # Enlarge chart height to 560px
            fig_h = px.histogram(
                hourly,
                x='created_hour_ist',
                y='count',
                color='Status',
                title="Ticket Volume & Breaches by Hour of Creation (IST)",
                labels={'created_hour_ist': 'Hour of Day (0-23 IST)', 'count': 'Tickets'},
                color_discrete_map={'Breached': '#dc2626', 'Within SLA': '#2563eb'},
                barmode='stack'
            )
            fig_h.update_layout(
                template="plotly_white",
                height=560,
                paper_bgcolor='#ffffff',
                plot_bgcolor='#f8fafc',
                font=dict(family="Inter, sans-serif", size=15, color="#0f172a"),
                title=dict(font=dict(size=20, color="#0f172a")),
                xaxis=dict(title_font=dict(size=16, color="#0f172a"), tickfont=dict(size=14, color="#0f172a")),
                yaxis=dict(title_font=dict(size=16, color="#0f172a"), tickfont=dict(size=14, color="#0f172a"), gridcolor="#e2e8f0"),
                legend=dict(font=dict(size=14, color="#0f172a"))
            )
            st.plotly_chart(fig_h, use_container_width=True)

    # -------------------------------------------------------------
    # TAB 3: AGENT & ROSTER LEADERBOARD
    # -------------------------------------------------------------
    with tab3:
        st.markdown('<div class="section-title">👥 Agent Performance & Roster Assignment Table</div>', unsafe_allow_html=True)
        st.markdown('<p style="font-size: 15px; color: #475569; font-weight: 500;">Note: Tier 2 agents manage multi-touch resolution cases measured in days, excluded from first-response volume comparisons.</p>', unsafe_allow_html=True)
        
        agent_df = engine.get_agent_leaderboard()
        
        # Format table cleanly
        display_agent = agent_df.copy()
        display_agent['breach_rate'] = display_agent['breach_rate'].map('{:.2f}%'.format)
        display_agent['sla_credit_inr'] = display_agent['sla_credit_inr'].map('₹{:,.0f}'.format)
        display_agent['avg_response_min'] = display_agent['avg_response_min'].map('{:.1f}m'.format)
        display_agent['avg_csat'] = display_agent['avg_csat'].map(lambda x: f"{x:.2f}" if pd.notna(x) else "No Response")
        
        st.dataframe(
            display_agent[[
                'agent_id', 'name', 'tier', 'shift', 'site', 'tickets',
                'breaches', 'breach_rate', 'sla_credit_inr', 'avg_response_min', 'avg_csat'
            ]],
            use_container_width=True,
            hide_index=True
        )

        st.markdown("<br><hr><br>", unsafe_allow_html=True)
        st.markdown('<div class="section-title">🔄 June Roster Boundary Reshuffle Diagnostic</div>', unsafe_allow_html=True)
        st.info("Context: Effective June 30, 2025, 3 Indore Chat Frontline agents moved from Night to Day shift.")
        
        reshuffle_df = engine.get_june_reshuffle_analysis()
        st.dataframe(reshuffle_df, use_container_width=True, hide_index=True)

    # -------------------------------------------------------------
    # TAB 4: CHANNEL BREAKDOWN
    # -------------------------------------------------------------
    with tab4:
        st.markdown('<div class="section-title">📱 Channel SLA Performance & Credit Loss</div>', unsafe_allow_html=True)
        
        ch_df = engine.get_channel_breakdown()
        st.dataframe(
            ch_df.rename(columns={
                'channel': 'Channel',
                'tickets': 'Total Tickets',
                'breaches': 'Breaches',
                'breach_rate': 'Breach Rate (%)',
                'sla_credit_inr': 'Credit Loss (₹)',
                'avg_response_min': 'Avg Response (Min)',
                'sla_target_min': 'SLA Target (Min)'
            }),
            use_container_width=True,
            hide_index=True
        )

    # -------------------------------------------------------------
    # TAB 5: AI INTELLIGENCE (WITH SESSION STATE PERSISTENCE)
    # -------------------------------------------------------------
    with tab5:
        st.markdown('<div class="section-title">🤖 Customer Complaint Analysis & Executive Summary Generator</div>', unsafe_allow_html=True)
        
        ai = AIAnalyst()
        
        col_ai1, col_ai2 = st.columns([1, 1])
        
        # 1. ANALYZE CUSTOMER COMPLAINTS (PERSISTED IN SESSION STATE)
        with col_ai1:
            st.markdown('<div class="section-title" style="font-size: 21px !important;">Analyze Operational Complaint Themes</div>', unsafe_allow_html=True)
            
            if st.button("Analyze Customer Complaints", type="primary"):
                with st.spinner("Classifying customer messages & agent notes..."):
                    breaches_df = df_rostered[df_rostered['is_breach']]
                    sample_classified = ai.classify_breach_sample(breaches_df, sample_size=50)
                    st.session_state['sample_classified'] = sample_classified

            # Display persisted result if available
            if 'sample_classified' in st.session_state:
                sample_classified = st.session_state['sample_classified']
                theme_counts = sample_classified['ai_category'].value_counts().reset_index()
                theme_counts.columns = ['Operational Delay Theme', 'Ticket Count']
                
                fig_themes = px.pie(
                    theme_counts,
                    names='Operational Delay Theme',
                    values='Ticket Count',
                    title="Breach Reason Distribution (Sample n=50)",
                    hole=0.4,
                    color_discrete_sequence=px.colors.qualitative.Set2
                )
                fig_themes.update_layout(
                    template="plotly_white",
                    height=540,
                    paper_bgcolor='#ffffff',
                    font=dict(family="Inter, sans-serif", size=15, color="#0f172a"),
                    title=dict(font=dict(size=20, color="#0f172a")),
                    legend=dict(font=dict(size=14, color="#0f172a"))
                )
                st.plotly_chart(fig_themes, use_container_width=True)
                
                st.dataframe(
                    sample_classified[['ticket_id', 'channel', 'shift', 'ai_category', 'customer_message']].head(10),
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.info("Click the button above to categorize breach customer notes & IVR transcripts.")

        # 2. CREATE MANAGER SUMMARY (PERSISTED IN SESSION STATE)
        with col_ai2:
            st.markdown('<div class="section-title" style="font-size: 21px !important;">Create Manager Executive Summary</div>', unsafe_allow_html=True)
            
            if st.button("Create Manager Summary", type="primary"):
                with st.spinner("Synthesizing evidence-grounded manager summary..."):
                    exec_summary = ai.generate_executive_summary(kpis)
                    st.session_state['exec_summary'] = exec_summary

            # Display persisted result if available
            if 'exec_summary' in st.session_state:
                st.markdown(st.session_state['exec_summary'])
            else:
                st.info("Click the button above to generate executive manager summary.")

    # -------------------------------------------------------------
    # TAB 6: EXPORT REPORTS
    # -------------------------------------------------------------
    with tab6:
        st.markdown('<div class="section-title">📥 Export Clean Data & Reports</div>', unsafe_allow_html=True)
        
        col_e1, col_e2 = st.columns(2)
        with col_e1:
            st.download_button(
                label="📥 Download Ticket Data (CSV)",
                data=filtered_df.to_csv(index=False).encode('utf-8'),
                file_name="vireo_clean_tickets_sla.csv",
                mime="text/csv",
                type="primary"
            )
        with col_e2:
            st.download_button(
                label="📥 Download Weekly Report (CSV)",
                data=engine.get_weekly_trends().to_csv(index=False).encode('utf-8'),
                file_name="vireo_weekly_breach_summary.csv",
                mime="text/csv",
                type="primary"
            )

if __name__ == '__main__':
    main()
