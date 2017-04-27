#!/usr/bin/env bash

# Install fresh virtual environment
echo -e "\n\nINSTALLING FRESH VIRTUAL ENVIRONMENT\n"
rm -rf ./venv
virtualenv -p /bin/python3.5 --no-site-packages venv

# Install project requirements
echo -e "\n\nINSTALLING REQUIREMENTS\n"
./venv/bin/pip3.5 install -r ./requirements.txt

# Correct SELinux permissions
echo -e "\n\nFIXING PERMISSIONS\n"
function fixPermission () {
    semanage fcontext -a -v -t $1 $2
    restorecon -R -v $2
}

CONTEXT=httpd_sys_script_exec_t

find $(pwd)/venv/lib/python3.5/site-packages/psycopg2/ -iname '*.so*'| while read line; do
    fixPermission ${CONTEXT} ${line}
done

echo -e "\n\nCOMPLETE"
