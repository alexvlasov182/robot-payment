"""Database migration environment configuration."""

import os
import sys
from logging.config import fileConfig
from typing import cast

from alembic import context
from alembic.config import Config
from dotenv import load_dotenv
from sqlalchemy import engine_from_config, pool

# ============================================
# ІМПОРТИ МОДЕЛЕЙ - ПОВИННІ БУТИ НА ПОЧАТКУ!
# ============================================
from app.core.database import Base  # noqa: F401
from app.models.robot import Robot  # noqa: F401
from app.models.user import User  # noqa: F401

target_metadata = Base.metadata


# Додаємо кореневу папку проєкту до sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

load_dotenv()

# Отримуємо конфігурацію
config: Config = cast(Config, context.config)

database_url = os.getenv("DATABASE_URL")
if not database_url:
    try:
        with open(".env") as f:
            for line in f:
                if line.startswith("DATABASE_URL="):
                    database_url = line.strip().split("=", 1)[1]
                    break
    except FileNotFoundError:
        pass

if not database_url:
    database_url = "postgresql://postgres:postgres@localhost:5432/robotdb"

config.set_main_option("sqlalchemy.url", database_url)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        version_table="alembic_version",  # Явно вказуємо таблицю версій
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            version_table="alembic_version",  # Явно вказуємо таблицю версій
        )
        with context.begin_transaction():
            context.run_migrations()


# ============================================
# ТОЧКА ВХОДУ - ТІЛЬКИ ОДИН РАЗ!
# ============================================
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
