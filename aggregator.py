import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from statsmodels.tsa.arima_model import ARIMA

st.title("Analyse des Courbes de Charge - Aggregators")

# Fonction pour tracer les courbes de charge à partir des fichiers Excel
def plot_load_curves(data_frames):
    fig, ax = plt.subplots(figsize=(10, 6))
    for df in data_frames:
        ax.plot(df['Datetime'].values, df['Load'].values, label=df['Name'].iloc[0])
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

data_frames = []

if uploaded_folder:
    for uploaded_file in uploaded_folder:
        data = pd.read_excel(uploaded_file, engine="openpyxl")
        data['Name'] = os.path.basename(uploaded_file.name)
        data_frames.append(data)

    # Afficher les courbes de charge à partir des fichiers Excel
    plot_load_curves(data_frames)

    # Détection des outliers pour la courbe globale
    st.header("Détection des Outliers pour la Courbe Globale")
    global_data = pd.concat(data_frames, ignore_index=True)
    global_series = global_data['Load']
    global_outliers = detect_outliers(global_series, threshold=2.0)

    if not global_outliers.empty:
        st.write("Outliers pour la courbe globale :")
        st.write(global_outliers)

        # Afficher les valeurs aberrantes avec leurs dates correspondantes
        outliers_with_datetime = global_data[global_data['Load'].isin(global_outliers)]
        st.write("Valeurs aberrantes avec leur date et heure correspondantes:")
        st.write(outliers_with_datetime[['Datetime', 'Load']])
