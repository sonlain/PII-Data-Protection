import pandas as pd
import numpy as np
import streamlit as st
import io
import openpyxl
from io import BytesIO

from presidio_structured import StructuredEngine,PandasAnalysisBuilder
from presidio_anonymizer.entities import OperatorConfig
from faker import Faker

def features_selection():
    features = ['PERSON_NAME',
                'PAN_NUMBER',
                'EMAIL',
                'ADDRESS',
                'PHONE_NUMBER']
    selected_features = st.multiselect(
        "Select Protected PII :",
        options=features,
        default=features  
    )
    return selected_features

def upload(df):
    uploaded_file = st.file_uploader("Drag and drop a CSV or Excel file", type=["csv", "xlsx"])
    if uploaded_file is not None:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file,na_values=[""], keep_default_na=False,index_col=0)
        else:
            df = pd.read_excel(uploaded_file,na_values=[""], keep_default_na=False)
    return df

def to_excel(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Data Profile')
    processed_data = output.getvalue()
    return processed_data

def download():
    st.download_button(
        label="Download Data Profile as an Excel",
        data=excel_data,
        file_name='PII.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

def pii_identification(df,feature):
    df=df.astype('object')
    pandas_engine = StructuredEngine()
    tabular_analysis=PandasAnalysisBuilder().generate_analysis(df,language="en",selection_strategy="highest_confidence")
    fake=Faker()
    feature_list = list(feature)
    operators={
    "PERSON": OperatorConfig("replace",{"new_value":"PERSON_NAME"}),
    "EMAIL_ADDRESS": OperatorConfig("custom",{"lambda": lambda x: fake.safe_email()}),
    "IN_PAN": OperatorConfig("replace",{"new_value":"PAN_NUMBER"}),
    "LOCATION": OperatorConfig("replace",{"new_value":"ADDRESS"}),
    "PHONE_NUMBER": OperatorConfig("replace",{"new_value":"PHONE_NUMBER"})
    }
    pii_dict={"PERSON":"PERSON_NAME","EMAIL_ADDRESS":"EMAIL","IN_PAN":"PAN_NUMBER","PHONE_NUMBER":"PHONE_NUMBER","LOCATION":"ADDRESS"}
    anonymized_pii = [key for key, value in pii_dict.items() if value in feature_list]
    tabular_analysis.entity_mapping = {key: value for key, value in tabular_analysis.entity_mapping.items() if value in anonymized_pii}
    anonymized_df = pandas_engine.anonymize(df, tabular_analysis, operators=operators)
    return anonymized_df

#Input Data
df=pd.DataFrame({'name':['Anurag','Gopal','Nitish'],'surname':['Kumar','Rai','Tripura'],'email':['anug@gmail.com','gopal@gmail.com','nitish@iitg.ac.in'],'roll':[1,2,3],'id_p':['ASFGK3240A','MPARW2789G','BSNPT3220N'],'no':[+916003438904,np.nan,6003438907],'state':['Karnataka','Assam','Mizoram']})


#Streamlit Code and Function Call

st.set_page_config(layout="wide")
st.markdown("<h1 style='text-align: center; color: blue;'>PII Data Protection</h1>", unsafe_allow_html=True)
st.markdown(f"<h3 style='text-align: center; color: lightblue;'>Insert Your Data</h3>", unsafe_allow_html=True)
l,col1, gap, col2,r = st.columns([0.05,1,0.1,1,0.05])
with col1:
    feature=features_selection()
with col2:
    df=upload(df)
st.markdown("")
st.markdown(f"<h3 style='text-align: center; color: lightblue;'>Raw Data</h3>", unsafe_allow_html=True)
st.dataframe(df)
ans=pii_identification(df,feature)
st.markdown("")
st.markdown(f"<h3 style='text-align: center; color: lightblue;'>Anonymized PII Data</h1>", unsafe_allow_html=True)
st.dataframe(ans)
st.markdown("")
st.markdown(f"<h3 style='text-align: center; color: lightblue;'>Download Data</h1>", unsafe_allow_html=True)
excel_data = to_excel(ans)
download()
