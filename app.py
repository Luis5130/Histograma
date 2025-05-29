import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Visualização de Preços", layout="wide")

st.title("📊 Análise de Preços por Serviço, Estado e Cidade")

# Carregar dados
@st.cache_data
def carregar_dados():
    return pd.read_csv("Preços Herois.csv")

df = carregar_dados()

# Verificar se as colunas esperadas existem
colunas_esperadas = ['servico', 'price', 'Estado', 'Cidade']
if not all(col in df.columns for col in colunas_esperadas):
    st.error(f"As colunas esperadas são: {colunas_esperadas}. Verifique o arquivo.")
    st.stop()

# Histograma por serviço
st.subheader("📌 Distribuição de Preços por Tipo de Serviço")
fig_servico = px.histogram(df, x="price", color="servico", barmode="overlay", nbins=30,
                           hover_data=['servico', 'price'], title="Distribuição por Serviço")
st.plotly_chart(fig_servico, use_container_width=True)

# Histograma por estado
st.subheader("📍 Distribuição de Preços por Estado")
fig_estado = px.histogram(df, x="price", color="Estado", barmode="overlay", nbins=30,
                          hover_data=['Estado', 'price'], title="Distribuição por Estado")
st.plotly_chart(fig_estado, use_container_width=True)

# Histograma por cidade com seleção
st.subheader("🏙️ Distribuição de Preços por Cidade")
cidades = df['Cidade'].unique()
cidade_selecionada = st.selectbox("Selecione a cidade", sorted(cidades))
df_cidade = df[df['Cidade'] == cidade_selecionada]

fig_cidade = px.histogram(df_cidade, x="price", color="servico", barmode="overlay", nbins=30,
                          hover_data=['Cidade', 'servico', 'price'],
                          title=f"Distribuição de Preços em {cidade_selecionada}")
st.plotly_chart(fig_cidade, use_container_width=True)

# Boxplot com média por grupo
st.subheader("📦 Boxplot de Preços por Serviço")
fig_box = px.box(df, x="servico", y="price", color="servico", points="all", notched=True,
                 hover_data=["servico", "price", "Cidade", "Estado"],
                 title="Boxplot com Média e Distribuição de Preço por Serviço")
fig_box.update_traces(boxmean='sd')  # mostra média e desvio padrão
st.plotly_chart(fig_box, use_container_width=True)
