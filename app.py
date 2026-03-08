import streamlit as st
import FinanceDataReader as fdr
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import plotly.graph_objects as go
from datetime import datetime, timedelta

st.title("📈 AI 주가 예측 서비스")

code = st.text_input("종목 코드 6자리를 입력하세요", value="005930")

if st.button("분석 시작"):
    try:
        # 데이터 수집
        df = fdr.DataReader(code, datetime.now() - timedelta(days=365), datetime.now())

        # AI 예측 (가장 가벼운 모델)
        model = ExponentialSmoothing(df['Close'], trend='add').fit()
        forecast = model.forecast(14) # 14일 예측

        # 차트 생성
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df.index[-60:], y=df['Close'].tail(60), name='과거 주가'))
        f_dates = [df.index[-1] + timedelta(days=i) for i in range(1, 15)]
        fig.add_trace(go.Scatter(x=f_dates, y=forecast, name='AI 예측', line=dict(dash='dash', color='red')))

        st.plotly_chart(fig)
        st.success(f"예측 완료! 14일 뒤 예상가: {forecast.iloc[-1]:,.0f}원")
    except:
        st.error("코드를 확인해주세요.")
