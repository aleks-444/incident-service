import os
import subprocess
import sys
from app.database import AsyncSessionLocal
from app.repository import IncidentRepository


async def run_alembic_migrations():
    try:
        result = subprocess.run([
            sys.executable, "-m", "alembic", "current"
        ], capture_output=True, text=True, cwd=os.path.dirname(os.path.dirname(__file__)))

        result = subprocess.run([
            sys.executable, "-m", "alembic", "revision", "--autogenerate", "-m", "Initial migration"
        ], capture_output=True, text=True, cwd=os.path.dirname(os.path.dirname(__file__)))

        if result.returncode != 0:
            if "Target database is not up to date" not in result.stderr and "No changes in schema detected" not in result.stdout:
                return False

        result = subprocess.run([
            sys.executable, "-m", "alembic", "upgrade", "head"
        ], capture_output=True, text=True, cwd=os.path.dirname(os.path.dirname(__file__)))

        return result.returncode == 0

    except Exception as e:
        return False


async def create_initial_data():
    async with AsyncSessionLocal() as db:
        try:
            repository = IncidentRepository(db)

            existing_incidents = await repository.get_incidents(limit=1)

            if not existing_incidents:
                await repository.create_incident(
                    description="сломался самокат",
                    source="operator"
                )
                return True
            else:
                return True

        except Exception:
            return False


async def run_migrations():
    migration_success = await run_alembic_migrations()
    data_success = await create_initial_data()

    return migration_success and data_success