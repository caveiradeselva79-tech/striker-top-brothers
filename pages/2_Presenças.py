import streamlit as st
import pandas as pd
from utils.data_handler import load_csv, save_csv
from datetime import datetime

st.title("🥋 Registro de Presenças")

df = load_csv("presencas.csv")

cpf = st.text_input("CPF do aluno")
modalidade = st.selectbox("Modalidade", ["Muay Thai", "Jiu-Jitsu", "Boxe", "Kickboxing"])
obs = st.text_input("Observação")

if st.button("Registrar presença"):
    novo = pd.DataFrame([[
        cpf,
        datetime.now().date(),
        datetime.now().strftime("%H:%M"),
        modalidade,
        obs
    ]], columns=["cpf","data","hora","modalidade","observacao"])

    df = pd.concat([df, novo], ignore_index=True)
    save_csv(df, "presencas.csv")
    st.success("Presença registrada!")

st.subheader("Presenças registradas")
st.dataframe(df)
