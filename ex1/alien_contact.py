#!/usr/bin/env python3

from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum

class ContactType(Enum):
    RADIO = "radio"
    VISUAL = "visual"
    PHYSICAL = "physical"
    TELEPATHIC = "telepathic"


class Spacetion(BaseModel):
    contact_id: str = Field(min_length=5, max_length=15)
    timestamp: datetime
    location: str = Field(min_length=3, max_length=100)
    contact_type: ContactType
    signal_strength: float = Field(ge=0.0, le=10.0)
    duration_minutes: int = Field(ge=1, le=1440)
    witness_count: int = Field(ge=1, le=100)
    message_received: str | None = Field(max_length=500)
    is_verified: bool = False

#    @model_validator(mode=’after’)
#    def checking(cls, self):
#        if self.contact_id == "AC"


def alien_contact() -> None:
    print("Alien Contact Log Validation")
    print("======================================")
    print("Valid contact report:")
    allien = Spacetion(contact_id = "AC_2024_001",
                       timestamp=datetime(2022, 2, 2),
                       location = "Area 51, Nevada",
                       contact_type= ContactType.RADIO,
                       signal_strength= 8.5,
                       duration_minutes = 45,
                       witness_count = 5,
                       message_received = 'Greetings from Zeta Reticuli'
                       )

    print("ID:", allien.contact_id)
    print("Type:", allien.contact_type.value)
    print("Location:", allien.location)
    print(f"Signal: {allien.signal_strength}/10")
    print("Duration:", allien.duration_minutes, "minutes")
    print("Witnesses:", allien.witness_count)
    print(f"Message: '{allien.message_received}'")

    print("\n======================================")
    print("Expected validation error:")


if __name__ == "__main__":
    alien_contact()
