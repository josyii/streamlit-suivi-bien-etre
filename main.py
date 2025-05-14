import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Configuration de la page
st.set_page_config(page_title="Suivi Bien-Être Personnel", layout="wide")

# Chargement des données
def load_data():
    try:
        df = pd.read_csv("data.csv")
        df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%Y-%m-%d')
        return df.sort_values('Date')
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
        date = st.date_input("Date", datetime.now())
        sommeil = st.number_input("Sommeil (h)", 0.0, 24.0, 7.0, 0.1)
        activite = st.number_input("Activité physique (min)", 0, 300, 30)
        humeur = st.slider("Humeur (/10)", 0, 10, 5)
        calories = st.number_input("Calories consommées", 0, 5000, 2000)

        submitted = st.form_submit_button("Ajouter")
        if submitted:
            new_data = pd.DataFrame([{
                "Date": date.strftime('%Y-%m-%d'),
                "Sommeil (h)": sommeil,
                "Activite physique (min)": activite,
                "Humeur (/10)": humeur,
                "Calories consommees": calories
            }])
            df = pd.concat([df, new_data], ignore_index=True)
            df = df.sort_values('Date')
            save_data(df)
            st.success("✅ Données ajoutées avec succès!")
            st.experimental_rerun()

if not df.empty and len(df) >= 2:
    st.markdown("## 📈 Évolution des métriques")

    # Sélection de la période
    dates = sorted(df['Date'].unique())
    date_debut, date_fin = st.select_slider(
        "Sélectionner la période :",
        options=dates,
        value=(dates[0], dates[-1])
    )

    # Filtrage des données
    mask = (df['Date'] >= date_debut) & (df['Date'] <= date_fin)
    df_filtered = df[mask]

    # Graphique
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df_filtered['Date'], df_filtered['Sommeil (h)'], label='Sommeil (h)')
    ax.plot(df_filtered['Date'], df_filtered['Activite physique (min)'], label='Activité (min)')
    ax.plot(df_filtered['Date'], df_filtered['Humeur (/10)'], label='Humeur (/10)')
    plt.xticks(rotation=45)
    ax.legend()
    st.pyplot(fig)

    # Statistiques
    st.subheader("📊 Statistiques moyennes")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Sommeil", f"{df_filtered['Sommeil (h)'].mean():.1f} h")
    col2.metric("Activité", f"{df_filtered['Activite physique (min)'].mean():.0f} min")
    col3.metric("Humeur", f"{df_filtered['Humeur (/10)'].mean():.1f} /10")
    col4.metric("Calories", f"{df_filtered['Calories consommees'].mean():.0f} kcal")
else:
    st.info("👆 Commencez par ajouter des données en utilisant le formulaire ci-dessus.")