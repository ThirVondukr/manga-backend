import hypothesis
from hypothesis.strategies import text


@hypothesis.given(password=text())
def test_can_verify_hashed_password(hash_service, password: str):
    password_hash = hash_service.hash(password)
    assert hash_service.verify(password, password_hash)


@hypothesis.given(password=text(), another_password=text())
def test_cant_verify_another_password(hash_service, password, another_password):
    hypothesis.assume(password != another_password)
    password_hash = hash_service.hash(password)
    assert not hash_service.verify(another_password, password_hash)
