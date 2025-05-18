import numpy as np
import matplotlib.pyplot as plt
import random
from func_aux import square_lattice, obtener_vecinos, MatrizInicial, FinInteraccion, similarity, misma_cultura, tamaño_mayor_cluster
from graficas import graf_Smax_vs_q
#L=  Lado de la red cuadrada
L=10
#N=Número de agentes
N=L*L

#Parámetros del modelo de Axelrod
f=3  #f=numero de rasgo de cada individuo
q_values=range(3,26) # Lista de q utilizados. q=numero de valores posibles para cada rasgo
p=0  #p=número de medios de comunicacion (prensa)
h=1.0     #probabilidad de interaccion con la prensa
sim_min=1/f #similitud mínima normalizada para que dos agentes se consideren similares

#Creamos la matriz de adyacencia y la lista de vecinos
adj_matrix = square_lattice(L)
vecinos_list=obtener_vecinos(adj_matrix, N, p)

resultados = []      #cada elemento de la lista (dim q) es una sublista (dimension M, numero de simulaciones) con el valor del par. orden para cada q
M=10
#Número de simulaciones del modelo de Axelrod para cada q, para promediar el tamaño del mayor cluster


for q in q_values:
    par_orden_q=[] #Lista en la que guardaremos el tamaño del mayor cluster para cada q en cada simulación m
    for m in range(M):
        #agentes=matriz de vectores f. Inicalizamos la matriz de agentes
        agentes=np.zeros((N+p,f),dtype=int) #agentes=matriz de vectores F
        MatrizInicial(agentes,N,f,q,p)

        #Bucle en el que realizamos el modelo de Axelrod
        haterminado=False
        while not haterminado:
            matrizaux=np.copy(agentes)
            for i in range(N):
                #Seleccionamos un agente vecino aleatorio
                j=random.choice(vecinos_list[i])
                #calculamos la similitud entre el agente i y el vecino j
                sim=similarity(i,j, matrizaux,f)
                if j < N:  # Interacción con otro agente
                    prob_interaccion = sim
                else:     # Interacción con medio
                    prob_interaccion = h * sim

                #si la similitud es mayor que la similitud mínima y menor que 1, se produce la interacción
                if sim>=sim_min and sim<1: 
                    if np.random.rand() < prob_interaccion:
                        diferentes = [k for k in range(f) if matrizaux[i][k] != matrizaux[j][k]] #Vemos que rasgos son diferentes
                        k = random.choice(diferentes) #Elegimos uno al azar y lo copiamos
                        agentes[i][k] = matrizaux[j][k]
            #comprobamos si ya no se pueden realizar más interacciones
            haterminado=FinInteraccion(agentes,vecinos_list,N,f,p,sim_min)

        #Calculamos el tamaño del mayor cluster
        mayor_cluster = tamaño_mayor_cluster(agentes, vecinos_list, N)
        par_orden_q.append(mayor_cluster)
    
    resultados.append(par_orden_q) 

#Calculamos el tamaño medio y la desviación típica
par_orden_medio=[np.mean(res) for res in resultados]
par_orden_std=[np.std(res) for res in resultados]

#Graficamos
graf_Smax_vs_q(q_values, par_orden_medio, par_orden_std, f, M, L, p, h)


    

