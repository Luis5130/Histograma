import streamlit as st
import pandas as pd
import plotly.express as px

# Carregamento do CSV
@st.cache_data
def carregar_dados():
    return pd.read_csv("Preços Herois.csv")  # Certifique-se de que o arquivo está no mesmo diretório

df = carregar_dados()

st.title("📊 Histograma Interativo de Preços")

# --- Filtros ---
st.sidebar.header("Filtros")

# Serviço
servicos = st.sidebar.multiselect("Serviço", options=sorted(df["servico"].unique()), default=df["servico"].unique())

# Estado
estados = st.sidebar.multiselect("Estado", options=sorted(df["Estado"].unique()), default=df["Estado"].unique())

# Cidade (baseada nos estados selecionados)
cidades_disponiveis = df[df["Estado"].isin(estados)]["Cidade"].unique()
cidades = st.sidebar.multiselect("Cidade", options=sorted(cidades_disponiveis), default=sorted(cidades_disponiveis))

# Aplicar os filtros
df_filtrado = df[
    (df["servico"].isin(servicos)) &
    (df["Estado"].isin(estados)) &
    (df["Cidade"].isin(cidades))
]

# --- Histograma Interativo ---
st.subheader("Distribuição de Preços (com filtros aplicados)")

fig = px.histogram(
    df_filtrado,
    x="price",
    color="servico",
    nbins=20,
    barmode="stack",
    title="Distribuição de Preços por Serviço",
    labels={"price": "Preço"}
)

fig.update_layout(hovermode="x unified")

st.plotly_chart(fig, use_container_width=True)

# Exibir dados filtrados (opcional)
with st.expander("🔍 Ver dados filtrados"):
    st.dataframe(df_filtrado.reset_index(drop=True))
