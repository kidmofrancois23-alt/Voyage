import streamlit as st
import pandas as pd
from datetime import datetime

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="VoyageCollect - INF232",
    page_icon="🌍",
    layout="wide"
)

# --- STYLE PERSONNALISÉ (CSS) ---
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #007BFF;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# --- INITIALISATION DE LA SESSION ---
if 'db_voyages' not in st.session_state:
    st.session_state.db_voyages = pd.DataFrame(columns=[
        "Voyageur", "Départ", "Destination", "Type", "Transport", "Date", "Note", "Commentaire"
    ])

# --- BARRE LATÉRALE ---
st.sidebar.header("À propos")
st.sidebar.info("Application de collecte de données touristiques pour le TP INF232.")
st.sidebar.metric("Total Collecté", len(st.session_state.db_voyages))

# --- TITRE PRINCIPAL ---
st.title("🌍 Système de Collecte : Expériences de Voyage")
st.write("Veuillez remplir le formulaire ci-dessous pour enregistrer une nouvelle étape de voyage.")

# --- FORMULAIRE DE COLLECTE ---
with st.container():
    with st.form("form_voyage", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            nom = st.text_input("Nom du voyageur", placeholder="Ex: Jean Dupont")
            depart = st.text_input("Point de départ", placeholder="Ex: Douala") # Ajout demandé
            destination = st.text_input("Destination (Ville, Pays)", placeholder="Ex: Kribi, Cameroun")
            type_voyage = st.selectbox("Type de séjour", ["Vacances", "Affaires", "Humanitaire", "Études"])
        
        with col2:
            transport = st.radio("Moyen de transport principal", ["Avion", "Train", "Bus", "Voiture"], horizontal=True)
            date_sejour = st.date_input("Date de fin de séjour", datetime.now())
            note = st.select_slider("Note globale de l'expérience", options=[1, 2, 3, 4, 5], value=3)

        commentaire = st.text_area("Observations (Points forts / Points faibles)", height=100)
        
        submit_button = st.form_submit_button("Enregistrer les données")

# --- LOGIQUE DE TRAITEMENT ---
if submit_button:
    if nom and depart and destination and commentaire:
        nouvelle_donnee = {
            "Voyageur": nom,
            "Départ": depart, # Ajout demandé
            "Destination": destination,
            "Type": type_voyage,
            "Transport": transport,
            "Date": date_sejour.strftime("%Y-%m-%d"),
            "Note": note,
            "Commentaire": commentaire
        }
        
        st.session_state.db_voyages = pd.concat([
            st.session_state.db_voyages, 
            pd.DataFrame([nouvelle_donnee])
        ], ignore_index=True)
        
        st.success(f"✅ Données pour '{destination}' enregistrées avec succès !")
        st.balloons()
    else:
        st.error("⚠️ Erreur : Veuillez remplir tous les champs obligatoires.")

# --- AFFICHAGE ET DIAGRAMMES (Améliorations demandées) ---
st.divider()

if not st.session_state.db_voyages.empty:
    col_list, col_charts = st.columns([1, 1])

    with col_list:
        st.subheader("📊 Données collectées")
        st.dataframe(st.session_state.db_voyages, use_container_width=True)

    with col_charts:
        st.subheader("📈 Analyses visuelles")
        tab1, tab2 = st.tabs(["Transport (Circulaire)", "Destinations (Barres)"])
        
        with tab1:
            # Diagramme circulaire (moyens de transport)
            st.write("Répartition des moyens de transport")
            df_trans = st.session_state.db_voyages['Transport'].value_counts()
            st.plotly_chart({
                "data": [{"values": df_trans.values, "labels": df_trans.index, "type": "pie", "hole": .4}],
                "layout": {"margin": {"t": 0, "b": 0, "l": 0, "r": 0}}
            }, use_container_width=True)

        with tab2:
            # Diagramme des destinations les plus visitées
            st.write("Fréquence des destinations")
            df_dest = st.session_state.db_voyages['Destination'].value_counts()
            st.bar_chart(df_dest)

    # Exportation
    csv = st.session_state.db_voyages.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Télécharger la base (CSV)", csv, "collecte_voyages.csv", "text/csv")
else:
    st.info("Aucune donnée n'a encore été collectée.")