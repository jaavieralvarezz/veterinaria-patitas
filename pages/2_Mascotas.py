import streamlit as st

from patitas.repository import get_repository

st.markdown("## 🐕 Mascotas")
st.caption("Fichas de los pacientes y su propietario.")
st.divider()

st.title("Gestión de Mascotas")

repo = get_repository()
owners_df = repo.list_owners()
pets_df = repo.list_pets()

# Si no hay propietarios, no tiene sentido crear mascotas
if owners_df.empty:
    st.warning("No hay propietarios registrados. Ve primero a **Clientes** y añade alguno.")
else:
    st.subheader("Añadir nueva mascota")

    owner_options = {
        f'{row["nombre"]} (ID: {row["id"]})': int(row["id"])
        for _, row in owners_df.iterrows()
    }

    with st.form("add_pet_form"):
        nombre_mascota = st.text_input("Nombre de la mascota")
        tipo_mascota = st.selectbox(
            "Tipo de mascota",
            ["Perro", "Gato", "Ave", "Reptil", "Roedor", "Otro"],
        )
        propietario_display = st.selectbox("Propietario", list(owner_options.keys()))

        submitted = st.form_submit_button("Guardar mascota")

    if submitted:
        if not nombre_mascota.strip():
            st.error("El nombre de la mascota es obligatorio.")
        else:
            propietario_id = owner_options[propietario_display]
            repo.add_pet(nombre_mascota, tipo_mascota, propietario_id)
            pets_df = repo.list_pets()

            st.success(
                f"Mascota '{nombre_mascota}' registrada para el propietario seleccionado."
            )

# Listado de mascotas
st.subheader("Listado de mascotas")

if pets_df.empty:
    st.info("Todavía no hay mascotas registradas.")
else:
    st.dataframe(pets_df, width="stretch")
