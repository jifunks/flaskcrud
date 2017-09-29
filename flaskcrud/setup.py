from setuptools import setup

setup(
    name='flaskcrud',
    packages=['flaskcrud'],
    include_package_data=True,
    install_requires=[
        'flask',
    ],
    setup_requires=[
        'pytest_runner',
    ],
    tests_require=[
        'pytest',
    ],
)
