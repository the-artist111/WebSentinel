
from setuptools import setup

setup(
    name="websentinel",
    version="1.0.0",
    description="Advanced web application vulnerability scanner for SQLi, XSS, and CSRF",
    author="the-artist111",
    license="MIT",

    py_modules=[
        "websentinel",
        "crawler",
        "scanner",
        "report"
    ],

    install_requires=[
        "requests",
        "beautifulsoup4"
    ],

    python_requires=">=3.8",

    entry_points={
        "console_scripts": [
            "websentinel=websentinel:main"
        ]
    },
)
