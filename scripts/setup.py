import os
import re
from os import getenv
from pathlib import Path
from typing import List

from setuptools import find_packages, setup

dag_name_pattern = re.compile('.*_dag\.py$')


def is_dag_file(path: Path) -> bool:
    name = os.path.basename(path)
    return dag_name_pattern.match(name) is not None


def list_dag_names(setup_dist_path: str) -> List[str]:
    project_path = Path(*Path(setup_dist_path).parts[:-2])
    dags_path = os.path.join(project_path, 'dags')
    dag_file_names = [extract_file_name(path) for path in Path(dags_path).glob('*.py') if is_dag_file(path)]
    return dag_file_names


def extract_file_name(file_path: Path) -> str:
    base = os.path.basename(file_path)
    return os.path.splitext(base)[0]


packages = find_packages(include="*")

file_location = Path(__file__).parent.absolute()
pymodules = list_dag_names(file_location)

setup(
    name='PROJECT_NAME',
    version="0.1.{}".format(getenv('BUILD_NUMBER', '0')),
    zip_safe=True,
    include_package_data=True,
    author_email='USER_EMAIL',
    description='Project derived from the airflow-template repo',
    url='https://github.com/kenshoo/PROJECT_NAME',
    py_modules=pymodules,
    packages=packages,
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python :: 3'
    ],
)
