import setuptools
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="AdsKit",
    version="1.0.0",
    author="vodkarm",
    author_email="vodkarm06@gmail.com",
    description="The first Ads network on python !",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vodkarm/adkit",
    project_urls={
        "Bug Tracker": "https://github.com/vodkarm/adkit/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.9",
)