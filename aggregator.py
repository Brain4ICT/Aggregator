import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np

st.title("Analyse des Courbes de Charge et Détection des Outliers")

# Fonction pour lire les fichiers Excel au format .xlsx
def read_excel_file(file_path):
    if file_path.endswith(".xlsx"):
        df = pd.read_excel(file_path, engine="openpyxl")
    else:
        df = pd.read_excel(file_path)
    return df

# Fonction pour tracer les courbes de charge à partir des fichiers Excel
def plot_load_curves(file_paths):
    fig, ax = plt.subplots(figsize=(10, 6))
    for file_path in file_paths:
        df = read_excel_file(file_path)
        ax.plot(df['Datetime'], df['Load'], label=os.path.basename(file_path))
    ax.set_xlabel('Datetime')
    ax.set_ylabel('Load')
    ax.legend()
    st.pyplot(fig)

# Fonction pour détecter les outliers dans une série temporelle
def detect_outliers(series, threshold=2.0):
    z_scores = np.abs((series - series.mean()) / series.std())
    outliers = series[z_scores > threshold]
    return outliers

# Uploader un dossier contenant des fichiers Excel
uploaded_folder = st.file_uploader("Uploader un dossier contenant des fichiers Excel", type=["xlsx"], accept_multiple_files=True, key="upload_folder")

if uploaded_folder:

    # Sauvegarder les fichiers Excel dans le répertoire temporaire
    file_paths = []
    for uploaded_file in uploaded_folder:
        file_path = os.path.join(uploaded_file.name)
        with open(file_path, 'wb') as f:
            f.write(uploaded_file.read())
        file_paths.append(file_path)

    # Afficher les courbes de charge à partir des fichiers Excel
    plot_load_curves(file_paths)

    # Nettoyer le répertoire temporaire après utilisation
    for file_path in file_paths:
        os.remove(file_path)

    # Détection des outliers pour la courbe globale
    st.header("Détection des Outliers pour la Courbe Globale")
    global_outliers = None

    if uploaded_folder:
        global_data = pd.DataFrame()
        for file_path in file_paths:
            df = read_excel_file(file_path)
            global_data = global_data.append(df, ignore_index=True)

        # Utiliser la fonction de détection des outliers pour la courbe globale
        global_series = global_data['Load']
        global_outliers = detect_outliers(global_series, threshold=2.0)

    if global_outliers is not None:
        st.write("Outliers pour la courbe globale :")
        st.write(global_outliers)
