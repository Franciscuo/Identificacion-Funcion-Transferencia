import numpy as np 
import matplotlib.pyplot as plt
import scipy.signal as sig
import argparse
import sys



parser = argparse.ArgumentParser(description="Valores caracteristicos funcion de transferencia")
parser.add_argument('aproximacion', metavar='a', type=int,
                    help='cantidad aproximaciones')
parser.add_argument('original', metavar='o', type=int,
                    help='graficar datos originales')
parser.add_argument('archivo', metavar='f', type=str,
                    help='nombre archvo plano')
args = parser.parse_args()



tiempo=[]
valor=[]
tiempo_original=[]
valor_original=[]

def argumentos_script():
        iteraciones=args.aproximacion
        mostrar_original=args.original
        archivo=args.archivo
        return iteraciones,mostrar_original,archivo
def ingreso_imagen(nombre_archivo):
    data = np.genfromtxt(nombre_archivo,delimiter=',')
    time=data[:,][:,0]
    val=data[:,][:,1]
    tiempo_o=data[:,][:,0]
    valor_o=data[:,][:,1]
    return time,val,tiempo_o,valor_o
def quitar_ruido(tiempo,valores):
    time2=tiempo[5:len(tiempo)-5]
    valor2=[]
    suma=0
    for x in range(5,len(tiempo)-5):
        for val in range(-5,6):
            suma=suma+valores[x+val]
        suma=suma/11
        valor2.append(suma)
        suma=0
    return time2,valor2
def graficar(mostrar,tiempo2,valores2,derivaprueba,cortes2,funcion):
    plt.figure(1)
    if mostrar==1:
        plt.plot(tiempo2,valores2, color="blue", linewidth="0.5", label="Original")
    plt.plot(tiempo,valor, color="red", linewidth="1.5", label="Aproximada") 
    #plt.plot(tiempo,derivaprueba, color="black", linewidth="1.5", label="derivada")  
    for x in range(0,len(cortes2)):
        plt.vlines(x=cortes2[x], ymin=0.9*min(valor), ymax=1.1*(max(valor)), color="purple", linestyles="--")
    plt.plot(*funcion.step(2.5), label="Funcion de transferencia calculada", color="black")
    plt.legend(loc=4,prop={'size':10})
    plt.xlabel('Tiempo [s]')
    plt.ylabel('Temperatura [grados C]')
    plt.grid()
    plt.title('Funcion de transferencia')
    plt.show()
def resultados(num,mostrar):
    print("Se realizaron %s iteraciones" %num)
    if mostrar==1:
        print("Grafica con datos originales")
    else:
        print("Grafica sin datos originales")
def puntos_criticos(x,y):
    dyb = []
    aux = []
    #derivada por diferencia hacia atras(senales sirvio pa algo :v)
    dyb.append( (y[0] - y[1])/(x[0] - x[1]))
    for i in range(1,len(y)):
        if x[i]!=x[i-1]:
            dyb.append((y[i] - y[i-1])/(x[i]-x[i-1])) 
        else:
            dyb.append(dyb[-1])
    for j in range(0,1):  
        if max(dyb)>abs(min(dyb)):
            aux2=(dyb.index(max(dyb)))/33
        else:
            aux2=(dyb.index(min(dyb)))/33
        aux.append(aux2)
        dyb[dyb.index(max(dyb))]=0
        aux.append((len(x)/33))
    return dyb,aux
def valores_funcion(cortes2,tiempo,valor):
    vec=[]
    if valor[cortes2[0]*33]>valor[cortes2[1]*33]:
        #bajada
        k=valor[cortes2[0]*33]-valor[cortes2[1]*33]
        aux=k*0.63
        aux=valor[cortes2[0]*33]-aux
        k=-k
        for x in range(0,len(tiempo)):
            if aux>valor[x]:
                tao=tiempo[x]
                break
        tao=tao-cortes2[0]
    else:
        #subida
        k=valor[cortes2[1]*33]-valor[cortes2[0]*33]
        aux=k*0.63
        aux=valor[cortes2[0]*33]+aux
        for x in range(0,len(tiempo)):
            if aux<valor[x]:
                tao=tiempo[x]
                break
        tao=tao-cortes2[0]
        

    return k,tao

def funcion_transferencia(k,tao):
    funcion=sig.lti(k, (tao,1))
    return funcion

#INICIO PROGRAMA

print("-------------------------------")
print("obteniendo parametros script...")
iteraciones,mostrar_original,archivo=argumentos_script() # se obtienen parametros script

print("obtienenido datos de archivo plano...")
tiempo,valor,tiempo_original,valor_original=ingreso_imagen(archivo) # se obtienen valores de matlab

print("realizando aproximaciones...")
for x in range(0,iteraciones):                              # se realizan aproximaciones
    tiempo,valor=quitar_ruido(tiempo,valor)

print("analizando funcion...")
derivada,cortes=puntos_criticos(tiempo,valor)              # se obtiene derivada discreta funcion aproximada

print("encontrando valores de k y tao...")
k,tao=valores_funcion(cortes,tiempo,valor)                     # Se obtienen valores de k y tao
print("K = %s Tao = %s" %(k,tao))
print("obteniendo funcion de transferencia...")               # Se obtiene funcion de transferencia
funcion=funcion_transferencia(k,tao)

print("graficando...")
graficar(mostrar_original,tiempo_original,valor_original,derivada,cortes,funcion) # se grafica

print("finalizando...")
print("-------------------------------")
resultados(iteraciones,mostrar_original)                    # se muestra informacion a usuario