
import streamlit as st
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm

# Traducciones básicas
lang = st.sidebar.selectbox("🌐 Idioma / Language", ["Español", "English"])
texts = {
    "Español": {
        "title": "Presupuesto personalizado Innovation Crafters",
        "client_data": "🧾 Datos del cliente",
        "product_info": "📦 Detalles del producto",
        "upload_photos": "📸 Muéstranos tu producto para empaquetar (hasta 4 imágenes)",
        "estimated_days": "Días de producción estimada",
        "download": "Descargar presupuesto",
        "recargo_eq": "¿Recargo de equivalencia (5,2%)?",
        "yes": "Sí",
        "no": "No"
    },
    "English": {
        "title": "Custom Quote - Innovation Crafters",
        "client_data": "🧾 Client Information",
        "product_info": "📦 Product Details",
        "upload_photos": "📸 Show us your product to pack (up to 4 images)",
        "estimated_days": "Estimated Production Days",
        "download": "Download Quote",
        "recargo_eq": "Equivalence surcharge (5.2%)?",
        "yes": "Yes",
        "no": "No"
    }
}

t = texts[lang]

st.set_page_config(page_title=t["title"], layout="centered")
st.title(t["title"])

# CLIENT DATA
st.header(t["client_data"])
nombre = st.text_input("Nombre / Name")
empresa = st.text_input("Empresa / Company")
direccion = st.text_input("Dirección / Address")
telefono = st.text_input("Teléfono / Phone")
email = st.text_input("Email")
cif = st.text_input("CIF / VAT ID")
observaciones = st.text_area("Observaciones / Notes")

# PRODUCT INFO
st.header(t["product_info"])
modalidad = st.selectbox("Modalidad", ["Standard", "Premium", "Platino"])
formato_bolsa = st.selectbox("Formato de Bolsa", ["1g, 2g, 3g", "5g, 10g, 20g", "50g, 100g"])

min_kg = {"Standard": 3.0, "Premium": 2.0, "Platino": 0.5}
mano_obra = {"Standard": 300, "Premium": 275, "Platino": 300}
coste_bolsa_dict = {"1g, 2g, 3g": 0.45, "5g, 10g, 20g": 0.50, "50g, 100g": 0.65}

kg = st.number_input("Kg a empaquetar", min_value=min_kg[modalidad], value=min_kg[modalidad], step=0.1)

tipo_envio = st.radio(t["estimated_days"], ["Standard (3-5 días hábiles + transporte)", "Express (3 días hábiles + transporte)"])
recargo_eq = st.selectbox(t["recargo_eq"], [t["no"], t["yes"]])

# Imágenes
st.header(t["upload_photos"])
imagenes = st.file_uploader("Sube tus imágenes", type=["png", "jpg", "jpeg"], accept_multiple_files=True, help="Máximo 4 imágenes")

# CÁLCULOS
precio_mano_obra = mano_obra[modalidad] * kg
n_bolsas = (kg * 1000) / 5
precio_bolsas = coste_bolsa_dict[formato_bolsa] * n_bolsas

if "Express" in tipo_envio:
    envio = kg * 1000 * 0.50  # 0,50€/g
else:
    envio = 5

precio_base = precio_mano_obra + precio_bolsas + envio
recargo = 0.052 * precio_base if recargo_eq == t["yes"] else 0
iva = 0.21 * (precio_base + recargo)
total = precio_base + recargo + iva

# GENERAR PDF
def generar_pdf():
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width / 2, height - 2 * cm, t["title"])

    c.setFont("Helvetica-Bold", 12)
    c.drawString(2 * cm, height - 3.5 * cm, t["client_data"])
    c.setFont("Helvetica", 10)
    y = height - 4.2 * cm
    for line in [
        f"Nombre: {nombre}",
        f"Empresa: {empresa}",
        f"Dirección: {direccion}",
        f"Teléfono: {telefono}",
        f"Email: {email}",
        f"CIF: {cif}",
        f"Observaciones: {observaciones}"
    ]:
        c.drawString(2 * cm, y, line)
        y -= 0.5 * cm

    y -= 0.2 * cm
    c.setFont("Helvetica-Bold", 12)
    c.drawString(2 * cm, y, t["product_info"])
    y -= 0.7 * cm
    c.setFont("Helvetica", 10)
    for line in [
        f"Modalidad: {modalidad}",
        f"Kg: {kg} kg",
        f"Formato bolsa: {formato_bolsa}",
        f"Tipo de envío: {tipo_envio}",
        f"Precio mano de obra: {precio_mano_obra:.2f} €",
        f"Precio bolsas: {precio_bolsas:.2f} €",
        f"Envío: {envio:.2f} €",
        f"Recargo equivalencia: {recargo:.2f} €",
        f"IVA (21%): {iva:.2f} €",
        f"TOTAL: {total:.2f} €"
    ]:
        c.drawString(2 * cm, y, line)
        y -= 0.5 * cm

    y -= 0.2 * cm
    c.setFont("Helvetica-Bold", 12)
    c.drawString(2 * cm, y, "📌 Datos fiscales:")
    y -= 0.6 * cm
    c.setFont("Helvetica", 10)
    for line in [
        "Inversiones Brandon e Hijos SL",
        "Calle Anselm Clavé 7, 17300, Blanes, Gerona",
        "CIF: B42761262",
        "IBAN: ESXX XXXX XXXX XXXX XXXX XXXX",
        "Pago: 60% por adelantado, 40% al salir el producto"
    ]:
        c.drawString(2 * cm, y, line)
        y -= 0.5 * cm

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer

if st.button(t["download"]):
    pdf = generar_pdf()
    st.download_button(label="📄 Descargar PDF", data=pdf, file_name="presupuesto_innovation_crafters.pdf")
