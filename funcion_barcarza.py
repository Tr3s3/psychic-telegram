import streamlit as st
import pandas as pd
import sympy as sp



#streamlit run funcion_barcarza.py

            
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
variables=[sp.symbols(nom) for nom in barcazas.keys() if nom !='contenedores totales' and nom!='FormSubmitter:Cargar Barcaza-Agregar nueva Barcaza :heavy_plus_sign:']
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

del colmunas[0]

#elementos del sistema
var_cols=[]

print(colmunas)
print()
print(variables)

#if len(variables)==len(colmunas):
#    print(True)
#else:
#    print(False)
    
""""
i=0
for col in colmunas:
    aux=[]
    for num in col:
        aux.append(f"{variables[i]}*{num}")
    var_cols.append(aux)
    i+=1

for i in var_cols:
    print(i)
"""  
    
        
    


            
    



    

ecuaciones=[]



    

        
        
    


    
        
        
    
    
    #tabla_barcazas=pd.DataFrame(columns=)
    
    

    



        
        
    