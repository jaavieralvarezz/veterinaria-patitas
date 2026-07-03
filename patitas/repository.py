from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Optional

import pandas as pd
from sqlalchemy import func, insert, select
from sqlalchemy.engine import Engine

from patitas.database import (
    DATA_DIR,
    appointments,
    create_db_engine,
    init_db,
    owners,
    pets,
)


OWNERS_COLUMNS = ["id", "nombre", "email", "telefono"]
PETS_COLUMNS = ["id", "nombre", "tipo", "propietario_id", "propietario_nombre"]
APPOINTMENTS_COLUMNS = ["id", "fecha", "hora", "mascota", "propietario", "motivo"]


class ClinicRepository:
    def __init__(self, engine: Optional[Engine] = None, seed_from_csv: bool = False):
        self.engine = engine or create_db_engine()
        init_db(self.engine)
        if seed_from_csv:
            self.seed_from_csv_if_empty(DATA_DIR)

    def _to_dataframe(self, rows: list[dict], columns: list[str]) -> pd.DataFrame:
        return pd.DataFrame(rows, columns=columns)

    def _table_is_empty(self, table) -> bool:
        with self.engine.connect() as conn:
            count = conn.execute(select(func.count()).select_from(table)).scalar_one()
        return count == 0

    def list_owners(self) -> pd.DataFrame:
        with self.engine.connect() as conn:
            rows = conn.execute(select(owners).order_by(owners.c.id)).mappings().all()
        return self._to_dataframe([dict(row) for row in rows], OWNERS_COLUMNS)

    def add_owner(self, nombre: str, email: str = "", telefono: str = "") -> int:
        nombre = nombre.strip()
        if not nombre:
            raise ValueError("El nombre es obligatorio.")

        with self.engine.begin() as conn:
            result = conn.execute(
                insert(owners).values(
                    nombre=nombre,
                    email=email.strip(),
                    telefono=telefono.strip(),
                )
            )
            return int(result.inserted_primary_key[0])

    def list_pets(self) -> pd.DataFrame:
        with self.engine.connect() as conn:
            rows = conn.execute(select(pets).order_by(pets.c.id)).mappings().all()
        return self._to_dataframe([dict(row) for row in rows], PETS_COLUMNS)

    def add_pet(self, nombre: str, tipo: str, propietario_id: int) -> int:
        nombre = nombre.strip()
        if not nombre:
            raise ValueError("El nombre de la mascota es obligatorio.")

        with self.engine.begin() as conn:
            owner_row = conn.execute(
                select(owners).where(owners.c.id == propietario_id)
            ).mappings().first()

            if owner_row is None:
                raise ValueError("El propietario seleccionado no existe.")

            result = conn.execute(
                insert(pets).values(
                    nombre=nombre,
                    tipo=tipo,
                    propietario_id=propietario_id,
                    propietario_nombre=owner_row["nombre"],
                )
            )
            return int(result.inserted_primary_key[0])

    def list_appointments(self) -> pd.DataFrame:
        with self.engine.connect() as conn:
            rows = (
                conn.execute(select(appointments).order_by(appointments.c.id))
                .mappings()
                .all()
            )
        return self._to_dataframe([dict(row) for row in rows], APPOINTMENTS_COLUMNS)

    def add_appointment(
        self,
        fecha: str,
        hora: str,
        mascota: str,
        propietario: str,
        motivo: str,
    ) -> int:
        motivo = motivo.strip()
        if not motivo:
            raise ValueError("El motivo de la cita es obligatorio.")

        with self.engine.begin() as conn:
            result = conn.execute(
                insert(appointments).values(
                    fecha=str(fecha),
                    hora=str(hora),
                    mascota=mascota,
                    propietario=propietario,
                    motivo=motivo,
                )
            )
            return int(result.inserted_primary_key[0])

    def seed_from_csv_if_empty(self, data_dir: Path) -> None:
        if self._table_is_empty(owners):
            self._seed_table_from_csv(data_dir / "owners.csv", owners, OWNERS_COLUMNS)
        if self._table_is_empty(pets):
            self._seed_table_from_csv(data_dir / "pets.csv", pets, PETS_COLUMNS)
        if self._table_is_empty(appointments):
            self._seed_table_from_csv(
                data_dir / "appointments.csv",
                appointments,
                APPOINTMENTS_COLUMNS,
            )

    def _seed_table_from_csv(self, csv_path: Path, table, columns: list[str]) -> None:
        if not csv_path.exists() or csv_path.stat().st_size == 0:
            return

        df = pd.read_csv(csv_path)
        if list(df.columns) != columns or df.empty:
            return

        records = df.where(pd.notna(df), "").to_dict(orient="records")
        with self.engine.begin() as conn:
            conn.execute(insert(table), records)


@lru_cache(maxsize=1)
def get_repository() -> ClinicRepository:
    return ClinicRepository(seed_from_csv=True)

