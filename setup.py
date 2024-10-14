import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setuptools.setup(
    name="simple_tem",
    version= '2024.10.14',
    author="Erik Frojdh",
    author_email="erik.frojdh@psi.ch",
    description="Configuration of experiments in the EPOC project",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/epoc-ed/epoc-utils",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GPL License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
