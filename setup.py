from setuptools import setup, find_packages

VERSION = '0.1'
DESCRIPTION = 'Python Payment SDK'
LONG_DESCRIPTION = 'EPG PaymentSDK is a combination of payment models and helpers'

# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
    name="payment-sdk",
    version=VERSION,
    author="CGP",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(exclude=["sdk.tests", "sdk.tests.*", "sdk/tests", "sdk/tests/*"]),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
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
