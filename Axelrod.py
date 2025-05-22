import numpy as np
import matplotlib.pyplot as plt
import random
from func_aux import square_lattice, obtener_vecinos, MatrizInicial, FinInteraccion, similarity, misma_cultura, tamaño_mayor_cluster, transformarmatriz
from graficas import graf_Smax_vs_q, links_activos_vs_tiempo, animar_matriz_vectores
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

qespecial=10 #q para el que se quiere guardar la matriz de agentes
matriz_paso=np.zeros((L,L,f),dtype=int) #matriz de agentes para q=10
matrizanimacion_list=[] #Lista en la que guardaremos las matrices de agentes para q=10

#Creamos la matriz de adyacencia y la lista de vecinos
adj_matrix = square_lattice(L)
vecinos_list=obtener_vecinos(adj_matrix, N, p)

resultados = []      #cada elemento de la lista (dim q) es una sublista (dimension M, numero de simulaciones) con el valor del par. orden para cada q
M=1
#Número de simulaciones del modelo de Axelrod para cada q, para promediar el tamaño del mayor cluster

#links activos
linksactivos=0
link_list=[]
#Abrimos fichero para guardar numero de links activos frente a tiempo
#with open("resultados_tiempo_links.csv", "w") as file:

for q in q_values:
    par_orden_q=[] #Lista en la que guardaremos el tamaño del mayor cluster para cada q en cada simulación m
    for m in range(M):
        #agentes=matriz de vectores f. Inicalizamos la matriz de agentes
        agentes=np.zeros((N+p,f),dtype=int) #agentes=matriz de vectores F
        MatrizInicial(agentes,N,f,q,p)

        #Bucle en el que realizamos el modelo de Axelrod
        haterminado=False
        tiempo=0
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

            

            if q == qespecial and m == M-1:
                matriz_paso = np.zeros((L, L, f), dtype=int)
                transformarmatriz(agentes, L, f, matriz_paso)
                matrizanimacion_list.append(matriz_paso)    

            #comprobamos si ya no se pueden realizar más interacciones
            haterminado, linksactivos=FinInteraccion(agentes,vecinos_list,N,f,p,sim_min)
            tiempo+=1
            link_list.append(linksactivos)

            '''
            if q==qespecial and m==M-1:
                transformarmatriz(agentes, L, f, matriznueva)
                matrizanimacion_list.append(matriznueva)    
                '''
            
            
            

        #Calculamos el tamaño del mayor cluster
        mayor_cluster = tamaño_mayor_cluster(agentes, vecinos_list, N)
        par_orden_q.append(mayor_cluster)
    
    resultados.append(par_orden_q) 

#Calculamos el tamaño medio y la desviación típica
par_orden_medio=[np.mean(res) for res in resultados]
par_orden_std=[np.std(res) for res in resultados]

#Graficamos
graf_Smax_vs_q(q_values, par_orden_medio, par_orden_std, f, M, L, p, h)
#graf_Smax_std_vs_q(q_values, par_orden_std, f, M, L,p,h)
links_activos_vs_tiempo(link_list)
animar_matriz_vectores(matrizanimacion_list,qespecial)


   #Falta:
   # numero de links activos 
   # animacion  
   # desviación estandar de Smax frente a q
   # finalizar cuando links activos = cte
   
   #######  variable continua 

