from setuptools import find_packages, setup


setup(
    name="morning-classes-check-backend",
    version="0.1.0",
    description="Backend API and data pipeline scaffold for Morning Classes Check",
    python_requires=">=3.9",
    packages=find_packages(include=["app", "app.*"]),
    install_requires=[
        "alembic>=1.14.0",
        "fastapi>=0.115.0",
        "psycopg[binary]>=3.2.0",
        "pydantic-settings>=2.7.0",
        "python-dotenv>=1.0.1",
        "python-multipart>=0.0.12",
        "sqlalchemy>=2.0.36",
        "uvicorn[standard]>=0.32.0",
    ],
)
