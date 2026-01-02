import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="NutriLife Analytics",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# DARK PROFESSIONAL PALETTE
COLOR_PRIMARY = "#3B82F6"      # Blue
COLOR_SECONDARY = "#10B981"    # Emerald
COLOR_ACCENT = "#F59E0B"       # Amber
COLOR_DANGER = "#EF4444"       # Red
COLOR_TEXT_LIGHT = "#E2E8F0"   # Light Gray
COLOR_TEXT_MEDIUM = "#94A3B8"  # Medium Gray
COLOR_BG_DARK = "#0F172A"      # Very Dark Blue
COLOR_BG_CARD = "#1E293B"      # Dark Card
COLOR_BG_GLASS = "rgba(30, 41, 59, 0.7)"  # Glass effect
COLOR_BORDER = "#334155"       # Border color

# --- 2. GLASSMORPHISM CSS ---
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }}
    
    .stApp {{
        background: linear-gradient(135deg, {COLOR_BG_DARK} 0%, #1a1f3a 100%);
    }}
    
    /* Typography */
    h1, h2, h3, h4, h5, h6 {{
        color: {COLOR_TEXT_LIGHT} !important;
        font-weight: 600 !important;
        letter-spacing: -0.02em;
    }}
    
    h1 {{
        font-size: 2.5rem !important;
        margin-bottom: 0.5rem !important;
    }}
    
    h2 {{
        font-size: 1.5rem !important;
        margin-top: 2rem !important;
        margin-bottom: 1rem !important;
    }}
    
    p, div, span, li {{
        color: {COLOR_TEXT_MEDIUM} !important;
        line-height: 1.6;
    }}
    
    /* Sidebar - Glass Effect */
    section[data-testid="stSidebar"] {{
        background: rgba(15, 23, 42, 0.95);
        backdrop-filter: blur(10px);
        border-right: 1px solid {COLOR_BORDER};
    }}
    
    section[data-testid="stSidebar"] > div {{
        padding-top: 2rem;
    }}
    
    section[data-testid="stSidebar"] h1 {{
        color: {COLOR_PRIMARY} !important;
        font-size: 1.3rem !important;
        margin-bottom: 1.5rem !important;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        font-weight: 700 !important;
    }}
    
    /* Multiselect Container */
    .stMultiSelect {{
        margin-bottom: 8px;
    }}
    
    .stMultiSelect > label {{
        color: {COLOR_TEXT_LIGHT} !important;
        font-size: 0.75rem !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 8px !important;
    }}
    
    /* Multiselect Field Styling */
    .stMultiSelect > div > div {{
        background: {COLOR_BG_CARD};
        border: 1.5px solid {COLOR_BORDER};
        border-radius: 10px;
        transition: all 0.3s ease;
        padding: 8px 12px;
    }}
    
    .stMultiSelect > div > div:hover {{
        border-color: {COLOR_PRIMARY};
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15);
        background: rgba(30, 41, 59, 0.9);
    }}
    
    .stMultiSelect > div > div:focus-within {{
        border-color: {COLOR_PRIMARY};
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2);
    }}
    
    /* Selected Tags */
    .stMultiSelect span[data-baseweb="tag"] {{
        background: linear-gradient(135deg, {COLOR_PRIMARY} 0%, #2563eb 100%) !important;
        color: white !important;
        border-radius: 8px;
        padding: 6px 14px;
        font-weight: 600;
        font-size: 0.85rem;
        margin: 2px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3);
    }}
    
    /* Close button in tags */
    .stMultiSelect span[data-baseweb="tag"] svg {{
        fill: white;
        opacity: 0.8;
    }}
    
    .stMultiSelect span[data-baseweb="tag"] svg:hover {{
        opacity: 1;
    }}
    
    /* Dropdown menu */
    [data-baseweb="popover"] {{
        background: {COLOR_BG_CARD} !important;
        border: 1px solid {COLOR_BORDER} !important;
        border-radius: 10px !important;
    }}
    
    /* Multiselect options */
    [role="option"] {{
        color: {COLOR_TEXT_LIGHT} !important;
        transition: all 0.2s ease;
    }}
    
    [role="option"]:hover {{
        background: rgba(59, 130, 246, 0.2) !important;
    }}
    
    /* KPI Cards - Glassmorphism */
    div[data-testid="stMetric"] {{
        background: {COLOR_BG_GLASS};
        backdrop-filter: blur(20px);
        border: 1px solid {COLOR_BORDER};
        border-radius: 16px;
        padding: 28px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
        min-height: 150px;
    }}
    
    div[data-testid="stMetric"]:hover {{
        transform: translateY(-4px);
        box-shadow: 0 12px 48px rgba(59, 130, 246, 0.2);
        border-color: {COLOR_PRIMARY};
    }}
    
    div[data-testid="stMetricLabel"] {{
        font-size: 0.75rem !important;
        font-weight: 600 !important;
        color: {COLOR_TEXT_MEDIUM} !important;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 12px !important;
    }}
    
    div[data-testid="stMetricValue"] {{
        font-size: 2.25rem !important;
        font-weight: 700 !important;
        color: {COLOR_TEXT_LIGHT} !important;
        text-shadow: 0 2px 10px rgba(59, 130, 246, 0.3);
    }}
    
    div[data-testid="stMetricDelta"] {{
        font-size: 0.875rem !important;
        font-weight: 600 !important;
    }}
    
    /* Glass Chart Container */
    .glass-chart {{
        background: {COLOR_BG_GLASS};
        backdrop-filter: blur(20px);
        border: 1px solid {COLOR_BORDER};
        border-radius: 16px;
        padding: 28px;
        margin-bottom: 24px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }}
    
    /* Expander */
    .streamlit-expanderHeader {{
        background: {COLOR_BG_GLASS} !important;
        backdrop-filter: blur(20px);
        color: {COLOR_TEXT_LIGHT} !important;
        border: 1px solid {COLOR_BORDER} !important;
        border-radius: 12px !important;
        padding: 18px 24px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease;
    }}
    
    .streamlit-expanderHeader:hover {{
        border-color: {COLOR_PRIMARY} !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2);
    }}
    
    /* Divider */
    hr {{
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, {COLOR_BORDER}, transparent);
        margin: 3rem 0;
    }}
    
    /* Info Box */
    .stAlert {{
        background: {COLOR_BG_GLASS};
        backdrop-filter: blur(20px);
        border: 1px solid {COLOR_BORDER};
        border-left: 4px solid {COLOR_PRIMARY};
        border-radius: 12px;
        padding: 16px;
    }}
    
    .block-container {{
        padding-top: 3rem;
        padding-bottom: 2rem;
    }}
    
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    
    .stCaption {{
        color: {COLOR_TEXT_MEDIUM} !important;
        font-size: 0.9rem !important;
    }}
    
    /* Section Headers */
    .section-header {{
        color: {COLOR_TEXT_LIGHT} !important;
        font-size: 0.85rem !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        letter-spacing: 0.15em;
        margin-bottom: 12px !important;
        opacity: 0.8;
    }}
    
    /* Custom Dataframe */
    .stDataFrame {{
        background: {COLOR_BG_GLASS} !important;
        backdrop-filter: blur(20px);
        border-radius: 12px;
        border: 1px solid {COLOR_BORDER} !important;
    }}
    
    /* Dataframe headers */
    .stDataFrame thead tr th {{
        background: {COLOR_BG_CARD} !important;
        color: {COLOR_TEXT_LIGHT} !important;
        font-weight: 600 !important;
        border-bottom: 2px solid {COLOR_BORDER} !important;
        padding: 14px 12px !important;
    }}
    
    /* Dataframe cells */
    .stDataFrame tbody tr td {{
        background: rgba(30, 41, 59, 0.3) !important;
        color: {COLOR_TEXT_LIGHT} !important;
        border-bottom: 1px solid {COLOR_BORDER} !important;
        padding: 12px !important;
    }}
    
    /* Dataframe hover effect */
    .stDataFrame tbody tr:hover td {{
        background: rgba(59, 130, 246, 0.1) !important;
    }}
</style>
""", unsafe_allow_html=True)

# --- 3. DATA LOADING ---
@st.cache_data
def load_data():
    file_path = 'data/processed/supplements_enriched.parquet'
    if not os.path.exists(file_path):
        file_path = '../data/processed/supplements_enriched.parquet'

    if os.path.exists(file_path):
        df = pd.read_parquet(file_path)
        df['category'] = df['category'].astype('category')
        return df
    else:
        return None

df = load_data()

if df is None:
    st.error("⚠ Data connection failed. Please check the file path.")
    st.stop()

# --- 4. SIDEBAR ---
with st.sidebar:
    st.title("PARAMETERS")
    st.markdown('<p class="section-header">Market Segment</p>', unsafe_allow_html=True)

    all_segments = df['segment_name'].unique()
    selected_segments = st.multiselect(
        "Select segments",
        options=all_segments,
        default=all_segments,
        label_visibility="collapsed"
    )

    st.markdown('<p class="section-header" style="margin-top: 24px;">Product Category</p>', unsafe_allow_html=True)
    all_categories = df['category'].unique()
    selected_categories = st.multiselect(
        "Select categories",
        options=all_categories,
        default=all_categories,
        label_visibility="collapsed"
    )


# Apply Filters
df_filtered = df[
    (df['segment_name'].isin(selected_segments)) &
    (df['category'].isin(selected_categories))
    ].copy()

df_filtered['magnesium_mg'] = df_filtered['magnesium_mg'].clip(lower=1)

# --- 5. HEADER ---
st.title("NutriLife Market Intelligence")
st.markdown(f"""
<div style='background: linear-gradient(135deg, rgba(59, 130, 246, 0.2) 0%, rgba(16, 185, 129, 0.2) 100%); 
            padding: 24px; border-radius: 16px; margin-bottom: 32px;
            border: 1px solid {COLOR_BORDER};
            backdrop-filter: blur(10px);'>
    <p style='color: {COLOR_TEXT_LIGHT} !important; margin: 0; font-size: 1rem; line-height: 1.6;'>
        <strong style='color: {COLOR_TEXT_LIGHT} !important;'>Dashboard Objective:</strong> Monitor product performance across pricing tiers and inventory levels.<br>
        Assists Product Management and Supply Chain teams in identifying high-value opportunities and stock risks.
    </p>
</div>
""", unsafe_allow_html=True)

# --- KPIs ---
st.markdown('<p class="section-header">KEY PERFORMANCE INDICATORS</p>', unsafe_allow_html=True)
st.caption("Real-time metrics for selected product range")

col1, col2, col3, col4 = st.columns(4)

total_products = len(df_filtered)
avg_price = df_filtered['price_eur'].mean()
avg_potency = (df_filtered['vitamin_c_mg'] + df_filtered['magnesium_mg']).mean()
critical_stock = len(df_filtered[df_filtered['stock_level'] < 20])

with col1:
    st.metric(
        "Total SKU Count",
        f"{total_products:,}"
    )
with col2:
    st.metric(
        "Avg Retail Price",
        f"€{avg_price:.2f}",
        delta=f"{avg_price/35*100-100:+.1f}% vs target"
    )
with col3:
    st.metric(
        "Avg Active Potency",
        f"{avg_potency:.0f} mg"
    )
with col4:
    st.metric(
        "Critical Stock",
        f"{critical_stock}",
        delta="Refill Needed",
        delta_color="inverse"
    )

st.markdown("---")

# --- PLOTLY THEME ---
plotly_layout = dict(
    template="plotly_dark",
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(
        family="Inter, sans-serif",
        color=COLOR_TEXT_LIGHT,
        size=12
    ),
    xaxis=dict(
        gridcolor='rgba(51, 65, 85, 0.3)',
        zerolinecolor='rgba(51, 65, 85, 0.5)'
    ),
    yaxis=dict(
        gridcolor='rgba(51, 65, 85, 0.3)',
        zerolinecolor='rgba(51, 65, 85, 0.5)'
    ),
    margin=dict(l=20, r=20, t=40, b=20),
    hoverlabel=dict(
        bgcolor=COLOR_BG_CARD,
        font_size=13,
        font_family="Inter",
        bordercolor=COLOR_PRIMARY,
        font_color=COLOR_TEXT_LIGHT
    ),
    modebar=dict(
        bgcolor='rgba(30, 41, 59, 0.8)',
        color=COLOR_TEXT_LIGHT,
        activecolor=COLOR_PRIMARY
    )
)

# --- CHARTS ROW 1: PRICING & INVENTORY SIDE BY SIDE ---
st.markdown('<p class="section-header">PRICING STRATEGY & INVENTORY ANALYSIS</p>', unsafe_allow_html=True)

col_chart1, col_chart2 = st.columns(2, gap="large")

with col_chart1:
    st.markdown(f"""
    <div class='glass-chart'>
        <h3 style='color: {COLOR_TEXT_LIGHT} !important; font-size: 1.1rem; margin-bottom: 8px;'>Pricing Distribution</h3>
        <p style='color: {COLOR_TEXT_MEDIUM} !important; font-size: 0.875rem; margin-bottom: 20px;'>Price spread across market segments</p>
    """, unsafe_allow_html=True)

    fig_price = go.Figure()

    for segment in df_filtered['segment_name'].unique():
        segment_data = df_filtered[df_filtered['segment_name'] == segment]['price_eur']

        color_map = {
            'High-Potency Premium': COLOR_SECONDARY,
            'Balanced / Standard': COLOR_PRIMARY,
            'Budget Essentials': COLOR_TEXT_MEDIUM
        }

        fig_price.add_trace(go.Box(
            y=segment_data,
            name=segment,
            marker_color=color_map.get(segment, COLOR_PRIMARY),
            marker=dict(
                line=dict(width=1.5, color=COLOR_BG_DARK),
                opacity=0.8
            ),
            boxmean=False,
            hovertemplate='<b>%{fullData.name}</b><br>Price: €%{y:.2f}<extra></extra>'
        ))

    fig_price.update_layout(
        **plotly_layout,
        xaxis_title="",
        yaxis_title="Price (€)",
        showlegend=False,
        height=380,
        hovermode='closest'
    )
    st.plotly_chart(fig_price, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col_chart2:
    st.markdown(f"""
    <div class='glass-chart'>
        <h3 style='color: {COLOR_TEXT_LIGHT} !important; font-size: 1.1rem; margin-bottom: 8px;'>Inventory Health</h3>
        <p style='color: {COLOR_TEXT_MEDIUM} !important; font-size: 0.875rem; margin-bottom: 20px;'>Average stock levels by category</p>
    """, unsafe_allow_html=True)

    stock_data = df_filtered.groupby('category')['stock_level'].mean().reset_index().sort_values('stock_level')

    fig_stock = px.bar(
        stock_data,
        x='stock_level',
        y='category',
        orientation='h',
        color='stock_level',
        color_continuous_scale=[
            [0, COLOR_DANGER],
            [0.5, COLOR_ACCENT],
            [1, COLOR_SECONDARY]
        ],
        text_auto='.0f'
    )
    fig_stock.update_layout(
        **plotly_layout,
        xaxis_title="Avg Stock Units",
        yaxis_title="",
        coloraxis_showscale=False,
        height=380,
        hovermode='closest'
    )
    fig_stock.update_traces(
        textposition='inside',
        textfont=dict(size=13, color='white', weight=600),
        insidetextanchor='end',
        hovertemplate='<b>%{y}</b><br>Avg Stock: %{x:.0f} units<extra></extra>'
    )
    st.plotly_chart(fig_stock, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")

# --- CHART 3: SCATTER ---
st.markdown('<p class="section-header">PRODUCT SEGMENTATION MAP</p>', unsafe_allow_html=True)

st.markdown(f"""
<div class='glass-chart'>
    <h3 style='color: {COLOR_TEXT_LIGHT} !important; font-size: 1.1rem; margin-bottom: 8px;'>ML Clustering Analysis</h3>
    <p style='color: {COLOR_TEXT_MEDIUM} !important; font-size: 0.875rem; margin-bottom: 20px;'>Relationship between product potency, pricing, and market positioning</p>
""", unsafe_allow_html=True)

fig_scatter = px.scatter(
    df_filtered,
    x="vitamin_c_mg",
    y="price_eur",
    color="segment_name",
    size="magnesium_mg",
    hover_name="product_name",
    labels={
        "segment_name": "Market Segment",
        "vitamin_c_mg": "Vitamin C Content (mg)",
        "price_eur": "Price (€)",
        "magnesium_mg": "Magnesium (mg)"
    },
    hover_data={
        'vitamin_c_mg': ':.0f',
        'price_eur': ':.2f',
        'magnesium_mg': ':.0f',
        'segment_name': False
    },
    color_discrete_map={
        'High-Potency Premium': COLOR_SECONDARY,
        'Balanced / Standard': COLOR_PRIMARY,
        'Budget Essentials': COLOR_TEXT_MEDIUM
    },
    size_max=25,
    opacity=0.75
)

fig_scatter.update_layout(
    **plotly_layout,
    legend_title_text="Market Segment",
    xaxis_title="Vitamin C Content (mg)",
    yaxis_title="Price (€)",
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1,
        bgcolor="rgba(30, 41, 59, 0.8)",
        bordercolor=COLOR_BORDER,
        borderwidth=1
    ),
    height=500
)

fig_scatter.update_traces(
    marker=dict(
        line=dict(width=1, color=COLOR_BG_DARK)
    )
)
st.plotly_chart(fig_scatter, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

# --- TABLE ---
st.markdown("---")
st.markdown('<p class="section-header">DETAILED DATA VIEW</p>', unsafe_allow_html=True)
st.caption("Drill down into individual SKU details")

with st.expander("▸ Product Inventory Table", expanded=False):
    st.dataframe(
        df_filtered[['product_name', 'category', 'segment_name', 'price_eur', 'stock_level']],
        use_container_width=True,
        hide_index=True,
        height=400,
        column_config={
            "product_name": st.column_config.TextColumn(
                "Product Name",
                width="large"
            ),
            "category": st.column_config.TextColumn(
                "Category",
                width="medium"
            ),
            "segment_name": st.column_config.TextColumn(
                "Market Segment",
                width="medium"
            ),
            "price_eur": st.column_config.NumberColumn(
                "Retail Price",
                format="€%.2f",
                width="small"
            ),
            "stock_level": st.column_config.ProgressColumn(
                "Stock Status",
                format="%d units",
                min_value=0,
                max_value=500,
                width="medium"
            ),
        }
    )


# --- FOOTER ---
st.markdown("---")
st.markdown(f"""
<div style='text-align: center; color: {COLOR_TEXT_MEDIUM}; font-size: 0.875rem; padding: 20px 0;'>
    <strong style='color: {COLOR_TEXT_LIGHT} !important;'>NutriLife Analytics Dashboard</strong> | Powered by Streamlit & Plotly<br>
</div>
""", unsafe_allow_html=True)