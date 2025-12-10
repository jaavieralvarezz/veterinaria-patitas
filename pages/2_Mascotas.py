import streamlit as st
import pandas as pd
from pathlib import Path

st.markdown("## 🐕 Mascotas")
st.caption("Fichas de los pacientes y su propietario.")
st.divider()


# =========================
# RUTAS Y CONSTANTES
# =========================

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

OWNERS_FILE = DATA_DIR / "owners.csv"
PETS_FILE = DATA_DIR / "pets.csv"

PETS_COLUMNS = ["id", "nombre", "tipo", "propietario_id", "propietario_nombre"]


def load_owners() -> pd.DataFrame:
    """Carga los propietarios desde owners.csv."""
    if OWNERS_FILE.exists() and OWNERS_FILE.stat().st_size > 0:
        return pd.read_csv(OWNERS_FILE)
    else:
        return pd.DataFrame(columns=["id", "nombre", "email", "telefono"])


def load_pets() -> pd.DataFrame:
    """Carga las mascotas desde pets.csv o devuelve DF vacío con columnas correctas."""
    if PETS_FILE.exists() and PETS_FILE.stat().st_size > 0:
        df = pd.read_csv(PETS_FILE)
        if list(df.columns) != PETS_COLUMNS:
            df = pd.DataFrame(columns=PETS_COLUMNS)
    else:
        df = pd.DataFrame(columns=PETS_COLUMNS)
    return df


def save_pets(df: pd.DataFrame) -> None:
    """Guarda las mascotas en pets.csv."""
    df.to_csv(PETS_FILE, index=False)


# =========================
# INTERFAZ STREAMLIT
# =========================

st.title("Gestión de Mascotas")

owners_df = load_owners()
pets_df = load_pets()

# Si no hay propietarios, no tiene sentido crear mascotas
if owners_df.empty:
    st.warning("No hay propietarios registrados. Ve primero a **Clientes** y añade alguno.")
else:
    st.subheader("Añadir nueva mascota")

    # Lista de propietarios para el selector
    owner_names = owners_df["nombre"].tolist()

    with st.form("add_pet_form"):
        nombre_mascota = st.text_input("Nombre de la mascota")
        tipo_mascota = st.selectbox(
            "Tipo de mascota",
            ["Perro", "Gato", "Ave", "Reptil", "Roedor", "Otro"],
        )
        propietario_nombre = st.selectbox("Propietario", owner_names)

        submitted = st.form_submit_button("Guardar mascota")

    if submitted:
        if not nombre_mascota.strip():
            st.error("El nombre de la mascota es obligatorio.")
        else:
            # Buscar id del propietario seleccionado
            owner_row = owners_df[owners_df["nombre"] == propietario_nombre].iloc[0]
            propietario_id = int(owner_row["id"])

            # Calcular id nuevo para la mascota
            if pets_df.empty:
                new_id = 1
            else:
                new_id = int(pets_df["id"].max()) + 1

            new_row = {
                "id": new_id,
                "nombre": nombre_mascota.strip(),
                "tipo": tipo_mascota,
                "propietario_id": propietario_id,
                "propietario_nombre": propietario_nombre,
            }

            pets_df = pd.concat(
                [pets_df, pd.DataFrame([new_row])],
                ignore_index=True
            )
            save_pets(pets_df)

            st.success(
                f"Mascota '{nombre_mascota}' registrada para el propietario '{propietario_nombre}'."
            )

# Listado de mascotas
st.subheader("Listado de mascotas")

if pets_df.empty:
    st.info("Todavía no hay mascotas registradas.")
else:
    st.dataframe(pets_df, use_container_width=True)

