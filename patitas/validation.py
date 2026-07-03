from datetime import date, time


OPEN_TIME = time(9, 0)
CLOSE_TIME = time(21, 0)


def is_open_day(appointment_date: date) -> bool:
    return appointment_date.weekday() != 6


def is_open_time(appointment_time: time) -> bool:
    return OPEN_TIME <= appointment_time <= CLOSE_TIME


def validate_appointment(appointment_date: date, appointment_time: time, motivo: str) -> None:
    if not motivo.strip():
        raise ValueError("El motivo de la cita es obligatorio.")
    if not is_open_day(appointment_date):
        raise ValueError("Solo se pueden reservar citas de lunes a sábado (no domingos).")
    if not is_open_time(appointment_time):
        raise ValueError("El horario de la clínica es de 09:00 a 21:00.")

