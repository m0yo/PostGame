import streamlit as st
import pandas as pd
from minhastats.desc import *
import matplotlib.pyplot as plt

st.set_page_config(page_title="Jogos", layout="wide")
st.title("PostGame Stats!")
st.caption("Aplicação interativa em Python para exploração e análise estatística utilizando o dataset 'Video Game Sales with Ratings'")

DATA = "data/dataset.csv"

@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    df['User_Score'] = pd.to_numeric(df['User_Score'], errors='coerce') # esta linha converte os dados da coluna User_Score para números e se não houver nenhum dado na coluna, ele retorna 'None'

    return df

df = load_data(DATA) # carrega a tabela

# aqui divide as colunas categoricas e as numericas
col_num = df.select_dtypes(include="number").columns.tolist()
col_cat = df.select_dtypes(exclude="number").columns.tolist()

col_1, col_2 = st.columns(2)

st.write(f"Formato do dataset: {df.shape[0]} linhas, {df.shape[1]} colunas")
with col_1:
    st.write("Colunas numéricas:", col_num)

with col_2:
    st.write("Colunas Categóricas:", col_cat)

st.write(df)

st.divider()
st.header ("Explore os dados do dataset")

var = st.selectbox("Escolha uma variável para análise: ", df.columns.tolist())

if var in col_num:
    dados_var = df[var].dropna().tolist()
    st.write(f"Analisando **{var}** (numérica) - {len(dados_var)} valores válidos")

    # tabela de frequência por classes para variaveis numericas
    # cria-se uma faixa numerica para organizar os valores, a regra de sturges ajuda a determinar a quantidade de faixas
    k = regra_sturges(len(dados_var))
    larg = amplitude(dados_var) / k
    minm = min(dados_var)

    limits = [minm + i * larg for i in range(k + 1)]
    _class = pd.cut(dados_var, bins=limits, include_lowest=True)
    num_tabela_f = _class.value_counts().sort_index().reset_index()
    num_tabela_f.columns = ["Classe", "Frequência"]

    def format_lim(x):
        x_arred = round(x, 1)
        return 0.0 if x_arred == 0 else x_arred

    num_tabela_f["Classe"] = num_tabela_f["Classe"].apply(
        lambda i: f'{format_lim(i.left):.0f} - {format_lim(i.right):.0f}'
    )
    st.dataframe(num_tabela_f)

    st.subheader("Medidas Estatísticas")

    col_a, col_b, col_c, col_d = st.columns(4)

    with col_a:
        st.metric("Média", f"{media(dados_var):.2f}")
        st.metric("Mediana", f"{mediana(dados_var):.2f}")

    with col_b:
        st.metric("Desvio Padrão", f"{desvio_padrao(dados_var):.2f}")
        st.metric("Variância", f"{variancia(dados_var):.2f}")
        st.caption("Variância e desvio padrão calculados como amostrais")

    with col_c:
        q = quartis(dados_var)
        st.metric("Q1", f"{q['Q1']:.2f}")
        st.metric("Q3", f"{q['Q3']:.2f}")

    with col_d:
        st.metric("Amplitude", f"{amplitude(dados_var):.2f}")
        moda_valores = moda(dados_var)
        moda_texto = ", ".join(f"{v:.2f}" for v in moda_valores)
        st.metric("Moda", moda_texto)

    res_outliers = detec_outliers(dados_var)
    qtd_outliers = len(res_outliers["outliers"])

    if qtd_outliers > 0:
        st.warning(
            f"Detectados **{qtd_outliers}** outliers pela regra do IQR "
            f"(fora do intervalo [{res_outliers['limite_inferior']:.0f}, "
            f"{res_outliers['limite_superior']:.0f}])."
        )
    else:
        st.success("Nenhum outlier detectado pela regra do IQR.")

    texto_assimetria = intr_assim(dados_var)
    st.info(texto_assimetria)

    st.subheader("Gráficos")

    col_e, col_f = st.columns(2)

    with col_e:
        fig_hist, ax_hist = plt.subplots(figsize=(5, 2.81))
        ax_hist.hist(dados_var, bins=limits, edgecolor="black")
        ax_hist.set_xlabel(var)
        ax_hist.set_ylabel("Frequência")
        ax_hist.set_title(f"Histograma de {var}")
        st.pyplot(fig_hist)

    with col_f:
        fig_box, ax_box = plt.subplots(figsize=(6, 3))
        ax_box.boxplot(dados_var)
        ax_box.set_xlabel(var)
        ax_box.set_title(f"Boxplot de {var}")
        st.pyplot(fig_box)


else:
    dados_var = df[var].dropna().tolist()
    st.write(f"Analisando **{var}** (categórica) - {len(dados_var)} valores válidos")

    # tabela de frequências - categorias
    cat_tabela_f = df[var].value_counts().reset_index()
    cat_tabela_f.columns = [var, "Frequência"]
    st.dataframe(cat_tabela_f)

    fig_bar, ax_bar = plt.subplots(figsize=(6, 4))
    ax_bar.bar(cat_tabela_f[var], cat_tabela_f["Frequência"])
    ax_bar.set_xlabel(var)
    ax_bar.set_ylabel("Frequência")
    ax_bar.set_title(f"Distribuição de {var}")
    plt.xticks(rotation=45, ha="right")
    st.pyplot(fig_bar)