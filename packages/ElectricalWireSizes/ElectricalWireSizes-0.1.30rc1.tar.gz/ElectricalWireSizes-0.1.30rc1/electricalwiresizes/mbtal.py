'''
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
| PYEWS, ElectricalWireSizes, 10/07/2022                                 |
| Version : 0.1.30rc1                                                    |
| Autor : Marco Polo Jacome Toss                                         |
| License: GNU Affero General Public License v3 (GPL-3.0)                |
| Requires: Python >=3.5                                                 |
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

Changelog:

0.1.30rc1: Se modifica y clasifica las protecciones por sistema descartando
           las no comerciales.

0.1.29:    Versión estable, en esta nueva actualización se agrega al módulo
           graph una línea indicadora de pérdida de tensión.

0.1.29rc1: Se modifican los módulos mbtcu, mbtal, mbtcustd, dbcircuit, dbcircuitcd
           adicionando un nuevo argumento Fcond y condiciones para el cumplimento
           del 125% de ampacidad en alimentadores y circuitos derivados sin considerar
           cualquier factor de ajuste, todas las versiones anteriores no cuentan con
           esta condición y esto puede causar error cuando se tienen las condiciones
           ideales en un conductor, sin agrupar y a temperatura ambiente de 30°C.

0.1.28   : Versión estable.

0.1.28rc2: Separación de operaciones, conductor y protección.

0.1.28rc1: En esta versión se actualiza las protecciones y se actualiza
           la fórmula de corriente incluyendo el factor de sobrecorriente,
           en la versión 0.1.27 no se logra ver la actualización de la
           corriente nominal.

0.1.27rc3: En esta versión los módulos se han clasificado e independizado
           en distintos archivos además se mejora la salida de datos
           del módulo dbcircuit para funciones futuras.

0.1.27:    Versione estable.

'''

import math, time
from tabulate import tabulate
from .bd import dbConductorCu, dbConductorAl
from .basicelecfunc import Rn, RnCd, Z, Rcd, dbc, FCT, zpucu, zpual

def mbtal(VF=None,VL=None,In=None,Nc=None,L=None,FA=None,Type=None,Ta=None,Vd=None,S=None,Fp=None,View=None,Fsc=None,To=None, Break=None, Fcond=None):

    if(VF==None or VL==None or In==None or Nc==None or L==None or FA==None or Type==None or Ta==None or Vd==None or S==None or Fp==None or View==None or Fsc==None or To==None or Break==None or Fcond==None):
        t = time.localtime()
        print("::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
        print("                    ElectricalWireSizes                   ")
        print("                 ",time.asctime(t))
        print("::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
        print("                                                          ")
        print("                         ─▄▀─▄▀")
        print("                         ──▀──▀")
        print("                         █▀▀▀▀▀█▄")
        print("                         █░░░░░█─█")
        print("                         ▀▄▄▄▄▄▀▀")
        print("                                                          ")
        print("----------------------------------------------------------")
        print("| Los parámetros no son correctos para el                |")
        print("| módulo mbtal(VF,VL,In,Nc,L,FA,Type,Ta,Vd,S,Fp,View,Fsc,|")
        print("|               To,Break,Fcond)                          |")
        print("----------------------------------------------------------")
        return  

    if Ta >= 60:
        FT60=0.0
    else :
        FT60=round(math.sqrt((60-Ta)/(60-30)),3)

    if Ta >= 75:
        FT75=0.0
    else :
        FT75=round(math.sqrt((75-Ta)/(75-30)),3)


    if Ta >= 90:
        FT90=0.0
    else :
        FT90=round(math.sqrt((90-Ta)/(90-30)),3)



    SITM=[0,15,20,25,30,35,40,45,50,60,70,80,90,100,110,125,150,175,200,225,250,300,350,400,450,500,600,700,800,1000,1200,1600,2000,2500,3000,4000,5000,6000]


    if Type==1:
    #Conductores en ducto de PVC
        Rj=1
        Xj=2
    elif Type==2:
    #Conductores en ducto de Alumunio
        Rj=3
        Xj=4
    elif Type==3:
    #Conductores en ducto de Acero
        Rj=5
        Xj=6
    #print(tabulate(datos))

    In=(In*Fsc)/Nc

    LIn=L*In
    
    datos=[
    ["6 AWG"],
    ["4 AWG"],
    ["2 AWG"],
    ["1/0 AWG"],
    ["2/0 AWG"],
    ["3/0 AWG"],
    ["4/0 AWG"],
    ["250 KCM"],
    ["300 KCM"],
    ["350 KCM"],
    ["400 KCM"],
    ["500 KCM"],
    ["600 KCM"],
    ["750 KCM"],
    ["1000 KCM"]]

    

    #for i in range(len(dbConductor)):
    #datos[i].append(round(Rn(dbConductor[i][1],75),4))

    #for i in range(len(dbConductor)):
    #    datos[i].append(dbConductor[i][2])

    for i in range(len(dbConductorAl)):
         Zunitaria=Z(round(Rn(dbConductorAl[i][Rj],Ta),4),dbConductorAl[i][Xj],Fp)
         datos[i].append(Zunitaria[0])
         
    for i in range(len(dbConductorAl)):
         Zunitaria=Z(round(Rn(dbConductorAl[i][Rj],Ta),4),dbConductorAl[i][Xj],Fp)
         datos[i].append(Zunitaria[1])
         
    for i in range(len(dbConductorAl)):
         Zunitaria=Z(round(Rn(dbConductorAl[i][Rj],Ta),4),dbConductorAl[i][Xj],Fp)
         datos[i].append(Zunitaria[2])
         
    for i in range(len(dbConductorAl)):
         Zunitaria=Z(round(Rn(dbConductorAl[i][Rj],Ta),4),dbConductorAl[i][Xj],Fp)
         datos[i].append(Zunitaria[3])

    for i in range(len(dbConductorAl)):
         datos[i].append(dbConductorAl[i][7])

    for i in range(len(dbConductorAl)):
         datos[i].append(dbConductorAl[i][8])

    for i in range(len(dbConductorAl)):
         datos[i].append(dbConductorAl[i][9])


    for i in range(len(datos)):

        if S==1:
            
            D1=LIn/(datos[i][1]*VF)
            datos[i].append(round(D1,3))
        
            D2=LIn/(datos[i][2]*VF)
            datos[i].append(round(D2,3))

            D3=LIn/(datos[i][3]*VL)
            datos[i].append(round(D3,3))

            D4=LIn/(datos[i][4]*VL)
            datos[i].append(round(D4,3))
            
            datos[i].append(Nc)
            datos[i].append(round(In,2))
            
            datos[i].append(round(datos[i][5],3)*FA*FT60)
            datos[i].append(round(datos[i][6],3)*FA*FT75)
            datos[i].append(round(datos[i][7],3)*FA*FT90)
            
            if Vd > D1:
                
                if (To==60):

                    if ((round(datos[i][5],3)*FA*FT60>=In) and (((round(datos[i][5],3))/In)>Fcond)):
                        datos[i].append('Yes')
                    else:
                        datos[i].append('Not')

                elif (To==75):

                    if ((round(datos[i][6],3)*FA*FT75>=In) and (((round(datos[i][6],3))/In)>Fcond)):
                        datos[i].append('Yes')
                    else:
                        datos[i].append('Not')


                elif (To==90):
                    
                    if ((round(datos[i][7],3)*FA*FT90>=In) and (((round(datos[i][7],3))/In)>Fcond)):
                        datos[i].append('Yes')
                    else:
                        datos[i].append('Not')
                    
            else:
                datos[i].append('Not')
                
            if VF<200:

                SITM=[0,15,20,30,40,50,60,70,"NA"]

            elif VF>=200:
                
                SITM=[0,15,20,30,40,50,60,70,80,100,125,"NA"]

            
            for j in range(len(SITM)):
                if (SITM[j]=="NA"):
                    datos[i].append('NA')
                    break
                    
                elif (SITM[j]>=Nc*(In/Fsc)*Break):
                    datos[i].append(SITM[j])
                    break
                    
                    
            
        elif S==2:
            
            D1=LIn/(datos[i][1]*VF)
            datos[i].append(round(D1,3))

            D2=LIn/(datos[i][2]*VF)
            datos[i].append(round(D2,3))

            D3=LIn/(datos[i][3]*VL)
            datos[i].append(round(D3,3))

            D4=LIn/(datos[i][4]*VL)
            datos[i].append(round(D4,3))

            datos[i].append(Nc)
            datos[i].append(round(In,2))
            
            datos[i].append(round(datos[i][5],3)*FA*FT60)
            datos[i].append(round(datos[i][6],3)*FA*FT75)
            datos[i].append(round(datos[i][7],3)*FA*FT90)

            if Vd > D2:
                
                if (To==60):

                    if ((round(datos[i][5],3)*FA*FT60>=In) and (((round(datos[i][5],3))/In)>Fcond)):
                        datos[i].append('Yes')
                    else:
                        datos[i].append('Not')

                elif (To==75):

                    if ((round(datos[i][6],3)*FA*FT75>=In) and (((round(datos[i][6],3))/In)>Fcond)):
                        datos[i].append('Yes')
                    else:
                        datos[i].append('Not')


                elif (To==90):
                    
                    if ((round(datos[i][7],3)*FA*FT90>=In) and (((round(datos[i][7],3))/In)>Fcond)):
                        datos[i].append('Yes')
                    else:
                        datos[i].append('Not')
                        
            else:
                datos[i].append('Not')
            
            SITM=[0,15,20,30,40,50,60,70,80,100,125,"NA"]

            for j in range(len(SITM)):
                if (SITM[j]=="NA"):
                    datos[i].append('NA')
                    break
                    
                elif (SITM[j]>=Nc*(In/Fsc)*Break):
                    datos[i].append(SITM[j])
                    break 
                     

                    
        
        elif S==3:
            
            D1=LIn/(datos[i][1]*VF)
            datos[i].append(round(D1,3))

            D2=LIn/(datos[i][2]*VF)
            datos[i].append(round(D2,3))

            D3=LIn/(datos[i][3]*VL)
            datos[i].append(round(D3,3))

            D4=LIn/(datos[i][4]*VL)
            datos[i].append(round(D4,3))

            datos[i].append(Nc)
            datos[i].append(round(In,2))
            
            datos[i].append(round(datos[i][5],3)*FA*FT60)
            datos[i].append(round(datos[i][6],3)*FA*FT75)
            datos[i].append(round(datos[i][7],3)*FA*FT90)
            
            if Vd > D3:
                
                if (To==60):

                    if ((round(datos[i][5],3)*FA*FT60>=In) and (((round(datos[i][5],3))/In)>Fcond)):
                        datos[i].append('Yes')
                    else:
                        datos[i].append('Not')

                elif (To==75):

                    if ((round(datos[i][6],3)*FA*FT75>=In) and (((round(datos[i][6],3))/In)>Fcond)):
                        datos[i].append('Yes')
                    else:
                        datos[i].append('Not')


                elif (To==90):
                    
                    if ((round(datos[i][7],3)*FA*FT90>=In) and (((round(datos[i][7],3))/In)>Fcond)):
                        datos[i].append('Yes')
                    else:
                        datos[i].append('Not')
                        
                    
            else:
                datos[i].append('Not')

            SITM=[0,15,20,30,40,50,60,70,80,100,125,150,175,200,225,250,300,350,400,450,500,600,700,800,1000,1200,1600,2000,2500,3000,4000,5000,6000,"NA"]

            for j in range(len(SITM)):
                if (SITM[j]=="NA"):
                    datos[i].append('NA')
                    break
                    
                elif (SITM[j]>=Nc*(In/Fsc)*Break):
                    datos[i].append(SITM[j])
                    break
                                    
        
        elif S==4:
            
            D1=LIn/(datos[i][1]*VF)
            datos[i].append(round(D1,3))

            D2=LIn/(datos[i][2]*VF)
            datos[i].append(round(D2,3))

            D3=LIn/(datos[i][3]*VL)
            datos[i].append(round(D3,3))

            D4=LIn/(datos[i][4]*VL)
            datos[i].append(round(D4,3))

            datos[i].append(Nc)
            datos[i].append(round(In,2))
            
            datos[i].append(round(datos[i][5],3)*FA*FT60)
            datos[i].append(round(datos[i][6],3)*FA*FT75)
            datos[i].append(round(datos[i][7],3)*FA*FT90)
            
            if Vd > D4:
                
                if (To==60):

                    if ((round(datos[i][5],3)*FA*FT60>=In) and (((round(datos[i][5],3))/In)>Fcond)):
                        datos[i].append('Yes')
                    else:
                        datos[i].append('Not')

                elif (To==75):

                    if ((round(datos[i][6],3)*FA*FT75>=In) and (((round(datos[i][6],3))/In)>Fcond)):
                        datos[i].append('Yes')
                    else:
                        datos[i].append('Not')


                elif (To==90):
                    
                    if ((round(datos[i][7],3)*FA*FT90>=In) and (((round(datos[i][7],3))/In)>Fcond)):
                        datos[i].append('Yes')
                    else:
                        datos[i].append('Not')
                        
            else:
                datos[i].append('Not')
                    
            SITM=[0,15,20,30,40,50,60,70,80,100,125,150,175,200,225,250,300,350,400,450,500,600,700,800,1000,1200,1600,2000,2500,3000,4000,5000,6000,"NA"]                
                    
            for j in range(len(SITM)):
                if (SITM[j]=="NA"):
                    datos[i].append('NA')
                    break
                    
                elif (SITM[j]>=Nc*(In/Fsc)*Break):
                    datos[i].append(SITM[j])
                    break
    if View == 1:
        #Mostrar información en PSQL
        print(tabulate(datos, headers=["AWG/KCM","1F/2H", "2F/3H","3F/3H","3F/4H", "60", "75", "90","%Vd/1F", "%Vd/2F","%Vd/3F","%Vd/3F","Nc", "In", "60", "75", "90", "Op", "ITM"], tablefmt='psql'))
    elif View == 2:
        #Mostrar la información en lista
        return datos
