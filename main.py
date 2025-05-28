    import streamlit as st
import pandas as pd
from datetime import datetime
import time  # <-- ajout

    st.set_page_config(page_title="Suivi Bien-Être Personnel", layout="wide")

    def load_data():
        try:
            return pd.read_csv("data.csv")
        except:
            return pd.DataFrame(columns=["Date", "Sommeil (h)", "Activite physique (min)", "Humeur (/10)", "Calories consommees"])

    def save_data(df):
        df.to_csv("data.csv", index=False)

    st.title("📊 Suivi Bien-Être Personnel")

    # Load existing data
    df = load_data()

    # Add new entry section
    with st.form("entry_form"):
        date = st.date_input("Date", datetime.now())
        sommeil = st.number_input("Sommeil (h)", 0.0, 24.0, 7.0, 0.1)
        activite = st.number_input("Activité physique (min)", 0, 300, 30)
        humeur = st.slider("Humeur (/10)", 0, 10, 5)
        calories = st.number_input("Calories consommées", 0, 5000, 2000)

        if st.form_submit_button("Ajouter"):
            new_row = {
                "Date": date.strftime("%Y-%m-%d"),
                "Sommeil (h)": sommeil,
                "Activite physique (min)": activite,
                "Humeur (/10)": humeur,
                "Calories consommees": calories
            }
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            save_data(df)
            st.success("✅ Données ajoutées avec succès!")
            time.sleep(0.5)  # <-- ajout ici
            st.experimental_rerun()

    # Display data if available
    if not df.empty:
        st.markdown("## 📈 Évolution des métriques")

        # Basic statistics
        st.subheader("📊 Statistiques moyennes")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Sommeil", f"{df['Sommeil (h)'].mean():.1f} h")
        col2.metric("Activité", f"{df['Activite physique (min)'].mean():.0f} min")
        col3.metric("Humeur", f"{df['Humeur (/10)'].mean():.1f} /10")
        col4.metric("Calories", f"{df['Calories consommees'].mean():.0f} kcal")

        # Display raw data
        st.dataframe(df)
