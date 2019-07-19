# -*- coding: utf-8 -*-


from setuptools import setup, find_packages


setup(
    name="articles",
    version="0.0.1",
    description="Use to manage articles-service",
    packages=find_packages("src", exclude=["test"]),
    package_dir={"": "src"},
    install_requires=[
        "alembic==1.0.10",
        "nameko==2.12.0",
        "nameko-sqlalchemy==1.5.0",
        "nameko-tracer==1.2.0",
        "mysql-connector-python==8.0.16",
        "marshmallow==2.19.5",
        "sqlalchemy_filters==0.10.0",
        "sqlalchemy_utils==0.34.1",
    ],
    extras_require={
        "dev": [
            "coverage==4.5.3",
            "flake8>=3.7.7",
            "pytest==4.5.0",
        ]
    },
    zip_safe=True,
)
