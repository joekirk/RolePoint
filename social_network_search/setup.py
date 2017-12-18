from setuptools import find_packages, setup

setup(
    name='social_network_search',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask', 'wtforms'
    ],
)
