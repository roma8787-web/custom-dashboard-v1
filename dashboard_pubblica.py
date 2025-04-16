import pandas as pd
import streamlit as st
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="Custom Dashboard v1", layout="wide")

# === Caricamento dati ===
import os
file_path = os.path.join(os.path.dirname(__file__), "dati_clienti_50.csv")
dati = pd.read_csv(file_path)

# === Pulizia ===
dati["Data"] = pd.to_datetime(dati["Data"], errors="coerce")
dati["Quantità"] = pd.to_numeric(dati["Quantità"], errors="coerce")
dati["Prezzo_unitario"] = pd.to_numeric(dati["Prezzo_unitario"], errors="coerce")
dati["Totale"] = pd.to_numeric(dati["Totale"], errors="coerce")
dati = dati.dropna(subset=["Data", "Totale"])

# === Sidebar: filtri dinamici ===
st.sidebar.header("🎛️ Filtri dinamici")
clienti = ["Tutti"] + sorted(dati["Cliente"].dropna().unique())
città = ["Tutte"] + sorted(dati["Città"].dropna().unique())
prodotti = ["Tutti"] + sorted(dati["Prodotto"].dropna().unique())

cliente_sel = st.sidebar.selectbox("Cliente", clienti)
città_sel = st.sidebar.selectbox("Città", città)
prodotto_sel = st.sidebar.selectbox("Prodotto", prodotti)

data_min = dati["Data"].min().date()
data_max = dati["Data"].max().date()
data_da, data_a = st.sidebar.date_input("Intervallo date", (data_min, data_max))

# === Applica i filtri ===
filtro = dati.copy()
if cliente_sel != "Tutti":
    filtro = filtro[filtro["Cliente"] == cliente_sel]
if città_sel != "Tutte":
    filtro = filtro[filtro["Città"] == città_sel]
if prodotto_sel != "Tutti":
    filtro = filtro[filtro["Prodotto"] == prodotto_sel]
filtro = filtro[(filtro["Data"].dt.date >= data_da) & (filtro["Data"].dt.date <= data_a)]

# === KPI ===
totale = filtro["Totale"].sum()
transazioni = filtro.shape[0]
prodotti_unici = filtro["Prodotto"].nunique()
ticket_medio = totale / transazioni if transazioni > 0 else 0

st.title("📊 Custom Dashboard v1")
st.markdown("Report dinamico con filtri per cliente, prodotto, città e intervallo temporale.")

col1, col2, col3, col4 = st.columns(4)
col1.metric("💰 Totale vendite", f"€ {totale:.2f}")
col2.metric("🧾 Transazioni", transazioni)
col3.metric("📦 Prodotti unici", prodotti_unici)
col4.metric("🎯 Ticket medio", f"€ {ticket_medio:.2f}")

st.markdown("---")

# === Andamento vendite nel tempo ===
filtro["Periodo"] = filtro["Data"].dt.to_period("M").apply(lambda r: r.start_time.date())
serie_temporale = filtro.groupby("Periodo")["Totale"].sum().reset_index()
fig_tempo = px.line(serie_temporale, x="Periodo", y="Totale", title="📆 Vendite mensili", markers=True)
st.plotly_chart(fig_tempo)

# === Grafico per città ===
st.subheader("📍 Vendite per città")
vendite_città = filtro.groupby("Città")["Totale"].sum().reset_index()
fig_città = px.bar(vendite_città, x="Città", y="Totale", title="Totale vendite per città")
st.plotly_chart(fig_città)

# === Grafico per prodotto ===
st.subheader("📦 Vendite per prodotto")
vendite_prodotto = filtro.groupby("Prodotto")["Totale"].sum().reset_index()
fig_prodotto = px.pie(vendite_prodotto, names="Prodotto", values="Totale", title="Distribuzione vendite per prodotto")
st.plotly_chart(fig_prodotto)

# === Grafico per cliente ===
st.subheader("🧑‍💼 Vendite per cliente")
vendite_cliente = filtro.groupby("Cliente")["Totale"].sum().reset_index()
fig_cliente = px.pie(vendite_cliente, names="Cliente", values="Totale", title="Distribuzione vendite per cliente")
st.plotly_chart(fig_cliente)

# === Tabella + download ===
with st.expander("📄 Dati filtrati"):
    st.dataframe(filtro)

st.download_button("📥 Scarica CSV", data=filtro.to_csv(index=False), file_name="dati_filtrati.csv", mime="text/csv")