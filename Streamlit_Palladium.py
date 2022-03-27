{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "name": "Streamlit_Palladium.ipynb",
      "provenance": [],
      "collapsed_sections": [],
      "authorship_tag": "ABX9TyMj6eM2iew7ep0Q1FEXYffz",
      "include_colab_link": true
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/luvimi/streamlit_palladium_demo/blob/main/Streamlit_Palladium.ipynb\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "!pip install -q streamlit\n",
        "import streamlit as st\n",
        "import pickle\n",
        "import datetime as dt"
      ],
      "metadata": {
        "id": "rgpymT6CaPQn"
      },
      "execution_count": 1,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "pick_read = open('Churn_Palladium.pkl','rb')\n",
        "loaded_model = pickle.load(pick_read)\n",
        "pick_read.close()\n",
        "loaded_model"
      ],
      "metadata": {
        "id": "JU2tQVkDZDzg"
      },
      "execution_count": 5,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "st.title(\"PALLADIUM\")\n",
        "st.write(\"\"\"\n",
        "         Modelo de predicción de CANCELACIÓN a partir de los datos de Reserva.\n",
        "         \"\"\")\n",
        "\n",
        "tratamiento = st.selectbox(\"Tratamiento\", options=['Sr.', 'Sra.'])\n",
        "tratosr = 1 if tratamiento == 'Sr.' else 0\n",
        "tratosra = 1 if tratamiento == 'Sra.' else 0\n",
        "nombre = st.text_input(\"Nombre\")\n",
        "apellido = st.text_input(\"Apellido\")\n",
        "\n",
        "pais = st.selectbox(\"País de Origen\", options=['Alemania', 'Canadá', 'España', 'Estados Unidos', 'Francia', 'México', 'Reino Unido', 'Otro'])\n",
        "#location = st.multiselect(\"País de Origen\", ('Alemania', 'Canadá', 'España', 'Estados Unidos', 'Francia', 'México', 'Reino Unido', 'Otro')\n",
        "zona = 1 if pais == ('Canadá' or 'Estados Unidos' or 'México')\n",
        "zona = 2 if pais == ('Alemania' or 'España' or 'Francia' or 'Reino Unido')\n",
        "zona = 3 if pais == ('Otro')\n",
        "tipocambio = 1.1 if zona == 1\n",
        "tipocambio = 1 if zona == 2\n",
        "tipocambio = 0.048 if zona == 3\n",
        "monedaeuro = 1 if tipocambio == 1 else 0\n",
        "\n",
        "#fecha_llegada = st.date_input(\"¿Cuándo es su fecha de llegada?\", datetime.date(2019, 7, 6))\n",
        "hoy = datetime.date.today()\n",
        "manana = hoy + datetime.timedelta(days=1)\n",
        "start_date = st.date_input('Start date', hoy)\n",
        "end_date = st.date_input('End date', manana)\n",
        "if start_date < end_date:\n",
        "    st.success('Día de Llegada: `%s`\\n\\nDía de Salida:`%s`' % (start_date, end_date))\n",
        "else:\n",
        "    st.error('Error: El día de Salida debe ser posterior al día de llegada.')\n",
        "ano = start_date.dt.year\n",
        "mes = start_date.dt.month\n",
        "diasemana = start_date.dt.day\n",
        "semanaano = start_date.dt.isocalendar().week\n",
        "noches = (end_date - start_date).days\n",
        "antiguedadreservar = (start_date - hoy).days\n",
        "\n",
        "adultos = st.slider(\"Nº de Adultos\", 1, 4, 1)\n",
        "nenes = st.slider(\"Nº de Niños\", 1, 4, 1)\n",
        "bebes = st.slider(\"Nº de Bebes\", 1, 4, 1)\n",
        "pax = (adultos + nenes)\n",
        "if (adultos > 2 or nenes > 0 or bebes > 0):\n",
        "  targetfam1 = 1\n",
        "elif adultos == 2:\n",
        "  targetfam2 = 2\n",
        "else:\n",
        "  targetfam3 = 3\n",
        "\n",
        "reservapago = st.radio(\"¿Pagará ahora su Reserva con un 10% de descuento?\", (\"SI\", \"Más tarde\"))\n",
        "reservapagada = 1 if reservapago == 'SI' else 0\n",
        "\n",
        "input_data = [['noches', 2, 'pax', 'adultos', 'nenes', 'bebes', 1, 0, 0, 0, 'bebes', \n",
        "               765, 0, 0, 0, 0, 0, 'antiguedadreservar', 'ano', 'mes', 'diasemana', \n",
        "               'semanaano', 'zona', 'tipocambio', 1, 2, 6, 1, 'monedaeuro', 0, 0, 0, \n",
        "               'tratosr', 'tratosra', 1, 0, 'targetfam2', 'targetfam3', 0, 0, \n",
        "               'reservapagada']]\n",
        "prediction = loaded_model.predict(input_data)\n",
        "\n",
        "if st.button(\"Aceptar\"):\n",
        "  if prediction == 1:\n",
        "    if {tratamiento} == 'Sr':\n",
        "      st.write(f\":+1: El {tramaiento} {nombre} {apellido} CANCELARÁ su reserva\")\n",
        "    else:\n",
        "      st.write(f\":+1: La {tramaiento} {nombre} {apellido} CANCELARÁ su reserva\")\n",
        "  else:\n",
        "    if {tratamiento} == 'Sr':\n",
        "      st.write(f\":+1: El {tramaiento} {nombre} {apellido} MANTENDRÁ SU RESERVA\")\n",
        "    else:\n",
        "      st.write(f\":+1: La {tramaiento} {nombre} {apellido} MANTENDRÁ SU RESERVA\")\n"
      ],
      "metadata": {
        "id": "L5Q78oOTd6kQ"
      },
      "execution_count": null,
      "outputs": []
    }
  ]
}