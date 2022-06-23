import setuptools

long_desc = open("README.md").read()
required = ["cv2>=2.0.2", "requests>=2.27.1", "olympe>=0.0.1"]

setuptools.setup(
    name="ParrotAnafiController",
    version="1.0.1",
    author="Kevyn Angueira Irizarry",
    author_email="kevyn.angueira@gmail.com",
    license="liscence.txt",
    description="Wrapper for Parrot Olympe",
    url="https://github.com/boredbot2/Parrot-Controller",
    key_words="Parrot Anafi, Drone, Olympe",
    install_requires=required,
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
)
