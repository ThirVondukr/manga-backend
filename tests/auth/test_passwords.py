import hypothesis
from hypothesis.strategies import text


@hypothesis.given(password=text())
def test_can_verify_hashed_password(hash_service, get_user, password):
    with get_user() as user:
        hash_service.update_user_password(user, password)
        assert hash_service.verify_user_password(user, password)


@hypothesis.given(password=text(), another_password=text())
def test_cant_verify_another_password(hash_service, get_user, password: str, another_password: str):
    hypothesis.assume(password != another_password)

    with get_user() as user:
        hash_service.update_user_password(user, password)
        assert not hash_service.verify_user_password(user, another_password)
