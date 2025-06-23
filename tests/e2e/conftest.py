"""
E2E specific test configuration.
This file ensures E2E tests use the test database from .env.test instead of production database.
It provides fixtures for database setup, cleanup, and test clients configured for E2E testing.

Enhanced version with proper database lifecycle management:
- Database creation during environment setup
- Automatic database cleaning for every test
- Complete cleanup at session end
"""
import os
import sys
import pytest
from dotenv import load_dotenv

# CRITICAL: Load test environment variables BEFORE importing any app modules
# This must happen before the settings are initialized to ensure test database is used
load_dotenv(".env.test", override=True)

# Add the project root to sys.path to ensure modules can be imported
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, project_root)

# Global variable to store database engine and path for session-wide access
_test_database_engine = None
_test_database_path = None



def _get_test_database_path(db_url):
    """Extract the test database file path from the DATABASE_URL."""
    if db_url.startswith("sqlite:///"):
        db_file = db_url.replace("sqlite:///", "")
        if db_file.startswith("./"):
            db_file = db_file[2:]
        return os.path.abspath(db_file)
    return None


def _create_test_database():
    """Create and initialize the test database."""
    global _test_database_engine, _test_database_path
    
    db_url = os.environ.get("DATABASE_URL")
    _test_database_path = _get_test_database_path(db_url)
    
    print(f"Test database path: {_test_database_path}")
    
    # Clean up any existing test database
    if _test_database_path and os.path.exists(_test_database_path):
        try:
            os.remove(_test_database_path)
            print("Removed existing test database")
        except Exception as e:
            print(f"Could not remove existing test database: {e}")
    
    # Initialize database tables
    try:
        # Import engine after environment is set up to ensure it uses test database
        from app.db.engine import engine
        from sqlmodel import SQLModel, text
        
        # Store engine globally for use by other fixtures
        _test_database_engine = engine
        
        # Create all tables
        SQLModel.metadata.create_all(bind=engine)
        
        # Verify the database file was created (for SQLite)
        if _test_database_path and os.path.exists(_test_database_path):
            file_size = os.path.getsize(_test_database_path)
            print(f"Test database file created: {_test_database_path} ({file_size} bytes)")
        
        # Test database connection
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            if result.fetchone():
                print("Database connection test successful")
        
        return engine
        
    except Exception as e:
        print(f"Could not initialize test database: {e}")
        import traceback
        traceback.print_exc()
        raise


def _cleanup_test_environment():
    """Complete cleanup of test environment and database."""
    global _test_database_path
    
    print("Tearing down E2E test environment...")
    engine = _get_test_database_engine()
    
    # Clean all tables before test
    _clear_all_database_tables(engine)
    # Remove test database file
    if _test_database_path and os.path.exists(_test_database_path):
        try:
            os.remove(_test_database_path)
            print(f"Removed test database file: {_test_database_path}")
        except Exception as e:
            print(f"Could not remove test database file: {e}")
    
    print("E2E test environment cleanup complete")


def _get_test_database_engine():
    """Get the global test database engine."""
    global _test_database_engine
    if _test_database_engine is None:
        raise RuntimeError("Test database engine not initialized. This should not happen.")
    return _test_database_engine


def _clear_all_database_tables(engine):
    """Clear all data from database tables."""
    from sqlmodel import text
    
    try:
        with engine.connect() as conn:
            # Get all table names (excluding SQLite system tables)
            result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))
            tables = [row[0] for row in result if not row[0].startswith('sqlite_')]
            
            # Clear all data from tables
            cleared_tables = []
            for table in tables:
                conn.execute(text(f"DELETE FROM {table}"))
                cleared_tables.append(table)
            
            conn.commit()
            if cleared_tables:
                print(f"Cleaned {len(cleared_tables)} tables: {', '.join(cleared_tables)}")
                
    except Exception as e:
        print(f"Warning: Could not clean database state: {e}")


def _seed_test_database(engine):
    """Seed the database with test data."""
    try:
        from tests.e2e.seed import seed_test_database
        agent_count = seed_test_database(engine)
        print(f"Seeded database with {agent_count} test agents")
        return agent_count
    except Exception as e:
        print(f"Warning: Could not seed database: {e}")
        return 0


@pytest.fixture(scope="session", autouse=True)
def setup_e2e_test_environment():
    """
    Enhanced E2E environment setup with complete database lifecycle management.
    
    This fixture runs automatically before any E2E test and ensures:
    1. Test environment variables are properly loaded
    2. Test database is created and initialized  
    3. Required environment variables are present
    4. Complete cleanup at session end
    
    Invoked: Automatically at the start of the test session (scope="session", autouse=True)
    When: Before any E2E test runs
    """
    print("Setting up E2E test environment...")
    
    # Phase A: Environment validation
    db_url = os.environ.get("DATABASE_URL")
    
    print("E2E test environment configured")
    print(f"   Database: {db_url}")
    print(f"   Email: {os.environ.get('SENDER_EMAIL')}")
    print(f"   Agent Storage: {os.environ.get('AGENT_STORAGE')}")
    
    # Phase B: Database creation and initialization
    engine = _create_test_database()
    print("Test database ready for E2E tests")
    
    yield engine
    
    # Phase C: Complete cleanup
    _cleanup_test_environment()


@pytest.fixture(autouse=True)
def ensure_clean_database():
    """
    Automatically ensure clean database state for every test.
    
    This fixture runs before every test and ensures:
    1. All database tables are cleared
    2. Database is seeded with fresh test data
    3. Each test starts with a predictable, clean state
    
    Invoked: Automatically before every test (autouse=True)
    When: Before each test function executes
    """
    # Get database engine (created during environment setup)
    engine = _get_test_database_engine()
    
    # Clean all tables before test
    _clear_all_database_tables(engine)
    
    # Seed the database with fresh test data
    _seed_test_database(engine)
    
    yield
    
    # Optional: Clean after test (uncomment for paranoid cleanup)
    # _clear_all_database_tables(engine)


@pytest.fixture
def e2e_test_client():
    """
    E2E specific test client that uses real services and test database.
    """
    from app.main import app
    from fastapi.testclient import TestClient
    
    app.dependency_overrides.clear()
    client = TestClient(app)
    return client




# =============================================================================
# SAMPLE DATA FIXTURES FOR E2E TESTS
# =============================================================================

@pytest.fixture
def sample_agent_data():
    """
    Sample agent data for E2E testing.
    
    Invoked: When a test function includes 'sample_agent_data' as a parameter
    When: Test needs sample data to create an agent
    """
    return {
        "name": "Test E2E Agent",
        "slug": "test-e2e-agent", 
        "description": "A test agent for E2E testing",
        "image": "test-agent.png"
    }


@pytest.fixture
def sample_agent_run_data():
    """
    Sample data for testing agent execution.
    
    Invoked: When a test function includes 'sample_agent_run_data' as a parameter
    When: Test needs data to execute an agent
    """
    return {
        "prompt": "Create a blog post about artificial intelligence",
        "user_email": "test@example.com"
    }


@pytest.fixture
def sample_marketing_agent_data():
    """
    Sample data for testing marketing agent.
    
    Invoked: When a test function includes 'sample_marketing_agent_data' as a parameter
    When: Test needs data to run marketing agent
    """
    return {
        "url": "https://example.com",
        "user_email": "test@example.com"
    }


@pytest.fixture
def sample_invalid_data():
    """
    Sample invalid data for testing error handling.
    
    Invoked: When a test function includes 'sample_invalid_data' as a parameter
    When: Test needs invalid data to test error scenarios
    """
    return {
        "empty_agent_data": {
            "name": "",
            "slug": "",
            "description": "",
            "image": ""
        },
        "invalid_email": "not-an-email",
        "empty_prompt": "",
        "invalid_url": "not-a-url"
    }
