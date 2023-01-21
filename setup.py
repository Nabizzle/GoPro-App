from setuptools import setup

setup(
    name='GoPro App',
    version='1.0.0',
    description='App to control the video from a GoPro',
    long_description='''Application to set video parameters and to start and stop video wirelessly. This is meant to preserve the battery life of the GoPro for as long as possible without having to directly interact with the GoPro.''',
    author='Nabeel Chowdhury',
    author_email='nabeel.chowdhury@case.edu',
    license = "MIT",
    keywords=["GoPro", "video", "wireless"],
    url="https://github.com/iSensTeam/GoPro-App",
    install_requires=["open-gopro==0.12.0"],
)