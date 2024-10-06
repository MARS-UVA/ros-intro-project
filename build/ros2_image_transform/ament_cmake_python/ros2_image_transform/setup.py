from setuptools import find_packages
from setuptools import setup

setup(
    name='ros2_image_transform',
    version='0.0.0',
    packages=find_packages(
        include=('ros2_image_transform', 'ros2_image_transform.*')),
)
