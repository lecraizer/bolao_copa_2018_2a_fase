# -*- coding: utf-8 -*-
import csv
import pandas as pd
from collections import Counter


# titulos = {u'Brasil': 5, u'Alemanha': 4, u'Argentina': 2, u'Uruguai': 2, u'França': 1, u'Espanha': 1,
# u'Inglaterra': 1, u'Suiça': 0, u'Croácia': 0, u'Portugal': 0, u'Rússia': 0, u'Bélgica': 0,
# u'México': 0, u'Japão': 0, u'Colômbia': 0, u'Dinamarca': 0}


pontuacoes_acertos = [3, 6, 10, 20, 50]
pontuacoes_erros = [1, 2, 4, 8]

conversao_fases = {u'8as': 0, u'4as': 1, u'Semi': 2, u'Final (\xc9 vice)': 3, u'Campe\xe3o': 4}

header = [u'Brasil', u'Suiça', u'Argentina', u'Croácia', u'Portugal', u'Espanha', u'Rússia', u'Uruguai', u'Bélgica', u'Inglaterra', u'México', u'Alemanha', u'Japão', u'Colômbia', u'França', u'Dinamarca']
fator_multiplicativo = [1, 2, 1.6, 2, 2, 1.8, 2, 1.6, 2, 1.8, 2, 1.2, 2, 2, 1.8, 2]


resultado_oficial = [2, 0, 0, 0, 0, 2, 0, 1, 0, 3, 1, 4, 0, 1, 1, 0]
empates_oficial =   ['TR', 'TR', 'TR', 'TR', 'PP', 'TR', 'TR', 'TR', 'PP', 'TR', 'PP', 'TR', 'TR', 'TR', 'PP', 'TR']

def assert_previsoes(lista):
    d = Counter(lista)
    if (d[0] != 8) or (d[1] != 4) or (d[2] != 2) or (d[3] != 1) or (d[4] != 1):
        raise ValueError('Previsão inválida.')


def pontua_acertos(lista):
    soma = 0
    for k in range(len(lista)):
        delta = 1.
        if lista[k] == resultado_oficial[k]:
            if lista[k] >= 2:
                delta = fator_multiplicativo[k]
            soma += pontuacoes_acertos[lista[k]]*delta
    return soma


def pontua_erros(lista):
    soma = 0
    for k in range(len(lista)):
        if resultado_oficial[k] - lista[k] == 1:
            soma += pontuacoes_erros[lista[k]]
        # nova condição, caso acerte o time que vai pra final pelo menos
        elif resultado_oficial[k] == 3 and lista[k] == 4:
            soma += 8
    return soma


def acertos_desempate(lista):
    soma = 0
    for i in range(len(lista)):
        if lista[i] == empates_oficial[i]:
            soma += 1
    return soma

if __name__ == '__main__':

    df = pd.read_excel('samples/sample_invalido_01.xls')
    A = df.as_matrix()
    previsoes = A[0][1:]
    cods_previsoes = map(conversao_fases.get, previsoes)
    prev_empates = A[1][1:]

    # checando se previsão é válida
    assert_previsoes(cods_previsoes)

    pontuacao_total = 0
    pontuacao_total += pontua_acertos(cods_previsoes)
    pontuacao_total += pontua_erros(cods_previsoes)

    print acertos_desempate(prev_empates)
    print pontuacao_total