#!/usr/bin/env python3

from pydantic import BaseModel, Field, ValidationError
from datetime import datetime


class Space_Station(BaseModel):
    station_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=1, max_length=50)
    crew_size: int = Field(ge=1, le=20)
    power_level: float = Field(ge=0.0, le=100.0)
    oxygen_level: float = Field(ge=10.0, le=100.0)
    last_maintenance: datetime
    is_operational: bool = True
    notes: str | None = Field(max_length=200)


def space_station() -> None:

    print("Space Station Data Validation")
    print("========================================")

    starstation = Space_Station(station_id="ISS001",
                                name="International Space Station",
                                crew_size=6,
                                power_level=85.5,
                                oxygen_level=92.3,
                                last_maintenance=datetime(2026, 1, 1),
                                is_operational=True,
                                notes=None)

    print("Valid station created:")

    print("ID:", starstation.station_id)
    print("Name:", starstation.name)
    print("Crew:", starstation.crew_size, "people")
    print(f"Power: {starstation.power_level}%")
    print(f"Oxygen: {starstation.oxygen_level}%")
    if starstation.is_operational:
        print("Status: Operational")
    else:
        print("Status: Not Operational")

    print()
    print("========================================")

    print("Expected validation error:")
    try:
        Space_Station(station_id="ISS001",
                      name="International Space Station",
                      crew_size=25,
                      power_level=85.5,
                      oxygen_level=92.3,
                      last_maintenance=datetime(2026, 1, 1),
                      is_operational=True,
                      notes=None)
    except ValidationError as e:
        print(e.errors()[0]['msg'])


if __name__ == "__main__":
    space_station()
