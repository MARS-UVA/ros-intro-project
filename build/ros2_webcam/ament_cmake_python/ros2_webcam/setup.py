from setuptools import find_packages
from setuptools import setup

setup(
    name='ros2_webcam',
    version='0.0.0',
    packages=find_packages(
        include=('ros2_webcam', 'ros2_webcam.*')),
)
