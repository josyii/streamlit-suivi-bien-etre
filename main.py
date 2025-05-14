
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Configuration de la page
st.set_page_config(page_title="Suivi Bien-Être Personnel", layout="wide")

# Chargement des données
@st.cache_data
def load_data():
    df = pd.read_csv("data.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    return df

df = load_data()

st.title("📊 Suivi Bien-Être Personnel")
st.markdown("Bienvenue dans votre application de suivi bien-être.")

date_min = df["Date"].min().to_pydatetime()
date_max = df["Date"].max().to_pydatetime()
date_range = st.slider("Sélectionner la période :", min_value=date_min, max_value=date_max, value=(date_min, date_max))
df_filtered = df[(df["Date"] >= date_range[0]) & (df["Date"] <= date_range[1])]

st.subheader("📈 Évolution quotidienne")
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(df_filtered["Date"], df_filtered["Sommeil (h)"], label="Sommeil (h)")
ax.plot(df_filtered["Date"], df_filtered["Activite physique (min)"], label="Activité (min)")
ax.plot(df_filtered["Date"], df_filtered["Humeur (/10)"], label="Humeur (/10)")
ax.set_xlabel("Date")
ax.set_ylabel("Valeurs")
ax.legend()
st.pyplot(fig)

st.subheader("📊 Statistiques moyennes")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Sommeil", f"{df_filtered['Sommeil (h)'].mean():.1f} h")
col2.metric("Activité", f"{df_filtered['Activite physique (min)'].mean():.0f} min")
col3.metric("Humeur", f"{df_filtered['Humeur (/10)'].mean():.1f} /10")
col4.metric("Calories", f"{df_filtered['Calories consommees'].mean():.0f} kcal")

if df_filtered['Sommeil (h)'].mean() < 6.5:
    st.warning("💤 Essayez d'augmenter votre sommeil pour améliorer votre humeur.")
else:
    st.success("✅ Votre durée de sommeil semble satisfaisante !")
