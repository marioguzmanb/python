import os
os.chdir("..")
import pandas as pd
import streamlit as st
import lib.utils as utils
from datetime import datetime
import json

# Configuración de la página
st.set_page_config(
    "Encrypt",
    "🔐",
    initial_sidebar_state="expanded",
    layout="centered"
)

# Generación de token
token = utils.generate_key()
# Fecha de encriptación
today = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
today_str = datetime.today().strftime("%Y-%m-%d")
token_json = {"token":str(token),
              "date":today}

with st.sidebar:
    st.header("Funcionamiento")
    st.markdown("Esta aplicación tiene como finalidad encriptar columnas de un archivo en formato **XLSX** o **CSV**.")
    st.markdown("Se recomienda que las columnas tenga valores únicos, debido a que el proceso puede dejar el mismo string con diferente valor encriptado.")
    st.header("Cargar archivos a encriptar")
    uploaded_file = st.file_uploader("Seleccione archivo csv o xlsx",
                                     accept_multiple_files=False)
    option = st.radio("Tipo de archivo cargado", options=["csv","xlsx"])
    if option == "xlsx" and uploaded_file:
        files = pd.ExcelFile(uploaded_file)
        sheet = st.radio("Seleccione hoja a encriptar",options=files.sheet_names)
        skiprows = st.number_input("Seleccione el número de saltos de linea del archivo",0)
        skiprows = int(skiprows)
    if option == "csv" and uploaded_file:
        delimiter = st.radio("Seleccione el delimitador", [",",";","|"])
        skiprows = st.number_input("Seleccione el número de saltos de linea del archivo",0)
        skiprows = int(skiprows)

if uploaded_file:
    if option == "csv":
        dataframe = pd.read_csv(uploaded_file,skiprows=skiprows,delimiter=delimiter)
    elif option=="xlsx":
        dataframe = pd.read_excel(uploaded_file,skiprows=skiprows,sheet_name=sheet)
    st.header("Encriptación de datos sensibles")
    st.write("Previsualización del dataframe a encriptar")
    st.dataframe(dataframe)

    cols = st.multiselect("Seleccione las columnas a encriptar",
                          options=dataframe.columns)
    # Encriptación
    start = datetime.now()
    for col in cols:
        dataframe[f"{col}_encrypt"] = dataframe[col].apply(lambda x: utils.encrypt(text=str(x), key=token))
    end = datetime.now()
    print(f"Time elapsed: {(end-start).total_secods/60} minutes")

    # Descarga de las llaves
    json_string = json.dumps(token_json)
    st.write("Clave de encriptación")
    st.json(json_string, expanded=False)
    st.download_button(
        label="Descargar par de llaves de encriptación",
        file_name=f"token_{today_str}.json",
        mime="application/json",
        data=json_string
    )

    # Descarga de dataframe encriptado
    csv_encrypt = utils.convert_df(dataframe)
    st.download_button(
        label="Descargar dataframe encriptado",
        file_name="file_encrypt.csv",
        mime="text/csv",
        key="download-csv",
        data=csv_encrypt
    )