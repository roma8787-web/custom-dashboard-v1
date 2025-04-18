import streamlit as st
import pandas as pd
import plotly.express as px
import json
import os
from utils import genera_commento_ai, crea_grafico

st.set_page_config(page_title="🤖 insight-analyzer-pro-ai", layout="wide")
st.title("🤖 insight-analyzer-pro-ai")

# === Tracciamento utilizzi ===
USER_TRACK_FILE = "user_tracker.json"
ACCESS_CODE = "KULO-KULO"

def load_tracker():
    if not os.path.exists(USER_TRACK_FILE):
        with open(USER_TRACK_FILE, "w") as f:
            json.dump({}, f)
    with open(USER_TRACK_FILE, "r") as f:
        return json.load(f)

def save_tracker(tracker):
    with open(USER_TRACK_FILE, "w") as f:
        json.dump(tracker, f)

# === Login utente ===
st.sidebar.header("🔑 Accesso utente")
user_input = st.sidebar.text_input("Inserisci il tuo codice o la tua email")

if user_input:
    tracker = load_tracker()
    is_access_code = user_input == ACCESS_CODE
    utilizzi = tracker.get(user_input, 0)

    if not is_access_code and utilizzi >= 5:
        st.error("Hai raggiunto il limite di 5 utilizzi gratuiti. Contattaci per sbloccare l'accesso completo.")
        st.stop()

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

            # === Se non è un codice, aggiorna l'utilizzo
            if not is_access_code:
                tracker[user_input] = utilizzi + 1
                save_tracker(tracker)

            # === Download dati
            with st.expander("📄 Dati analizzati"):
                st.dataframe(df)
                st.download_button(
                    label="📥 Scarica CSV",
                    data=df.to_csv(index=False),
                    file_name="dati_analizzati.csv",
                    mime="text/csv"
                )
else:
    st.info("Per favore inserisci la tua email o il tuo codice nella sidebar per iniziare.")
        
