import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

@st.cache_data
def carregar_dados():
    return pd.read_csv("Preços Herois.csv")

df = carregar_dados()

st.title("📊 Histograma Interativo de Preços")

# Filtros
st.sidebar.header("Filtros")
servicos = st.sidebar.multiselect("Serviço", options=sorted(df["servico"].unique()), default=df["servico"].unique())
estados = st.sidebar.multiselect("Estado", options=sorted(df["Estado"].unique()), default=df["Estado"].unique())
cidades_disponiveis = df[df["Estado"].isin(estados)]["Cidade"].unique()
cidades = st.sidebar.multiselect("Cidade", options=sorted(cidades_disponiveis), default=sorted(cidades_disponiveis))

df_filtrado = df[
    (df["servico"].isin(servicos)) &
    (df["Estado"].isin(estados)) &
    (df["Cidade"].isin(cidades))
]

# Histograma com hover mais exato
st.subheader("Distribuição de Preços (com filtros aplicados)")

bin_size = 10  # Altere conforme o nível de detalhe desejado

fig = px.histogram(
    df_filtrado,
    x="price",
    color="servico",
    nbins=int((df_filtrado["price"].max() - df_filtrado["price"].min()) / bin_size),
    barmode="stack",
    labels={"price": "Preço"},
    text_auto=True
)

# Mostrar percentual no hover
total = len(df_filtrado)
fig.update_traces(
    hovertemplate=(
        'Faixa de Preço: %{x}<br>'
        'Serviço: %{customdata[0]}<br>'
        'Contagem: %{y}<br>'
        'Percentual: %{customdata[1]:.2f}%<extra></extra>'
    ),
    customdata=[
        [row["servico"], (1 / total) * 100] for _, row in df_filtrado.iterrows()
    ]
)

# Opcional: linha de média
media = df_filtrado["price"].mean()
fig.add_vline(
    x=media,
    line_dash="dot",
    line_color="red",
    annotation_text=f"Média: R${media:.2f}",
    annotation_position="top left"
)

fig.update_layout(
    hovermode="x unified",
    xaxis_title="Preço",
    yaxis_title="Quantidade",
)

st.plotly_chart(fig, use_container_width=True)

with st.expander("🔍 Ver dados filtrados"):
    st.dataframe(df_filtrado.reset_index(drop=True))
