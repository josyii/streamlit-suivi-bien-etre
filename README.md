# 📊 Application Streamlit – Suivi Bien-Être Personnel

Cette application Streamlit permet de visualiser et d'analyser des données personnelles de bien-être sur 60 jours :  
**sommeil**, **activité physique**, **humeur** et **alimentation**.

---

## 🎯 Objectif

Offrir une interface simple et interactive pour suivre l’évolution de ses habitudes quotidiennes  
et identifier des corrélations entre différents aspects de la santé.

---

## 🛠️ Technologies utilisées

- [Python](https://www.python.org/)
- [Pandas](https://pandas.pydata.org/)
- [Matplotlib](https://matplotlib.org/)
- [Streamlit](https://streamlit.io/)

---

## 📁 Contenu du projet
streamlit-suivi-bien-etre/
├── main.py                  # Application principale Streamlit
├── data.csv                # Données bien-être simulées (60 jours)
└── README.md               # Présentation du projet

---

## ⚙️ Fonctionnalités

- Sélection d’une **plage de dates** via un slider
- Graphique de l’évolution du **sommeil**, de l’**activité physique** et de la **humeur**
- Affichage de **statistiques moyennes** (durée de sommeil, activité, humeur, calories)
- **Recommandation personnalisée** en fonction du niveau de sommeil

---

## ▶️ Lancer l'application localement

```bash
pip install streamlit pandas matplotlib
streamlit run app.py