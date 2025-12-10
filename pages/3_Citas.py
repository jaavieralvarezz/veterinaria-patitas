import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import time  # 👈 para comparar horas

st.markdown("## 📅 Citas")
st.caption("Agenda de la clínica: día, hora, mascota y motivo.")
st.divider()


# =========================
# RUTAS Y CONSTANTES
# =========================

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

OWNERS_FILE = DATA_DIR / "owners.csv"
PETS_FILE = DATA_DIR / "pets.csv"
APPOINTMENTS_FILE = DATA_DIR / "appointments.csv"

APPOINTMENTS_COLS = [
    "id",
    "fecha",
    "hora",
    "mascota",
    "propietario",
    "motivo",
]

# Horario de la clínica
OPEN_TIME = time(9, 0)   # 09:00
CLOSE_TIME = time(21, 0) # 21:00


def load_owners() -> pd.DataFrame:
    if OWNERS_FILE.exists() and OWNERS_FILE.stat().st_size > 0:
        return pd.read_csv(OWNERS_FILE)
    else:
        return pd.DataFrame(columns=["id", "nombre", "email", "telefono"])


def load_pets() -> pd.DataFrame:
    if PETS_FILE.exists() and PETS_FILE.stat().st_size > 0:
        df = pd.read_csv(PETS_FILE)
        return df
    else:
        return pd.DataFrame(
            columns=["id", "nombre", "tipo", "propietario_id", "propietario_nombre"]
        )


def load_appointments() -> pd.DataFrame:
    if APPOINTMENTS_FILE.exists() and APPOINTMENTS_FILE.stat().st_size > 0:
        df = pd.read_csv(APPOINTMENTS_FILE)
        if list(df.columns) != APPOINTMENTS_COLS:
            df = pd.DataFrame(columns=APPOINTMENTS_COLS)
    else:
        df = pd.DataFrame(columns=APPOINTMENTS_COLS)
    return df


def save_appointments(df: pd.DataFrame) -> None:
    df.to_csv(APPOINTMENTS_FILE, index=False)


# =========================
# INTERFAZ STREAMLIT
# =========================

st.title("Gestión de Citas")

owners_df = load_owners()
pets_df = load_pets()
appointments_df = load_appointments()

# Sin mascotas no hay citas
if pets_df.empty:
    st.warning("No hay mascotas registradas. Ve a **Mascotas** y añade alguna primero.")
else:
    st.subheader("Crear nueva cita")

    # Selector de mascota (mostramos nombre + propietario)
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
        # ---------- VALIDACIONES ESPECIALES ----------
        # 1) Motivo obligatorio
        if not motivo.strip():
            st.error("El motivo de la cita es obligatorio.")
        else:
            # 2) Solo lunes a sábado
            # weekday(): 0 = lunes, ..., 5 = sábado, 6 = domingo
            if fecha.weekday() == 6:
                st.error("Solo se pueden reservar citas de lunes a sábado (no domingos).")
            # 3) Solo entre 09:00 y 21:00
            elif not (OPEN_TIME <= hora <= CLOSE_TIME):
                st.error("El horario de la clínica es de 09:00 a 21:00.")
            else:
                # ---------- SI TODO ES VÁLIDO, GUARDAMOS ----------
                pet_row = pets_df[pets_df["display"] == mascota_display].iloc[0]
                mascota_nombre = pet_row["nombre"]
                propietario_nombre = pet_row["propietario_nombre"]

                if appointments_df.empty:
                    new_id = 1
                else:
                    new_id = int(appointments_df["id"].max()) + 1

                new_row = {
                    "id": new_id,
                    "fecha": str(fecha),
                    "hora": str(hora),
                    "mascota": mascota_nombre,
                    "propietario": propietario_nombre,
                    "motivo": motivo.strip(),
                }

                appointments_df = pd.concat(
                    [appointments_df, pd.DataFrame([new_row])],
                    ignore_index=True,
                )
                save_appointments(appointments_df)

                st.success(
                    f"Cita guardada para '{mascota_nombre}' "
                    f"({propietario_nombre}) el {fecha} a las {hora}."
                )

# Listado de citas
st.subheader("Listado de citas")

if appointments_df.empty:
    st.info("Todavía no hay citas registradas.")
else:
    st.dataframe(appointments_df, use_container_width=True)
