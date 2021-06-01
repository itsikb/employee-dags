#!/bin/bash
check_status(){
    if [ $? -eq 0 ]
    then
      echo "The command ran ok"
    else
      echo "The command failed" >&2
      exit 1
    fi
}

# determine scripts and project root directory
SCRIPTS_PATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
PROJECT_PATH="$SCRIPTS_PATH/.."
echo Scripts path: $SCRIPTS_PATH
echo Project root: $PROJECT_PATH

DIST_PATH="$PROJECT_PATH/dist"
echo Distribution root: $DIST_PATH
rm -rf $DIST_PATH
mkdir $DIST_PATH

VENV_PATH="$DIST_PATH/zip_dag"
echo Create virtualenv: $VENV_PATH
virtualenv -p python3.7 "$VENV_PATH"
echo Start virtualenv
# shellcheck disable=SC1090
source "$VENV_PATH/bin/activate"
check_status

ZIP_CONTENT_ROOT="$DIST_PATH/zip_dag_contents"
echo Creating zip content root: $ZIP_CONTENT_ROOT
mkdir $ZIP_CONTENT_ROOT

#delete sagemaker package
FILTERED_REQUIREMENTS="$ZIP_CONTENT_ROOT/requirements.txt"
echo Updating filtered requirements file: $FILTERED_REQUIREMENTS
touch $FILTERED_REQUIREMENTS
sed '/sagemaker\|boto/d' $PROJECT_PATH/requirements.txt > $FILTERED_REQUIREMENTS

# install our requirements
#pip install --target "$ZIP_CONTENT_ROOT" -r "$FILTERED_REQUIREMENTS"
#check_status

# root directory should not have an init file
rsync -a "$PROJECT_PATH/APP_NAME" "$ZIP_CONTENT_ROOT"
rsync -a "$PROJECT_PATH/dags" "$ZIP_CONTENT_ROOT"
rsync -a "$PROJECT_PATH/plugins" "$ZIP_CONTENT_ROOT"
cp "$PROJECT_PATH/scripts/MANIFEST.in" "$ZIP_CONTENT_ROOT"
cp "$PROJECT_PATH/scripts/.pypirc" "$ZIP_CONTENT_ROOT"
cp "$PROJECT_PATH/scripts/setup.py" "$ZIP_CONTENT_ROOT"

#clean tests and pycache files everywhere
find "$ZIP_CONTENT_ROOT" -type d -name "tests" -exec rm -rfv {} +
find "$ZIP_CONTENT_ROOT" -type d -name "__pycache__" -exec rm -rfv {} +

#build the package
echo $ZIP_CONTENT_ROOT
cd "$ZIP_CONTENT_ROOT" || exit
echo $PWD
python "$ZIP_CONTENT_ROOT/setup.py" bdist_wheel --universal
check_status

###upload to artifactory
pip3 install -Iv twine==3.2.0
check_status

twine upload dist/* -r PyPI-releaes -u "$MICROSERVICES_ARTIFACTORY_USER" -p "$MICROSERVICES_ARTIFACTORY_PASSWORD" --config-file .pypirc
check_status
echo Project SUCCESSFULLY deployed to Artifactory
