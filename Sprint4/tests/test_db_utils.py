import sqlite3

import pytest

from Sprint4.utils import get_db_connection, initialize_user_db


@pytest.fixture
def setup_db():
    # Initialize the test database before each test
    db_name = 'test_users.db'
    initialize_user_db()

    yield db_name  # This will return the database name to the test functions

    # Cleanup after each test
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    # Clean up after test
    cursor.execute('DROP TABLE IF EXISTS user_information')
    conn.commit()
    conn.close()


def test_get_db_connection(setup_db):
    # Test that a connection can be made to the database
    db_name = setup_db
    conn = get_db_connection(db_name)
    assert isinstance(conn, sqlite3.Connection)
    conn.close()
