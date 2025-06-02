import streamlit as st
import pandas as pd

st.title('DataFrame Examples')

dataframe = pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
})

st.dataframe(dataframe)

st.table(dataframe)

st.metric(label = '온도', value="10 °C", delta='1.2 °C')
st.metric(label = '삼성전자', value="61,000 원", delta='-1,200 원')

col1, col2, col3 = st.columns(3)
col1.metric(label = '달러(USD)', value="1,383 원", delta='-12.00원')
col2.metric(label = '엔화(JPY)_100엔', value="958.63 원", delta='-7.44원')
col3.metric(label = '유로(EUR))', value="1,3333.82 원", delta='11.44원')