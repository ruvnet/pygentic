from setuptools import setup, find_packages

setup(
    name='pygentic',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'fastapi',
        'pydantic',
        'httpx',
        'uvicorn',
        'liteLLM',
        'pydbantic',
        'databases[sqlite]',
        'pytest',
        'pytest-asyncio',
    ],
    entry_points={
        'console_scripts': [
            'pygentic=pygentic.__main__:main',
        ],
    },
)