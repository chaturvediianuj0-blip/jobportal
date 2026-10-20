import pytest
from unittest.mock import patch, MagicMock
from app import app
import auth
import categories

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_app_module_exists():
    """Verify app.py can be imported"""
    import app
    assert app is not None

def test_homepage_returns_dict():
    """Verify homepage returns correct structure"""
    from homepage import get_homepage
    result = get_homepage()
    assert isinstance(result, dict)
    assert "message" in result
    assert "jobs" in result

def test_list_jobs_returns_list():
    """Verify list_jobs returns a list"""
    from jobs import list_jobs
    result = list_jobs()
    assert isinstance(result, list)

def test_search_jobs_returns_list():
    """Verify search_jobs returns a list"""
    from jobs import search_jobs
    result = search_jobs("engineer")
    assert isinstance(result, list)

def test_format_job_title():
    from utils import format_job_title
    assert format_job_title('  software engineer  ') == 'Software Engineer'

# Flask route integration tests
def test_homepage_route(client):
    response = client.get('/')
    assert response.status_code == 200

def test_jobs_route(client):
    response = client.get('/jobs')
    assert response.status_code == 200

def test_search_jobs_route(client):
    response = client.get('/jobs/search/engineer')
    assert response.status_code == 200

def test_health_route(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json['status'] == 'ok'

# Database check (/db-check) unit tests
@patch('psycopg2.connect')
def test_db_check_success(mock_connect, client):
    mock_conn = MagicMock()
    mock_connect.return_value = mock_conn

    response = client.get('/db-check')
    assert response.status_code == 200
    assert response.json['db'] == 'connected'
    mock_conn.close.assert_called_once()

@patch('psycopg2.connect')
def test_db_check_failure(mock_connect, client):
    mock_connect.side_effect = Exception("Connection refused")

    response = client.get('/db-check')
    assert response.status_code == 500
    assert response.json['db'] == 'error'
    assert 'Connection refused' in response.json['message']

# Cache check (/cache-check) unit tests
@patch('redis.Redis')
def test_cache_check_success(mock_redis, client):
    mock_instance = MagicMock()
    mock_instance.get.return_value = 'ok'
    mock_redis.return_value = mock_instance

    response = client.get('/cache-check')
    assert response.status_code == 200
    assert response.json['redis'] == 'connected'
    assert response.json['test_value'] == 'ok'
    mock_instance.set.assert_called_once_with('health_check', 'ok', ex=60)

@patch('redis.Redis')
def test_cache_check_failure(mock_redis, client):
    mock_redis.side_effect = Exception("Redis unreachable")

    response = client.get('/cache-check')
    assert response.status_code == 500
    assert response.json['redis'] == 'error'
    assert 'Redis unreachable' in response.json['message']

# Module import checks for coverage
def test_auth_and_categories_import():
    assert auth is not None
    assert categories is not None