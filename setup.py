import setuptools

setuptools.setup(
    name="pokerl-harwiltz"
    version="0.0.1"
    author="Harley Wiltzer"
    author_email="harley.wiltzer@mail.mcgill.ca"
    description="A platform to experiment with poker AI"
    url="https://github.com/harwiltz/pokerl"
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
