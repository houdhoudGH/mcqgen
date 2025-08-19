from setuptools import find_packages, setup

setup(
    name="mcqgenerator",
    version="0.0.1",
    author="Nour El Houda Gheffari",
    author_email="nourgheffari@gmail.com",
    install_requires=[
        "huggingface_hub",
        "langchain",
        "langchain-huggingface",
        "langchain-community",
        "streamlit",
        "python-dotenv",
        "PyPDF2",
        "transformers",
    ],
    packages=find_packages(),
)
