import pytest

from modules.auth.services import HashingService


@pytest.fixture(scope="module")
def hash_service() -> HashingService:
    return HashingService()
