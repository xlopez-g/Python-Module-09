#!/usr/bin/env python3

from pydantic import BaseModel, Field, model_validator, ValidationError
from datetime import datetime
from enum import Enum


class RANK(Enum):
    CADET = "cadet"
    OFFICER = "officer"
    LIEUTNANT = "lieutnant"
    CAPTAIN = "captain"
    COMMANDER = "commander"


class CrewMember(BaseModel):
    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: RANK
    age: int = Field(ge=18, le=80)
    specialization: str = Field(min_length=3, max_length=30)
    years_experience: int = Field(ge=0, le=50)
    is_active: bool = True


class SpaceMission(BaseModel):
    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=100)
    destination: str = Field(min_length=3, max_length=50)
    launch_date: datetime
    duration_days: int = Field(ge=1, le=3650)
    crew: list[CrewMember]
    mission_status: str = "planned"
    budget_millions: float = Field(ge=1.0, le=10000.0)

    @model_validator(mode='after')
    def mission_validator(self) -> 'SpaceMission':
        if not self.mission_id.startswith("M"):
            raise ValueError('Mission ID must start with "M"')

        member_list = self.crew
        is_valid = False
        for member in member_list:
            rank_val = member.rank.value
            if rank_val == "commander" or rank_val == "captain":
                is_valid = True
        if is_valid is False:
            raise ValueError("Mission must have at least one"
                             " Commander or Captain")

        experienced_crew = 0
        for member in self.crew:
            if member.years_experience >= 5:
                experienced_crew += 1
        average_experience: float = experienced_crew / len(self.crew)
        if self.duration_days > 365 and average_experience < 0.5:

            raise ValueError("Long missions (> 365 days) need "
                             r"50% experienced crew (5+ years)")

        all_active = True
        for member in self.crew:
            if member.is_active is False:
                all_active = False
        if all_active is False:
            raise ValueError("All crew members must be active")

        return (self)


def mission_ft() -> None:

    member01 = CrewMember(member_id="comman01",
                          name="Sarah Connor",
                          rank=RANK.COMMANDER,
                          age=45,
                          specialization="Mission Command",
                          years_experience=20)

    member02 = CrewMember(member_id="lieut040",
                          name="John Smith",
                          rank=RANK.LIEUTNANT,
                          age=65,
                          specialization="Navigation",
                          years_experience=10)

    member03 = CrewMember(member_id="officer09",
                          name="Alice Johnson",
                          rank=RANK.OFFICER,
                          age=25,
                          specialization="Engineering",
                          years_experience=4)

    member04 = CrewMember(member_id="cadet09",
                          name="Alice Johnson",
                          rank=RANK.CADET,
                          age=25,
                          specialization="Engineering",
                          years_experience=4)

    member05 = CrewMember(member_id="cadet05",
                          name="Alice Johnson",
                          rank=RANK.CADET,
                          age=25,
                          specialization="Engineering",
                          years_experience=24,
                          is_active=False
                          )

    print("Space Mission Crew Validation")
    print("======================================")
    print("Valid mission created:")
    mission = SpaceMission(mission_id="M2024_MARS",
                           mission_name="Mars Colony Establishment",
                           destination="Mars",
                           launch_date=datetime(2026, 1, 1),
                           duration_days=900,
                           budget_millions=2500.0,
                           crew=[member01, member02, member03]
                           )

    print("Mission:", mission.mission_name)
    print("ID:", mission.mission_id)
    print("Destination:", mission.destination)
    print("Duration:", mission.duration_days, "days")
    print(f"Budget: ${mission.budget_millions}M")
    print("Crew size:", len(mission.crew))
    print("Crew members:")
    for member in mission.crew:
        rank_value = member.rank.value
        print(f"- {member.name} ({rank_value}) - {member.specialization}")

    print("\n======================================")
    print("Expected validation error:")

    try:
        SpaceMission(mission_id="0M2024_MARS",
                     mission_name="Mars Colony Establishmen",
                     destination="Mars",
                     launch_date=datetime(2026, 1, 1),
                     duration_days=900,
                     budget_millions=2500.0,
                     crew=[member01, member02, member03]
                     )
    except ValidationError as e:
        print(e.errors()[0]["msg"].replace("Value error, ", ""))

    print()

    try:
        SpaceMission(mission_id="M2024_MARS",
                     mission_name="Mars Colony Establishmen",
                     destination="Mars",
                     launch_date=datetime(2026, 1, 1),
                     duration_days=900,
                     budget_millions=2500.0,
                     crew=[member02, member03]
                     )
    except ValidationError as e:
        print(e.errors()[0]["msg"].replace("Value error, ", ""))

    print()

    try:
        SpaceMission(mission_id="M2024_MARS",
                     mission_name="Mars Colony Establishmen",
                     destination="Mars",
                     launch_date=datetime(2026, 1, 1),
                     duration_days=900,
                     budget_millions=2500.0,
                     crew=[member04, member01, member03]
                     )
    except ValidationError as e:
        print(e.errors()[0]["msg"].replace("Value error, ", ""))

    print()

    try:
        SpaceMission(mission_id="M2024_MARS",
                     mission_name="Mars Colony Establishmen",
                     destination="Mars",
                     launch_date=datetime(2026, 1, 1),
                     duration_days=900,
                     budget_millions=2500.0,
                     crew=[member01, member04, member05, member03]
                     )
    except ValidationError as e:
        print(e.errors()[0]["msg"].replace("Value error, ", ""))


if __name__ == "__main__":
    mission_ft()
