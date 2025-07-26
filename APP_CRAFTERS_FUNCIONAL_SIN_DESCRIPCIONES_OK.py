
import streamlit as st
import os

st.set_page_config(page_title="Presupuesto personalizado Innovation Crafters", layout="centered")

st.title("Presupuesto personalizado Innovation Crafters")

modalidades = ["Standard", "Premium", "Platino"]
modalidad = st.selectbox("Selecciona la modalidad", modalidades)

# Continuar con resto de lógica de negocio, cálculo de costos, formularios, imagen, etc.
st.write("Esta versión está limpia, lista para continuar.")
