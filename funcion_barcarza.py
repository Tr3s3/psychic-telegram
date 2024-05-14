import streamlit as st
import pandas as pd




#streamlit run funcion_barcarza.py

#a:50,b:30,c:40
#a:20,b:50,c:50
#a:40,b:30,c:60

#a:4500,b:4400,c:5800

            
barcazas=st.session_state

#controlar q datos de la barcaza sean adecuados
def verificar_contenido(contenedores):
    for dat in contenedores:
        if not dat[dat.find(":")+1:].isdigit():
            return False
    return True

with st.container():
    st.title(":red[Calculadora de Barcazas]")
    
with st.container():
    form=st.form("Cargar Barcaza")
    
    nombre=form.text_input("Nombre de la barcaza")
    #ver que haya un nombre 
    if not nombre:
        form.warning("Cargue el nombre de la Barcaza")
    
  
    
    #controlar q no haya dos st.session_state con nombre igual   
    if nombre in barcazas:
        form.warning("Esa Barcaza ya se encuentra en el sistema")
   
  
  
    contenedores=form.text_input("Contenedores",placeholder="Ejemplo: A:20,B:40,C:30,...")
    if not contenedores:
        form.warning("Cargue los contenedores")
    
    
    #controlar q datos de la barcaza sean adecuados
    contenedores=contenedores.replace(" ","")
    contenedores=contenedores.split(",")
    for dat in contenedores:
        if not dat[dat.find(":")+1:].isdigit():
            form.warning("Uno o varios parametros son incorrectos")
            
   
    sub=form.form_submit_button("Agregar nueva Barcaza :heavy_plus_sign:",type="primary")
    if sub and verificar_contenido(contenedores) and len(nombre)>0:
        barcazas[nombre]=contenedores


with st.container():
    #lista de diccionarios hecha a partir de diccionarios formados por los datos de la barcazas
    dic_f=[]
    for nom,cap in barcazas.items():
        aux_d={"Barcaza":nom}
        if type(cap)==list and nom!="contenedores totales":
            for item in cap:
                aux_d[item[:item.find(":")]]=item[item.find(":")+1:]
            dic_f.append(aux_d)
    #data frame
    df = pd.DataFrame(dic_f)
    
    #data fame tabla sitio web
    dfe=st.data_editor(df)
    

contenedores_at=st.session_state  
with st.container():
    txt="Total a transportar para cada contenedor"
    txt_e="Ejemplo: A:20,B:40,C:30,..."
    tot_cont=st.text_input(txt,placeholder=txt_e)
    #controles
    if not tot_cont:
        st.warning("Cargue el parametro")
        
    tot_cont=tot_cont.replace(" ","")
    tot_cont=tot_cont.split(",")
    for dat in tot_cont:
        if not dat[dat.find(":")+1:].isdigit():
            st.warning("Uno o varios parametros son incorrectos")
    
    sub=st.button("Confirmar Carga",type="primary")
    if len(tot_cont)>0 and verificar_contenido(tot_cont) and sub:
        dic_tot_cont={}
        for item in tot_cont:
            dic_tot_cont[item[:item.find(":")]]=item[item.find(":")+1:]

        tabla_tot_cant=pd.DataFrame([dic_tot_cont])
        tabla_tot_cant_final=st.data_editor(tabla_tot_cant)
        
        contenedores_at["contenedores totales"]=tot_cont
        
    
#crear sistema de ecuaciones:

#extraer variables para el sistema
variables=[nom for nom in df.columns if nom !="Barcaza"]
colmunas=[]
#asegurarse de que todos los valores none/empty/null sean 0
for nc in df.columns:
    data=df[nc]
    if data.isnull().any():
        df[nc].fillna(0, inplace=True)

#extraer valores de cada variable
for nc in df.columns:
    data=df[nc]
    aux=[]
    for i in data:
        if str(i).isdigit():
            aux.append(i)
    colmunas.append(aux)
if len(colmunas)>0:
    del colmunas[0]

#elementos del sistema
var_cols=[]


if len(variables)==len(colmunas):
    i=0
    for col in colmunas:
        aux=[]
        for num in col:
            aux.append(f"{variables[i]}*{num}")
        var_cols.append(aux)
        i+=1




#auxiliar con las variables de los contenedores totales:
aux_tc=[x[:x.find(":")] for x in tot_cont]
print(aux_tc)
#verificar que se hayan cargado los contedores totales correspondientes 
for v in variables:
    if v not in aux_tc:
        tot_cont.append(f"{v}:0")

#ecuaciones sin igualar a cero:
ecuaciones=[]
for cols in var_cols:
    s=""
    for x in cols:
        if x!=cols[len(cols)-1]:
            s+=f"{x}"
            s+="+"
        else:
            s+=f"{x}"
    ecuaciones.append(s)
   

#ecuaciones igualadas a cero
for cont in tot_cont:
    for eq in ecuaciones:
        if cont[:cont.find(":")] in eq:
            ecuaciones[ecuaciones.index(eq)]+="="+cont[cont.find(":")+1:]
            




def gaussJordan(A,b):
    n=len(A)
    
    for i in range(n):
        A[i].append(b[i])
    print(A)
    for i in range(n):
        if A[i][i]==0:
            return "No se puede dividir por cero"
        for j in range(n):
            if i!=j:
                ratio=A[j][i]/A[i][i]
                for k in range(n+1):
                    A[j][k]=A[j][k]-ratio*A[i][k]
    x=[]
    for i in range(n):
        x.append(A[i][n]/A[i][i])
    return x


def agregar_cargas_dic(m,d):
    pass


def crear_tabla(matriz):
        #obtener elementos del lado = "num"
        tot=[(x[x.find("=")+1:]) for x in matriz]
        for i in range(len(tot)):
            if "=" in tot[i]:
                tot[i]=tot[i].replace("=","")
                tot[i]=float(tot[i])
            else:
                tot[i]=float(tot[i])
        #obtener los numeros 
        matriz=[x[:x.find("=")] for x in matriz]
        for i in range(len(matriz)):
            eq=matriz[i]
            eq=eq.split("+")
            eq=[float(x[x.find("*")+1:]) for x in eq]
            matriz[i]=eq
        sol=gaussJordan(matriz,tot)
        #print("Matriz: ")
        #print(matriz)
        #print()
        #print("Totales: ")
        #print(tot)
        #print()
        #print("Soluciones: ")
        #print(sol)
        l_d=[]
        i=0
        
        for nom in barcazas.keys():
            if nom!="FormSubmitter:Cargar Barcaza-Agregar nueva Barcaza :heavy_plus_sign:" and nom!="contenedores totales":
                dic={"Barcazas":nom,"Viajes":sol[i]}
                for num in matriz:
                    
                l_d.append(dic)
                i+=1
        bt=pd.DataFrame(l_d)
        btf=st.table(bt)

print("Ecuaciones")
print(ecuaciones)
with st.container():
    b=st.button("CALCULAR",type="primary",on_click=crear_tabla(ecuaciones))

    
        

    
        
        
    
        
    
   




#visualizacion de todos los elementos importantes del sistema:
#print()
#print("Columnas: ",colmunas)
#print()
#print("variales: ",variables)
#print()
#print("Total de contenedores: ",tot_cont)
#print()
#print("variables * columnas")
#for i in var_cols:
#    print(i)
#print()
#
#print("Ecuaciones: ")
#for i in ecuaciones:
#    print(i)
#print()

   
        
    


            
    



    





    

    
    
    

    



        
        
    