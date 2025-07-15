import streamlit as st

import pandas as pd

import plotly.graph_objects as go

import numpy as np



# --- Carregar dados ---

@st.cache_data

def carregar_dados():

    return pd.read_csv("Preços Herois.csv")



df = carregar_dados()



st.title("📊 Histograma Interativo de Preços")



# --- Filtros ---

st.sidebar.header("Filtros")



# Serviço

todos_servicos = sorted(df["servico"].unique())

selecionar_todos_servicos = st.sidebar.checkbox("Selecionar todos os serviços", value=True)

if selecionar_todos_servicos:

    servicos = st.sidebar.multiselect("Serviço", todos_servicos, default=todos_servicos)

else:

    servicos = st.sidebar.multiselect("Serviço", todos_servicos)



# Estado

todos_estados = sorted(df["Estado"].unique())

selecionar_todos_estados = st.sidebar.checkbox("Selecionar todos os estados", value=True)

if selecionar_todos_estados:

    estados = st.sidebar.multiselect("Estado", todos_estados, default=todos_estados)

else:

    estados = st.sidebar.multiselect("Estado", todos_estados)



# Cidade

cidades_disponiveis = sorted(df[df["Estado"].isin(estados)]["Cidade"].unique())

selecionar_todas_cidades = st.sidebar.checkbox("Selecionar todas as cidades", value=True)

if selecionar_todas_cidades:

    cidades = st.sidebar.multiselect("Cidade", cidades_disponiveis, default=cidades_disponiveis)

else:

    cidades = st.sidebar.multiselect("Cidade", cidades_disponiveis)



# --- Filtrar dados ---

df_filtrado = df[

    (df["servico"].isin(servicos)) &

    (df["Estado"].isin(estados)) &

    (df["Cidade"].isin(cidades))

]



# --- Plot ---

st.subheader("Distribuição de Preços (com filtros aplicados)")



if df_filtrado.empty:

    st.warning("Nenhum dado encontrado com os filtros selecionados.")

else:

    bin_size = 20

    max_price = df_filtrado["price"].max()

    bins = np.arange(0, max_price + bin_size, bin_size)



    # Calcular histograma

    hist_data = []

    for serv in df_filtrado["servico"].unique():

        df_serv = df_filtrado[df_filtrado["servico"] == serv]

        counts, _ = np.histogram(df_serv["price"], bins=bins)

        percent = (counts / counts.sum()) * 100

        labels = [f"R${bins[i]:.0f} - R${bins[i+1]-1:.0f}" for i in range(len(counts))]



        hist_data.append(go.Bar(

            x=labels,

            y=counts,

            name=serv,

            hovertemplate="<br>".join([

                "Serviço: " + serv,

                "Faixa de preço: %{x}",

                "Quantidade: %{y}",

                "Percentual: %{customdata:.1f}%",

            ]),

            customdata=percent

        ))



    # Média

    media = df_filtrado["price"].mean()



    layout = go.Layout(

        title="Distribuição de Preços por Serviço",

        xaxis_title="Faixa de Preço (R$)",

        yaxis_title="Quantidade",

        barmode="stack",

        bargap=0.05,

        shapes=[

            dict(

                type="line",

                x0=f"R${int(media // bin_size) * bin_size} - R${int(media // bin_size) * bin_size + bin_size - 1}",

                x1=f"R${int(media // bin_size) * bin_size} - R${int(media // bin_size) * bin_size + bin_size - 1}",

                y0=0,

                y1=max(counts),

                line=dict(color="black", dash="dash"),

            )

        ],

        annotations=[

            dict(

                x=f"R${int(media // bin_size) * bin_size} - R${int(media // bin_size) * bin_size + bin_size - 1}",

                y=max(counts),

                text=f"Média: R${media:.2f}",

                showarrow=True,

                arrowhead=1

            )

        ]

    )



    fig = go.Figure(data=hist_data, layout=layout)



    st.plotly_chart(fig, use_container_width=True)
