import streamlit as st
import requests
import pandas as pd

#Configuration de la page
st.set_page_config(
    page_title="Agritech Answers",
    page_icon="🌾",
    layout="wide"
)

#URL de l'API FastAPI (par défaut sur le port 8000)
API_URL = "http://127.0.0.1:8000"

#En-tête
st.title("🌾 Agritech Answers : Assistant Agricole IA")
st.markdown("Cette application utilise un modèle XGBoost pour estimer vos rendements agricoles et vous conseiller la meilleure culture pour votre parcelle.")

#--- BARRE LATÉRALE : Saisie des données de la parcelle ---
st.sidebar.header("📃 Conditions de la Parcelle")
st.sidebar.markdown("Renseignez les caractéristiques de votre champ :")

region = st.sidebar.selectbox("Région", ["North", "South", "East", "West"])
soil_type = st.sidebar.selectbox("Type de sol", ["Sandy", "Clay", "Loam", "Silt", "Peaty", "Chalky"])
weather = st.sidebar.selectbox("Météo dominante", ["Sunny", "Cloudy", "Rainy"])

temperature = st.sidebar.slider("Température Moyenne (°C)", min_value=0.0, max_value=50.0, value=25.0, step=0.5)
rainfall = st.sidebar.number_input("Précipitations annuelles (mm)", min_value=0.0, max_value=3000.0, value=500.0)
pesticides = st.sidebar.number_input("Pesticides (tonnes)", min_value=0.0, max_value=100000.0, value=0.0)

col1, col2 = st.sidebar.columns(2)
with col1:
    irrigation = st.checkbox("Irrigation 💧", value=True)
with col2:
    fertilizer = st.checkbox("Engrais 🧪", value=True)

days_to_harvest = st.sidebar.number_input("Jours avant récolte estimés", min_value=30, max_value=365, value=120)

#Dictionnaire de base pour les requêtes (SANS la culture, idéal pour la route /recommend)
base_payload = {
    "Region": region,
    "Soil_Type": soil_type,
    "Rainfall_mm": rainfall,
    "Temperature_Celsius": temperature,
    "Fertilizer_Used": fertilizer,
    "Irrigation_Used": irrigation,
    "Weather_Condition": weather,
    "Days_to_Harvest": days_to_harvest,
    "pesticides_tonnes_mean": pesticides
}

#--- CONTENU PRINCIPAL : Onglets ---
tab1, tab2 = st.tabs(["🔮 Prédiction Simple", "🏆 Recommandation de Culture (IA)"])

#ONGLET 1 : Prédiction d'une culture spécifique
with tab1:
    st.header("Estimer le rendement d'une culture spécifique")
    crop = st.selectbox("Quelle culture souhaitez-vous planter ?", ["Cotton", "Rice", "Barley", "Soybean", "Wheat", "Maize"])
    
    if st.button("Lancer la prédiction", type="primary"):
        #On ajoute la culture choisie au payload
        payload = base_payload.copy()
        payload["Crop"] = crop
        
        with st.spinner("Analyse par le modèle XGBoost en cours..."):
            try:
                response = requests.post(f"{API_URL}/predict", json=payload)
                if response.status_code == 200:
                    result = response.json()
                    yield_pred = result.get("yield_tons_per_hectare_pred", 0)
                    st.success(f"###Rendement estimé : **{yield_pred:.2f}** tonnes/hectare")
                else:
                    st.error(f"Erreur de l'API ({response.status_code}) : Veuillez vérifier que les données sont correctes.")
            except requests.exceptions.ConnectionError:
                st.error("🚨 Impossible de joindre l'API. Assurez-vous d'avoir lancé `uvicorn src.api.main:app --reload` dans un autre terminal.")

#ONGLET 2 : La recommandation (Classement)
with tab2:
    st.header("Trouver la culture la plus rentable")
    st.markdown("L'IA va simuler le rendement de **toutes les cultures possibles** sur votre parcelle pour vous recommander la meilleure option.")
    
    if st.button("Lancer l'analyse complète (Batch Prediction)", type="primary", key="btn_reco"):
        with st.spinner("Simulation des différents scénarios en cours..."):
            try:
                #Appel à ta route ultra-optimisée !
                response = requests.post(f"{API_URL}/recommend", json=base_payload)
                if response.status_code == 200:
                    result = response.json()
                    
                    #Récupération du vainqueur
                    best_crop = result["recommended_crop_data"]["Crop"]
                    best_yield = result["recommended_crop_data"]["predicted_yield"]
                    
                    st.success(f"🥇 **Meilleur choix : {best_crop}** avec un rendement estimé à **{best_yield:.2f} t/ha**.")
                    
                    #Affichage graphique du classement complet
                    st.subheader("Classement comparatif des cultures")
                    all_predictions = result["predicted_data"]
                    
                    #Transformation en DataFrame pour un affichage facile
                    df_results = pd.DataFrame(all_predictions)
                    df_results = df_results.sort_values(by="predicted_yield", ascending=True) #Ascending pour le bar_chart horizontal
                    
                    #Graphique en barres natif Streamlit
                    st.bar_chart(df_results.set_index("Crop")["predicted_yield"], horizontal=True)
                else:
                    st.error(f"Erreur de l'API ({response.status_code}) : {response.text}")
            except requests.exceptions.ConnectionError:
                st.error("🚨 Impossible de joindre l'API. Assurez-vous d'avoir lancé FastAPI sur le port 8000.")
