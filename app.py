import streamlit as st
import pandas as pd
from minhastats.desc import *
import matplotlib.pyplot as plt
import random
from minhastats.regress import *

st.set_page_config(page_title="Jogos", layout="wide")
st.title("PostGame Stats!")
st.caption("Aplicação interativa em Python para exploração e análise estatística utilizando o dataset 'Video Game Sales with Ratings'")

DATA = "data/dataset.csv"

# interpreta a assimetria de uma distribuição comparando média e mediana:
# se forem aproximadamente iguais (dentro de uma margem baseada no desvio padrão),
# a distribuição é considerada simétrica; se a média for maior, assimetria positiva
# (cauda à direita); se for menor, assimetria negativa (cauda à esquerda)
def intr_assim(dados):
    med = media(dados)
    medn = mediana(dados)
    dp = desvio_padrao(dados)

    margem = 0.05 * dp

    if margem > abs(med - medn):
        return f"Distribuição aproximadamente simétrica (média {med:.2f} ≈ mediana {medn:.2f})."
    
    elif med > medn:
        return f"Assimetria positiva, cauda à direita (média {med:.2f} ≈ mediana {medn:.2f})"

    elif med < medn:
        return f"Assimetria negativa, cauda à esquerda (média {med:.2f} ≈ mediana {medn:.2f})"

# A Lei dos Grandes Números afirma que, conforme o número de repetições de um experimento aleatório aumenta, a frequência relativa observada de um evento
# tende a convergir para a sua probabilidade teórica. Aqui simulamos lançamentos de uma moeda honesta (P(cara) = 0.5) e acompanhamos essa convergência
def lei_bigNum(n):
        caras = 0
        freq = []

        for i in range(1, n + 1):
            resultado = random.random()
            if resultado < 0.5:
                caras += 1

            freq_relativa = caras / i
            freq.append(freq_relativa)

        return freq

# O Teorema Central do Limite afirma que, ao retirar amostras aleatórias de uma população (mesmo que a distribuição da população não seja normal) e calcular
# a média de cada amostra, a distribuição dessas médias amostrais se aproxima de uma distribuição Normal conforme o tamanho da amostra aumenta
def tcl(dados, tamanho_amostra, n_repeticoes):
    medias_amostrais = []

    for i in range(n_repeticoes):
        amostra = random.choices(dados, k=tamanho_amostra)
        media_amostra = media(amostra)
        medias_amostrais.append(media_amostra)

    return medias_amostrais

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
        st.subheader("Histograma")
        fig_hist, ax_hist = plt.subplots(figsize=(6, 4))
        ax_hist.hist(dados_var, bins=limits, edgecolor="black")
        ax_hist.set_xlabel(var)
        ax_hist.set_ylabel("Frequência")
        ax_hist.set_title(f"Histograma de {var}")
        fig_hist.tight_layout()
        fig_hist.subplots_adjust(left=0.15, right=0.95, top=0.9, bottom=0.15)
        st.pyplot(fig_hist, width='content')

    with col_f:
        st.subheader("Boxplot")
        fig_box, ax_box = plt.subplots(figsize=(6, 3))
        ax_box.boxplot(dados_var)
        ax_box.set_xlabel(var)
        ax_box.set_title(f"Boxplot de {var}")
        fig_box.tight_layout()
        fig_hist.subplots_adjust(left=0.15, right=0.95, top=0.9, bottom=0.15)
        st.pyplot(fig_box, width='content')

    col_g, col_h = st.columns(2)

    with col_g:
        st.subheader("Ajuste de Distribuição Teórica")
        
        med = media(dados_var)
        dp = desvio_padrao(dados_var)
        
        x_vals = [min(dados_var) + i * (max(dados_var) - min(dados_var)) / 200 for i in range(201)]
        y_vals = [pdf_norm(x, med, dp) for x in x_vals]
        
        fig_dist, ax_dist = plt.subplots(figsize=(8, 4))
        ax_dist.hist(dados_var, bins=limits, density=True, edgecolor="black", alpha=0.6, label="Dados reais")
        ax_dist.plot(x_vals, y_vals, color="red", linewidth=2, label=f"Normal (μ={med:.2f}, σ={dp:.2f})")
        ax_dist.set_xlabel(var)
        ax_dist.set_ylabel("Densidade")
        ax_dist.set_title(f"Ajuste da Distribuição Normal para {var}")
        ax_dist.legend()
        st.pyplot(fig_dist)

    with col_h:
        st.subheader("Ajuste de Distribuição Exponencial")

        lam = 1 / med

        y_vals_exp = [pdf_exp(x, lam) for x in x_vals]

        fig_exp, ax_exp = plt.subplots(figsize=(8, 4))
        ax_exp.hist(dados_var, bins=limits, density=True, edgecolor="black", alpha=0.6, label="Dados reais")
        ax_exp.plot(x_vals, y_vals_exp, color="green", linewidth=2, label=f"Exponencial (λ={lam:.4f})")
        ax_exp.set_xlabel(var)
        ax_exp.set_ylabel("Densidade")
        ax_exp.set_title(f"Ajuste da Distribuição Exponencial para {var}")
        ax_exp.legend()
        st.pyplot(fig_exp)


else:
    dados_var = df[var].dropna().tolist()
    st.write(f"Analisando **{var}** (categórica) - {len(dados_var)} valores válidos")

    # tabela de frequências - categorias
    cat_tabela_f = df[var].value_counts().reset_index()
    cat_tabela_f.columns = [var, "Frequência"]
    st.dataframe(cat_tabela_f)

    top_n = 10  # ajuste esse número como preferir

    st.subheader("Gráficos")
    if len(cat_tabela_f) > top_n:
        dados_grafico = cat_tabela_f.head(top_n)
        st.caption(f"Mostrando as {top_n} categorias mais frequentes de {len(cat_tabela_f)} totais")
    else:
        dados_grafico = cat_tabela_f

    col_g, col_h = st.columns(2)
    with col_g:
        fig_bar, ax_bar = plt.subplots(figsize=(6, 4))
        ax_bar.bar(dados_grafico[var], dados_grafico["Frequência"])
        ax_bar.set_xlabel(var)
        ax_bar.set_ylabel("Frequência")
        ax_bar.set_title(f"Distribuição de {var}")
        plt.xticks(rotation=45, ha="right")
        st.pyplot(fig_bar)

    with col_h:
        fig_pizza, ax_pizza = plt.subplots(figsize=(6, 4))
        ax_pizza.pie(dados_grafico["Frequência"], labels=dados_grafico[var], autopct="%1.1f%%")
        ax_pizza.set_title(f"Distribuição de {var} (top {top_n})")
        st.pyplot(fig_pizza)

st.divider()
st.header("Probabilidade e Simulação")

st.subheader("Lei dos Grandes Números")
n_lancamentos = st.slider("Número de lançamentos:", min_value=10, max_value=10000, value=1000, step=10)

if st.button("Simular Lei dos Grandes Números"):
    freqs = lei_bigNum(n_lancamentos)

    fig_lgn, ax_lgn = plt.subplots(figsize=(8, 4))
    ax_lgn.plot(range(1, n_lancamentos + 1), freqs, linewidth=1)
    ax_lgn.axhline(y=0.5, color="red", linestyle="--", label="Valor teórico (0.5)")
    ax_lgn.set_xlabel("Número de lançamentos")
    ax_lgn.set_ylabel("Frequência relativa de 'cara'")
    ax_lgn.set_title("Convergência da Frequência Relativa")
    ax_lgn.legend()
    st.pyplot(fig_lgn)

    st.write(f"Frequência relativa final (após {n_lancamentos} lançamentos): **{freqs[-1]:.4f}**")

st.subheader("Teorema Central do Limite")

var_tcl = st.selectbox("Escolha uma variável numérica:", col_num, key="var_tcl")
tam_amostra = st.slider("Tamanho de cada amostra:", min_value=2, max_value=200, value=30, step=1)
n_rep = st.slider("Número de repetições:", min_value=100, max_value=5000, value=1000, step=100)

if st.button("Simular Teorema Central do Limite"):
    dados_tcl = df[var_tcl].dropna().tolist()
    medias = tcl(dados_tcl, tam_amostra, n_rep)

    fig_tcl, ax_tcl = plt.subplots(figsize=(8, 4))
    ax_tcl.hist(medias, bins=30, edgecolor="black")
    ax_tcl.set_xlabel(f"Média amostral de {var_tcl}")
    ax_tcl.set_ylabel("Frequência")
    ax_tcl.set_title(f"Distribuição das Médias Amostrais (n={tam_amostra}, repetições={n_rep})")
    st.pyplot(fig_tcl)

    st.write(f"Média das médias amostrais: **{media(medias):.4f}**")
    st.write(f"Desvio padrão das médias amostrais: **{desvio_padrao(medias):.4f}**")

st.divider()
st.header("Correlação e Regressão Linear")

col_x, col_y = st.columns(2)
with col_x:
    var_x = st.selectbox("Variável X:", col_num, key="var_x")
with col_y:
    var_y = st.selectbox("Variável Y:", col_num, key="var_y", index=1)

if var_x == var_y:
    st.warning("Escolha duas variáveis diferentes para X e Y.")
else:
    df_xy = df[[var_x, var_y]].dropna()
    x_dados = df_xy[var_x].tolist()
    y_dados = df_xy[var_y].tolist()

    resultado = regress_lin(x_dados, y_dados)
    a, b, r, r2 = resultado["a"], resultado["b"], resultado["r"], resultado["r2"]

    fig_reg, ax_reg = plt.subplots(figsize=(8, 5))
    ax_reg.scatter(x_dados, y_dados, alpha=0.4, label="Dados")

    x_linha = [min(x_dados), max(x_dados)]
    y_linha = [a + b * xi for xi in x_linha]
    ax_reg.plot(x_linha, y_linha, color="red", linewidth=2, label="Reta de regressão")

    ax_reg.set_xlabel(var_x)
    ax_reg.set_ylabel(var_y)
    ax_reg.set_title(f"{var_y} em função de {var_x}")
    ax_reg.legend()
    st.pyplot(fig_reg)

    st.write(f"**Equação:** {var_y} = {a:.4f} + {b:.4f} × {var_x}")
    st.write(f"**Correlação de Pearson (r):** {r:.4f}")
    st.write(f"**R²:** {r2:.4f}")

    st.info(
    f"Para cada unidade a mais em {var_x}, "
    f"{var_y} muda em média {b:.4f} unidades. "
    f"Quando {var_x} = 0, o modelo prevê {var_y} = {a:.4f}.")

    st.subheader("Predição Interativa")
    x_input = st.number_input(f"Digite um valor de {var_x}:", value=float(media(x_dados)))
    y_previsto = a + b * x_input
    st.metric(f"{var_y} previsto", f"{y_previsto:.2f}")

    st.warning("Correlação não implica causalidade! Uma relação estatística entre duas variáveis não significa que uma causa a outra.")