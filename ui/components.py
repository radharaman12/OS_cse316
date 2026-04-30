import streamlit as st
import plotly.graph_objects as go

def inject_css(css_file_path: str):
    """Reads a CSS file and injects it into Streamlit."""
    try:
        with open(css_file_path, "r", encoding="utf-8") as f:
            css = f.read()
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"Could not find CSS file at {css_file_path}")

def create_premium_area_chart(df, y_cols, title, colors, height=280):
    """Generates an aesthetic area chart for timeseries telemetry."""
    fig = go.Figure()
    for i, col in enumerate(y_cols):
        color = colors[i % len(colors)]
        # convert hex to rgba for Plotly
        fill_color = color
        if 'rgb' in color:
            fill_color = color.replace('rgb', 'rgba').replace(')', ', 0.15)')
        elif color.startswith('#'):
            hex_color = color.lstrip('#')
            if len(hex_color) == 6:
                r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
                fill_color = f"rgba({r},{g},{b},0.15)"
            
        fig.add_trace(go.Scatter(
            x=df['Time'], y=df[col],
            mode='lines',
            name=col,
            line=dict(width=3, color=color, shape='spline', smoothing=0.8),
            fill='tozeroy',
            fillcolor=fill_color,
            hoverinfo='y+name'
        ))
    
    fig.update_layout(
        height=height,
        title=dict(text=title, font=dict(family="Space Grotesk", size=18, color="#f8fafc"), pad=dict(b=20)),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=50, b=0),
        xaxis=dict(showgrid=False, showticklabels=False),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', gridwidth=1, zeroline=False),
        font=dict(family="Inter", color="#94a3b8"),
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="right", x=1),
        hoverlabel=dict(bgcolor="rgba(17,24,39,0.9)", font_size=13, font_family="Inter")
    )
    return fig

def create_gauge_chart(value, title, threshold_warn, threshold_crit, color):
    """Generates a styled gauge meter chart."""
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = value,
        title = {'text': title, 'font': {'size': 16, 'family': 'Space Grotesk', 'color': '#94a3b8'}},
        number = {'suffix': "%", 'font': {'size': 36, 'family': 'Space Grotesk', 'color': '#fff'}},
        gauge = {
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "rgba(255,255,255,0.1)"},
            'bar': {'color': color},
            'bgcolor': "rgba(255,255,255,0.05)",
            'borderwidth': 0,
            'steps': [
                {'range': [0, threshold_warn], 'color': 'rgba(255,255,255,0.0)'},
                {'range': [threshold_warn, threshold_crit], 'color': 'rgba(245, 158, 11, 0.15)'},
                {'range': [threshold_crit, 100], 'color': 'rgba(244, 63, 94, 0.2)'}],
            'threshold': {
                'line': {'color': "rgba(244, 63, 94, 0.8)", 'width': 2},
                'thickness': 0.75, 'value': threshold_crit}
        }
    ))
    fig.update_layout(height=250, margin=dict(l=40, r=40, t=50, b=20), paper_bgcolor='rgba(0,0,0,0)', font={'family': "Inter"})
    return fig

def premium_metric(title, value, delta, delay=0.1, icon=""):
    """Renders a custom HTML metric component with glassmorphism."""
    delta_class = "delta-positive" if delta < 0 else "delta-negative" if delta > 0 else "delta-neutral"
    delta_icon = "↓" if delta < 0 else "↑" if delta > 0 else "−"
    delta_text = f"{delta_icon} {abs(delta)}%"
    
    html = f'''
    <div class="premium-metric" style="animation-delay: {delay}s;">
        <div class="premium-metric-title"><span>{title}</span> <span>{icon}</span></div>
        <div class="premium-metric-value">{value}</div>
        <div class="premium-metric-delta {delta_class}">
            {delta_text} <span style="color:var(--text-muted); font-size:0.75rem; margin-left:4px;">vs baseline</span>
        </div>
    </div>
    '''
    st.markdown(html, unsafe_allow_html=True)
