#!/bin/sh

de_www="/var/www"
de_log="/var/log"
de_nginx_loc="/var/etc/nginx"
de_env_type="test"
de_nginx_conf_name="nginx.conf"

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

while [[ "$env_type" != "test" && "$env_type" != "deploy" ]]
do
    read -p "Environment type (test/deploy): " env_type
    env_type=${env_type:-$de_env_type}
done

read -p "name for nginx config file [${de_nginx_conf_name}]" nginx_conf_name
nginx_conf_name=${nginx_conf_name:-$de_nginx_conf_name}

nginx_conf="${nginx_loc}/${nginx_conf_name}"
cp "./config/nginx.${env_type}.conf.default" $nginx_conf

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
    mkdir "${log}/nginx"
    mkdir "${log}/uwsgi"
fi

if [ "$env_type" == "deploy" ]; then
    # Make a copy of the ini which will be used to serve in production
    uwsgi_ini="${www}/eula-aat_uwsgi.ini" 
    cp "./config/eula-aat_uwsgi.ini.default" "${uwsgi_ini}"
    # Replace the content and log roots for our config files (test doesn't need these since it is port linked)
    sed -i '' "s:@CONTENTROOT@:${www}:g" $nginx_conf
    sed -i '' "s:@CONTENTROOT@:${www}:g" $uwsgi_ini
    sed -i '' "s:@LOGROOT@:${log}:g" $uwsgi_ini

    # Read in the directory to symlink into our wwww dir
    source_dir="INVALID"
    while [[ ! -d "$source_dir" ]]
    do
        read -p "directory of project for symlink: " source_dir
        source_dir=${source_dir%/}
    done

    # Make symlink
    ln -s "${source_dir}" "${www}/eula-aat"
fi