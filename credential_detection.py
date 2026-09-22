import re

from dataclasses import dataclass


EMAIL_PATTERN = re.compile(
    r"^[^\s@]+@[^\s@]+\.[^\s@]+$"
)

USERNAME_PATTERN = re.compile(
    r"^[A-Za-z0-9][A-Za-z0-9._-]{2,31}$"
)


@dataclass(frozen=True)
class LoginCandidate:
    """Represent a suspected username and password pair."""

    username: str
    password: str


class CredentialDetector:
    """Identify simple username and password-like input patterns."""

    @staticmethod
    def is_username(value):
        """Determine whether a value resembles a username."""
        if not value or any(character.isspace() for character in value):
            return False

        return bool(
            EMAIL_PATTERN.fullmatch(value)
            or USERNAME_PATTERN.fullmatch(value)
        )

    @staticmethod
    def is_password(value):
        """Determine whether a value resembles a password."""
        if not value or len(value) < 6:
            return False

        if EMAIL_PATTERN.fullmatch(value):
            return False

        has_letter = any(character.isalpha() for character in value)
        has_non_letter = any(
            not character.isalpha()
            for character in value
        )

        return has_letter and has_non_letter

    @staticmethod
    def _split_input(text):
        """Split captured input into individual entries for analysis."""
        return [
            entry
            for entry in re.split(r"[\s]+", text)
            if entry
        ]

    def find_logins(self, text):
        """Find adjacent username and password-like values."""
        entries = self._split_input(text)
        candidates = []

        for index in range(len(entries) - 1):
            username = entries[index]
            password = entries[index + 1]

            if not self.is_username(username):
                continue

            if not self.is_password(password):
                continue

            candidate = LoginCandidate(
                username=username,
                password=password
            )

            if candidate not in candidates:
                candidates.append(candidate)

        return candidates
