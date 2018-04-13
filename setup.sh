#!/bin/bash

de_www="/var/www"
de_log="/var/log"
de_nginx_loc="/etc/nginx"
de_env_type="test"
de_nginx_conf_name="nginx.conf"
de_symlink_src=$(pwd)

if [[ "$OSTYPE" == "darwin"* ]]; then
    de_www="/usr/local/var/www"
    de_log="/usr/local/var/log"
    de_nginx_loc="/usr/local/etc/nginx"
fi

read -p "nginx configuration location [${de_nginx_loc}]: " nginx_loc
nginx_loc=${nginx_loc:-$de_nginx_loc}
nginx_loc=${nginx_loc%/}

if [ ! -d "$nginx_loc" ]; then
    echo "Cannot open nginx conf directory ${nginx_loc}, make sure nginx is installed."
    exit
fi

read -p "name for nginx config file [${de_nginx_conf_name}]" nginx_conf_name
nginx_conf_name=${nginx_conf_name:-$de_nginx_conf_name}

nginx_conf="${nginx_loc}/${nginx_conf_name}"
cp "./config.default/nginx.${env_type}.conf" $nginx_conf

read -p "directory for www directory [${de_www}]: " www
www=${www:-$de_www}
www=${www%/}

read -p "directory for log directory [${de_log}]: " log
log=${log:-$de_log}
log=${log%/}

if [ ! -d "$www" ]; then
    mkdir "${www}"
fi

if [ ! -d "$log" ]; then
    mkdir "${log}"
fi

if [ ! -d "${log}/nginx" ]; then
    mkdir "${log}/nginx"
fi

if [ ! -d "${log}/uwsgi" ]; then
    mkdir "${log}/uwsgi"
fi

while [[ "$env_type" != "test" && "$env_type" != "deploy" ]]
do
    read -p "Environment type (test/deploy): " env_type
    env_type=${env_type:-$de_env_type}
done

if [ "$env_type" == "deploy" ]; then
    # Make a copy of the ini which will be used to serve in production
    uwsgi_ini="${www}/eula-aat_uwsgi.ini" 

    # Add the conda env location to the ini
    conda_loc="notexist"
    while [[ ! -d "${conda_loc}" ]]
    do
        read -p "Location of conda env: " conda_loc
    done

    cp "./config.default/eula-aat_uwsgi.ini" "${uwsgi_ini}"

    # Replace the content and log roots for our config files (test doesn't need these since it is port linked)
    # OSX and Linux have different default splicers for sed, so split the commands into two
    if [[ "$OSTYPE" == "darwin"* ]]; then
        sed -i '' "s:@CONTENTROOT@:${www}:g" $nginx_conf
        sed -i '' "s:@CONTENTROOT@:${www}:g" $uwsgi_ini
        sed -i '' "s:@LOGROOT@:${log}:g" $uwsgi_ini
        sed -i '' "s:@CONDALOC@:${conda_loc}:g" $uwsgi_ini
    else
        sed -i "s:@CONTENTROOT@:${www}:g" $nginx_conf
        sed -i "s:@CONTENTROOT@:${www}:g" $uwsgi_ini
        sed -i "s:@LOGROOT@:${log}:g" $uwsgi_ini
        sed -i "s:@CONDALOC@:${conda_loc}:g" $uwsgi_ini
    fi

    # Read in the directory to symlink into our wwww dir
    source_dir=$de_symlink_src
    while [[ ! -d "$source_dir" ]]
    do
        read -p "directory of project for symlink: " source_dir
        source_dir=${source_dir%/}
    done

    # Make symlink
    ln -s "${source_dir}" "${www}/eula-aat"
fi