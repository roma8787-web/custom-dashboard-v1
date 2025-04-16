import streamlit as st
import pandas as pd
import plotly.express as px
from utils import genera_commento_ai, crea_grafico

st.set_page_config(page_title="AI Report Assistant", layout="wide")
st.title("🤖 AI Report Assistant")

file = st.file_uploader("📂 Carica un file CSV", type="csv")

if file:
    df = pd.read_csv(file)
    st.subheader("📊 Anteprima dati")
    st.dataframe(df)

    colonna = st.selectbox("Scegli una colonna numerica da analizzare", df.select_dtypes("number").columns)

    if st.button("Analizza con AI"):
        st.subheader("🧠 Commento AI")
        commento = genera_commento_ai(df, colonna)
        st.write(commento)

        st.subheader("📈 Grafico")
        fig = crea_grafico(df, colonna)
        st.plotly_chart(fig)
        