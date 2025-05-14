
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Configuration de la page
st.set_page_config(page_title="Suivi Bien-Être Personnel", layout="wide")

# Chargement des données
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("data.csv", parse_dates=['Date'])
        return df.sort_values('Date', ascending=True)
    except:
        return pd.DataFrame(columns=["Date", "Sommeil (h)", "Activite physique (min)", "Humeur (/10)", "Calories consommees"])

# Fonction pour sauvegarder les données
def save_data(df):
    df.to_csv("data.csv", index=False)

df = load_data()

st.title("📊 Suivi Bien-Être Personnel")

# Section pour ajouter des données
with st.expander("➕ Ajouter une nouvelle entrée"):
    with st.form("entry_form"):
        col1, col2 = st.columns(2)
        with col1:
            date = st.date_input("Date", datetime.now())
            sommeil = st.number_input("Sommeil (h)", 0.0, 24.0, 7.0, 0.1)
            activite = st.number_input("Activité physique (min)", 0, 300, 30)
        with col2:
            humeur = st.slider("Humeur (/10)", 0, 10, 5)
            calories = st.number_input("Calories consommées", 0, 5000, 2000)
        
        submitted = st.form_submit_button("Ajouter")
        if submitted:
            # Convert date to string format first
            date_str = date.strftime('%Y-%m-%d')
            new_data = pd.DataFrame([{
                "Date": pd.Timestamp(date),
                "Sommeil (h)": sommeil,
                "Activite physique (min)": activite,
                "Humeur (/10)": humeur,
                "Calories consommees": calories
            }])
            df = pd.concat([df, new_data], ignore_index=True)
            df = df.sort_values('Date', ascending=True)
            save_data(df)
            st.success("✅ Données ajoutées avec succès!")
            st.experimental_rerun()

st.markdown("Bienvenue dans votre application de suivi bien-être.")

if not df.empty:
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
else:
    st.info("👆 Commencez par ajouter des données en utilisant le formulaire ci-dessus.")
