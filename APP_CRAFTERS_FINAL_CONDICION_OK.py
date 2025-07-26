
import streamlit as st

st.set_page_config(page_title="Presupuesto personalizado Innovation Crafters", layout="centered")
st.title("Presupuesto personalizado Innovation Crafters")

modalidades = ["Standard", "Premium", "Platino"]
modalidad = st.selectbox("Selecciona la modalidad", modalidades)

# Mostrar mensaje informativo general (sin descripciones detalladas)
st.info(f"Has seleccionado la modalidad: {modalidad}")

# Subida de imágenes solo si es Premium
if modalidad == "Premium":
    imagenes = st.file_uploader("📸 Sube hasta 4 imágenes", accept_multiple_files=True, type=["png", "jpg", "jpeg"], key="imagenes_uploader")
    if imagenes:
        st.success(f"{len(imagenes)} imagen(es) cargada(s).")
else:
    st.warning("La subida de imágenes está desactivada en esta modalidad.")
