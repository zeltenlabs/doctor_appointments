from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in doctor_appointments/__init__.py
from doctor_appointments import __version__ as version

setup(
	name="doctor_appointments",
	version=version,
	description="Doctor appointment portal",
	author="ZeltenLabs",
	author_email="info@zeltenlabs.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
