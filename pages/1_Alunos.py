import streamlit as st
import pandas as pd
from utils.data_handler import load_csv, save_csv

st.title("👨‍🎓 Cadastro de Alunos")

df = load_csv("aluno.csv")

st.subheader("Adicionar novo aluno")
nome = st.text_input("Nome")
cpf = st.text_input("CPF")
telefone = st.text_input("Telefone")
modalidade = st.selectbox("Modalidade", ["Muay Thai", "Jiu-Jitsu", "Boxe", "Kickboxing"])
plano = st.selectbox("Plano", ["Beginner", "Intermediate", "Hard"])
ativo = st.selectbox("Ativo?", ["SIM", "NÃO"])

if st.button("Salvar aluno"):
    novo = pd.DataFrame([[cpf, nome, telefone, plano, modalidade, ativo]], 
                        columns=["cpf", "nome", "telefone", "plano", "modalidade", "ativo"])
    df = pd.concat([df, novo], ignore_index=True)
    save_csv(df, "aluno.csv")
    st.success("Aluno salvo com sucesso!")

st.subheader("Lista de alunos cadastrados")
st.dataframe(df)
