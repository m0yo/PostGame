from minhastats.desc import _validate, covariancia, variancia, media, corr_pearson

# A regressão linear simples ajusta uma reta y = a + b*x aos dados, pelo método
# dos mínimos quadrados, minimizando a soma dos quadrados dos resíduos.
# O coeficiente angular (b) e o intercepto (a) se dão por:
# b = covariância(x, y) / variância(x)
# a = média(y) - b * média(x)
# R² (coeficiente de determinação) é o quadrado da correlação de Pearson,
# e mede o quanto da variação de y é explicada pela reta
def regress_lin(x, y):
    dx = _validate(x)
    dy = _validate(y)

    if len(dx) != len(dy):
        raise ValueError("x e y devem ter o mesmo tamanho.")

    b = covariancia(dx, dy) / variancia(dx)
    a = media(dy) - b * media(dx)
    r = corr_pearson(dx, dy)
    r2 = r ** 2

    return {"a": a, "b": b, "r": r, "r2": r2}