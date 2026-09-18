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