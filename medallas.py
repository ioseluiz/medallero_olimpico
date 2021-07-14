from tabulate import tabulate
import pandas as pd 
'''
medallas = [
    {
        'id_atleta': '001',
        'nombre': 'Alonso Edward',
        'pais': 'Panama',
        'deporte': 'Atletismo',
        'tipo_medalla':'oro'
    },{
        'id_atleta': '002',
        'nombre': 'Simone Biles',
        'pais': 'USA',
        'deporte': 'Gimnasia',
        'tipo_medalla':'plata'
    },
    {
        'id_atleta': '003',
        'nombre': 'Ismael Borrero',
        'pais': 'Cuba',
        'deporte': 'Lucha',
        'tipo_medalla':'bronce'
    }
]
'''
medallas = []
###############################################################################################################
# Funciones de Tabla de Atletas
def agregar_medalla(id_atleta,nombre,pais,deporte,tipo_medalla):
    print('Agregar Atleta Ganador de Medalla')
    print("")

    datos_medalla = {
        'id_atleta': id_atleta,
        'nombre': nombre,
        'pais': pais,
        'deporte': deporte,
        'tipo_medalla':tipo_medalla
    }
    return datos_medalla
    

def listar_medallas(medallas):
    print('TABLA DE MEDALLAS OLIMPICAS')
    print(tabulate(medallas, headers='keys', tablefmt='psql' ))

def leer_file(file):
    try:
        with open(file, 'r') as f:
            lines = f.readlines()
            _medallas = []
            for line in lines:
                datos = {}
                textos = line.split(',')
                id_atleta = textos[0]
                nombre = textos[1]
                pais = textos[2]
                deporte = textos[3]
                tipo_medalla = textos[4][:-1]
                datos = {
                    'id_atleta': id_atleta,
                    'nombre':nombre,
                    'pais': pais,
                    'deporte': deporte,
                    'tipo_medalla': tipo_medalla
                }
                _medallas.append(datos)

        return _medallas
    except IOError:
        array_vacia = []
        error = 'No existe el archivo'
        return array_vacia


def guardar_file(medallas):
    with open('medallas.txt', 'w') as f:
        for medalla in medallas:
            cadena = ''
            for key, value in medalla.items():
                cadena += f'{value},'

            f.write(cadena[:-1]+'\n')
#############################################################################################################
def registro_medallas(medallas):
    if medallas:
        listar_medallas(medallas)
    print('')
    registrar = input('¿Desea registrar una nueva medalla? si/no: ')
    if registrar == 'si':
        print('Registrar medalla ganada por un atleta')
        id_atleta = input('Ingresar id del atleta: ')
        nombre = input('Ingresar el nombre del atleta: ')
        pais = input('Ingresar el pais del atleta: ')
        deporte = input('Ingresar el deporte del atleta: ')
        tipo_medalla = input('Ingresar el tipo de medalla (oro/plata/bronce : ')

        datos_medalla = agregar_medalla(id_atleta, nombre, pais, deporte, tipo_medalla)
        medallas.append(datos_medalla)
        guardar_file(medallas)
        print('Medalla agregada de forma exitosa!')
        print('')
        listar_medallas(medallas)


def consultar_medallas(_medallas):
    print('CONSULTA DE MEDALLAS POR PAIS')
    print('')
    pais = input('Ingresar pais: ')
    medallas_pais = []
    for medalla in _medallas:
        if medalla['pais'] == pais:
            #Contabilizar medallas por atleta y deporte (en ese pais)
            
            datos = {
                'nombre': medalla['nombre'],
                'deporte': medalla['deporte'],
                'tipo_medella':medalla['tipo_medalla']
            }
            medallas_pais.append(datos)
    df = pd.DataFrame(medallas_pais) # Pandas DataFrame
    medallas_atleta = df.groupby(['nombre','deporte']).size()
    #print(medallas_atleta)
    cantidades = medallas_atleta.tolist() # Lista de enteros
    nombres = medallas_atleta.index.tolist() # Lista de Tuplas
    resumen = []
    for i in range(len(cantidades)):
        _datos = {
            'nombre': nombres[i][0],
            'deporte': nombres[i][1],
            'cantidad_medallas': cantidades[i]
        }
        resumen.append(_datos)
    

    print(tabulate(resumen,  headers='keys', tablefmt='psql'))

def consultar_medallas_atleta(_medallas):
    print('CONSULTA DE MEDALLAS POR ATLETA')
    print('')
    nombre = input('Ingresar Nombre de Atleta: ')
    deporte = input('Ingresar Deporte: ')
    medallas_atleta = []
    for medalla in _medallas:
        if (medalla['nombre'] == nombre and medalla['deporte'] == deporte):
            datos = {
                'nombre': medalla['nombre'],
                'deporte': medalla['deporte'],
                'tipo_medalla': medalla['tipo_medalla']
            }
            medallas_atleta.append(datos)

    if medallas_atleta:
        print(tabulate(medallas_atleta, headers='keys', tablefmt='psql'))
    else:
        print('No se encontraron medallas para ese atleta y deporte.')
    


def consultar_mayor_cantidad(_medallas):
    print('CONSULTAR PAIS CON MAYOR CANTIDAD DE MEDALLAS')
    print('')
    df = pd.DataFrame(_medallas) # Pandas DataFrame
    pais_filtro = df['pais'].value_counts()
    #print(pais_filtro)
    cantidades = pais_filtro.tolist()
    #print(cantidades)
    paises = pais_filtro.index.tolist()
    #print(paises)
    cantidad_mayor = max(cantidades)
    mayor = []
    contador = 0
    for cantidad in cantidades:
        if cantidad == cantidad_mayor:
            mayor.append(paises[contador])
        contador +=1
    #print(mayor)
    if len(mayor) == 1:
        print(f'Pais con mayor cantidad de medallas: {mayor[0]} con {cantidades[0]} medallas')
    else:
        cadena = ''
        for dato in mayor:
            cadena += f'{dato}, '
        print(f'Paises con mayor cantidad de medallas: {cadena[:-2]}')

    datos_mayor = []
    for pais in mayor:
        deportes = buscar_deportes(_medallas,pais) # lista
        #print(deportes)
        for deporte in deportes:
            datos = contabilizar_pais_deporte_tipo(_medallas, pais,deporte) # diccionario
            datos_mayor.append(datos)
            
    print('')
    print(tabulate(datos_mayor, headers='keys', tablefmt='psql'))
    print('')

def buscar_deportes(_medallas, pais):
    deportes = []
    for medalla in _medallas:
        if medalla['pais'] == pais:
            if (medalla['deporte'] not in deportes):
                deportes.append(medalla['deporte'])
    return deportes



def contabilizar_pais_deporte_tipo(_medallas, pais, deporte):
    contador_oro = 0
    contador_plata = 0
    contador_bronce = 0
    total = 0
    #print(pais,deporte)
    for medalla in _medallas:
        #print(pais)
        if (medalla['pais'] == pais):
            if (medalla['deporte'] == deporte):
                if medalla['tipo_medalla'] == 'oro':
                    contador_oro += 1
                elif medalla['tipo_medalla'] == 'plata':
                    contador_plata += 1
                elif medalla['tipo_medalla'] == 'bronce':
                    contador_bronce += 1
    total = contador_oro + contador_plata + contador_bronce
    cantidades_tipo = {
        'pais':pais,
        'deporte': deporte,
        'oro': contador_oro,
        'plata': contador_plata,
        'bronce': contador_bronce,
        'total': total
    }

    return cantidades_tipo



def listar_medallas_deporte(_medallas):
    print('CONSULTAR MEDALLAS POR DEPORTE')
    deporte = input('Ingrese el deporte: ')
    
    medallas_deporte = []
    for medalla in _medallas:
        if medalla['deporte'] == deporte:
            datos = {
                'atleta': medalla['nombre'],
                'pais': medalla['pais'],
                'tipo_medella':medalla['tipo_medalla']
            }
            medallas_deporte.append(datos)
    print(tabulate(medallas_deporte,  headers='keys', tablefmt='psql'))




    

def main():
    
    medallas = leer_file('medallas.txt')
    #if medallas:
        #print(medallas)

    menuControl = True
    
    while menuControl:
        print('')
        print("REGISTRO DE MEDALLAS JUEGOS OLIMPICOS")
        print('')
        print('1. Registro de Atletas')
        print('2. Consulta de Medallas por pais')
        print('3. Consulta de Pais con mayor cantidad de Medallas')
        print('4. Consulta de Medallas obtenidas por atleta')
        print('5. Listar medallas por deporte')
        print('6. Salir')
        opcion = input("Ingrese opcion: ")
        if opcion == '1':
            registro_medallas(medallas)
        elif opcion == '2':
            consultar_medallas(medallas)
        elif opcion == '3':
            consultar_mayor_cantidad(medallas)
        elif opcion == '4':
            consultar_medallas_atleta(medallas)
        elif opcion == '5':
            listar_medallas_deporte(medallas)
        elif opcion == '6':
            break
        else:
            print("error opcion no valida")


    #agregar_medalla('001', 'Michael Andrew', 'USA', 'Natacion', 'plata' )
    #agregar_medalla('002', 'Ateyna Baylon', 'Panama', 'Boxeo', 'oro' )
    #print(medallas)
    #guardar_file(medallas)
    #leer_file()
    #print(medallas)

if __name__ == '__main__':
    main()
