from setuptools import setup

setup(
    name="OctoPrint-Fan2Mqtt",
    version="0.0.4",
    description="Publish fan speed by MQTT",
    author="X4V1T0",
    license="AGPLv3",
    packages=["fan2mqtt"],
    include_package_data=True,
    install_requires=["OctoPrint>=1.4.0"],
    entry_points={"octoprint.plugin": ["fan2mqtt = fan2mqtt"]},
)
