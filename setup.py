import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jsonalize-stanley",
    version="0.0.1",
    author="Stanley Nian",
    author_email="stanley.nian@yandex.com",
    description="A JSON data binding library for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nianxy/jsonalize",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.7',
)

