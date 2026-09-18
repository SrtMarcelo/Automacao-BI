import pytest
import app

@pytest.fixture(autouse=True)
def disable_rate_limiting_for_tests():
    app.app.config.update(
        TESTING=True,
        RATELIMIT_ENABLED=False,
    )
    yield