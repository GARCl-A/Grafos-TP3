from collections import defaultdict
from typing import *
import numpy as np

class Vertice:  
    def __init__(self, identificacao:int, capacidade:int, fluxo:int) -> None:
        self.identificacao = identificacao
        self.capacidade = capacidade
        self.fluxo = fluxo

class Grafo:
    def __init__(self, txt:str) -> None:
        self.grafo = defaultdict(list)
        arquivo = open(txt, 'r')
        self.tamanho = int(arquivo.readline())
        for linha in arquivo:   #Adicionando vizinhos às listas
            split = linha.split() #Split 0:vertice1, 1:vertice2, 2:peso, necessário casing para inteiro, já que no txt são strings
            self.grafo[int(split[0])].append(Vertice(int(split[1]), int(split[2]),0))
        arquivo.close

    def get_vizinhos_identificacao(self, vertice:int) -> List[int]:
        vizinhos = []
        for vizinho in self.grafo[vertice]:
            vizinhos.append(vizinho.identificacao)
        return vizinhos

    def get_vizinhos_objeto(self, vertice:int) -> List[Vertice]:
        vizinhos = []
        for vizinho in self.grafo[vertice]:
            vizinhos.append(vizinho)
        return vizinhos

    def bfs(self, inicio: int, fim:int) -> List[int]:
        lista_marcacao = [0] * self.tamanho
        lista_pais = [-1] * self.tamanho
        lista_marcacao[inicio - 1] = 1
        lista_pais[inicio - 1] = 0
        fila = [inicio]
        while fila != []:
            atual = fila.pop()
            vizinhos = self.get_vizinhos_identificacao(atual)
            for vizinho in vizinhos:
                if lista_marcacao[vizinho - 1] == 0:
                    lista_marcacao[vizinho - 1] = 1
                    lista_pais[vizinho - 1] = atual
                    if vizinho == fim:
                        return lista_pais
                    fila.append(vizinho)
        raise Exception(f"Não há caminho entre {inicio} e {fim}")

    def get_caminho(self, pais: List[int], inicio: int, fim: int) -> List[int]:
        caminho = [fim]
        atual = fim
        while atual != inicio:
            atual = pais[atual - 1]
            caminho.append(atual)
        caminho.reverse()
        return caminho