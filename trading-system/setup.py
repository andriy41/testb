from setuptools import setup, find_namespace_packages

setup(
    name='trading-system',
    version='0.1.0',
    packages=find_namespace_packages(include=['backend.*']),
    package_dir={'': '.'},
    install_requires=[
        'fastapi',
        'uvicorn',
        'pyyaml',
        'pandas',
        'numpy',
        'yfinance',
        'python-dotenv'
    ],
    python_requires='>=3.8',
)
