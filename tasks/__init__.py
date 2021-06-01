from os import path, getenv

from invoke import task, run, UnexpectedExit
from vaultka_tasks import populate_env_file_with_secrets, inject_env_file_to_ctx

DOCKER_ARTIFACTORY_REPO = "kenshoo-docker.jfrog.io"
DOCKER_ARTIFACTORY_USER = getenv('MICROSERVICES_ARTIFACTORY_USER')
DOCKER_ARTIFACTORY_PASSWORD_KEY = getenv('MICROSERVICES_ARTIFACTORY_PASSWORD')

HOME_DIR = path.expanduser("~")


@task
def clean(ctx):
    '''--->  Clean Docker Env'''
    run("docker rm -f $(docker ps -aq)", echo=True, warn=True)
    run("docker network prune -f", echo=True)
    run("sudo rm -rf ./tmp", echo=True, warn=True)


@task
def docker_artifactory_login(ctx):
    ''' --->  Login to artifactory'''
    try:
        if __is_login_needed():
            run("docker login -u {user} -p {password} {artifactory_url}".format(
                user=DOCKER_ARTIFACTORY_USER,
                password=DOCKER_ARTIFACTORY_PASSWORD_KEY,
                artifactory_url=DOCKER_ARTIFACTORY_REPO))
    except UnexpectedExit as auth_error:
        password = getattr(ctx, 'artifactory_password', None)
        password = '****' + password[-4:] if password else "None provided"

        print("Could not log into Artifactory.\n"
              "Your credentials are 'user={user} pass={password}'\n"
              "Make sure you provide a username and password to login to artifactory.\n"
              "If this is your first time running your application then please run the\n"
              "environment setup task => `invoke init-project-context`".format(
            user=ctx.artifactory_user,
            password=password))
        raise auth_error


@task(pre=[docker_artifactory_login])
def build(ctx):
    ctx.run("docker build . -t airflow", echo=True, warn=True)


@task
def docker_compose_up(ctx):
    '''--->  Starts docker, do not run this before running build '''
    run("docker-compose --project-directory docker-compose -f docker-compose/docker-compose.yml up -d", echo=True,
        warn=True)


@task
def setup_test_dags(ctx):
    '''--->  Adds test dags only to development env. Do not run this manually '''
    run("mkdir -p ./tmp/test_dags", echo=True, warn=True)
    run("sudo cp ./dags/*.py ./tests/common/test_dags/*.py ./tmp/test_dags", echo=True, warn=True)
    run("sudo chmod -R 777 ./tmp", echo=True, warn=True)


@task
def docker_compose_down(ctx):
    '''--->  Downs docker '''
    run("docker-compose -f docker-compose/docker-compose.yml down", echo=True, warn=True)


@task(aliases=["smoke"])
def smoke_test(ctx, env):
    # called post deployment - we have nothing to test here
    return

@task
def component_test(ctx):
    '''--->  Run Component Tests (Behave) '''
    ctx.run("behave tests/component/features --no-capture --no-capture-stderr --tags=-wip")


@task
def integration_test(ctx):
    '''--->  Run Integration Tests '''
    ctx.run("py.test -s tests/integration -v")


@task
def unit_test(ctx):
    '''--->  Run Unit Tests '''
    run("py.test tests/unit "
        "--cov=. "
        "--cov-report=term "
        "--cov-report=xml "
        "--cov-fail-under=95 -v")


@task(pre=[])
def post_test(ctx):
    '''--->  Change file permissions after local deployment, do not run this manually. '''
    run("sudo chmod -R 777 ./tmp", echo=True, warn=True)


@task(pre=[populate_env_file_with_secrets, inject_env_file_to_ctx, unit_test, build, setup_test_dags,
           docker_compose_up, integration_test, component_test], post=[post_test])
def test(ctx):
    '''--->  Run Test Suite on fresh build '''
    pass


@task
def deploy(ctx, env):
    #we only upload artifact once.
    if env=="staging":
        return
    scripts_path = path.join(path.dirname(__file__), "../scripts")
    run('{scripts_path}/create_dist.sh'.format(scripts_path=scripts_path))


def getEnvOrError(variable_name: str):
    result = getenv(variable_name, None)
    if result is None:
        raise RuntimeError('Unable to get value for environment variable: {}'.format(variable_name))
    return result


def __is_login_needed():
    shell_action = run("cat {home}/.docker/config.json | "
                       "grep -q '{artifactory_url}'".format(home=HOME_DIR,
                                                            artifactory_url=DOCKER_ARTIFACTORY_REPO),
                       warn=True)
    return not shell_action.ok
