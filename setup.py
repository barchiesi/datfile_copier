import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
        name="datfile_copier",
        version="1.0.0",
        author="David Barchiesi",
        author_email="david@barchie.si",
        description="A dat file based rom copier",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://gitlab.barchie.si/david/datfile_copier",
        packages=setuptools.find_packages(),
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
            "Operating System :: OS Independent",
            ],
        entry_points={
            'console_scripts': [
                'datfile_copier = datfile_copier.main:main',
                ],
            },
        )
