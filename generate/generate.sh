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

SCRIPTS_PATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
PROJECT_PATH="$SCRIPTS_PATH/.."
echo $SCRIPTS_PATH
echo $PROJECT_PATH

cd "$PROJECT_PATH" || exit

virtualenv -p python3.7 venv
source venv/bin/activate
pip install -r generate/requirements-generate.txt
check_status

echo "Running generate.py"
python3 "$SCRIPTS_PATH/generate.py" -p "$PROJECT_PATH"
check_status

REQUIREMENTS_DEV="$PROJECT_PATH/requirements-dev.txt"
pip install -r "$REQUIREMENTS_DEV"
check_status
