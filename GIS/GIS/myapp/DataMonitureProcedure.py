from django.db import connection
import logging
import time

logger = logging.getLogger(__name__)


def execute_stored_procedure_continuously():
    """Runs the stored procedure in a loop every second."""
    while True:
        try:
            with connection.cursor() as cursor:
                cursor.execute("EXEC dbo.DataMonitorTable")
            logger.info("Stored procedure executed successfully.")
        except Exception as e:
            logger.error(f"Error executing stored procedure: {e}")

        time.sleep(1)

