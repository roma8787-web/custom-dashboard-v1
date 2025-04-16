import streamlit as st
import pandas as pd
import plotly.express as px
import json
import os
from utils import genera_commento_ai, crea_grafico

st.set_page_config(page_title="AI Report Assistant", layout="wide")
st.title("🤖 AI Report Assistant")

# === Config ===
USER_TRACK_FILE = "user_tracker.json"
CODICE_PERSONALE = "KULO-KULO"

# === Funzioni per tracciamento ===
def load_tracker():
    if not os.path.exists(USER_TRACK_FILE):
        with open(USER_TRACK_FILE, "w") as f:
            json.dump({}, f)
    with open(USER_TRACK_FILE, "r") as f:
        return json.load(f)

def save_tracker(tracker):
    with open(USER_TRACK_FILE, "w") as f:
        json.dump(tracker, f)

# === Accesso utente ===
st.sidebar.header("🔑 Accesso utente")
user_email = st.sidebar.text_input("Inserisci la tua email o codice personale")

if user_email:
    tracker = load_tracker()

    # Controllo se ha inserito il codice segreto
    if user_email == CODICE_PERSONALE:
        st.success("🎉 Accesso illimitato attivato! Bentornato capo 👑")
        utilizzi = -1  # codice speciale per uso illimitato
    else:
        utilizzi = tracker.get(user_email, 0)
        if utilizzi >= 5:
            st.error("❌ Hai raggiunto il limite di 5 utilizzi gratuiti. Contattaci per sbloccare l'accesso completo.")
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

            if utilizzi != -1:
                tracker[user_email] = utilizzi + 1
                save_tracker(tracker)
else:
    st.info("Per favore inserisci la tua email o codice nella sidebar per iniziare.")
        