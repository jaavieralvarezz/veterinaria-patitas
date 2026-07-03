import streamlit as st

from patitas.repository import get_repository
from patitas.validation import validate_appointment

st.markdown("## 📅 Citas")
st.caption("Agenda de la clínica: día, hora, mascota y motivo.")
st.divider()

st.title("Gestión de Citas")

repo = get_repository()
pets_df = repo.list_pets()
appointments_df = repo.list_appointments()

if pets_df.empty:
    st.warning("No hay mascotas registradas. Ve a **Mascotas** y añade alguna primero.")
else:
    st.subheader("Crear nueva cita")

    pets_df["display"] = (
        pets_df["nombre"] + " (Propietario: " + pets_df["propietario_nombre"] + ")"
    )
    pet_options = pets_df["display"].tolist()

    with st.form("add_appointment_form"):
        mascota_display = st.selectbox("Mascota", pet_options)
        fecha = st.date_input("Fecha")
        hora = st.time_input("Hora")
        motivo = st.text_input("Motivo de la cita")

        submitted = st.form_submit_button("Guardar cita")

    if submitted:
        try:
            validate_appointment(fecha, hora, motivo)
            pet_row = pets_df[pets_df["display"] == mascota_display].iloc[0]
            mascota_nombre = pet_row["nombre"]
            propietario_nombre = pet_row["propietario_nombre"]

            repo.add_appointment(
                fecha=str(fecha),
                hora=str(hora),
                mascota=mascota_nombre,
                propietario=propietario_nombre,
                motivo=motivo,
            )
            appointments_df = repo.list_appointments()

            st.success(
                f"Cita guardada para '{mascota_nombre}' "
                f"({propietario_nombre}) el {fecha} a las {hora}."
            )
        except ValueError as exc:
            st.error(str(exc))

st.subheader("Listado de citas")

if appointments_df.empty:
    st.info("Todavía no hay citas registradas.")
else:
    st.dataframe(appointments_df, width="stretch")
