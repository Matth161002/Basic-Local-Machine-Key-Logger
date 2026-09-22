import unittest

from credential_detection import CredentialDetector, LoginCandidate


class CredentialDetectorTests(unittest.TestCase):
    """Test simple username and password detection rules."""

    def setUp(self):
        self.detector = CredentialDetector()

    def test_detects_email_and_password(self):
        results = self.detector.find_logins(
            "matt@example.com password!"
        )

        self.assertEqual(
            results,
            [
                LoginCandidate(
                    username="matt@example.com",
                    password="password!"
                )
            ]
        )

    def test_detects_login_split_across_lines(self):
        results = self.detector.find_logins(
            "matt@example.com\nP@ssword123!"
        )

        self.assertEqual(
            results,
            [
                LoginCandidate(
                    username="matt@example.com",
                    password="P@ssword123!"
                )
            ]
        )

    def test_ignores_username_without_password(self):
        results = self.detector.find_logins(
            "matt@example.com"
        )

        self.assertEqual(
            results,
            []
        )

    def test_ignores_short_password_like_values(self):
        results = self.detector.find_logins(
            "matt@example.com abc!"
        )

        self.assertEqual(
            results,
            []
        )

    def test_deduplicates_repeated_login(self):
        results = self.detector.find_logins(
            "matt@example.com password! "
            "matt@example.com password!"
        )

        self.assertEqual(
            results,
            [
                LoginCandidate(
                    username="matt@example.com",
                    password="password!"
                )
            ]
        )


if __name__ == "__main__":
    unittest.main()
