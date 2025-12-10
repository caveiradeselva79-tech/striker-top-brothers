import streamlit as st
import pandas as pd
from utils.data_handler import load_csv, save_csv
from datetime import datetime

st.title("💰 Controle de Pagamentos")

df = load_csv("pagamentos.csv")

cpf = st.text_input("CPF")
valor = st.number_input("Valor", min_value=0.0)
forma = st.selectbox("Forma de pagamento", ["PIX", "Dinheiro", "Cartão"])
mes = st.selectbox("Mês", list(range(1,13)))
ano = st.number_input("Ano", min_value=2020, max_value=2030)

if st.button("Registrar pagamento"):
    novo = pd.DataFrame([[
        cpf, mes, ano, valor, datetime.now().date(), forma, "PAGO"
    ]], columns=["cpf","mes","ano","valor","data_pagamento","forma_pagamento","status"])

    df = pd.concat([df, novo], ignore_index=True)
    save_csv(df, "pagamentos.csv")
    st.success("Pagamento registrado!")

st.subheader("Pagamentos cadastrados")
st.dataframe(df)
