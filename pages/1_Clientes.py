import streamlit as st

from patitas.repository import get_repository

st.markdown("## 👤 Clientes")
st.caption("Registro de propietarios de la clínica.")
st.divider()

st.title("Gestión de Clientes")

repo = get_repository()
owners_df = repo.list_owners()

st.subheader("Añadir nuevo cliente")

with st.form("add_client_form"):
    nombre = st.text_input("Nombre del cliente")
    email = st.text_input("Email")
    telefono = st.text_input("Teléfono")

    submitted = st.form_submit_button("Guardar cliente")

if submitted:
    if not nombre.strip():
        st.error("El nombre es obligatorio.")
    else:
        repo.add_owner(nombre, email, telefono)
        owners_df = repo.list_owners()
        st.success(f"Cliente '{nombre}' guardado correctamente.")

st.subheader("Lista de Clientes")

if owners_df.empty:
    st.info("Todavía no hay clientes registrados.")
else:
    st.dataframe(owners_df, width="stretch")
