from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of README.md
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="pygentic",
    version="0.2.3",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "pydantic",
        "httpx",
        "uvicorn",
        "liteLLM",
        "pydbantic",
        "databases[sqlite]",
        "pytest",
        "pytest-asyncio",
        "sqlalchemy",  # Add any other dependencies here
    ],
    entry_points={
        "console_scripts": ["pygentic=app.main:run"],
    },
    author="Your Name",
    author_email="your-email@example.com",
    description="An innovative system designed to enhance the capabilities of AI assistants by providing a flexible and standardized API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ruvnet/pygentic",
    license="Apache License 2.0",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
