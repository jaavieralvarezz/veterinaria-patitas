import streamlit as st
import pandas as pd
from pathlib import Path
import altair as alt

st.markdown("## 📊 Analítica")
st.caption("Resumen de la actividad de la clínica.")
st.divider()


# =============================
# RUTAS A LOS DATOS
# =============================

DATA_DIR = Path(__file__).resolve().parents[1] / "data"

OWNERS_FILE = DATA_DIR / "owners.csv"
PETS_FILE = DATA_DIR / "pets.csv"
APPOINTMENTS_FILE = DATA_DIR / "appointments.csv"

st.title("📊 Panel de Analítica de la Clínica Veterinaria")


# =============================
# CARGA DE DATOS
# =============================

def load_csv(path, columns=None):
    if path.exists() and path.stat().st_size > 0:
        df = pd.read_csv(path)
        if columns and list(df.columns) != columns:
            df = pd.DataFrame(columns=columns)
    else:
        df = pd.DataFrame(columns=columns)
    return df

owners_df = load_csv(OWNERS_FILE, ["id", "nombre", "email", "telefono"])
pets_df = load_csv(PETS_FILE, ["id", "nombre", "tipo", "propietario_id", "propietario_nombre"])
appointments_df = load_csv(APPOINTMENTS_FILE, ["id", "fecha", "hora", "mascota", "propietario", "motivo"])


# =============================
# TARJETAS RESUMEN
# =============================

st.subheader("Resumen general")

col1, col2, col3 = st.columns(3)

col1.metric("Clientes registrados", len(owners_df))
col2.metric("Mascotas registradas", len(pets_df))
col3.metric("Citas programadas", len(appointments_df))


# =============================
# GRÁFICO: MASCOTAS POR TIPO
# =============================

st.subheader("🐾 Mascotas por tipo")

if pets_df.empty:
    st.info("No hay mascotas registradas aún.")
else:
    mascotas_por_tipo = pets_df["tipo"].value_counts().reset_index()
    mascotas_por_tipo.columns = ["Tipo", "Cantidad"]

    chart1 = (
        alt.Chart(mascotas_por_tipo)
        .mark_bar(color="#4C9AFF")
        .encode(
            x=alt.X("Tipo:N", title="Tipo de mascota"),
            y=alt.Y("Cantidad:Q", title="Número de mascotas")
        )
        .properties(height=300)
    )

    st.altair_chart(chart1, use_container_width=True)


# =============================
# GRÁFICO: CITAS POR FECHA
# =============================

st.subheader("📅 Citas por fecha")

if appointments_df.empty:
    st.info("No hay citas registradas aún.")
else:
    citas_por_fecha = appointments_df["fecha"].value_counts().sort_index().reset_index()
    citas_por_fecha.columns = ["Fecha", "Cantidad"]

    chart2 = (
        alt.Chart(citas_por_fecha)
        .mark_bar(color="#FF6F61")
        .encode(
            x=alt.X("Fecha:N", title="Fecha"),
            y=alt.Y("Cantidad:Q", title="Número de citas")
        )
        .properties(height=300)
    )

    st.altair_chart(chart2, use_container_width=True)

