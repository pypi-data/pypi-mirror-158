# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
import setuptools

# Custom Packages

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
def readme_handler() -> str:
    with open("README.md", "r") as readme_file:
        return readme_file.read()

def version_handler() -> str:
    # ------------------------------------------------------------------------------------------------------------------
    version = 0,2,0 # <-- DEFINE THE VERSION IN A TUPLE FORMAT HERE
    # ------------------------------------------------------------------------------------------------------------------
    version_str = ".".join(str(i) for i in version)
    #
    # with open("src/AthenaMock/_info/_v.py", "w") as file:
    #     file.write(f"def _version():\n    return '{version_str}'")

    return version_str

# ------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    setuptools.setup(
        name="AthenaMock",
        version=version_handler(),
        author="Andreas Sas",
        author_email="",
        description="A Library of mock data and mock data generation",
        # long_description=readme_handler(),
        # long_description_content_type="text/markdown",
        url="https://github.com/DirectiveAthena/AthenaMock",
        project_urls={
            "Bug Tracker": "https://github.com/DirectiveAthena/AthenaMock/issues",
        },
        license="GPLv3",
        package_dir={"": "src"},
        packages=setuptools.find_packages(where="src"),
        python_requires=">=3.10",
        install_requires=[
        ]
    )