import setuptools

long_desc = open("README.md").read()
required = [
	"docker>=5.0.3",
	"opencv-python>=4.6.0.66",
	"parrot-olympe>=7.3.0",
	"requests>=2.22.0",
	"PySDL2>=0.9.12",
	"PyOpenGL>=3.1.6",
	"fastapi>=0.79.0",
	"uvicorn>=0.18.2",
	"python-multipart>=0.0.5"
]

setuptools.setup(
    name="SoftwarePilot",
    version="1.0.6",
    author="Kevyn Angueira Irizarry",
    author_email="kevyn.angueira@gmail.com",
    description="SoftwarePilot is an open source middleware and API that supports aerial applications for Parrot Anafi drones",
    long_description=long_desc,
    long_description_content_type="text/markdown",
    url="https://github.com/boredbot2/SoftwarePilot",
    key_words="Parrot Anafi, Drone, Olympe",
    install_requires=required,
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
)

