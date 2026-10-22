import os
import sys

# Set env vars BEFORE any app import
os.environ.setdefault("SECRET_KEY", "test-secret")

# Add repository root to sys.path so demo_app or app package can be imported
app_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
repo_root = os.path.abspath(os.path.join(app_root, '..'))
for path in (app_root, repo_root):
    if path not in sys.path:
        sys.path.insert(0, path)

import pytest
try:
    from app import create_app
except ImportError:
    from demo_app.app import create_app


@pytest.fixture
def client(tmp_path):
    db_path = str(tmp_path / 'test.db')
    app = create_app(db_path=db_path)
    with app.test_client() as client:
        yield client
