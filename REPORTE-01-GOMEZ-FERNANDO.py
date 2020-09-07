#!/usr/bin/env python
# coding: utf-8

# Por: Fernando Gómez Perera

import lifestore_file as lifestore

# Variables que contienen los distintos conjuntos de datos
products = lifestore.lifestore_products
sales = lifestore.lifestore_sales
searches = lifestore.lifestore_searches


# Listas con los usuarios y contrasenas registradas en el sistema
users = ['fernando', 'vanessa', 'javier']
passwords = ['fernando123', 'vanessa123', 'javier123']

# Variables auxiliares para la ejecucion del login de usuario
attempts = 3
can_run = False
user_input = None

# Implementacion del login de usuario
while attempts > 0:
    # El usuario ingresa su nombre de usuario si previamente no lo ha hecho
    if user_input == None:
        user_input = input('Ingrese un nombre de usuario: ')
        user_exists = False
    # Se comprueba si el nombre de usuario existe en el sistema
    for i in range(len(users)):
        if user_input == users[i]:
            user_ind = i
            user_exists = True
    # Si el nombre de usuario no existe en el sistema, el sistema se cierra
    if not(user_exists):
        print('El usuario ingresado no existe.')
        break
    # El usuario ingresa su contrasena
    else:
        password_input = input('Ingrese su contrasena: ')
        # Si su contrasena es invalida, entonces pierde un intento
        if password_input != passwords[user_ind]:
            print('La contraseña ingresada es invalida.')
            attempts -= 1
        # Si su contrasena es valida, entonces el sistema le da acceso
        else:
            can_run = True
            break

# Comprobar si el usuario tiene acceso al sistema
if can_run:
    print('\n¡Bienvenido!')
else:
    exit()

# Lista para guardar el acumulado de ventas por producto
sales_by_prod = list()

# Contador de ventas totales de todos los productos
total_sales = 0

# Obtener las ventas totales por producto
for product in products:
    sales_product = 0
    sales_product_refund = 0
    sum_score = 0
    mean_score = -1
    refunds = 0
    for sale in sales:
        # Comprobar si la venta le pertenece al producto actual
        if product[0] == sale[1]:
            # Se aumenta el total de ventas de ese producto
            sales_product += 1
            # Se aumenta la puntuacion del producto
            sum_score += sale[2]
            # Si el producto fue reembolsado, se aumenta el total de reembolsos de ese producto
            if sale[-1]:
                sales_product_refund += 1
    # Las ventas totales de todos los productos se aumentan
    total_sales += sales_product
    # Se calcula el promedio de puntuacion del producto
    if sales_product:
        mean_score = sum_score // sales_product
    # Se indica si el producto tuvo reembolsos
    if sales_product_refund:
        refunds = 1
    sales_by_prod.append(product + [mean_score, refunds, sales_product])

# Lista para guardar el acumulado de busquedas por producto
searches_by_prod = list()

# Acumulador del total de busquedas de todos los productos
total_searches = 0

# Obtener las busquedas totales por producto
for product in products:
    searches_product = 0
    for search in searches:
        if product[0] == search[1]:
            searches_product += 1
    total_searches += searches_product
    searches_by_prod.append(product + [searches_product])

# Filtrar y obtener las categorias de los productos
categories = list()

for product in products:
    unique_category = True
    for category in categories:
        if product[3] == category:
            unique_category = False
            break
    if unique_category:
        categories.append(product[3])

# Menu para ejecutar alguna de las funciones disponibles en el sistema
while True:
    print('*** Elija una de las siguientes opciones: ***')
    print('1. Explorar los datos')
    print('2. Ver los productos mas vendidos y productos rezagados')
    print('3. Ver los productos por reseña en el servicio')
    print('4. Total de ingresos y ventas promedio mensuales, total anual y meses con mas ventas al anio')
    print('Ingrese cualquier otra tecla u oprima Ctrl+C para salir.')
    functions = ['1', '2', '3', '4']
    function_input = input('\nIngrese el numero de la funcion y oprima Enter: ')
    function_selected = 0
    # Comprobar la entrada del usuario
    if len(function_input) == 1 and function_input != '':
        for function in functions:
            if function_input == function:
                function_selected = int(function_input)
    # Ejecutar alguna de las funciones disponibles en el sistema si la entrada del usuario es valida
    if function_selected:
        if function_selected == 1:
            # Visualizar los primeros 5 registros de la lista de productos
            print('\nTotal de productos: ', len(products))
            print('* Primeros 5 registros:')
            print('----------------------------------------------------------------')
            print(' ID |           Nombre          | Precio |   Categoria  | Stock ')
            print('----|---------------------------|--------|--------------|-------')
            for product in products[0:5]:
                print(' '+str(product[0])+'  | '+product[1][0:20]+'. . .'+' |  '+str(product[2])+'  | '+product[3]+' |  '+str(product[4]))

            # Visualizar los primeros 5 registros de la lista de ventas
            print('\nTotal de ventas: ', len(sales))
            print('* Primeros 5 registros:')
            print('-------------------------------------------------------')
            print(' ID | ID prod | Puntuacion |   Fecha    |   Reembolso  ')
            print('    |         |  (1 al 5)  |            | (1 sí, 0 no) ')
            print('----|---------|------------|------------|--------------')
            for sale in sales[0:5]:
                print('  '+str(sale[0])+' |    '+str(sale[1])+'    |      '+str(sale[2])+'     | '+sale[3]+' |      '+str(sale[4]))

            # Visualizar los primeros 5 registros de la lista de busquedas
            print('\nTotal de busquedas: ', len(searches))
            print('* Primeros 5 registros:')
            print('------------------')
            print(' ID | ID producto ')
            print('----|-------------')
            for search in searches[0:5]:
                print('  '+str(search[0])+' |      '+str(search[1]))
            print('\n')
        if function_selected == 2:
            # Ordenar los productos por sus ventas totales de forma descendente
            for i in range(len(sales_by_prod)):
                current_ind = i
                last_ind = i - 1
                while sales_by_prod[last_ind][-1] < sales_by_prod[current_ind][-1] and last_ind > -1:
                    sales_by_prod[current_ind], sales_by_prod[last_ind] = sales_by_prod[last_ind], sales_by_prod[current_ind]
                    current_ind -= 1
                    last_ind -= 1

            # Lista para almacenar los productos mas vendidos
            best_selling_products = list()

            # Obtener los productos que representen el 60% de todas las ventas
            sum_sales = sales_by_prod[0][-1]
            i = 0
            while sum_sales <= total_sales*0.6:
                best_selling_products.append(sales_by_prod[i])
                i += 1
                sum_sales += sales_by_prod[i][-1]

            # Mostrar el listado con los productos obtenidos
            print('\n* Productos mas vendidos')
            print('--------------------------------------')
            print('           Nombre            | Ventas ')
            print('-----------------------------|--------')
            for product in best_selling_products:
                print('  '+product[1][0:20] + '. . .  | ', product[-1])

            # Ordenar los productos por sus busquedas totales de forma descendente
            for i in range(len(searches_by_prod)):
                current_ind = i
                last_ind = i - 1
                while searches_by_prod[last_ind][-1] < searches_by_prod[current_ind][-1] and last_ind > -1:
                    searches_by_prod[current_ind], searches_by_prod[last_ind] = searches_by_prod[last_ind], searches_by_prod[current_ind]
                    current_ind -= 1
                    last_ind -= 1

            # Lista para almacenar los productos mas buscados
            most_searched_products = list()

            # Obtener los productos que representen el 60% de todas las busquedas
            sum_searches = searches_by_prod[0][-1]
            i = 0
            while sum_searches <= total_searches*0.6:
                most_searched_products.append(searches_by_prod[i])
                i += 1
                sum_searches += searches_by_prod[i][-1]

            # Mostrar el listado con los productos obtenidos
            print('\n* Productos mas buscados')
            print('-----------------------------------------')
            print('           Nombre            | Busquedas ')
            print('-----------------------------|-----------')
            for product in most_searched_products:
                print('  '+product[1][0:20] + '. . .  |   ', product[-1])

            # Lista para almacenar los productos menos vendidos por categoria
            worst_selling_products = list()

            # Obtener los 6 productos menos vendidos por categoria
            for category in categories:
                i = 0
                category_products = list()
                for product in sales_by_prod[::-1]:
                    if product[3] == category:
                        i += 1
                        if i > 6:
                            break
                        category_products.append(product)
                worst_selling_products.append(category_products)
                
            # Mostrar el listado con los productos obtenidos
            print('\n* Productos menos vendidos por categoria')
            for category in worst_selling_products:
                print('Categoria: ', category[0][3])
                print('--------------------------------------')
                print('           Nombre            | Ventas ')
                print('-----------------------------|--------')
                for product in category:
                    print('  '+product[1][0:20] + '. . .  | ', product[-1])
                print('\n')

            # Lista para almacenar los productos menos buscados por categoria
            less_searched_products = list()

            # Obtener los 7 productos menos vendidos por categoria
            for category in categories:
                i = 0
                category_products = list()
                for product in searches_by_prod[::-1]:
                    if product[3] == category:
                        i += 1
                        if i > 6:
                            break
                        category_products.append(product)
                less_searched_products.append(category_products)
                
            # Mostrar el listado con los productos obtenidos
            print('\n* Productos menos buscados por categoria')
            for category in less_searched_products:
                print('Categoria: ', category[0][3])
                print('-----------------------------------------')
                print('           Nombre            | Busquedas ')
                print('-----------------------------|-----------')
                for product in category:
                    print('  '+product[1][0:20] + '. . .  |   ', product[-1])
                print('\n')
            print('\n')
        if function_selected == 3:
            # Ordenar los productos por su puntuacion promedio de forma descendente
            for i in range(len(sales_by_prod)):
                current_ind = i
                last_ind = i - 1
                while sales_by_prod[last_ind][5] < sales_by_prod[current_ind][5] and last_ind > -1:
                    sales_by_prod[current_ind], sales_by_prod[last_ind] = sales_by_prod[last_ind], sales_by_prod[current_ind]
                    current_ind -= 1
                    last_ind -= 1

            high_score_products = list()

            # Obtener los 20 productos con las mejores puntuaciones
            i = 0
            while i < 20:
                high_score_products.append(sales_by_prod[i])
                i += 1

            print('\n* Productos con mejores puntuaciones')
            print('-----------------------------------------')
            print('           Nombre            | Puntuacion ')
            print('-----------------------------|-----------')
            for product in high_score_products:
                print('   '+product[1][0:20] + '. . . |  ', product[5])

            # Ordenar los productos por su puntuacion promedio de forma ascendente
            for i in range(len(sales_by_prod)):
                current_ind = i
                last_ind = i - 1
                while sales_by_prod[last_ind][5] > sales_by_prod[current_ind][5] and last_ind > -1:
                    sales_by_prod[current_ind], sales_by_prod[last_ind] = sales_by_prod[last_ind], sales_by_prod[current_ind]
                    current_ind -= 1
                    last_ind -= 1

            low_score_products = list()

            # Obtener los 20 productos con las peores puntuaciones si tuvieron reembolsos
            i = 0
            for product in sales_by_prod:
                if product[6]:
                    low_score_products.append(product)
                    i += 1
                if i == 20:
                    break
            print('\n* Productos con peores puntuaciones, si tuvieron reembolsos')
            print('-----------------------------------------')
            print('           Nombre            | Puntuacion ')
            print('-----------------------------|-----------')
            for product in low_score_products:
                print('   '+product[1][0:20] + '. . . |  ', product[5])
            print('\n')
        if function_selected == 4:
            # Filtrar y obtener los meses
            months = list()

            for sale in sales:
                current_month = sale[3][3:5]
                unique_month = True
                for month in months:
                    if current_month == month:
                        unique_month = False
                        break
                if unique_month:
                    months.append(current_month)
                    
            # Ordenar los meses de forma ascendentes
            for i in range(len(months)):
                current_ind = i
                last_ind = i - 1
                while months[last_ind] > months[current_ind] and last_ind > -1:
                    months[current_ind], months[last_ind] = months[last_ind], months[current_ind]
                    current_ind -= 1
                    last_ind -= 1

            # Listas para almacenar las ventas y los ingresos por mes
            months_sales = list()
            months_incomes = list()

            print('\n** Resumen mensual:')
            # Se obtienen los valores mensuales
            for month in months:
                print('Mes: ', month)
                month_sales = 0
                month_incomes = 0
                # La busqueda se hace por producto
                for product in sales_by_prod:
                    month_sales_prod = 0
                    # Se calculan las ventas del mes de cada producto
                    for sale in sales:
                        current_product = sale[1]
                        current_month = sale[3][3:5]
                        if current_month == month and current_product == product[0]:
                            month_sales_prod += 1
                    # Se calculan las entradas que genero el producto en el mes
                    incomes_prod = product[2] * month_sales_prod
                    month_sales += month_sales_prod
                    month_incomes += incomes_prod
                    # Se despliegan los totales del producto si tuvo ventas en el mes
                    if month_sales_prod:
                        print('El producto '+product[1][0:20]+'. . . '+' de la categoria '+product[3]+ ' tuvo '+str(month_sales)+' ventas en el mes, ingresando $'+str(incomes_prod)+' en total.')
                months_sales.append(month_sales)
                months_incomes.append(month_incomes)
                print('* El mes registro '+str(month_sales)+' ventas totales e ingresos por $'+str(month_incomes)+'.\n')
                print('* En promedio, el mes registro ingresos por $' + str(month_incomes // month_sales)+'.\n')

            # Se calculan los ingresos del anio
            total_incomes = 0
            for income in months_incomes:
                total_incomes += income

            print('\n** Resumen anual:')
            print('El anio tuvo ' + str(total_sales) + ' ventas totales.')
            print('El anio registro ingresos por $' + str(total_incomes) + ' en total.')

            # Se obtiene el mes que registro mas ventas
            max_sale = 0
            for i in range(len(months_sales)):
                if months_sales[max_sale] < months_sales[i]:
                    max_sale = i
                    
            print('* El mes ' + months[max_sale] + ' es el mes que registro mas ventas, con ' + str(months_sales[max_sale]) + ' ventas.')
                    
            # Se obtiene el mes que registro mas ingresos
            max_income = 0
            for i in range(len(months_incomes)):
                if months_incomes[max_sale] < months_incomes[i]:
                    max_income = i
                    
            print('* El mes ' + months[max_income] + ' es el mes que registro mas ingresos, con ingresos por $' + str(months_incomes[max_income]) + ' totales.\n')
    # Sino, el sistema se cierra
    else:
        print('\n¡Hasta luego!')
        break
