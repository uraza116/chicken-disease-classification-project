import os
from pathlib import Path
import logging
import platform
import subprocess


def create_file_structure():
    logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s:')

    print("\n--- Project Setup ---")
    print("We'll collect a few details to auto-generate your setup.py file.")
    print("These values are used for linking your project to GitHub, setting up logging, and preparing a virtual environment.\n")

    # Ask for user inputs
    repo_name = input("Enter repository name (GitHub repo, e.g., 'WineQuality'): ").strip()
    username = input("Enter your GitHub username (e.g., 'uraza116'): ").strip()
    src_repo = input("Enter source repo/package folder name (e.g., 'mlProject'): ").strip()
    author_email = input("Enter author email (used in setup metadata): ").strip()

    list_of_files = [
        f"src/{src_repo}/__init__.py",
        f"src/{src_repo}/components/__init__.py",
        f"src/{src_repo}/utils/__init__.py",
        f"src/{src_repo}/utils/common.py",
        f"src/{src_repo}/config/__init__.py",
        f"src/{src_repo}/config/configuration.py",
        f"src/{src_repo}/pipeline/__init__.py",
        f"src/{src_repo}/entity/__init__.py",
        f"src/{src_repo}/entity/config_entity.py",
        f"src/{src_repo}/constants/__init__.py",
        "data/text.csv",
        "config/config.yaml",
        "params.yaml",
        "schema.yaml",
        "main.py",
        "app.py",
        "requirements.txt",
        "setup.py",
        "research/trials.ipynb",
        "templates/index.html"
    ]

    for filepath in list_of_files:
        filepath = Path(filepath)
        filedir, filename = os.path.split(filepath)

        if filedir != "":
            os.makedirs(filedir, exist_ok=True)
            logging.info(f"Creating directory; {filedir} for the file: {filename}")

        if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
            with open(filepath, "w", encoding="utf-8") as f:

                # setup.py content
                if filename == "setup.py":
                    content = f"""import setuptools

__version__ = "0.0.0"

REPO_NAME = "{repo_name}"
AUTHOR_USER_NAME = "{username}"
SRC_REPO = "{src_repo}"
AUTHOR_EMAIL = "{author_email}"

setuptools.setup(
    name=SRC_REPO,
    version=__version__,
    author=AUTHOR_USER_NAME,
    author_email=AUTHOR_EMAIL,
    description="A small python package for ML app",
    long_description="A small python package for ML app",
    long_description_content_type="text/plain",
    url=f"https://github.com/{{AUTHOR_USER_NAME}}/{{REPO_NAME}}",
    project_urls={{
        "Bug Tracker": f"https://github.com/{{AUTHOR_USER_NAME}}/{{REPO_NAME}}/issues",
    }},
    package_dir={{"": "src"}},
    packages=setuptools.find_packages(where="src"),
)
"""
                    f.write(content)
                    logging.info("Populated setup.py with project and GitHub details.")

                # logger setup in src/<src_repo>/__init__.py
                elif filename == "__init__.py" and str(filedir) == os.path.join("src", src_repo):
                    logger_code = f"""import os
import sys
import logging

logging_str = "[%(asctime)s: %(levelname)s: %(module)s: %(message)s]"

log_dir = "logs"
log_filepath = os.path.join(log_dir, "running_logs.log")
os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format=logging_str,
    handlers=[
        logging.FileHandler(log_filepath),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger("{src_repo}Logger")
"""
                    f.write(logger_code)
                    logging.info(f"Added logger setup to src/{src_repo}/__init__.py")

                # populate src/<src_repo>/utils/common.py with your utilities
                elif filename == "common.py" and str(filepath) == os.path.join("src", src_repo, "utils", "common.py"):
                    common_py_content = f"""import os
from box.exceptions import BoxValueError
import yaml
from {src_repo} import logger
import json
import joblib
from ensure import ensure_annotations
from box import ConfigBox
from pathlib import Path
from typing import Any


@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    \"\"\"reads yaml file and returns

    Args:
        path_to_yaml (str): path like input

    Raises:
        ValueError: if yaml file is empty
        e: empty file

    Returns:
        ConfigBox: ConfigBox type
    \"\"\"
    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f"yaml file: {{path_to_yaml}} loaded successfully")
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError("yaml file is empty")
    except Exception as e:
        raise e


@ensure_annotations
def create_directories(path_to_directories: list, verbose: bool = True):
    \"\"\"create list of directories

    Args:
        path_to_directories (list): list of path of directories
        ignore_log (bool, optional): ignore if multiple dirs is to be created. Defaults to False.
    \"\"\"
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logger.info(f"created directory at: {{path}}")


@ensure_annotations
def save_json(path: Path, data: dict):
    \"\"\"save json data

    Args:
        path (Path): path to json file
        data (dict): data to be saved in json file
    \"\"\"
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

    logger.info(f"json file saved at: {{path}}")


@ensure_annotations
def load_json(path: Path) -> ConfigBox:
    \"\"\"load json files data

    Args:
        path (Path): path to json file

    Returns:
        ConfigBox: data as class attributes instead of dict
    \"\"\"
    with open(path) as f:
        content = json.load(f)

    logger.info(f"json file loaded succesfully from: {{path}}")
    return ConfigBox(content)


@ensure_annotations
def save_bin(data: Any, path: Path):
    \"\"\"save binary file

    Args:
        data (Any): data to be saved as binary
        path (Path): path to binary file
    \"\"\"
    joblib.dump(value=data, filename=path)
    logger.info(f"binary file saved at: {{path}}")


@ensure_annotations
def load_bin(path: Path) -> Any:
    \"\"\"load binary data

    Args:
        path (Path): path to binary file

    Returns:
        Any: object stored in the file
    \"\"\"
    data = joblib.load(path)
    logger.info(f"binary file loaded from: {{path}}")
    return data


@ensure_annotations
def get_size(path: Path) -> str:
    \"\"\"get size in KB

    Args:
        path (Path): path of the file

    Returns:
        str: size in KB
    \"\"\"
    size_in_kb = round(os.path.getsize(path) / 1024)
    return f"~ {{size_in_kb}} KB"
"""
                    f.write(common_py_content)
                    logging.info(f"Populated src/{src_repo}/utils/common.py")

                # Leave other files empty
                else:
                    pass

                logging.info(f"Creating empty file: {filepath}")
        else:
            logging.info(f"{filename} already exists.")


def write_to_file(file_path, text):
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(text)
        print(f"Successfully wrote to '{file_path}'.")
    except Exception as e:
        print(f"Error writing to file '{file_path}': {e}")


def create_virtual_env():
    system_name = platform.system().lower()

    if system_name == "windows":
        cmd = ["python", "-m", "venv", "myenv"]
    else:
        cmd = ["python3", "-m", "venv", "myenv"]

    print(f"Creating virtual environment using: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)
    print("Virtual environment 'myenv' created.\n")


def set_execution_policy():
    """Allow PowerShell scripts to run (Windows only)."""
    if platform.system().lower() == "windows":
        print("Setting PowerShell execution policy...")
        policy_cmd = [
            "powershell",
            "Set-ExecutionPolicy",
            "-Scope", "CurrentUser",
            "-ExecutionPolicy", "Unrestricted",
            "-Force"
        ]
        subprocess.run(policy_cmd, shell=True)
        print("Execution policy set to 'Unrestricted'.\n")


def activate_virtual_env():
    """Activate the virtual environment in a new shell."""
    system_name = platform.system().lower()

    if system_name == "windows":
        # Open new PowerShell window activated
        activate_cmd = r".\myenv\Scripts\activate"
        subprocess.run(["powershell", "-NoExit", activate_cmd], shell=True)
    else:
        # Open a new interactive bash shell activated
        activate_cmd = "source myenv/bin/activate && bash"
        subprocess.run(["bash", "-c", activate_cmd], shell=True)


def main():
    create_file_structure()
    create_virtual_env()
    set_execution_policy()
    print("Launching new shell with virtual environment activated...\n")
    activate_virtual_env()


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as e:
        print(f"Error during setup: {e}")
    except Exception as ex:
        print(f"Unexpected error: {ex}")
