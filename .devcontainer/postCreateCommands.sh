set -eo pipefail

export PIPENV_VERBOSITY=-1

echo -e "\n###############################################################"
echo -e "Setting up Python Environment \n"

pipenv install --dev

echo -e "\n###############################################################"
echo -e "Compiling Website \n"

pipenv run build

echo -e "\n###############################################################"
echo -e  "Run Web Server ... \n"

pipenv run dev
