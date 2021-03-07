import setuptools

description = "CLI for opening local files on browsers based on a remote git repository"

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gropen",
    version="0.1.0",
    author="Tiago Guedes",
    author_email="tiagopog@gmail.com",
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tiagopog/gropen/",
    project_urls={
        "Bug Tracker": "https://github.com/tiagopog/gropen/issues",
    },
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.6",
    packages=setuptools.find_packages(),
    entry_points={"console_scripts": ["gropen = gropen.gropen:main"]},
)
