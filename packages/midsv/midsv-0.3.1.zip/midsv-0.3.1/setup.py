import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="midsv",
    version="0.3.1",
    author="Akihiro Kuno",
    author_email="akuno@md.tsukuba.ac.jp",
    description="Python module to convert SAM to MIDSV format.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/akikuno/mids",
    packages=setuptools.find_packages(where="src",),
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
