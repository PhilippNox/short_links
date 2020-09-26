#/bin/bash

OS=$(uname -s)
if [ "$OS" != "Darwin" ] && [ "$OS" != "Linux" ]; then
    echo 'This script works on MacOS or Linux'
    exit 0
fi

read -p 'Give psql user (default= postgres): ' puser
puser=${puser:-postgres}
#echo $puser

read -p 'Give psql password (default= postgres): ' PGPASSWORD
PGPASSWORD=${PGPASSWORD:-postgres}
export PGPASSWORD

#read -sp 'Password: ' passvar
read -p 'Give database name (default= db_for_project): ' dbname
dbname=${dbname:-db_for_project}

read -p 'Give user name for with db (default= db_for_project): ' dbuser
dbuser=${dbuser:-db_for_project}

read -p 'Give password for user (default= will be generated): ' dbpass
dbpass=${dbpass:-$(openssl rand -hex 32)}

read -p 'Next command will ask you password for psql (ex.: postgres). Press Enter to continue.'

if [ "$OS" = "Darwin" ]; then
    psql -U $puser -c "DROP DATABASE ${dbname}"
    psql -U $puser -c "DROP USER ${dbuser}"
    psql -U $puser -c "CREATE DATABASE ${dbname}"
    psql -U $puser -c "CREATE ROLE ${dbuser} WITH LOGIN PASSWORD '${dbpass}'"
    psql -U $puser -c "GRANT ALL PRIVILEGES ON DATABASE ${dbname} TO ${dbuser}"

    mv .env env.txt

    sed -i '' 's/DB_HOST=.*/DB_HOST=127.0.0.1/' env.txt
    sed -i '' 's/DB_PORT=.*/DB_PORT=5432/' env.txt
    sed -i '' "s/DB_USER=.*/DB_USER=${dbuser}/" env.txt
    sed -i '' "s/DB_PASSWORD=.*/DB_PASSWORD=${dbpass}/" env.txt
    sed -i '' "s/DB_DATABASE=.*/DB_DATABASE=${dbname}/" env.txt

    mv env.txt .env

    echo "Check updated .env"
else
    sudo -u postgres psql -c "DROP DATABASE ${dbname}"
    sudo -u postgres psql -c "DROP USER ${dbuser}"
    sudo -u postgres psql -c "CREATE DATABASE ${dbname}"
    sudo -u postgres psql -c "CREATE ROLE ${dbuser} WITH LOGIN PASSWORD '${dbpass}'"
    sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE ${dbname} TO ${dbuser}"

    sed -i 's/DB_HOST=.*/DB_HOST=127.0.0.1/' .env
    sed -i 's/DB_PORT=.*/DB_PORT=5432/' .env
    sed -i "s/DB_USER=.*/DB_USER=${dbuser}/" .env
    sed -i "s/DB_PASSWORD=.*/DB_PASSWORD=${dbpass}/" .env
    sed -i "s/DB_DATABASE=.*/DB_DATABASE=${dbname}/" .env

    echo "Check updated .env"
fi
