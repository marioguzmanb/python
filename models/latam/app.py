from datetime import datetime

NOW = datetime.now()
BEFORE = NOW
print(f"Top of script, time elapsed: {NOW - BEFORE}")

# Libraries
import streamlit as st
import pandas as pd
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
from utils import *
from config import *
import warnings
warnings.simplefilter("ignore")

TEMP_DIR_NAME = "temp_data"

if not os.path.isdir(TEMP_DIR_NAME):
    os.mkdir(TEMP_DIR_NAME)

def save_uploadedfile(uploadedfile):
     with open(os.path.join(TEMP_DIR_NAME,uploadedfile.name),"wb") as f:
         f.write(uploadedfile.getbuffer())
     return st.success("Saved File:{} to {}".format(uploadedfile.name,TEMP_DIR_NAME))

st.set_page_config(
    page_title="Modelamiento",
    layout="wide",
    page_icon="🦈")

NOW = datetime.now()
print(f"function definitions, time elapsed: {NOW - BEFORE}")
BEFORE = NOW

def main():
    global BEFORE
    global NOW
    search_title = "Error en las órdenes"
    with st.sidebar:
        st.markdown("***")
        st.markdown(search_title)
        st.markdown("")
        uploaded_file = st.file_uploader("Carga de la información en formato csv",type=["csv"])
    if uploaded_file:
        save_uploadedfile(uploaded_file)
        col1, col2,col3 = st.columns((1,4,1))
        with col2:
            st.title("Modelamiento de errores en las órdenes")
            st.header("Carga de la data")
            with st.spinner(text="This may take a moment ..."):
                df = pd.read_csv(os.path.join(TEMP_DIR_NAME,uploaded_file.name))
            st.dataframe(data=df)
            NOW = datetime.now()
            print(f"load data, time elapsed: {NOW - BEFORE}")
            BEFORE = NOW
            st.header("Modelamiento")
            with st.spinner(text="Preprocesamiento de la información"):
                df = df[COLUMNS_ACTIVATE]
                df["target"] = df["target"].astype(int)
                X_train, X_test, y_train, y_test = preproc(dataframe = df)
            NOW = datetime.now()
            print(f"preprocessing data, time elapsed: {NOW - BEFORE}")
            BEFORE = NOW
            with st.spinner(text="Entrenamiento del modelo"):
                # Create a Gaussian Classifier
                clf=RandomForestClassifier(**CONFIG_RF)
                # Train the model using the training sets y_pred=clf.predict(X_test)
                clf.fit(X_train,y_train)
                y_pred=clf.predict(X_test)
            NOW = datetime.now()
            print(f"training model, time elapsed: {NOW - BEFORE}")
            BEFORE = NOW
            # feature importance top 10
            with st.spinner(text="Gráfica de importancia de variables"):
                feature_scores = pd.Series(clf.feature_importances_, index=X_train.columns).sort_values(ascending=False).head(35)
                priorized = feature_scores.index[0:9].to_list()
                chart_features_importance(features_scores=feature_scores)

            with st.spinner(text="Calculo de accuracy"):
                st.write(f"Accuracy: {round(metrics.accuracy_score(y_test, y_pred),2)}")
            st.header("Predicciones")
            for i in priorized:
                texto = i
                substring = "enc_"
                if texto.find(substring) != -1:
                    text = texto[4:]
                    data_comparada = comparison_data(df=df,text=text)
                    st.write(f"la comparación de {text} es")
                    st.dataframe(data_comparada)
                else:
                    text = i
                    data_comparada = comparison_data(df=df,text=text)
                    st.write(f"la comparación de {text} es:")
                    st.dataframe(data_comparada)

main()