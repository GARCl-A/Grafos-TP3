from grafo2 import Grafo

#Teste exemplo para adquirir a identificação dos vizinhos
print('inicio')
teste = Grafo('teste.txt')
caminho = teste.get_caminho(1,4)
for i in caminho:
    print(i.identificacao, i.capacidade, i.fluxo)

# bfs = teste.bfs(1,4)
# for i in bfs:
#     if type(i) == int:
#         print( i)
#     else:
#         print( i.identificacao)
