import numpy as np
import pytest
from scipy import stats
from minhastats.desc import *
from minhastats.regress import *

# Testes da função media ===============================================================================
def test_media_simple():
    dados = [5, 3, 7, 9, 10, 12, 15] # dados de entrada para teste

    expected = np.mean(dados) # media esperada, calculdada pela a lib de referência
    result = media(dados) # media calculada por implementação própria

    assert result == pytest.approx(expected, abs=1e-6) # comparação dos resultados com tolerância float

def test_media_vazia(): # testa se a função de validação funciona quando a lista for vazia
    with pytest.raises(ValueError):
        media([])

# Testes da função mediana ===============================================================================
def test_mediana_odd(): # testa a mediana por implementação própria quando a quantidade de elementos da listagem é ímpar
    dados = [1, 3, 5, 7, 9]

    expected = np.median(dados)
    result = mediana(dados)

    assert result == pytest.approx(expected, abs=1e-6) 

def test_mediana_even(): # testa a mediana por implementação própria quando a quantidade de elementos da listagem é par
    dados = [1, 3, 5, 7]

    expected = np.median(dados)
    result = mediana(dados)

    assert result == pytest.approx(expected, abs=1e-6)

def test_mediana_vazia(): # testa se a função de validação funciona quando a lista for vazia
    with pytest.raises(ValueError):
        mediana([])

# Testes da função moda ===============================================================================
def test_moda_single(): # testa a moda por implementação própria, quando a moda for única
    dados = [1, 2, 2, 3, 3, 4, 1, 3, 2, 5, 2] # 2 é a moda pois aparece 4 vezes

    assert moda(dados) == [2]

def test_moda_multi(): # neste caso é quando a moda for multimodal
    dados = [1, 1, 2, 2, 3]

    result = moda(dados)
    assert sorted(result) == [1, 2] 

def test_moda_vazia(): # testa se a função de validação funciona quando a lista for vazia
    with pytest.raises(ValueError):
        moda([])

# Testes da função amplitude ===============================================================================
def test_ampl_simple(): # testa a amplitude com valores variados
    dados = [105, 93, 495, 102, 583, 123, 134, 205] # valor esperado: 583 - 93 = 490

    expected = np.ptp(dados)
    result = amplitude(dados)

    assert result == pytest.approx(expected, abs=1e-6)

def test_ampl_equal(): # nesnte caso é quando os valores forem iguais
    dados = [5, 5, 5] # o esperado é 0, já que o max e o min coincidem

    assert amplitude(dados) == 0

def test_ampl_vazia(): # testa se a função de validação funciona quando a lista for vazia
    with pytest.raises(ValueError):
        amplitude([])

# Testes da função variância ===============================================================================
def test_var_ams_simple(): # testa a variancia amostral em um caso simples
    dados = [2, 4, 4, 4, 5, 5, 7, 9] # amostral, espera-se: ~4,571

    expected = np.var(dados, ddof=1)
    result = variancia(dados)

    assert result == pytest.approx(expected, abs=1e-6)

def test_var_pop_simple(): # testa a variancia populacional em um caso simples
    dados = [2, 4, 4, 4, 5, 5, 7, 9] # populacional, espera-se: 4.0

    expected = np.var(dados, ddof=0)
    result = variancia(dados, amostral=False)

    assert result == pytest.approx(expected, abs=1e-6)

def test_var_vazia(): # testa se a função de validação funciona quando a lista for vazia
    with pytest.raises(ValueError):
        variancia([])

def test_var_single(): # testa se a função de validação funciona quando a lista tiver apenas um elemento
    with pytest.raises(ValueError):
        variancia([5])

# Testes da função desvio padrão ===============================================================================
def test_dp_ams_simple(): # testa o desvio padrão amostral em um caso simples
    dados = [2, 4, 4, 4, 5, 5, 7, 9] # espera-se: ~2,135

    expected = np.std(dados, ddof=1)
    result = desvio_padrao(dados)

    assert result == pytest.approx(expected, abs=1e-6)

def test_dp_pop_simple(): # testa o desvio padrão populacional em um caso simples
    dados = [2, 4, 4, 4, 5, 5, 7, 9] # espera-se: 2.0

    expected = np.std(dados, ddof=0)
    result = desvio_padrao(dados, amostral=False)

    assert result == pytest.approx(expected, abs=1e-6)

def test_dp_vazia(): # testa se a função de validação funciona quando a lista for vazia
    with pytest.raises(ValueError):
        desvio_padrao([])

def test_dp_single(): # testa se a função de validação funciona quando a lista tiver apenas um elemento
    with pytest.raises(ValueError):
        desvio_padrao([5])

# Teste percentil ===============================================================================
def test_percentil_val():  # compara vários percentis com np.percentile
    dados = [2, 4, 4, 4, 5, 5, 7, 9]

    for p in [10, 25, 50, 75, 90]:
        expected = np.percentile(dados, p)
        result = percentil(dados, p)
        assert result == pytest.approx(expected, abs=1e-6)

def test_percentil_out():  # p deve estar entre 0 e 100
    with pytest.raises(ValueError):
        percentil([1, 2, 3], 150)

# Teste quartis ===============================================================================
def test_quartis_simple():  # confere Q1, Q2 e Q3 contra np.percentile
    dados = [2, 4, 4, 4, 5, 5, 7, 9]

    result = quartis(dados)
    assert result["Q1"] == pytest.approx(np.percentile(dados, 25), abs=1e-6)
    assert result["Q2"] == pytest.approx(np.percentile(dados, 50), abs=1e-6)
    assert result["Q3"] == pytest.approx(np.percentile(dados, 75), abs=1e-6)

# Teste iqr ===============================================================================
def test_iqr_simple():  # IQR = Q3 - Q1
    dados = [2, 4, 4, 4, 5, 5, 7, 9]

    expected = np.percentile(dados, 75) - np.percentile(dados, 25)
    result = iqr(dados)
    assert result == pytest.approx(expected, abs=1e-6)

#Teste coeficiente de variação ===============================================================================
def test_coef_var_simple():  # compara o CV com o cálculo manual via numpy
    dados = [2, 4, 4, 4, 5, 5, 7, 9]

    expected = np.std(dados, ddof=1) / np.mean(dados)
    result = coef_var(dados)
    assert result == pytest.approx(expected, abs=1e-6)

def test_coef_var_media_zero():  # média zero deve lançar erro
    with pytest.raises(ValueError):
        coef_var([-3, 0, 3])

# Teste covariancia ===============================================================================
def test_covariancia_simple():  # compara com np.cov
    x = [1, 2, 3, 4, 5]
    y = [2, 4, 5, 4, 5]

    expected = np.cov(x, y, ddof=1)[0][1]
    result = covariancia(x, y)

    assert result == pytest.approx(expected, abs=1e-6)

def test_covariancia_pop():  # versão populacional (ddof=0)
    x = [1, 2, 3, 4, 5]
    y = [2, 4, 5, 4, 5]

    expected = np.cov(x, y, ddof=0)[0][1]
    result = covariancia(x, y, amostral=False)

    assert result == pytest.approx(expected, abs=1e-6)

def test_covariancia_diff():  # x e y devem ter o mesmo tamanho
    with pytest.raises(ValueError):
        covariancia([1, 2, 3], [1, 2])

def test_covariancia_vazia():  # listas vazias devem lançar erro
    with pytest.raises(ValueError):
        covariancia([], [])

# Teste correlação pearson ===============================================================================
def test_corr_pearson_simple():  # compara com scipy.stats.pearsonr
    x = [1, 2, 3, 4, 5]
    y = [2, 4, 5, 4, 5]

    expected = stats.pearsonr(x, y)[0]
    result = corr_pearson(x, y)

    assert result == pytest.approx(expected, abs=1e-6)

def test_corr_pearson_constante():  # correlação indefinida quando uma variável é constante
    x = [1, 2, 3, 4, 5]
    y = [7, 7, 7, 7, 7]

    with pytest.raises(ValueError):
        corr_pearson(x, y)

# Teste regra struges ===============================================================================
def test_sturges_simple():
    assert regra_sturges(1000) == 11 # espera-se o valor 11
    assert regra_sturges(100) == 8 # esepra-se o valor 8

def test_struges_vazio():
    with pytest.raises(ValueError):
        regra_sturges(0)

# Teste detecção de outliers ===============================================================================

def test_detec_simple():
    dados = [10, 12, 12, 13, 12, 11, 14, 13, 15, 10, 100]  # 100 é um outlier
    resultado = detec_outliers(dados)
    assert 100 in resultado["outliers"]
    assert len(resultado["outliers"]) == 1

def test_regress_lin_simple():
    x = [1, 2, 3, 4, 5]
    y = [2, 4, 5, 4, 5]

    esperado = stats.linregress(x, y)
    resultado = regress_lin(x, y)

    assert resultado["a"] == pytest.approx(esperado.intercept, abs=1e-6)
    assert resultado["b"] == pytest.approx(esperado.slope, abs=1e-6)
    assert resultado["r"] == pytest.approx(esperado.rvalue, abs=1e-6)

def test_regress_lin_diff(): # teste da regressao linear quando os valores forem diferentes
    with pytest.raises(ValueError):
        regress_lin([1, 2, 3], [1, 2])