import streamlit as st
import pickle
import gc
import os
import datetime as dt
from datetime import date
import pandas as pd
import random
from sklearn.preprocessing import MinMaxScaler
import sklearn
from sklearn.ensemble import GradientBoostingClassifier
from xgboost import XGBClassifier

model_filename = 'Churn_Palladium_Europa_XGBOOST.pkl'
loaded_model = pickle.load(open(model_filename, 'rb'))
scaler_filename = 'Scaler_Europa_Palladium.pkl'
scaler = pickle.load(open(scaler_filename, 'rb'))

st.title("PALLADIUM")
st.write("""
         Modelo de predicción de CANCELACIÓN a partir de los datos de Reserva.
         """)

tratamiento = st.selectbox("Tratamiento", options=['Sr.', 'Sra.'])
tratosr = 1 if tratamiento == 'Sr.' else 0
tratosra = 1 if tratamiento == 'Sra.' else 0
nombre = st.text_input("Nombre")
apellido = st.text_input("Apellido")
pais = st.selectbox("País de Origen", options=['Alemania', 'Canadá', 'España', 'Estados Unidos', 'Francia', 'México', 'Reino Unido', 'Otro'])
hotel = st.selectbox("Hotel de Destino", options=['Bless', 'Fiesta', 'Hard Rock Hotel', 'Mallorca Rocks', 'Palladium', 'Sa Talaia', 'TRS', 'Ushuaia'])
adultos = st.slider("Adultos", 0, 8, 1)
nenes = st.slider("Niños", 0, 8, 1)
bebes = st.slider("Bebes", 0, 4, 1)
start_date = st.date_input('Fecha de Entrada: ')
end_date = st.date_input('Fecha de Salida: ')
reservapago = st.selectbox("Pagará ahora la reserva con un 10% de descuento o más tarde: ", options=['Ahora', 'Más tarde'])

# ZONAORIGEN
if pais == 'Otro':
  zonaorigen = 3
elif (pais == 'Canadá' or pais == 'Estados Unidos' or pais == 'México'):
  zonaorigen = 1
else:
  zonaorigen = 2

# TIPOCAMBIO
if zonaorigen == 1:
  tipocambio = 1.1 
elif zonaorigen == 2:
  tipocambio = 1
else:
  tipocambio = 0.048

if tipocambio == 1:
  monedaeuro = 1 
else: 0
         
# HOTEL
if hotel == 'Bless':
  Bless = 1
  Fiesta = 0
  Hard_Rock_Hotel = 0
  Mallorca_Rocks = 0
  Palladium = 0
  Sa_Talaia = 0
  TRS = 0
  Ushuaia = 0
elif hotel == 'Fiesta':
  Bless = 0
  Fiesta = 1
  Hard_Rock_Hotel = 0
  Mallorca_Rocks = 0
  Palladium = 0
  Sa_Talaia = 0
  TRS = 0
  Ushuaia = 0
elif hotel == 'Hard Rock Hotel':
  Bless = 0
  Fiesta = 0
  Hard_Rock_Hotel = 1
  Mallorca_Rocks = 0
  Palladium = 0
  Sa_Talaia = 0
  TRS = 0
  Ushuaia = 0
elif hotel == 'Mallorca Rocks':
  Bless = 0
  Fiesta = 0
  Hard_Rock_Hotel = 0
  Mallorca_Rocks = 1
  Palladium = 0
  Sa_Talaia = 0
  TRS = 0
  Ushuaia = 0
elif hotel == 'Palladium':
  Bless = 0
  Fiesta = 0
  Hard_Rock_Hotel = 0
  Mallorca_Rocks = 0
  Palladium = 1
  Sa_Talaia = 0
  TRS = 0
  Ushuaia = 0
elif hotel == 'Sa Talaia':
  Bless = 0
  Fiesta = 0
  Hard_Rock_Hotel = 0
  Mallorca_Rocks = 0
  Palladium = 0
  Sa_Talaia = 1
  TRS = 0
  Ushuaia = 0
elif hotel == 'TRS':
  Bless = 0
  Fiesta = 0
  Hard_Rock_Hotel = 0
  Mallorca_Rocks = 0
  Palladium = 0
  Sa_Talaia = 0
  TRS = 1
  Ushuaia = 0
else:
  Bless = 0
  Fiesta = 0
  Hard_Rock_Hotel = 0
  Mallorca_Rocks = 0
  Palladium = 0
  Sa_Talaia = 0
  TRS = 0
  Ushuaia = 1


# FECHAS
hoy = dt.date.today()
dateisohoy = hoy.isocalendar()
anottoo = hoy.year
mesttoo = hoy.month
diattoo = hoy.day
diasemanattoo = dateisohoy[2]
semanaanottoo = dateisohoy[1]
dateisostart = start_date.isocalendar()
ano = start_date.year
mes = start_date.month
dia = start_date.day
diasemana = dateisostart[2]
semanaano = dateisostart[1]
hoy = dt.date.today()
antiguedadreserva = (start_date - hoy).days

# PAX
pax = (adultos + nenes)

# TARGETFAM
if (adultos > 2 or nenes > 0 or bebes > 0):
  targetfam1 = 1
elif adultos == 2:
  targetfam2 = 2
else:
  targetfam3 = 3

# RESERVAPAGO
if reservapago == 'Ahora':
  reservapagada = 1 
else: 0
         
# COMERCIALIZADORA CMS
cms = random.randint(1,9)

# Construimos los datos de entrada (X) para el predict (y) del modelo
input_data = [[noches, 2, pax, adultos, nenes, bebes, 1, 0, 0, 0, 
               bebes, 765, 0, 0, 0, 0, 0, antiguedadreserva, ano, mes, 
               diasemana, semanaano,anottoo, mesttoo, diasemanattoo, 
               semanaanottoo, zonaorigen, 1, tipocambio, 1, 2, 6, 1, cms, 0, 
               Fiesta, Palladium, Mallorca_Rocks, Palladium, Sa_Talaia, 
               Ushuaia, tratosr, tratosra, 1, 0, targetfam2, targetfam3, 0, 0, 
               reservapagada]]

# Escalamos las variables numéricas con el scaler guardado con pickle
cols = ['NOCHES', 'USO', 'PAX', 'ADULTOS', 'NENES', 'BEBES', 'TIPO_CLIENTE',
       'REPETIDOR', 'MANTENER_HIST', 'SUPLETORIA', 'CUNAS', 'VALHAB', 'VALPEN',
       'VALSERV', 'VALFIJOS', 'COMERCIALIZADORA', 'GRATIS',
       'ANTIGUEDAD_RESERVA', 'ANO', 'MES', 'DIASEMANA', 'SEMANAANO',
       'ANO_TTOO', 'MES_TTOO', 'DIASEMANA_TTOO', 'SEMANAANO_TTOO',
       'ZONA_ORIGEN', 'ZONA_HOTEL', 'TIPO_CAMBIO', 'TIPO_CLI', 'TIPO_HAB',
       'TIPO_FUENTE', 'TIPO_CATEGORIA', 'CMS', 'PAIS_HOTEL_Italia',
       'MARCA_Fiesta', 'MARCA_Grand Palladium', 'MARCA_Hard Rock Hotel',
       'MARCA_Palladium', 'MARCA_Sa Talaia', 'MARCA_Ushuaïa', 'TRATO_Sr.',
       'TRATO_Sra.', 'CUPO_CUPO CONTRATO', 'CUPO_NO AFECTA', 'TARGETFAM_2',
       'TARGETFAM_3', 'FIDELIDAD_YES_True', 'GRUPOMULTIPLE_True',
       'RESERVA_PAGADA_True']
cols_num = ['NOCHES', 'USO', 'PAX', 'ADULTOS', 'NENES', 'BEBES', 'TIPO_CLIENTE',
       'REPETIDOR', 'MANTENER_HIST', 'SUPLETORIA', 'CUNAS', 'VALHAB', 'VALPEN',
       'VALSERV', 'VALFIJOS', 'COMERCIALIZADORA', 'GRATIS',
       'ANTIGUEDAD_RESERVA', 'ANO', 'MES', 'DIASEMANA', 'SEMANAANO',
       'ANO_TTOO', 'MES_TTOO', 'DIASEMANA_TTOO', 'SEMANAANO_TTOO',
       'ZONA_ORIGEN', 'ZONA_HOTEL', 'TIPO_CAMBIO', 'TIPO_CLI', 'TIPO_HAB',
       'TIPO_FUENTE', 'TIPO_CATEGORIA', 'CMS']

input = pd.DataFrame(input_data, columns=cols)
input[cols_num] = scaler.transform(input[cols_num])

# Realizamos la prediccion con el modelo cargado con pickle
prediction = loaded_model.predict(input)

# Devolvemos resultado
if st.button("Aceptar"):
  if prediction == 1: 
         st.write(f":+1: No se lo debería de decir, pero usted, {tratamiento} {nombre} {apellido}, CANCELARÁ su reserva")
  else: 
         st.write(f":+1: Gracias, me congratulo en anunciarle que usted, {tratamiento} {nombre} {apellido} MANTENDRÁ su reserva")
