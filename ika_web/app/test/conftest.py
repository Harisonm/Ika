# import pytest
# import os

# def pytest_addoption(parser):
#     # ability to test API on different hosts
#     parser.addoption("--host", action="store", default="http://localhost:8040")

# @pytest.fixture(scope="session")
# def host(request):
#     return request.config.getoption("--host")

# @pytest.fixture(scope="session")
# def api_v1_host(host):
#     return os.path.join(host, "api", "v1")