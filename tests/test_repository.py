import pandas as pd

from patitas.database import create_db_engine
from patitas.repository import ClinicRepository


def make_repository():
    engine = create_db_engine("sqlite:///:memory:")
    return ClinicRepository(engine=engine)


def test_add_owner_persists_data():
    repo = make_repository()

    owner_id = repo.add_owner("Ana Perez", "ana@example.com", "600111222")
    owners = repo.list_owners()

    assert owner_id == 1
    assert len(owners) == 1
    assert owners.iloc[0]["nombre"] == "Ana Perez"
    assert owners.iloc[0]["email"] == "ana@example.com"


def test_add_pet_links_pet_with_owner_name():
    repo = make_repository()
    owner_id = repo.add_owner("Luis Garcia", "luis@example.com", "600333444")

    pet_id = repo.add_pet("Nala", "Gato", owner_id)
    pets = repo.list_pets()

    assert pet_id == 1
    assert pets.iloc[0]["nombre"] == "Nala"
    assert pets.iloc[0]["propietario_id"] == owner_id
    assert pets.iloc[0]["propietario_nombre"] == "Luis Garcia"


def test_add_appointment_persists_data():
    repo = make_repository()

    appointment_id = repo.add_appointment(
        fecha="2026-07-03",
        hora="10:30:00",
        mascota="Nala",
        propietario="Luis Garcia",
        motivo="Revision general",
    )
    appointments = repo.list_appointments()

    assert appointment_id == 1
    assert len(appointments) == 1
    assert appointments.iloc[0]["motivo"] == "Revision general"


def test_seed_from_csv_imports_existing_files(tmp_path):
    repo = make_repository()
    pd.DataFrame(
        [{"id": 1, "nombre": "Ana", "email": "ana@example.com", "telefono": "600"}]
    ).to_csv(tmp_path / "owners.csv", index=False)
    pd.DataFrame(
        [
            {
                "id": 1,
                "nombre": "Nala",
                "tipo": "Gato",
                "propietario_id": 1,
                "propietario_nombre": "Ana",
            }
        ]
    ).to_csv(tmp_path / "pets.csv", index=False)
    pd.DataFrame(
        [
            {
                "id": 1,
                "fecha": "2026-07-03",
                "hora": "10:30:00",
                "mascota": "Nala",
                "propietario": "Ana",
                "motivo": "Revision",
            }
        ]
    ).to_csv(tmp_path / "appointments.csv", index=False)

    repo.seed_from_csv_if_empty(tmp_path)

    assert len(repo.list_owners()) == 1
    assert len(repo.list_pets()) == 1
    assert len(repo.list_appointments()) == 1

