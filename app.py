import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Carregamento do CSV
@st.cache_data
def carregar_dados():
    return pd.read_csv("Preços Herois.csv")  # Certifique-se de que o arquivo está no mesmo diretório

df = carregar_dados()

st.title("📊 Histograma Interativo de Preços")

# --- Filtros ---
st.sidebar.header("Filtros")

# --- SERVIÇO ---
st.sidebar.subheader("Serviço")
todos_servicos = sorted(df["servico"].unique())
selecionar_todos_servicos = st.sidebar.checkbox("Selecionar todos os serviços", value=True)
if selecionar_todos_servicos:
    servicos = st.sidebar.multiselect("Serviço", options=todos_servicos, default=todos_servicos)
else:
    servicos = st.sidebar.multiselect("Serviço", options=todos_servicos)

# --- ESTADO ---
st.sidebar.subheader("Estado")
todos_estados = sorted(df["Estado"].unique())
selecionar_todos_estados = st.sidebar.checkbox("Selecionar todos os estados", value=True)
if selecionar_todos_estados:
    estados = st.sidebar.multiselect("Estado", options=todos_estados, default=todos_estados)
else:
    estados = st.sidebar.multiselect("Estado", options=todos_estados)

# --- CIDADE ---
st.sidebar.subheader("Cidade")
cidades_disponiveis = sorted(df[df["Estado"].isin(estados)]["Cidade"].unique())
selecionar_todas_cidades = st.sidebar.checkbox("Selecionar todas as cidades", value=True)
if selecionar_todas_cidades:
    cidades = st.sidebar.multiselect("Cidade", options=cidades_disponiveis, default=cidades_disponiveis)
else:
    cidades = st.sidebar.multiselect("Cidade", options=cidades_disponiveis)

# --- Aplicar os filtros ---
df_filtrado = df[
    (df["servico"].isin(servicos)) &
    (df["Estado"].isin(estados)) &
    (df["Cidade"].isin(cidades))
]

# --- Histograma ---
st.subheader("Distribuição de Preços (com filtros aplicados)")
fig, ax = plt.subplots()
sns.histplot(data=df_filtrado, x="price", hue="servico", multiple="stack", bins=20, ax=ax)
st.pyplot(fig)

# --- Exibir dados filtrados ---
with st.expander("🔍 Ver dados filtrados"):
    st.dataframe(df_filtrado.reset_index(drop=True))
