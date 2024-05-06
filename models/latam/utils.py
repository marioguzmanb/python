from sklearn import preprocessing
from config import *
from sklearn.model_selection import train_test_split
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
 
def dummy_ebizz(data_in, dummy_target_variables):
    data_out = data_in[dummy_target_variables]
    for i in data_out.columns:
        data_out.loc[data_out[i]>=1,i] = 1
        data_out.loc[data_out[i]<1,i] = 0
    return data_out
        
def encoder_ebizz(data_in, data_out, variable):
    le = preprocessing.LabelEncoder()
    le.fit(data_in[variable])
    data_out[f"enc_{variable}"] = le.transform(data_in[variable])
    return data_out
        
def continuos_ebizz(data_in, data_out, variable):
    data_out[variable] = data_in[[variable]].fillna(0)
    return data_out

def preproc(dataframe):
    #preprocess
    data1 = dummy_ebizz(data_in = dataframe, dummy_target_variables = DUMMY_TARGET_VARIABLES)
    for i in ENCODERS_VARIABLES:
        data1 = encoder_ebizz(data_in = dataframe, data_out = data1, variable = i)

    for i in CONTINUOS_VARIABLE:
        data1 = continuos_ebizz(data_in = dataframe, data_out = data1, variable = i)

    X = data1.iloc[:, 1:].fillna(0)
    y = data1.iloc[:, 0].fillna(0)
    # Split dataset into training set and test set
    X_train, X_test, y_train, y_test = train_test_split(X, 
                                                        y,
                                                        test_size=0.3,
                                                        stratify=y,
                                                        random_state=2342) # 70% training and 30% test
    return X_train, X_test, y_train, y_test

def chart_features_importance(features_scores):
    fig,ax = plt.subplots(figsize=(5,5))
    ax = sns.barplot(x=features_scores[0:9], y=features_scores.index[0:9],palette="mako").set_title('Tree-Based Feature Analysis')
    plt.xlabel('Feature Importance Score')
    plt.ylabel('Features')
    return st.pyplot(fig)

def comparison_data(df,text):
    left = pd.DataFrame(df[(df["target"] == 1)].groupby(text).count().target.sort_values(ascending = False))
    right = pd.DataFrame(df[(df["target"] == 0)].groupby(text).count().target.sort_values(ascending = False))
    data_comparada = left.merge(right, left_index = True, right_index =True)
    data_comparada.columns = ["Valor_1", "valor_0"]
    data_comparada["prctg_1"] = data_comparada["Valor_1"]/(data_comparada["Valor_1"]+data_comparada["valor_0"])
    data_comparada = data_comparada.sort_values("prctg_1", ascending = False)
    return data_comparada
