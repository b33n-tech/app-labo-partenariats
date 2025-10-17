import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

st.title("Scraper de projets Lelabo")

# Upload du fichier Excel
uploaded_file = st.file_uploader("Choisis ton fichier Excel", type=["xlsx"])
if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.write("Aperçu des URLs :", df.head())

    # Choisir la colonne contenant les URLs
    url_col = st.selectbox("Sélectionne la colonne contenant les URLs", df.columns)

    if st.button("Scraper les emails et sites web"):
        results = []
        for url in df[url_col]:
            try:
                r = requests.get(url)
                soup = BeautifulSoup(r.text, "html.parser")

                # Exemple : récupérer un lien qui contient "mailto:"
                email = soup.select_one('a[href^=mailto]')
                email = email['href'].replace('mailto:', '') if email else None

                # Exemple : récupérer un lien externe (site web)
                website = soup.select_one('a[href^=http]:not([href*="lelabo"])')
                website = website['href'] if website else None

                results.append({"URL Projet": url, "Email": email, "Site Web": website})
            except Exception as e:
                results.append({"URL Projet": url, "Email": None, "Site Web": None})
                print(f"Erreur sur {url}: {e}")

        # Afficher et proposer de télécharger
        result_df = pd.DataFrame(results)
        st.write(result_df)
        result_df.to_excel("resultats_scraping.xlsx", index=False)
        st.success("Scraping terminé, fichier Excel généré !")
