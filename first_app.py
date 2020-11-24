import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy as np
import pandas as pd

@st.cache  # 👈 This function will be cached
def gen_data():
    return np.random.randn(10, 20)

dataframe = gen_data()
st.dataframe(dataframe)

x = st.slider('x')  # 👈 this is a widget
st.write(x, 'squared is', x * x)