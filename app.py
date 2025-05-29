import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Análise de Preços por Serviço, Estado e Cidade")

# Upload do arquivo CSV
dados = st.file_uploader("Envie seu arquivo CSV com colunas: servico, price, Estado, Cidade", type="csv")

if dados is not None:
    df = pd.read_csv(dados)

    # Filtros
    cidades = df["Cidade"].unique().tolist()
    cidade_selecionada = st.selectbox("Selecione uma cidade (opcional):", ["Todas"] + cidades)

    if cidade_selecionada != "Todas":
        df = df[df["Cidade"] == cidade_selecionada]

    # Histograma por Serviço
    st.subheader("Histograma de Preços por Serviço")
    fig_servico = px.histogram(df, x="price", color="servico", barmode="overlay", nbins=30,
                                hover_data=df.columns, title="Distribuição de Preços por Serviço")
    st.plotly_chart(fig_servico)

    # Histograma por Estado
    st.subheader("Histograma de Preços por Estado")
    fig_estado = px.histogram(df, x="price", color="Estado", barmode="overlay", nbins=30,
                               hover_data=df.columns, title="Distribuição de Preços por Estado")
    st.plotly_chart(fig_estado)

    # Histograma por Cidade
    st.subheader("Histograma de Preços por Cidade")
    fig_cidade = px.histogram(df, x="price", color="Cidade", barmode="overlay", nbins=30,
                               hover_data=df.columns, title="Distribuição de Preços por Cidade")
    st.plotly_chart(fig_cidade)

    # Boxplot por Serviço
    st.subheader("Boxplot de Preços por Serviço")
    fig_box_servico = px.box(df, x="servico", y="price", points="all",
                              hover_data=df.columns, title="Boxplot de Preços por Serviço")
    st.plotly_chart(fig_box_servico)

    # Tabelas de médias por grupo
    st.subheader("Preço Médio por Grupo")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### Por Serviço")
        media_servico = df.groupby("servico")["price"].mean().reset_index().rename(columns={"price": "Preço Médio"})
        st.dataframe(media_servico)

    with col2:
        st.markdown("### Por Estado")
        media_estado = df.groupby("Estado")["price"].mean().reset_index().rename(columns={"price": "Preço Médio"})
        st.dataframe(media_estado)

    with col3:
        st.markdown("### Por Cidade")
        media_cidade = df.groupby("Cidade")["price"].mean().reset_index().rename(columns={"price": "Preço Médio"})
        st.dataframe(media_cidade)

else:
    st.info("Aguardando o envio do arquivo CSV.")
