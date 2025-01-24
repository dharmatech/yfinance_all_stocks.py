
import analysis.pct_spx_components_rsi_above_75

import yfinance_download

import streamlit as st

import plotly.graph_objects as go

spy = yfinance_download.load_records(symbol='SPY', interval='1d')

@st.cache_data
def load_data():
    
    df = analysis.pct_spx_components_rsi_above_75.pct_spx_rsi_above(75)

    return df

df = load_data()

fig = go.Figure()

fig.add_trace(go.Scatter(x=spy.index, y=spy['Close'], mode='lines', name='SPY Close Price'))

fig.add_trace(go.Scatter(x=df['Date'], y=df['pct_greater_than_75'], mode='lines', name='SPX Components RSI > 75', yaxis='y2'))

fig.update_layout(
    title='SPY and RSI Pct Greater Than 75',
    xaxis_title='Date',
    yaxis=dict(
        title='SPY Close Price'
    ),
    yaxis2=dict(
        title='Pct Greater Than 75',
        overlaying='y',
        side='right',
        showgrid=False,
        range=[0, 100]
    )
)

st.plotly_chart(fig)