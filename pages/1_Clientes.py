import streamlit as st
import pandas as pd
from pathlib import Path

st.markdown("## 👤 Clientes")
st.caption("Registro de propietarios de la clínica.")
st.divider()


# Ruta al CSV de clientes
DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "owners.csv"
DATA_PATH.parent.mkdir(parents=True, exist_ok=True)

COLUMNS = ["id", "nombre", "email", "telefono"]


def load_owners() -> pd.DataFrame:
    """Carga el CSV de propietarios o devuelve un DF vacío con columnas correctas."""
    if DATA_PATH.exists() and DATA_PATH.stat().st_size > 0:
        df = pd.read_csv(DATA_PATH)
        # Si el fichero tiene otras columnas, lo reseteamos
        if list(df.columns) != COLUMNS:
            df = pd.DataFrame(columns=COLUMNS)
    else:
        df = pd.DataFrame(columns=COLUMNS)
    return df


def save_owners(df: pd.DataFrame) -> None:
    """Guarda el DataFrame en el CSV."""
    df.to_csv(DATA_PATH, index=False)


st.title("Gestión de Clientes")

# 1) Cargar datos
owners_df = load_owners()

st.subheader("Añadir nuevo cliente")

# 2) Formulario (no vaciamos automáticamente, se hace a mano y ya)
with st.form("add_client_form"):
    nombre = st.text_input("Nombre del cliente")
    email = st.text_input("Email")
    telefono = st.text_input("Teléfono")

    submitted = st.form_submit_button("Guardar cliente")

if submitted:
    if not nombre.strip():
        st.error("El nombre es obligatorio.")
    else:
        if owners_df.empty:
            new_id = 1
        else:
            new_id = int(owners_df["id"].max()) + 1

        new_row = {
            "id": new_id,
            "nombre": nombre.strip(),
            "email": email.strip(),
            "telefono": telefono.strip(),
        }

        owners_df = pd.concat(
            [owners_df, pd.DataFrame([new_row])],
            ignore_index=True
        )
        save_owners(owners_df)
        st.success(f"Cliente '{nombre}' guardado correctamente.")

st.subheader("Lista de Clientes")

if owners_df.empty:
    st.info("Todavía no hay clientes registrados.")
else:
    st.dataframe(owners_df, use_container_width=True)
