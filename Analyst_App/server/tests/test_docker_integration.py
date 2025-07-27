import pytest
import httpx
import time
from pytest_docker.plugin import docker_ip

@pytest.fixture(scope="session")
def docker_compose_file(pytestconfig):
    return pytestconfig.rootpath.parent / "docker-compose.yml"

@pytest.fixture(scope="session")
def docker_compose_project_name(pytestconfig):
    return "analystapp_test"

@pytest.fixture(scope="session")
def server_url(docker_ip, docker_services):
    port = docker_services.port_for("server", 8000)
    url = f"http://{docker_ip}:{port}"
    
    return url

def test_server_is_running(server_url):
    response = httpx.get(f"{server_url}/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}

def test_ping_coingecko_endpoint(server_url):
    response = httpx.get(f"{server_url}/ping")
    assert response.status_code == 200
    assert "gecko_says" in response.json()