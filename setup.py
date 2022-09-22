from pathlib import Path
from setuptools import find_packages, setup
dependencies = ['beard-portscan','Pillow']
# read the contents of README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()
setup(
    name='nutui',
    packages=find_packages(),
    version='0.1.1',
    description="Nut Web UI using Flask",
    author="The Bearded Tek",
    author_email="kenny@beardedtek.com",
    url="https://github.com/beardedtek-com/nutui",
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='AGPLv3',
    project_urls={
        "Bug Tracker": "https://github.com/beardedtek-com/RTSPScanner/issues",
    },
    keywords=[
        "ups",
        "nut-server",
        "nutd",
        "nut",
        "battery-backup",
        "apc",
        "cyberpower",
        "tripp-lite"
    ],
    classifiers=[
        "Environment :: Web Environment",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Topic :: System :: Power (UPS)",
        "Topic :: Utilities",
        "Development Status :: 3 - Alpha",
        "Framework :: Flask",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators"
    ],
    install_requires=dependencies,
    py_modules=['nutui','app'],
    entry_points={
        'console_scripts': [
            "nutui=nutui:main"
        ],
    },
)
