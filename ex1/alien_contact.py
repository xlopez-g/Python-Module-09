#!/usr/bin/env python3

from pydantic import BaseModel, Field, model_validator, ValidationError
from datetime import datetime
from enum import Enum


class ContactType(Enum):
    RADIO = "radio"
    VISUAL = "visual"
    PHYSICAL = "physical"
    TELEPATHIC = "telepathic"


class Alien_Contact(BaseModel):
    contact_id: str = Field(min_length=5, max_length=15)
    timestamp: datetime
    location: str = Field(min_length=3, max_length=100)
    contact_type: ContactType
    signal_strength: float = Field(ge=0.0, le=10.0)
    duration_minutes: int = Field(ge=1, le=1440)
    witness_count: int = Field(ge=1, le=100)
    message_received: str | None = Field(max_length=500)
    is_verified: bool = False

    @model_validator(mode='after')
    def alien_validator(self) -> 'Alien_Contact':
        if not self.contact_id.startswith("AC"):
            raise ValueError('Contact ID must start with "AC" (Alien Contact)')

        if self.contact_type.value == "physical" and self.is_verified is False:
            raise ValueError("Physical contact reports must be veried")

        if self.contact_type.value == "telepathic" and self.witness_count < 3:
            message = "Telepathic contact requires at least 3 witnesses"
            raise ValueError(message)

        if self.signal_strength > 7.0 and self.message_received is None:
            message = "Strong signals (> 7.0) should include received messages"
            raise ValueError(message)

        return (self)


def alien_contact() -> None:
    print("Alien Contact Log Validation")
    print("======================================")
    print("Valid contact report:")
    alien = Alien_Contact(contact_id="AC_2024_001",
                          timestamp=datetime(2022, 2, 2),
                          location="Area 51, Nevada",
                          contact_type=ContactType.RADIO,
                          signal_strength=8.5,
                          duration_minutes=45,
                          witness_count=5,
                          message_received='Greetings from Zeta Reticuli'
                          )

    print("ID:", alien.contact_id)
    print("Type:", alien.contact_type.value)
    print("Location:", alien.location)
    print(f"Signal: {alien.signal_strength}/10")
    print("Duration:", alien.duration_minutes, "minutes")
    print("Witnesses:", alien.witness_count)
    print(f"Message: '{alien.message_received}'")

    print("\n======================================")
    print("Expected validation error:")

    try:
        Alien_Contact(contact_id="AC_2024_001",
                      timestamp=datetime(2022, 2, 2),
                      location="Area 51, Nevada",
                      contact_type=ContactType.TELEPATHIC,
                      signal_strength=8.5,
                      duration_minutes=45,
                      witness_count=2,
                      message_received='Greetings from Zeta '
                      )
    except ValidationError as e:
        print(e.errors()[0]["msg"].replace("Value error, ", ""))

    print()

    try:
        Alien_Contact(contact_id="iAC_2024_001",
                      timestamp=datetime(2022, 2, 2),
                      location="Area 51, Nevada",
                      contact_type=ContactType.TELEPATHIC,
                      signal_strength=8.5,
                      duration_minutes=45,
                      witness_count=6,
                      message_received='Greetings from Zeta '
                      )
    except ValidationError as e:
        print(e.errors()[0]["msg"].replace("Value error, ", ""))

    print()

    try:
        Alien_Contact(contact_id="AC_2024_001",
                      timestamp=datetime(2022, 2, 2),
                      location="Area 51, Nevada",
                      contact_type=ContactType.VISUAL,
                      signal_strength=8.5,
                      duration_minutes=45,
                      witness_count=6,
                      message_received=None
                      )
    except ValidationError as e:
        print(e.errors()[0]["msg"].replace("Value error, ", ""))

    print()
    try:
        Alien_Contact(contact_id="AC_2024_001",
                      timestamp=datetime(2022, 2, 2),
                      location="Area 51, Nevada",
                      contact_type=ContactType.PHYSICAL,
                      signal_strength=8.5,
                      duration_minutes=45,
                      witness_count=2,
                      message_received='Greetings from Zeta ',
                      is_verified=False
                      )
    except ValidationError as e:
        print(e.errors()[0]["msg"].replace("Value error, ", ""))


if __name__ == "__main__":
    alien_contact()
