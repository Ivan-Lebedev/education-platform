from dataclasses import dataclass


@dataclass(slots=True)
class AuthToken:
    "DTO результата логина."

    access_token: str
    token_type: str = 'bearer'
