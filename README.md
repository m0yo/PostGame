# PostGame Stats
### Laboratório de Estatística Interativo sobre Venda e Avaliações de Jogos

Aplicação interativa em Python para exploração e análise estatística utilizando o dataset [*Video Game Sales with Ratings*](https://www.kaggle.com/datasets/rush4ratio/video-game-sales-with-ratings). A aplicação foi construída por uma biblioteca de estatística própria (`minhastats`), sem utilizar funções existentes do NumPy/SciPy para cálculos estatísticos. Tais funções foram utilizados somente como referência nos testes automatizados para validar as funções em `minhastats`.

Desenvolvido por:
  - Maria Clara Canuto Gontijo
  - Matrícula (RA): 72601725

> ⚠️ Projeto em Desenvolvimento: Este README cobre apenas o que foi implementado até o momento e cumpre o papel de referência para a dev. Critérios e módulos não implementados serão documentados em breve.

## Estrutura do projeto
 
```
PostGame/
├── app.py                  # Aplicação Streamlit (carregamento e visualização inicial dos dados)
├── data/
│   └── dataset.csv         # Dataset: Video Game Sales with Ratings
├── minhastats/
│   ├── __init__.py
│   └── desc.py              # Estatística descritiva própria
├── tests/
│   └── test_desc.py         # Testes automatizados (pytest) comparando com NumPy
├── requirements.txt
└── README.md
```
## Dependências

- Python 3.10+
- Disponíveis em `requirements.txt`:
  - Streamlit
  - NumPy
  - SciPy
  - Pytest
  - Matplotlib
 
## Como rodar o projeto

1. Clone o repositório do projeto
```bash
  git clone https://github.com/m0yo/PostGame.git
```

2. Crie e rode um ambiente virtual
```bash
  python -m venv venv
  source venv/bin/activate      # Linux/macOS
  venv\Scripts\activate         # Windows
```

3. Baixe as depedências em `requirements.txt`
```bash
  pip install requirements.txt
```

4. Rode a aplicação:
```bash
 streamlit run app.py
```
A aplicação abrirá no navegador, exibindo o dataset carregado, o formato dos dados e a separação entre colunas numéricas e categóricas.

5. Rode os testes automatizados:
```bash
   pytest
```
Os testes em `tests/test_desc.py` validam as funções de `minhastats/desc.py` (média, mediana e moda) comparando os resultados com o NumPy, usando tolerância numérica (`pytest.approx`).

## Estado atual
 
- [x] Carregamento do dataset e visualização inicial (`app.py`)
- [x] Implementação própria de média, mediana e moda (`minhastats/desc.py`)
- [x] Testes automatizados para as funções implementadas
- [ ] Medidas de dispersão (variância, desvio padrão, etc.)
- [ ] Estatística descritiva interativa completa
- [ ] Probabilidade e simulação Monte Carlo
- [ ] Distribuições teóricas
- [ ] Correlação e regressão linear
- [ ] Relatório de descobertas
