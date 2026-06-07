from setuptools import setup, find_packages

setup(
    name="cascade",
    version="0.1.1",
    description="Stateless, zero-dependency local-only Python-to-Web visual audit and drill-down framework",
    author="Google DeepMind team on Advanced Agentic Coding & Waynes",
    packages=find_packages(),
    package_data={
        "cascade": [
            "index.html",
            "templates/*.py"
        ]
    },
    include_package_data=True,
    install_requires=[], # STRICTLY zero third-party dependencies!
    entry_points={
        "console_scripts": [
            "cascade=cascade.__main__:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
