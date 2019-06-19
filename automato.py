def stringArq():
    nomeArq = raw_input("Nome do arquivo com o automato: ")
    #nomeArq = "teste.txt"

    arquivo = open(nomeArq, 'r')

    linhas = arquivo.read()

    arquivo.close()

    linhas = linhas.splitlines()

    return linhas


class AFN():
    def __init__(self):
        self.estados =[]
        self.numEstados = 0
        self.alfabeto = []
        self.estInicial = []
        self.estFinais = []
        self.numFinais = 0
        self.transicoes = []

    def init_estados(self):
        self.estados = list(range(self.numEstados))

    def leAFN(self,linhas):
        """Indices da linha 0:
        [0]-ESTADOS [1]-ALFABETO [2]-EST INICIAL [3]-EST FINAL"""
        linhas[0] = linhas[0].split('(')
        linhas[0] = linhas[0][1].split('}')

        self.numEstados = len(linhas[0][0][1:].split(','))
        self.estados = linhas[0][0][1:].split(',')
        self.alfabeto = linhas[0][1][2:].split(',')
        self.estInicial = linhas[0][2][2:].split(',')
        self.estFinais = linhas[0][3][2:].split(',')
        self.numFinais = len(linhas[0][3][2:].split(','))
        self.transicoes = linhas[2:]

        return self.estInicial


    def printaAFN(self):
        print "Numero de estados: "+str(self.numEstados)
        print "Estados: "+str(self.estados)
        print "Alfabeto: "+str(self.alfabeto)
        print "Estados iniciais: " + str(self.estInicial)
        print "Estados finais: "+str(self.estFinais)
        print "Numero de estados finais: " + str(self.numFinais)
        print "Transicoes: "+str(self.transicoes)


class AFD():
    def __init__(self):
        self.estados = []
        self.numEstados = 0
        self.alfabeto = []
        self.estInicial = []
        self.estFinais = []
        self.numFinais = 0
        self.transicoes = []
        self.q = []

    def printaAFD(self):
        print "Numero de estados: "+str(self.numEstados)
        print "Estados: "+str(self.estados)
        print "Alfabeto: "+str(self.alfabeto)
        print "Estados iniciais: " + str(self.estInicial)
        print "Estados finais: "+str(self.estFinais)
        print "Numero de estados finais: " + str(self.numFinais)
        print "Transicoes: "+str(self.transicoes)
        print "Estados temporarios: " + str(self.q)


def estadosEq(afn,afd):

   # afd.q.append(afn.estInicial)
    afd.estados.append(afn.estInicial)

    for a in range(afn.numEstados):
        pos1 = afn.transicoes[a].find(',')
        pos2 = afn.transicoes[a+1].find(',')

        if (afn.transicoes[a][1:pos1] == afn.transicoes[a+1][1:pos2]):    # se os estados sao os mesmos
            pos3 = afn.transicoes[a].find(')')
            pos4 = afn.transicoes[a+1].find(')')

            pos1 += 1
            pos2 += 1

            if(afn.transicoes[a][pos1:pos3] == afn.transicoes[a+1][pos2:pos4] ):   #e as entradas sao as mesmas
                afd.numEstados = afd.numEstados + 1

                pos5 = afn.transicoes[a].find('=') + 1
                pos6 = afn.transicoes[a+1].find('=') + 1


                #afd.estados.append(afn.transicoes[a][pos5+1] + afn.transicoes[a][pos5+2] + afn.transicoes[a+1][pos6+1] + afn.transicoes[a+1][pos6+2])
                afd.q.append([afn.transicoes[a][pos5:],afn.transicoes[a+1][pos6:]])#resultando na concatenacao dos destinos (ex: q5q6)
                afd.estados.append(afn.transicoes[a][pos5:] + afn.transicoes[a + 1][pos6:])
    lista = []
    afd.transicoes = afn.transicoes
    lista = afd.estados
    lista = lista + afn.estados[1:]
    return lista

def detAFN(afd):

    #afd.transicoes.append("("+afd.estados[indicedoestado]+")="+estadoDestino)
    #estadoDestino
    transPraUm = []
    transPraZero = []
    novaTrans =[]

    # para cada estado na lista temporaria de estados
    for estado in afd.q:
        # para cada estado concatenado nesse novo estado do AFD
        for parte in estado:
            # triplas eh uma lista de todas as transicoes deste estado individual
            triplas = procuraTrans(parte,afd.transicoes)

            # para cada transicao em triplas
            for item in triplas:
                # verifica se destino nao eh zero ( se for zero, significa indefinicao)
                if item[2] != '0':
                    # se o simbolo do alfabeto for zero, inclui na lista dos estados destinos gerados quando um 0 eh lido
                    if item[1] == '0':
                        transPraZero.append(item[2])
                    # se o simbolo do alfabeto for um, inclui na lista dos estados destinos gerados quando um 1 eh lido
                    elif item[1] == '1':
                        transPraUm.append(item[2])

        # inclui em uma lista de novas transicoes, as transicoes deste novo estado que eh a concatenacao de estados
        # equivalentes
        novaTrans.append('('+str(estado)+',0)='+str(transPraZero))
        novaTrans.append('(' +str(estado)+',1)='+str(transPraUm))

    print "novas transicoes: "+str(novaTrans)

    #procuraTrans(afd.q[0][0], afd.transicoes)
    #print procuraTrans(afd.q[0][0],afd.transicoes)

# dado um estado e uma lista de transicoes, retorna uma lista de tuplas com todas as transicoes
# do estado recebido
def procuraTrans(origem,transicoes):

    triplaTransicoes = []

    for transicao in transicoes:
        virgula = transicao.find(',')
        igual = transicao.find('=')

        if(transicao[1:virgula] == origem):
            triplaTransicoes.append([origem,transicao[virgula+1:igual-1],transicao[igual+1:]])

    return triplaTransicoes



















