from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
    create_engine,
)
from sqlalchemy.engine import Engine
from sqlalchemy.pool import StaticPool


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
DEFAULT_SQLITE_PATH = DATA_DIR / "vet_clinic.db"

metadata = MetaData()

owners = Table(
    "owners",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("nombre", String(120), nullable=False),
    Column("email", String(160), nullable=True),
    Column("telefono", String(40), nullable=True),
)

pets = Table(
    "pets",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("nombre", String(120), nullable=False),
    Column("tipo", String(60), nullable=False),
    Column("propietario_id", Integer, ForeignKey("owners.id"), nullable=False),
    Column("propietario_nombre", String(120), nullable=False),
)

appointments = Table(
    "appointments",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("fecha", String(20), nullable=False),
    Column("hora", String(20), nullable=False),
    Column("mascota", String(120), nullable=False),
    Column("propietario", String(120), nullable=False),
    Column("motivo", String(250), nullable=False),
)


def _read_streamlit_secret(name: str) -> Optional[str]:
    try:
        import streamlit as st

        value = st.secrets.get(name)
        return str(value) if value else None
    except Exception:
        return None


def get_database_url() -> str:
    database_url = os.getenv("DATABASE_URL") or _read_streamlit_secret("DATABASE_URL")

    if not database_url:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        return f"sqlite:///{DEFAULT_SQLITE_PATH}"

    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql+psycopg://", 1)
    elif database_url.startswith("postgresql://"):
        database_url = database_url.replace("postgresql://", "postgresql+psycopg://", 1)

    return database_url


def create_db_engine(database_url: Optional[str] = None) -> Engine:
    url = database_url or get_database_url()

    if url == "sqlite:///:memory:":
        return create_engine(
            url,
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
            future=True,
        )

    return create_engine(url, future=True)


def init_db(engine: Engine) -> None:
    metadata.create_all(engine)


def database_mode(database_url: Optional[str] = None) -> str:
    url = database_url or get_database_url()
    if url.startswith("sqlite"):
        return "SQLite local"
    if url.startswith("postgresql"):
        return "PostgreSQL en la nube"
    return "Base de datos configurada"

