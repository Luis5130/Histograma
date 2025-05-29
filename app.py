import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- Carregamento do CSV ---
@st.cache_data
def carregar_dados():
    return pd.read_csv("Preços Herois.csv")  # Certifique-se de que o arquivo está no mesmo diretório

df = carregar_dados()

st.title("📊 Histograma Interativo de Preços")

# --- Filtros ---
st.sidebar.header("Filtros")

# SERVIÇO
st.sidebar.subheader("Serviço")
todos_servicos = sorted(df["servico"].unique())
selecionar_todos_servicos = st.sidebar.checkbox("Selecionar todos os serviços", value=True)
if selecionar_todos_servicos:
    servicos = st.sidebar.multiselect("Serviço", options=todos_servicos, default=todos_servicos)
else:
    servicos = st.sidebar.multiselect("Serviço", options=todos_servicos)

# ESTADO
st.sidebar.subheader("Estado")
todos_estados = sorted(df["Estado"].unique())
selecionar_todos_estados = st.sidebar.checkbox("Selecionar todos os estados", value=True)
if selecionar_todos_estados:
    estados = st.sidebar.multiselect("Estado", options=todos_estados, default=todos_estados)
else:
    estados = st.sidebar.multiselect("Estado", options=todos_estados)

# CIDADE
st.sidebar.subheader("Cidade")
cidades_disponiveis = sorted(df[df["Estado"].isin(estados)]["Cidade"].unique())
selecionar_todas_cidades = st.sidebar.checkbox("Selecionar todas as cidades", value=True)
if selecionar_todas_cidades:
    cidades = st.sidebar.multiselect("Cidade", options=cidades_disponiveis, default=cidades_disponiveis)
else:
    cidades = st.sidebar.multiselect("Cidade", options=cidades_disponiveis)

# Aplicar filtros
df_filtrado = df[
    (df["servico"].isin(servicos)) &
    (df["Estado"].isin(estados)) &
    (df["Cidade"].isin(cidades))
]

# --- Histograma com Plotly ---
st.subheader("Distribuição de Preços (com filtros aplicados)")

if not df_filtrado.empty:
    total = len(df_filtrado)

    fig = px.histogram(
        df_filtrado,
        x="price",
        color="servico",
        nbins=20,
        barmode="stack",
        custom_data=["servico"],
    )

    # Atualizar hover com detalhes
    fig.update_traces(
        hovertemplate="<br>".join([
            "Faixa de Preço: %{x} – %{x+bin}",  # bin será substituído
            "Serviço: %{customdata[0]}",
            "Qtd: %{y}",
            "Percentual: %{y:.0f} / " + str(total) + " = %{percent:.1f}%",
        ]),
    )

    # Adicionar linha vertical com a média
    media = df_filtrado["price"].mean()
    fig.add_vline(
        x=media,
        line_dash="dash",
        line_color="black",
        annotation_text=f"Média: R${media:.2f}",
        annotation_position="top right",
    )

    # Adiciona eixo e layout limpo
    fig.update_layout(
        xaxis_title="Preço",
        yaxis_title="Quantidade",
        bargap=0.05,
        title="Distribuição de Preços por Serviço",
    )

    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Nenhum dado encontrado com os filtros selecionados.")

# --- Dados filtrados ---
with st.expander("🔍 Ver dados filtrados"):
    st.dataframe(df_filtrado.reset_index(drop=True))
