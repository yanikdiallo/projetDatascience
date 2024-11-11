import streamlit as st
import pickle
import pandas as pd
#import sklearn
import os

# Charger le modèle avec Pickle
@st.cache_resource
def load_model():
    model_path = 'model.pkl'
    if os.path.exists(model_path):
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        return model
    else:
        st.error(f"Le modèle n'a pas été trouvé à {model_path}. Vérifiez le chemin du fichier.")
        return None

# Créer le formulaire pour saisir les données utilisateur
def create_form():
    st.title("Prédiction de l'octroi de prêt")

    with st.form(key="loan_form"):
        Married = st.selectbox("Êtes-vous marié ?", ["Oui", "Non"])
        Credit_History = st.selectbox("Avez-vous un bon historique de crédit ?", ["Oui", "Non"])
        CoapplicantIncome = st.number_input("Revenu du co-emprunteur (en INR)", min_value=0, value=1000)

        submit_button = st.form_submit_button("Soumettre")

        Married  = 1 if Married == "Oui" else 0
        Credit_History = 1 if  Credit_History == "Oui" else 0
        
        return submit_button, Married, Credit_History,CoapplicantIncome

# Faire la prédiction avec le modèle
def make_prediction(model, Credit_History,Married, CoapplicantIncome):
    # Créer un DataFrame avec les données de l'utilisateur
    user_input = pd.DataFrame({
        'CreditHistory': [Credit_History],
        'Married': [Married],
          # Utilisez 'CreditHistory' pour correspondre aux noms d'entrée
        'CoapplicantIncome': [CoapplicantIncome]
    })

    # Vérifiez et renommez les colonnes pour correspondre à celles utilisées lors de l'entraînement
    if 'CreditHistory' in user_input.columns:
        user_input.rename(columns={'CreditHistory': 'Credit_History'}, inplace=True)

    # S'assurer que la colonne 'Credit_History' est bien présente
    if 'Credit_History' not in user_input.columns:
        st.error("La colonne 'Credit_History' est manquante. Veuillez vérifier vos données d'entrée.")
        return

    # Faire la prédiction
    prediction = model.predict(user_input)

    if prediction[0] == 1:
        st.success("Vous êtes éligible pour un prêt !")
    else:
        st.error("Désolé, votre demande de prêt a été rejetée.")

# Fonction principale
def main():
    model = load_model()

    if model is None:
        return

    submit_button, Credit_History,Married, CoapplicantIncome = create_form()

    if submit_button:
        make_prediction(model, Credit_History,Married,CoapplicantIncome)

if __name__ == "__main__":
    main()
