from setuptools import setup, find_packages

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
readme_description = (this_directory / "README.md").read_text()


VERSION = '1.0.3'
DESCRIPTION = 'Comercia Global Payments - Python SDK'

# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
    name="cgp-payment-sdk",
    version=VERSION,
    author="Comercia Global Payments",
    description=DESCRIPTION,
    long_description=readme_description,
    long_description_content_type='text/markdown',
    packages=find_packages(exclude=["sdk.tests", "sdk.tests.*", "sdk/tests", "sdk/tests/*"]),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        'License :: OSI Approved :: MIT License',
    ],
    install_requires=[
        "dataclasses-json==0.6.7",
        "validators==0.29.0",
        "requests==2.32.3",
        "urllib3==2.2.2",
        "certifi==2024.6.2",
        "charset-normalizer==3.3.2",
        "idna==3.7",
        "marshmallow==3.21.3",
        "mypy-extensions==1.0.0",
        "packaging==24.1",
        "pycryptodome==3.20.0",
        "typing-inspect==0.9.0",
        "typing_extensions==4.12.2"
    ],
)
