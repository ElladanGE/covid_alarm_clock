import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Covid19AlarmClock",
    version="0.0.1",
    author="Duncan Watson",
    author_email="dw574@exeter.ac.uk",
    description="COVID-19 Alarm Clock",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ElladanGE",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
