import setuptools

with open("README.md") as f:
    long_description = f.read()

with open("./src/progshot/__init__.py") as f:
    for line in f.readlines():
        if line.startswith("__version__"):
            # __version__ = "0.9"
            delim = '"' if '"' in line else "'"
            version = line.split(delim)[1]
            break
    else:
        print("Can't find version! Stop Here!")
        exit(1)

setuptools.setup(
    name="progshot",
    version=version,
    author="Tian Gao",
    author_email="gaogaotiantian@hotmail.com",
    description="A debugging tool to take 'screenshot' of your program",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gaogaotiantian/progshot",
    packages=setuptools.find_packages("src"),
    package_dir={"":"src"},
    package_data={
        "progshot": [
            "frontend/*",
            "frontend/static/*",
            "frontend/static/css/*",
            "frontend/static/js/*",
        ]
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent"
    ],
    python_requires=">=3.6",
    install_requires = [
        "dill>=0.3.3",
        "rich>=10.2.1",
        "objprint>=0.1.0",
        "websockets>=9.1"
    ],
    entry_points={
        "console_scripts": [
            "psview-cli = progshot:cli_main",
            "psview = progshot:web_server_main"
        ]
    }
)
