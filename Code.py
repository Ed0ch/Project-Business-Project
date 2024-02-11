

# # Proyecto 7 Análisis de Negocio
# 
# En este proyecto estaremos analizando los distintos datasets para poder realizar distintas conclusiones acerca de las visitas que tienen los usuarios, así como ver como se comportan los pedidos dentro de la plataformas y observar los gastos que se van teniendo en ella en las distintas configuraciones que nos ofrece con los comportamientos de los usuarios en la plataforma.


#Importación de librerías

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from math import factorial
from scipy import stats as st
import datetime as dt


# ### Importación de datasets

df_visits=pd.read_csv('C:/Users/carlo/OneDrive/Documentos/Project-Business Project/costs_us (1).csv') #Informacióna acerca de las visitas
df_orders=pd.read_csv('C:/Users/carlo/OneDrive/Documentos/Project-Business Project/orders_log_us (1).csv') #Información acerca de las ordenes
df_costs=pd.read_csv('C:/Users/carlo/OneDrive/Documentos/Project-Business Project/visits_log_us (1).csv') #Informacióna acerca de los costos


#Revisión del contenido de los datasets

# En esta parte voy a restar revisando cuales son  los datos que voy a estar utilizando, si hay faltantes y los formatos de cada uno de ellos, así como sus encabezados y ver que información contiene.

#Dataset de visitas
df_visits.info()

df_visits.columns=df_visits.columns.str.lower().str.replace(' ','_') #convertir a minusculas y quitar los espacios
df_visits.head()
#  Podemos observar que nuestro primer dataframe no tiene valores duplicados o ausentes y que también la categoría de las columnas de inicio y fin tienen otro formato, por lo que le daremos el formato de fecha.

df_visits['end_ts']=pd.to_datetime(df_visits['end_ts']) #Convertir la columna a formato de fecha
df_visits['start_ts']=pd.to_datetime(df_visits['start_ts']) #Actualizar la columna a formato de fecha


#Dataset de ordenes 

df_orders.info()

#Revisión de las columnas del dataset para ver su contenido
df_orders.columns=df_orders.columns.str.lower().str.replace(' ','_')
df_orders.head()
df_orders['buy_ts']=pd.to_datetime(df_orders['buy_ts']) #Actualizar la columna a formato de fecha


# Dataset de costos
df_costs.info() #Revisión del tipo de datos que vamos a analizar.

df_costs.head() #Revisar los datos de las primeras columnas

df_costs['dt']=pd.to_datetime(df_costs['dt']) #Actualizar la columna  a formato de fecha





# En esta parte estaremos analizando las personas que usan por dia, semana, mes, revisaremos las sesiones, estaremos analizando la duración de cada sesión, así como la frecuencia y que tanta probabilidad es que los ususarios regresen.
 

#¿Cuántas personas lo usan cada día, semana y mes? 

df_visits['session_year']=df_visits['start_ts'].dt.year
df_visits['session_month']=df_visits['start_ts'].dt.month
df_visits['session_week']=df_visits['start_ts'].dt.week
df_visits['session_date']=df_visits['start_ts'].dt.date

print(df_visits.head())


dau_total=df_visits.groupby('session_date').agg({'uid':'nunique'}).mean() #Numero de usuarios activos diarios
wau_total=df_visits.groupby('session_week').agg({'uid':'nunique'}).mean() #'Numero de usuarios activos por semana'
mau_total=df_visits.groupby('session_month').agg({'uid':'nunique'}).mean()#Número de usuarios activos por mes

print(int(dau_total))
print(int(wau_total))
print(int(mau_total))


persons=pd.concat([dau_total,wau_total,mau_total])

persons.columns=['dau_total','wau_total','mau_total']

grafico=persons.plot(kind='bar',color=['darkblue','gray','purple'])
bar_names = ['Día', 'Semana', 'Mes']
grafico.set_xticklabels(bar_names, rotation=0)

# Agregar etiquetas y título
plt.xlabel('Periodo')
plt.ylabel('Número de usuarios')
plt.title('Usuarios Activos Diarios, Semanales y Mensuales')


# Podemos obsvervar que el numero diario de usuarios es de 907, así como el de 5825 usuarios por semana, dando un total de 23228 usuarios al mes, lo que nos muestra que el número de usuarios tiene una buena actividad conforme va pasando el resto de la semana.



# ¿Cuántos usuarios hay por día?

sessions_per_user=df_visits.groupby(['session_year','session_month']).agg({'uid':['count','nunique']})
sessions_per_user.columns=['n_sessions','n_users']
sessions_per_user['sessions_per_user']=(sessions_per_user['n_sessions']/sessions_per_user['n_users'])

print(sessions_per_user)


sessions_per_user_graph=sessions_per_user['n_users']

sessions_per_user_graph.plot(kind='bar',title='Número de usuarios por mes',xlabel='Periodo',ylabel='Cantidad de usuarios')


# Podemos observar que apartir del 2017 en Octubre se ve el principal aumento importante en la cantidad de tráfico que existe en el sitio, se ve un aumento considerable que tiene a bajar poco, hasta Abril del  2018 es cuando vemos una tendencia decreciente.
# Podríamos indagar más a si tiene que ver con temporada Navideña el inicio del repunte y obtener más datos de ello.



#¿Cuál es la duración de cada sesión?


df_visits['session_duration']=(df_visits['end_ts']-df_visits['start_ts']).dt.seconds
print(df_visits['session_duration'].mean())


# Cada sesión tiene una duración promedio de 643 segundos, lo que equivale a casi 11 minutos por cada una de las sesiones de los usarios.

print(df_visits['session_duration'].mode())


# ¿Con qué frecuencia regresan los ususarios?

sticky_factor_wau=dau_total/wau_total *100
sticky_factor_mau=dau_total/mau_total*100
print(sticky_factor_wau)
print(sticky_factor_mau)


# Ventas

devices=df_visits.groupby('device').agg({'uid':'count'}) #Aqui estaré analizando por donde es que se compra más a la hora de visitar el sitio web
print(devices)


# Aqui podemos observar que el usuario compró más por el dispositivo de escritorio que en su celular, siendo con 262567 el numero total, lo que viene siendo más del doble que por el otro dispositivo.

devices_count=df_visits.groupby('device').agg({'uid': 'nunique'})
print(devices_count)

devices_count.plot(kind='bar',title='Devices')


# Podemos ver que se compró más por el computador de escritorio, representando solo el 30% de las ventas en el caso del teléfono celular



first_order_date=df_orders.groupby('uid')['buy_ts'].min() #En este caso estaremos agrupando cada cliente para obtener la fecha de su primer pedido.
first_order_date.name='first_order_date'


# ¿Cuántos pedidos hacen sobre un cierto tiempo dado?

orders=df_orders.join(first_order_date,on='uid') #Esto nos permite ver las fechas con las primeras compras de los clientes
print(orders.head(10))

orders['first_order_month']=orders['first_order_date'].astype('datetime64[M]') #Separar los meses
orders['order_month']=orders['buy_ts'].astype('datetime64[M]')

print(orders.head(15))

cohort=orders.groupby('first_order_month').agg({'uid':'nunique','revenue':'sum'})
print(cohort)


# Como podemos observar se hacen más de mil pedidos por mes, siendo el mes de diciembre de 2017 el mes que más pedidos tuvo pero no fue el mes que más ingresos dejó, en ese caso fue el mes de septiembre.
# Esto nos indica que podría ser que en ese mes las personas fueron más adherentes o que hicieron ordenes con mayor costo.


#¿Cuál es el tamaño promedio de compra?
cohort['revenue'].mean() #Tamaño promedio de compra

# El tamaño promedio que nos arroja de la cohorte viene siendo de 19389




orders_by_cohort=orders.reset_index()
orders_by_cohort['cohort_lifetime']=(orders['buy_ts']-orders['first_order_date'])
orders_by_cohort['cohort_lifetime'].head()


# ## Marketing

df_orders['buy_ts'].describe() #Esto nos sirve para ver la distribución de fecha de los pedidos
df_costs['dt'].describe()


# Aqui podemos ver en las fechas que el rango de ellas nos sirven para realizar nuestro analisis, para poder encontrar el LTV y el CAC.
# Vamos a tener que separarlos por mes por que tenemos información de más de un año, lo cual separarlo será de utilidad.

df_orders['order_month']=df_orders['buy_ts'].astype('datetime64[M]')
df_costs['month']=df_costs['dt'].astype('datetime64[M]')


# Ahora vamos a recuperar el numero de mes de la primera compra de nuestros clientes

first_order=df_orders.groupby('uid').agg({'order_month':'min'}).reset_index()
first_order.columns=['uid','first_order_month']
first_order.head()


# Con esto tenemos el identificador de cada uno de los usuarios de las primeras compras de cada uno de los clientes.

# Acá abajo calcularemos el número de nuevos lientes para cada mes

cohort_size=first_order.groupby('first_order_month').agg({'uid':'nunique'}).reset_index()
cohort_size.columns=['first_order_month','n_buyers']
print(cohort_size.head())
      


cohort_graph=cohort_size
cohort_graph['first_order_month']=pd.to_datetime(cohort_graph['first_order_month'])
cohort_graph['month']=cohort_graph['first_order_month'].dt.month
cohort_graph['year']=cohort_graph['first_order_month'].dt.year
cohort_plot=cohort_graph[['n_buyers','month','year']]
cohort_plot.plot(kind='bar',x='month',y='n_buyers',title='Primeros compradores',xlabel='Periodo',ylabel='Compradores',color='green')


# Esto nos permite ver la cantidad de compradores que tuvimos por mes en el cohorte.



# Ahora vamos a agregar al dataframe original de ordenes esta de primeras ordenes

ord=pd.merge(df_orders,first_order,on='uid')
ord.head()
cohorts=ord.groupby(['first_order_month','order_month']).agg({'revenue':'sum'}).reset_index() #Ordenamos la tabla de pedidos por mes de la primera compra y el mesa de la compra para totalizar los ingresos
cohorts.head(15)
cohorts.head().plot(kind='bar',title='Ingresos',x='order_month',y='revenue',xlabel='Periodo',ylabel='Ingresos')


# Esta parte especifica los ingresos que fueron generados por la cohorte, siendo así su primero pedido el primero de Junio de 2017 con un total de $9557.49.
reporte=pd.merge(cohorts,cohort_size,on='first_order_month')
reporte.head(15)


# Esta tablas nos indica la cantidad de usuarios que realizaron sus primeras compras cada mes en la tabla.

margin_rate=0.5

reporte['gp']=reporte['revenue']*margin_rate
reporte['age']=(reporte['order_month']-reporte['first_order_month'])/np.timedelta64(1,'M')
reporte['age']=reporte['age'].round().astype('int')

reporte.head(15)


# Esta tabla es para poder evaluar la edad de la cohorte y obtener más datos para poder sacar el LTV.

reporte['ltv']=reporte['gp']/reporte['n_buyers']

output=reporte.pivot_table(index='first_order_month',columns='age',values='ltv',aggfunc='mean').round()

output.fillna('')

ltv_20170901=output.loc['2017-09-01'].sum()
ltv_20170901


# En promedio cada cliente de la primera cohorte generó 6 dolares de ingresos durante su ciclo de vida de 12 meses.

cohort_20170901=reporte[reporte['first_order_month']=='2017-09-01']

costs_20170901=df_costs[df_costs['month']=='2017-09-01']['costs'].sum()

n_buyers_20170901=cohort_20170901['n_buyers']

cac_20170901=costs_20170901/n_buyers_20170901

print(cac_20170901)


# En este caso podemos ver que el costo para poder adquirir un cliente es de 9.44 dolares.

# # Conclusión

# Para concluir podemos observar que el año 2017 tuvo mucho más tráfico en comparación con el año 2018, podemos observar que comenzamos el año con buenos volumenes de venta, en los cuales los usuarios suelen concentrarse más utilizando computadores de escritorio para realizar sus pedidos en linea, en los cuales tienen un tiempo promedio de sesión de un poco más de 10 minutos y teniendo un factor de retorno moderablemente alto.



# ### Comentarios

