import argparse
import logging
import os
import re
import yaml
from pathlib import Path
from typing import List, Dict

from git import Repo

APP_DIRECTORY_NAME = 'employee_dags'
FILE_SEARCH_LOCATIONS = ['scripts', 'tests', 'dags', 'plugins', 'employee_dags']

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)
log = logging.getLogger(__name__)


class MatchSubstitute:
    def __init__(self, template_params: Dict):
        self._count = 0
        self._template_params = template_params

    def make_substitutions(self, match_object) -> str:
        self._count += 1
        return self._template_params[match_object.string[match_object.start():match_object.end()]]

    def substitutions(self) -> int:
        return self._count


def get_project_name(project_path: str) -> str:
    invoke_path = os.path.join(project_path, 'invoke.yaml')
    with open(invoke_path, 'r') as file:
        docs = yaml.load(file, Loader=yaml.FullLoader)
        return docs['employee_dags'].replace('{{', '').replace('}}', '').strip()


def first_to_upper(fragment: str) -> str:
    return fragment[0].upper() + fragment[1:]


def camelize(name: str) -> str:
    return ''.join(first_to_upper(a) for a in re.split('([^a-zA-Z0-9])', name) if a.isalnum())


def find_user_email(repo: Repo) -> str:
    reader = repo.config_reader()
    return reader.get_value("user", "email")


def make_template_substitutions(template_paths: List[Path], template_params: Dict):
    log.info('String substitutions: {}'.format(template_params))
    regex = re.compile("(%s)" % "|".join(map(re.escape, template_params.keys())))
    for file_path in template_paths:
        with open(file_path, 'r+') as target_file:
            text = target_file.read()
            match_substitute = MatchSubstitute(template_params)
            new_text = regex.sub(match_substitute.make_substitutions, text)
            if not match_substitute.substitutions():
                log.debug('Skipping {}'.format(file_path.absolute()))
                continue
            log.info('Updating {}'.format(file_path.absolute()))
            target_file.seek(0)
            target_file.write(new_text)
            target_file.truncate()


def collect_project_files(project_path: str) -> List[Path]:
    targets = find_files_in_directory([project_path])
    search_paths = [os.path.join(project_path, directory) for directory in FILE_SEARCH_LOCATIONS]
    targets.extend(find_files_recursively(search_paths))
    return targets


def find_files_recursively(full_paths: List[str]) -> List[Path]:
    result = list()
    for path in full_paths:
        result.extend([x.absolute() for x in Path(path).rglob('*.py')])
        result.extend([x.absolute() for x in Path(path).rglob('*.sh')])
        result.extend([x.absolute() for x in Path(path).rglob('*.in')])
    return result


def find_files_in_directory(full_paths: List[str]) -> List[Path]:
    result = list()
    for path in full_paths:
        result.extend([x.absolute() for x in Path(path).glob('*.py')])
    return result


def rename_app_directory(project_path: str, project_name: str):
    app_name_path = os.path.join(project_path, APP_DIRECTORY_NAME)
    project_name_path = os.path.join(project_path, project_name)
    os.rename(app_name_path, project_name_path)


def generate_project_from_template(project_path: str):
    project_raw_name = get_project_name(project_path)
    project_camel_name = camelize(project_raw_name)
    project_pep_name = project_raw_name.lower().replace('-', '_')

    repo = Repo(project_path)
    user_email = find_user_email(repo)

    log.info('Making string substitutions.')
    template_params = dict(app_name=project_pep_name,
                           APP_NAME=project_pep_name,
                           PROJECT_NAME=project_raw_name,
                           PROJECT_CAMEL_NAME=project_camel_name,
                           USER_EMAIL=user_email)
    project_file_paths = collect_project_files(project_path)
    make_template_substitutions(project_file_paths, template_params)

    log.info('Renaming app directory.')
    rename_app_directory(project_path, project_pep_name)

    log.info('Committing changes.')
    repo.git.add('.')
    repo.git.commit('-m', 'FINISH PROJECT GENERATION')
    log.info('Please complete repository push by running micro publish-project')
    log.info(
        'You might get error for unrelated histories , to avoid that run git pull origin master --allow-unrelated-histories before pushing your changes')


def extract_file_name(file_path: Path) -> str:
    base = os.path.basename(file_path)
    return os.path.splitext(base)[0]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-p', '--project_path', required=True, type=str, help='project root path')
    args = parser.parse_args()

    generate_project_from_template(args.project_path)
