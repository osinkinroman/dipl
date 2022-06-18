import streamlit as st
from datetime import date
import yfinance as yf
from fbprophet import Prophet
from fbprophet.plot import plot_plotly
from plotly import graph_objs as go


stocks = ('BTC-USD', 'ETH-USD', 'USDT-USD', 'USDC-USD', 'BNB-USD', 'BUSD-USD','ADA-USD', 'XRP-USD','SOL-USD', 'DOT-USD','HEX-USD','DOGE-USD','DAI-USD','TRX-USD','WBTC-USD','LEO-USD','SHIB-USD','BIT1-USD','STETH-USD','AVAX-USD','LTC-USD','FTT-USD','MATIC-USD','LINK-USD','UNI1-USD','WEMIX-USD','OKB-USD','BCH-USD','XLM-USD','CRON1-USD','ALGO-USD','USDI-USD','NEAR-USD','XMR-USD','MIN-USD','TITAN-USD','ATOM-USD','MANA-USD','BTCB-USD','ETC-USD','FXS-USD','VET-USD','ICP-USD','HBAR-USD','XTZ-USD','THETA-USD','CAKE-USD','HNT-USD','USDP-USD','BSV-USD','SAND-USD','EGLD-USD','NEO-USD','PAXG-USD','EOS-USD','ZEC-USD','TUSD-USD','SENSO-USD','1INCH-USD','AXS-USD','HT-USD','KCS-USD','HBTC-USD','BNX-USD','AAVE-USD','MKR-USD','MIOTA-USD','XEC-USD','COMP1-ETH','AMP-USD','BLOK-USD','PAXG-USD','CDAI-USD','KLAY-USD','MX-USD','GT-USD','CHZ-USD','TEM-USD','ZIL-USD','LPNT-USD','WAVES-USD','GAL2-USD','QNT-USD','RUNE-USD','BAT-USD','DEP-USD','APE3-USD','CUSDT-USD','FIL-USD','DASH-USD','KSM-USD','LDO-USD','RVN-USD','GALA-USD','FLOW-USD','FTM-USD','STG1-USD')
START = "2015-01-01"
TODAY = date.today().strftime("%Y-%m-%d")


selected_stock = st.selectbox(' ', stocks)

n_years = st.slider('Количество лет для предсказания:', 1, 4)
period = n_years * 365


@st.cache
def load_data(ticker):
    data = yf.download(ticker, START, TODAY)
    data.reset_index(inplace=True)
    return data


#data_load_state = st.text('Loading data...')
data = load_data(selected_stock)
#data_load_state.text('Loading data... done!')

st.subheader('Пример изначальных данных')
st.write(data.tail())

# Plot raw data
def plot_raw_data():
	fig = go.Figure()
	fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name="открытие_позиции"))
	fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name="закрытие_позиции"))
	fig.layout.update(title_text='График всех действий с акциями с 2015 года', xaxis_rangeslider_visible=True)
	st.plotly_chart(fig)

plot_raw_data()

# Predict forecast with Prophet.
df_train = data[['Date','Close']]
df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})

m = Prophet()
m.fit(df_train)
future = m.make_future_dataframe(periods=period)
forecast = m.predict(future)

# Show and plot forecast
st.subheader('Пример обработанных данных предсказания графика')
st.write(forecast.tail())

if n_years == 1:
    st.write(f'График с предсказанием на {n_years} год')
else:
    st.write(f'График с предсказанием на {n_years} года')
fig1 = plot_plotly(m, forecast)
st.plotly_chart(fig1)

st.write("Компоненты предсказания")
fig2 = m.plot_components(forecast)
st.write(fig2)
