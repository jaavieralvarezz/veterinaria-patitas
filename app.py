import streamlit as st

from patitas.database import database_mode

st.set_page_config(
    page_title="Clínica veterinaria",
    page_icon="🐶",   # ← icono válido
    layout="wide"
)

st.title("Clínica Veterinaria Patitas 🐶")
st.sidebar.caption(f"Datos: {database_mode()}")

st.markdown(
    """
    Bienvenido al sistema de gestión de la clínica veterinaria.

    Usa el menú de la izquierda (barra lateral) para navegar entre:
    - **Clientes** (propietarios)
    - **Mascotas**
    - **Citas**
    - **Analítica**
    
    Hola a todos los padres y madres de algun animal. En primer lugar queremos dirigirnos a vosotros de una manera cercana.
    Ya que cuando de una mascota se habla tratamos de familia. Y eso es lo que queremos ser para vosotros.
    Hemos desarrollado nuestra primera pagina web, para que en cuanto al bienestar de vuestas mascotas os sintais seguros al 100%.
    Desde aqui podreis registraros con vuestros datos, al igual que a vuestras mascotas para pedir cita sin necesidad de llamar
    o esperar colas en la clinica.
    """
)
