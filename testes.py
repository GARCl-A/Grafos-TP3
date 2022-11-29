from grafo2 import Grafo

#Teste exemplo para adquirir a identificação dos vizinhos
print('inicio')
teste = Grafo('teste.txt')
print('inicio/2')
print(teste.bfs(1,4))
print('inicio/3')
print(teste.get_caminho(teste.bfs(1,4),1,4))