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