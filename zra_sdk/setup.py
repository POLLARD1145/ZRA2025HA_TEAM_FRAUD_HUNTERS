from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="zra-sdk",
    version="0.1.0",
    author="Team Fraud Hunters",
    author_email="",
    description="Fraud Detection SDK for Zambia Revenue Authority",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/POLLARD1145/ZRA2025HA_TEAM_FRAUD_HUNTERS",
    packages=find_packages(exclude=["tests", "tests.*"]),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
)
