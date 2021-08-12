from setuptools import find_packages, setup

setup(
    name="dca-binance",
    version="1.0.0",
    url="https://github.com/aussedatlo/dca-binance",
    author="Louis Aussedat",
    author_email="louis.aussedat@pm.me",
    description="Simple python cli for DCA using Binance",
    packages=find_packages(),
    scripts=[
        "bin/dca-binance",
    ],
    install_requires=[
        "python-binance>=1.0",
    ],
    python_requires=">=3.7",
)
