import streamlit as st
import pickle
import datetime as dt

model_filename = 'Churn_Palladium.pkl'
loaded_model = pickle.load(open(model_filename, 'rb'))

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
#location = st.multiselect("País de Origen", ('Alemania', 'Canadá', 'España', 'Estados Unidos', 'Francia', 'México', 'Reino Unido', 'Otro')
if pais == 'Otro':
  zona = 3
elif (pais == 'Canadá' or pais == 'Estados Unidos' or pais == 'México'):
  zona = 1
else:
  zona = 2

if zona == 1:
  tipocambio = 1.1 
elif zona == 2:
  tipocambio = 1
else:
  tipocambio = 0.048

if tipocambio == 1:
  monedaeuro = 1 
else: 0

#fecha_llegada = st.date_input("¿Cuándo es su fecha de llegada?", datetime.date(2019, 7, 6))
hoy = datetime.date.today()
manana = hoy + datetime.timedelta(days=1)
start_date = st.date_input('Start date', hoy)
end_date = st.date_input('End date', manana)

if start_date < end_date:
    st.success('Día de Llegada: `%s`\n\nDía de Salida:`%s`' % (start_date, end_date))
else:
    st.error('Error: El día de Salida debe ser posterior al día de llegada.')

ano = start_date.dt.year
mes = start_date.dt.month
diasemana = start_date.dt.day
semanaano = start_date.dt.isocalendar().week
noches = (end_date - start_date).days
antiguedadreservar = (start_date - hoy).days

adultos = st.slider("Nº de Adultos", 1, 4, 1)
nenes = st.slider("Nº de Niños", 1, 4, 1)
bebes = st.slider("Nº de Bebes", 1, 4, 1)
pax = (adultos + nenes)

if (adultos > 2 or nenes > 0 or bebes > 0):
  targetfam1 = 1
elif adultos == 2:
  targetfam2 = 2
else:
  targetfam3 = 3

reservapago = st.radio("¿Pagará ahora su Reserva con un 10% de descuento?", ("SI", "Más tarde"))

if reservapago == 'SI':
  reservapagada = 1 
else: 0

input_data = [['noches', 2, 'pax', 'adultos', 'nenes', 'bebes', 1, 0, 0, 0, 'bebes', 
               765, 0, 0, 0, 0, 0, 'antiguedadreservar', 'ano', 'mes', 'diasemana', 
               'semanaano', 'zona', 'tipocambio', 1, 2, 6, 1, 'monedaeuro', 0, 0, 0, 
               'tratosr', 'tratosra', 1, 0, 'targetfam2', 'targetfam3', 0, 0, 
               'reservapagada']]
prediction = loaded_model.predict(input_data)

if st.button("Aceptar"):
  if prediction == 1:
    if {tratamiento} == 'Sr':
      st.write(f":+1: El {tramaiento} {nombre} {apellido} CANCELARÁ su reserva")
    else:
      st.write(f":+1: La {tramaiento} {nombre} {apellido} CANCELARÁ su reserva")
  else:
    if {tratamiento} == 'Sr':
      st.write(f":+1: El {tramaiento} {nombre} {apellido} MANTENDRÁ SU RESERVA")
    else:
      st.write(f":+1: La {tramaiento} {nombre} {apellido} MANTENDRÁ SU RESERVA")
