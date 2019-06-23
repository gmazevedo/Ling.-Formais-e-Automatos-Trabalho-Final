from automato import *

def criaDict(afd):
    dict = {estado: {} for estado in afd.estados}

    for chave in dict:
        lista = procuraTrans(chave,afd.transicoes)
        for transicao in lista:
            dict[chave].update({transicao[1]:transicao[2]})

    return dict


def reconhece(dict,inicial,finais,palavra):
    estAtual = inicial

    for char in palavra:
        try:
            estAtual = dict[estAtual][char]
        except KeyError:
            return False

    return estAtual in finais


def listaDef(nome):
    arquivo = open(nome, 'r')

    linhas = arquivo.read()
    linhas = linhas.splitlines()

    while (True):
        if '' not in linhas:
            break
        else:
            linhas.pop(linhas.index(''))

    try:
        linhas.remove('Palavras aceitas:')
        linhas.remove('Palavras rejeitadas:')
    except ValueError:
        pass

    return linhas