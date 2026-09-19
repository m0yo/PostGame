import math

# A função a seguir valida se a listagem de dados é vazia ou não e depois devolve os dados
def _validate(dados):
    x = len(dados)
    if x == 0:
        raise ValueError("A listagem não pode ser vazia.")

    return list(dados)

# A média é definida pelo somatório dos elementos divididos pela quantidade de elementos
# como demonstra a equação a seguir:
# x = (d_1 + d_2 + ... + d_n) / n
def media(dados):
    d = _validate(dados)

    soma = 0.0
    for x in d:
        soma += x
    
    return soma / len(d)

# A mediana é o elemento que se encontra na posição central de uma listagem ordenada
# Se a listagem tiver um número par de elementos, faz-se a média dos dois elementos centrais
def mediana(dados):
    d = _validate(dados)

    ord = sorted(d)
    n = len(ord)

    if n % 2 != 0:
        return ord[n // 2]

    else:
        mid1 = ord[(n // 2) - 1]
        mid2 = ord[n // 2]

        return (mid1 + mid2) / 2

# A moda é o elemento que mais se repete em uma listagem
def moda(dados):
    d = _validate(dados)

    count = {}

    for x in d:
        count[x] = count.get(x, 0) + 1

    high = max(count.values())
    modas = []

    for valor, freq in count.items():
        if freq == high:
            modas.append(valor)

    return modas

# Amplitude é dada pela diferença entre o maior e o menor dado de uma listagem
def amplitude(dados):
    d = _validate(dados)
    return max(d) - min(d)

# A variância mostra o espelhamento de dados ao redor do valor central (média), podendo ser a amostral e a populacional
# A variância populacional é definida por: var_p = (somátorio dos (x - média)^2) / n
# A variância amostral é definida por: var_a = (somátorio dos (x - média)^2) / (n - 1)

def variancia(dados, amostral=True):
    d = _validate(dados)
    med = media(d)

    sum_q = 0.0
    for x in d:
        sum_q += (x - med) ** 2

    if amostral == True:
        if len(d) == 1:
            raise ValueError("Para o cálculo da variância amostral, a quantidade de valores precisa ser maior que 1.")

        else:
            return sum_q / (len(d) - 1)

    else:
        return sum_q / len(d)

# O desvio-padrão demostra o quão distantes estão os valores de um conjunto em relação à média
# Ele se dá por: Dp = √(variância)

def desvio_padrao(dados, amostral=True):
    d = _validate(dados)
    var = variancia(d, amostral)

    return (var)**0.5 # raíz quadrada sem o uso da biblioteca math

# O percentil divide um conjunto de dados ordenados do menor para o maior em cem partes iguais
# nesse caso, o percentil p é calculado por interpolação linear
def percentil(dados, p):
    if not (0 <= p <= 100):
        raise ValueError("O percentil deve estar entre 0 e 100")

    d = sorted(_validate(dados))
    n = len(d)

    if n == 1:
        return float(d[0])

    pos = (p / 100)*(n - 1)
    id_inf = int(pos)
    id_sup = min(id_inf + 1, n - 1) # proteção contra estouro
    frac = pos - id_inf

    return d[id_inf] + frac * (d[id_sup] - d[id_inf])

# O quartil dividem os dados ordenados em quatro partes iguais, nesse caso utiliza-se a função de percentil já implementada
def quartis(dados):
    return {
        "Q1": percentil(dados, 25),
        "Q2": percentil(dados, 50),
        "Q3" : percentil(dados, 75),
    }

# O IQR (intervalo interquartil) mede a dispersão dos 50% centrais dos dados
# se dá por: IQR = Q3 - Q1
def iqr(dados):
    q = quartis(dados)
    return q["Q3"] - q["Q1"]

# O coeficiente de variação mede a dispersão relativa à média (adimensional),bom pra comparar variáveis com escalas diferentes
# se dá por: CV = desvio_padrao / média
def coef_var(dados, amostral=True):
    med = media(dados)

    if med == 0:
        raise ValueError("Coeficiente de variação indefinido quando a média é zero.")
    return desvio_padrao(dados, amostral=amostral) / med

# A covariância mede se duas variáveis "andam juntas": positiva quando crescem juntas, negativa quando uma cresce e a outra decresce, perto de zero quando
# não há relação linear clara. Trabalha com pares (x_i, y_i)
# se dá por: cov = (somatório de (x_i - média_x)*(y_i - média_y)) / divisor
# (divisor = n-1 para amostral, n para populacional)
def covariancia(x, y, amostral=True):
    dx = _validate(x)
    dy = _validate(y)

    if len(dx) != len(dy):
        raise ValueError("x e y devem ter o mesmo tamanho.")

    n = len(dx)
    if amostral and n == 1:
        raise ValueError("Para o cálculo da covariância amostral, a quantidade de pares precisa ser maior que 1.")

    mx = media(dx)
    my = media(dy)

    sum_q = 0.0
    for xi, yi in zip(dx, dy):
        sum_q += (xi - mx) * (yi - my)

    if amostral:
        return sum_q / (n - 1)
    else:
        return sum_q / n


# A correlação de Pearson é a covariância "normalizada" pelos desvios padrão
# de x e y, sempre entre -1 e 1, o que facilita interpretar a força e direção
# da relação linear entre as duas variáveis, independente da escala de cada uma
# Se dá por: r = cov(x, y) / (desvio_padrao(x) * desvio_padrao(y))
def corr_pearson(x, y):
    cov = covariancia(x, y, amostral=True)
    dpx = desvio_padrao(x, amostral=True)
    dpy = desvio_padrao(y, amostral=True)

    if dpx == 0 or dpy == 0:
        raise ValueError("Correlação indefinida quando uma variável é constante.")

    return cov / (dpx * dpy)

# regra de Sturges éuma fórmula estatística usada para calcular o número ideal de classes 
# ou intervalos em um histograma ou tabela de distribuição de frequências
# ela se dá pela equação: k = 1 + 3,322 * (log (n))
def regra_sturges(num):
    if num <= 0:
        raise ValueError("O número de dados deve ser maior que zero.") # retorna um erro se o valor for zero
    x = 1 + 3.322 * (math.log10(num))

    return math.ceil(x)

# Outliers são valores atípicos que se afasta muito de um conjunto de dados.
# A sua detectção pode ser feita usando interquantis (IQR), a regra é:
# um valor é outlier se estiver abaixo de Q1 - 1.5*IQR ou acima de Q3 + 1.5*IQR
def detec_outliers(dados):
    d = _validate(dados)
    val_q = quartis(d)
    faixa = iqr(d)

    lim_inf = val_q['Q1'] - 1.5*faixa
    lim_sup = val_q["Q3"] + 1.5*faixa

    outliers =[
        x for x in d 
        if x < lim_inf or x > lim_sup
    ]

    return {
        "outliers": outliers,
        "limite_inferior": lim_inf,
        "limite_superior": lim_sup
    }

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