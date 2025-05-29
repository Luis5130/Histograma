import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Título
st.title("Visualização dos Meus Dados")

# Carregar o CSV
@st.cache_data
def carregar_dados():
    return pd.read_csv("Preços Herois.csv")

df = carregar_dados()

# Mostrar os dados
st.subheader("Prévia dos dados")
st.write(df.head())

# Selecionar a coluna para o histograma
coluna = st.selectbox("Escolha a coluna para visualizar o histograma:", df.columns)

# Plotar o histograma
fig, ax = plt.subplots()
sns.histplot(df[coluna].dropna(), kde=True, ax=ax)
ax.set_title(f"Histograma da coluna {coluna}")
st.pyplot(fig)
