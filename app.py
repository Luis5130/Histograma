import streamlit as st
import pandas as pd
import plotly.express as px

# Carrega dados do CSV no repo (coloque o CSV no mesmo repo ou defina o path certo)
df = pd.read_csv("Preços Herois.csv")

st.title("Histograma Interativo de Preços por Serviço")

# Filtro por Cidade
cidade_selecionada = st.selectbox("Selecione a Cidade", options=["Todas"] + df['Cidade'].unique().tolist())

if cidade_selecionada != "Todas":
    df = df[df['Cidade'] == cidade_selecionada]

# Histograma por Serviço (preços)
fig = px.histogram(df, x='servico', y='price', color='servico',
                   histfunc='avg',  # média
                   labels={'servico': 'Serviço', 'price': 'Preço Médio'},
                   title='Preço médio por serviço',
                   hover_data={'price': ':.2f'})

fig.update_layout(bargap=0.2)

st.plotly_chart(fig, use_container_width=True)
