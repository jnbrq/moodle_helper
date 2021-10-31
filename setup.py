import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="moodle-helper-jnbrq",
    version="0.0.1",
    author="Canberk Sönmez",
    author_email="canberk.sonmez.409@gmail.com",
    description="Package for helping create Moodle quizzes.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jnbrq/moodle_helper",
    project_urls={
        "Bug Tracker": "https://github.com/jnbrq/moodle_helper/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=[
        'jinja2',
    ],
)
