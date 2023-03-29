import random # Gera números aleatórios
import time # Cronometrar o tempo de exec. do algoritmo
from math import sqrt # Realizar calc. matemáticos (distancia Euclidiana)

# Acima, as importações necessárias

def gerarPopulacaoInicial(listaDePontos, tamanhoDaPop): # Função para gerar a população inicial desejada
    populacao = [] # Cria lista vazia da população
    contadorDeIndividuos = 0 # Contador para interromper o while
    while contadorDeIndividuos < tamanhoDaPop:  
        novoIndividuo = listaDePontos.copy() # Cópia para não alterar a lista original 
        random.shuffle(novoIndividuo) # Embaralha os pontos de entrega

        if novoIndividuo not in populacao: # Condicional - O indivíduo existe? Se sim, o tam. da pop. eh incrementado e o loop continua. Se não, este indivíduo é adicionado à população
            populacao += [novoIndividuo]
        else:
            tamanhoDaPop += 1
        contadorDeIndividuos += 1
    return populacao


def calcularDistanciaDeDoisPontosEntrega(primeiroPonto, segundoPonto): # Calcular a distância entre dois pontos de entrega, recebendo x e y
  return int(sqrt((primeiroPonto[0] - segundoPonto[0]) ** 2 + (primeiroPonto[1] - segundoPonto[1]) ** 2)) # Distância Euclidiana entre 2 pontos


def avaliarAptidaoDeIndividuo(restaurante, percurso): # Função que define a aptidão de um indivíduo (fitness) (com base na distância)
    sairDoRestaurante = calcularDistanciaDeDoisPontosEntrega(restaurante, percurso[0]) # Distancia de R ao primeiro ponto de entrega
    voltarProRestaurante = calcularDistanciaDeDoisPontosEntrega(percurso[-1], restaurante) # Distancia para voltar ao restaurante
    distanciaTotal = 0

    for indiceDePonto, pontoDeEntrega in enumerate(percurso): # Calcula distância entre os pontos, distância total
        if pontoDeEntrega != percurso[-1]: 
            distanciaTotal += calcularDistanciaDeDoisPontosEntrega(pontoDeEntrega, percurso[indiceDePonto + 1])

    return sairDoRestaurante + distanciaTotal + voltarProRestaurante # Retorna a distância incluindo o restaurante, sair e chegar em R
    # Em resumo, a apitdão é a soma total da distância: R -> 1o ponto + Ult. ponto -> R + distância entre os pontos | Quanto menor a dist, mais apto


def avaliarPopulacao(populacao, restaurante): # Função que avalia a aptidão de toda a população
    listaDeAptidoes = []

    for individuo in populacao: # Irá percorrer  e iterar em cada indivíduo
        aptidaoDoIndividuo = avaliarAptidaoDeIndividuo(restaurante, individuo)
        listaDeAptidoes.append(aptidaoDoIndividuo)

    return listaDeAptidoes


def torneio(dicionarioDaPopulacao): # Seleciona aleatoriamente 2 pais e retorna o de menor distância (mais apto), recebendo o dic. da pop. atual do A.G que definirei mais pra frente, quando chamar a função que executará o A.G
    populacao = dicionarioDaPopulacao["populacao"] # Pop. atual do A.G extraída do dicionário
    aptidoes = dicionarioDaPopulacao["aptidoes"] # Lista de avaliações de aptidao da população atual do A.G, também extraída do dicionário
    listaDePais = [] # Lista que será sobrescrita com os pais escolhidos
    tamanhoDaPopulacao = len(populacao) # Tamanho da pop. atual

    for _ in range(tamanhoDaPopulacao): # Laço que utiliza lib random para escolher dois pais aleatórios
        paiUm = random.randint(0, tamanhoDaPopulacao - 1)
        paiDois = random.randint(0, tamanhoDaPopulacao - 1)

        if aptidoes[paiDois] < aptidoes[paiUm]: # Condicional que seleciona, com base na escolha aleatória de pais, àquele de maior aptidão
            listaDePais.append(paiDois)
        else:
            listaDePais.append(paiUm)

    return listaDePais

def crossover(listaDePais, dicionarioDaPopulacao, taxaDeCrossover): # Realiza a combinação genética entre os pais selecionados, ordem em q os pontos serão visitados

    def pmx(p1, p2): # Partially Mapped Crossover - Leva em consideração a estrutura de permutação dos indivíduos e preserva a integridade dos genes (pontos de entrega), gerando novos indivíduos com um equilíbrio entre a herança dos pais.
        corte = random.randint(1, len(p1) - 2) # Escolhe um corte aleatório no percurso (entre 1 e o comprimento do pai menos 2 para evitar cortes no início/fim da lista)

        novaPermutacao = p1.copy()
        novaPermutacao = novaPermutacao[:corte] # Faz uma cópia do 1o pai até o corte

        for item in p2: # Para cada gene (ponto de entrega) do segundo pai (p2) que não está na cópia do 1o pai, adicionará o respectivo gene do 2o pai
            if item not in novaPermutacao:
                novaPermutacao.append(item)
        return novaPermutacao

    numeroDePais = len(listaDePais) # Define o numero de pais, correspondente ao comp. da lista de pais
    listaDeFilhos = [] # Lista que será sobrescrita com os filhos
    numeroDelistaDeFilhos = 0

    while numeroDelistaDeFilhos < numeroDePais: # Repete enquanto o num de filhos gerados for menor que o num de pais
        pai1 = dicionarioDaPopulacao["populacao"][listaDePais[random.randint(0, numeroDePais - 1)]] # Seleciona aleatoriamente um pai na lista de pais
        pai2 = dicionarioDaPopulacao["populacao"][listaDePais[random.randint(0, numeroDePais - 1)]] # Seleciona aleatoriamente um outro pai na lista de pais

        if random.random() <= taxaDeCrossover: # Se uma var. gerada aleatoriamente for menor que a taxa de cross
            filho = pmx(pai1, pai2)
            filho2 = pmx(pai2, pai1)
            # Chama a função pmx com os dois pais selecionados, gerando filho1 e filho2
            if filho not in listaDeFilhos:
                listaDeFilhos.append(filho)
                numeroDelistaDeFilhos += 1
            if filho2 not in listaDeFilhos:
                listaDeFilhos.append(filho2)
                numeroDelistaDeFilhos += 1


    if numeroDelistaDeFilhos > numeroDePais:
        listaDeFilhos.pop()
    # Se o num de filhos ultrapassar o num de pais, remove o ult filho com o método pop, a fim de não exceder o num de pais (precisamos manter o tam da pop constante, caso contrário a cada geração a população cresceria mais e mais até não caber em memória)

    return listaDeFilhos

def mutacao(listaDelistaDeFilhos, taxaDeMutacao):
    for filho in listaDelistaDeFilhos: # Percorre cada indivíduo
        for indiceDoFilho in range(len(filho)):
            if random.random() <= taxaDeMutacao: # Mutação ocorre se um num aleatório for menor que a taxa definida
                if filho[indiceDoFilho] != filho[-1]: # Se não for o último índice, troca o índice pelo próximo
                    filho[indiceDoFilho], filho[indiceDoFilho + 1] = filho[indiceDoFilho + 1], filho[indiceDoFilho]
                else: # Se for, troca o último índice pelo primeiro
                    filho[indiceDoFilho], filho[0] = filho[0], filho[indiceDoFilho]


def selecionarSobreviventes(dicionarioDaPopulacao, listaDeFilhos, aptidoes_listaDeFilhos, elitismo : bool): # Função de seleção de sobreviventes

    novaPopulacao = [] # Lista que será sobrescrita com os individuos sobreviventes
    novalistaDeAptidoes = [] # Lista que será sobrescrita com a aptidão dos sobreviventes

    if elitismo == True: # Se for utilizado elitismo...
        indiceDoMelhorPai = dicionarioDaPopulacao["aptidoes"].index(min(dicionarioDaPopulacao["aptidoes"])) # Obtém o índice do melhor pai (menor distância, utilizando a função min)
        melhorPai = dicionarioDaPopulacao["populacao"][indiceDoMelhorPai] # Melhor pai, na posíção correspondente ao índice do melhor pai na populacao 
        aptidaoDoMelhorPai = dicionarioDaPopulacao["aptidoes"][indiceDoMelhorPai] # Aptidao do melhor, utilizando-se novamente do indice dele

        indiceDoPiorFilho = aptidoes_listaDeFilhos.index(max(aptidoes_listaDeFilhos)) # Mesmo esquema, só que utilizando a função max do py, já que quanto maior a distância, pior a aptidão
        listaDeFilhos.pop(indiceDoPiorFilho) # Remove o pior filho da lista de filhos, com base no indice que pegamos anteriormente
        aptidoes_listaDeFilhos.pop(indiceDoPiorFilho) # Remove a aptidao o pior filho da lista de aptdões utilizando o mesmo método

        novaPopulacao = listaDeFilhos + [melhorPai] # Adiciona os filhos restantes e o melhor pai à nova população
        novalistaDeAptidoes = aptidoes_listaDeFilhos + [aptidaoDoMelhorPai] # Adiciona as aptidões dos filhos restantes e a do melhor pai à nova lista de aptidões
        return novaPopulacao, novalistaDeAptidoes
    else: # Se não for utilizado elitismo...
        novaPopulacao = listaDeFilhos # A nova população é apenas os filhos
        return novaPopulacao, aptidoes_listaDeFilhos


def algoritmoGenetico(tamanhoDaPopulacao, taxaDeCrossover, taxaDeMutacao, numeroDeGeracoes, elitismo, restaurante, listaDePontos): # Função principal, responsável por gerar novas gerações

    populacao = gerarPopulacaoInicial(listaDePontos, tamanhoDaPopulacao) # Chama a função que gera a população inicial e armazena em populacao
    aptidoes = avaliarPopulacao(populacao, restaurante) # Chama a função que avalia a população e armazena em aptidoes
    dicionarioDaPopulacao = { "populacao": populacao, "aptidoes": aptidoes } # Armazena populacao e aptidoes em um dicionario, que foi usado em quase todas as funções do código

    melhorIndividuo = (0, []) # Inicializa o melhorIndividuo como uma tupla, com 0 pois nenhum indivíduo foi avaliado por enquanto, logo não temos aptidão, assim como a lista vazia

    for _ in range(numeroDeGeracoes): # Loop que irá rodar até que o número de gerações fornecido na entrada seja alcançado
        paisSelecionados = torneio(dicionarioDaPopulacao) # Chama a função de torneio para selecionar os pais, enviando a tupla de dicionário como parâmetro
        listaDeFilhos = crossover(paisSelecionados, dicionarioDaPopulacao, taxaDeCrossover) # Chama a função de crossover passando os pais q foram selecionados no torneio, o dicionario como param para usarmos na função crossover e a taxa de cross, que também será usada 
        mutacao(listaDeFilhos, taxaDeMutacao) # # Chama a função de mutação
        listaDeAptidoesDosFilhos = avaliarPopulacao(listaDeFilhos, restaurante) # Armazena o retorno da função de avaliar pop. em listaDeAptidoesDosFilhos
        dicionarioDaPopulacao["populacao"], dicionarioDaPopulacao["aptidoes"] = selecionarSobreviventes(dicionarioDaPopulacao, listaDeFilhos, listaDeAptidoesDosFilhos, elitismo) # Atualiza a população e as avaliações de aptidão armazenadas no dicionário dicionarioDaPopulacao com os indivíduos sobreviventes da nova geração, chamando a função de selecionar os sobreviventes
        indiceDoMelhorIndividuo = dicionarioDaPopulacao["aptidoes"].index(min(dicionarioDaPopulacao["aptidoes"])) # Escolhe o indice do melhor individuo para a geração atual da iteração
        melhorIndividuo = dicionarioDaPopulacao["populacao"][indiceDoMelhorIndividuo] # Sobrescreve os dados da tupla que contém o melgorIndividuo

        print(f'Melhor individuo da geração {_}º foi {avaliarAptidaoDeIndividuo(restaurante, melhorIndividuo)}') # Printa o resultado

    indiceDoMelhorIndividuo = dicionarioDaPopulacao["aptidoes"].index(min(dicionarioDaPopulacao["aptidoes"]))
    melhorIndividuo = dicionarioDaPopulacao["populacao"][indiceDoMelhorIndividuo]

    print(f'Melhor individuo da geração {_+ 1}º foi {avaliarAptidaoDeIndividuo(restaurante, melhorIndividuo)}')
    return avaliarAptidaoDeIndividuo(restaurante, melhorIndividuo), melhorIndividuo

if __name__ == "__main__": # Printar quando o algoritmo iniciar
    print('inicio da execução do algoritmo')
    print('-='*15)
    tempoInicial = time.time()

    matrizDeEntrada = open('Entrada.txt').readlines()  # ler o arquivo de entrada

    pontosDeEntrega = []
    restaurante = ()
    distanciaMinima = 0
    melhorPercurso = []
    # Inicialização das variáveis

    for indiceLinha, item in enumerate(matrizDeEntrada):  # percorrer a matriz de entrada e adicionar os pontos de entrega na lista de pontos de entrega
        linha = matrizDeEntrada[indiceLinha].split()
        for indiceColuna in range(len(linha)):
            if linha[indiceColuna] == 'R': # Achou o R => armazena na variável restaurante
                restaurante = (indiceLinha, indiceColuna, linha[indiceColuna])
            elif linha[indiceColuna] != '0': # Se nào for 0, quer dizer que é um ponto de entrega
                pontosDeEntrega.append((indiceLinha, indiceColuna, linha[indiceColuna]))  # adicionar os pontos de entrega na lista de pontos de entrega


    melhorDistanciaEncontrada, melhorIndividuo = algoritmoGenetico(100, 0.8, 0.1, 200, True, restaurante, pontosDeEntrega) # Atribui ao retorno da função principal que executa o A.G a melhor distancia e o melhor individuo, para que posteriormente possamos printar

    print('-='*15)
    print(f'A melhor distancia encontrada foi {melhorDistanciaEncontrada} com o caminho abaixo: \n{melhorIndividuo}')
    tempoFinal = time.time()
    print(f"Solução encontrada em {tempoFinal - tempoInicial} segundos")


