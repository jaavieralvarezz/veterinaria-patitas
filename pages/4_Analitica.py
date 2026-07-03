import streamlit as st
import altair as alt

from patitas.repository import get_repository

st.markdown("## 📊 Analítica")
st.caption("Resumen de la actividad de la clínica.")
st.divider()

st.title("📊 Panel de Analítica de la Clínica Veterinaria")

repo = get_repository()
owners_df = repo.list_owners()
pets_df = repo.list_pets()
appointments_df = repo.list_appointments()


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

    st.altair_chart(chart1, width="stretch")


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

    st.altair_chart(chart2, width="stretch")
