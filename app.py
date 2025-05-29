import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

st.title("Análise com Seaborn")

df = sns.load_dataset("penguins")

st.write("### Visualização dos dados")
st.write(df.head())

st.write("### Gráfico de dispersão")
fig, ax = plt.subplots()
sns.scatterplot(data=df, x="bill_length_mm", y="bill_depth_mm", hue="species", ax=ax)
st.pyplot(fig)
