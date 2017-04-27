#!/usr/bin/env bash

# Install fresh virtual environment
rm -rf ./venv
virtualenv -p /bin/python3.5 --no-site-packages venv

# Install project requirements
./venv/bin/pip3.5 install -r ./requirements.txt

# Correct SELinux permissions
function fixPermission () {
    semanage fcontext -a -t $1 $2
    restorecon -R -v $2
}

CONTEXT=httpd_sys_script_exec_t

find $(pwd)/venv/lib/python3.5/site-packages/psycopg2/ -iname '*.so*'| while read line; do
    fixPermission ${CONTEXT} ${line}
done
