import pytest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from unittest.mock import MagicMock, patch
from src.services.product_service import ProductService
from src.database.postgres import PostgresDB


@pytest.fixture
def product_service():
    return ProductService()


def test_add_product_rollback_on_failure(product_service):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    # Configure the mock connection to return the mock cursor
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

    mock_cursor.execute.side_effect = Exception("Database error")

    # Patch PostgresDB.get_connection to return our mock connection
    # Also patch return_connection to avoid PoolError with mock connection
    with patch.object(
        PostgresDB, "get_connection", return_value=mock_conn
    ), patch.object(PostgresDB, "return_connection") as mock_return_conn:
        # Expect the exception to be raised
        with pytest.raises(Exception) as excinfo:
            product_service.add_product(
                name="Test Product",
                category="Test Category",
                price=100.0,
                stock=10,
                metadata={"key": "value"},
            )

        # Verify the exception message
        assert "Database error" in str(excinfo.value)

        # Verify rollback was called
        mock_conn.rollback.assert_called_once()

        # Verify return_connection was called with the mock connection
        mock_return_conn.assert_called_once_with(mock_conn)
