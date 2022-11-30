from grafo3 import Grafo
from datetime import datetime

#Teste exemplo para adquirir a identificação dos vizinhos
# t1 = datetime.now()
# print('inicio')
# teste = Grafo('grafo_rf_8.txt')
# print('fim')
# t2 = datetime.now()

# t3 = datetime.now()
# print('inicio')
# teste = Grafo('grafo_rf_8.txt', reverso= True)
# print('fim')
# t4 = datetime.now()


# 



t1 = datetime.now()
print('inicio')
teste = Grafo('teste.txt')
t2 = datetime.now()
print('fim')

t3 = datetime.now()
print('inicio')
print(teste.ford_fulkerson(3,4))
print('fim')
t4 = datetime.now()

print('gerar', t2-t1)
print('ford', t4-t3)
