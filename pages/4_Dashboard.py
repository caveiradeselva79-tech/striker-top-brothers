import streamlit as st
import pandas as pd
from utils.data_handler import load_csv

st.title("📊 Dashboard STRIKER")

alunos = load_csv("aluno.csv")
pagamentos = load_csv("pagamentos.csv")
presencas = load_csv("presencas.csv")

col1, col2, col3 = st.columns(3)

col1.metric("Alunos ativos", alunos[alunos["ativo"]=="SIM"].shape[0] if not alunos.empty else 0)
col2.metric("Pagamentos registrados", pagamentos.shape[0])
col3.metric("Presenças registradas", presencas.shape[0])

if not alunos.empty:
    st.subheader("Distribuição por modalidade")
    st.bar_chart(alunos["modalidade"].value_counts())
