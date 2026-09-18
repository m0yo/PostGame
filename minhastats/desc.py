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