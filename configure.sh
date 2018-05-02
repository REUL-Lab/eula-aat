#!/bin/bash

de_www="/var/www"
de_log="/var/log"
de_nginx_loc="/etc/nginx"
de_env_type="dev"
de_nginx_conf_name="nginx.conf"
de_uwsgi_loc="/etc/uwsgi/apps-enabled"
de_symlink_src=$(pwd)
de_service_user="root"
de_service_group="root"
de_host="localhost"

rec_uwsgi_workers=8

if [[ "$OSTYPE" == "darwin"* ]]; then
    de_www="/usr/local/var/www"
    de_log="/usr/local/var/log"
    de_nginx_loc="/usr/local/etc/nginx"
    de_wsgi_loc="/usr/local/etc/uwsgi/apps-enabled"
    de_uwsgi_loc="/usr/local/etc/uwsgi/apps-enabled"
    de_service_user="www"
    de_service_group="www"
fi

while [[ "$env_type" != "dev" && "$env_type" != "prod" ]]
do
    read -p "Environment type (dev/prod): " env_type
    env_type=${env_type:-$de_env_type}
done

if [[ "$env_type" == "prod" && "$(whoami)" != "root" ]]; then
    echo "Deploy configuration requires root privileges"
    exit
fi

read -p "Hostname of API server [${de_host}]: " host
host=${host:-$de_host}
host=${host%/}

if [[ "$OSTYPE" == "darwin"* ]]; then
    sed -i '' "s:@APIDOMAIN@:${host}:g" "./app/config/environment.js"
else
    sed -i "s:@APIDOMAIN@:${host}:g" "./app/config/environment.js"
fi

read -p "nginx config location [${de_nginx_loc}]: " nginx_loc
nginx_loc=${nginx_loc:-$de_nginx_loc}
nginx_loc=${nginx_loc%/}

if [ ! -d "$nginx_loc" ]; then
    echo "Cannot open nginx config directory ${nginx_loc}, make sure nginx is installed."
    exit
fi

read -p "name for nginx config file [${de_nginx_conf_name}]: " nginx_conf_name
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
    chmod 660 "${log}/nginx"
fi

if [ ! -d "${log}/uwsgi" ]; then
    mkdir "${log}/uwsgi"
    chmod 660 "${log}/uwsgi"
fi

re='^[0-9]+$'
nginx_workers="n"
while ! [[ $nginx_workers =~ $re ]]
do
    read -p "number of nginx worker processes: " nginx_workers
done

processing_threads="n"
while ! [[ $processing_threads =~ $re ]]
do
    read -p "number of processing threads for a request: " processing_threads
done

read -p "key for google APIs: " google_api_key

if [ "$env_type" == "dev" ]; then

    read -p "Add analyze_max_threads and google_api_key to .bashrc [y/N]? " bashrc
    if [[ $bashrc =~ ^[Yy]$ ]]; then
        echo "export google_api_key=${google_api_key}" >> ~/.bashrc
        echo "export analyze_max_threads=${processing_threads}" >> ~/.bashrc
        source ~/.bashrc
    fi

    if [[ "$OSTYPE" == "darwin"* ]]; then
        sed -i '' "s:@CONTENTROOT@:${www}:g" $nginx_conf
        sed -i '' "s:@SERVICEUSER@:$(whoami):g" $nginx_conf
        sed -i '' "s:@SERVICEGROUP@:$(whoami):g" $nginx_conf
        sed -i '' "s:@NGINXWORKERS@:${nginx_workers}:g" $nginx_conf
    else
        sed -i "s:@CONTENTROOT@:${www}:g" $nginx_conf
        sed -i "s:@SERVICEUSER@:$(whoami):g" $nginx_conf
        sed -i "s:@SERVICEGROUP@:$(whoami):g" $nginx_conf
        sed -i "s:@NGINXWORKERS@:${nginx_workers}:g" $nginx_conf
    fi
else
    read -p "uwsgi configuration location [${de_uwsgi_loc}]: " uwsgi_loc
    uwsgi_loc=${uwsgi_loc:-$de_uwsgi_loc}
    uwsgi_loc=${uwsgi_loc%/}

    if [ ! -d "$uwsgi_loc" ]; then
        echo "Cannot open uwsgi conf directory ${uwsgi_loc}, make sure uwsgi is installed."
        exit
    fi

    # Make a copy of the ini which will be used to serve in production
    uwsgi_ini="${uwsgi_loc}/eula-aat_uwsgi.ini"
    cp "./config.default/eula-aat_uwsgi.ini" "${uwsgi_ini}"

    # Set number of service workers
    re='^[0-9]+$'
    uwsgi_workers="n"
    rec_override=0
    seen_message=0

    while [[ $rec_override != 1 ]]
    do
        rec_override=$seen_message
        uwsgi_workers="n"
        while ! [[ $uwsgi_workers =~ $re ]]
        do
            read -p "number of uwsgi worker processes:  " uwsgi_workers
        done

        if [[ (($uwsgi_workers < $rec_uwsgi_workers || $uwsgi_workers != $rec_uwsgi_workers )) &&  $seen_message == 0 ]]; then
            seen_message=1
            tput setaf 1
            echo ""
            echo -n "WARNING:  "
            tput sgr0
            echo "UWSGI workers limit the number of EULAs that can be processed simultaneously. It is recommended that value be at least ${rec_uwsgi_workers}. Re-enter your value or choose a larger one."
            echo ""
        else
            rec_override=1
        fi
    done

    # Pull user of service worker for permissions between uwsgi and nginx
    service_user=""
    while ! id "$service_user" >/dev/null 2>&1
    do
        read -p "uid of service user [${de_service_user}]: " service_user
        service_user=${service_user:-$de_service_user}
    done


    # For OSX Support
    service_prompted=0
    while [[ $service_prompted != 1 || ! "$(grep -m 1 $service_group /etc/group)" ]]
    do
        service_prompted=1
        read -p "gid of service usergroup [${de_service_group}]: " service_group
        service_group=${service_group:-$de_service_group}
    done

    while [[ ! -d "$source_dir" ]]
    do
        read -p "directory of project accessible by your service worker: " source_dir
        source_dir=${source_dir%/}
    done

    # Replace the content and log roots for our config files (dev doesn't need these since it is port linked)
    # OSX and Linux have different default splicers for sed, so split the commands into two
    if [[ "$OSTYPE" == "darwin"* ]]; then
        sed -i '' "s:@CONTENTROOT@:${www}:g" $nginx_conf
        sed -i '' "s:@CONTENTROOT@:${www}:g" $uwsgi_ini
        sed -i '' "s:@SERVICEUSER@:${service_user}:g" $uwsgi_ini
        sed -i '' "s:@SERVICEGROUP@:${service_group}:g" $uwsgi_ini
        sed -i '' "s:@GOOGLE_API_KEY@:${google_api_key}:g" $uwsgi_ini
        sed -i '' "s:@ANALYZE_MAX_THREADS@:${processing_threads}:g" $uwsgi_ini
        sed -i '' "s:@UWSGIWORKERS@:${uwsgi_workers}:g" $uwsgi_ini
        sed -i '' "s:@SERVICEUSER@:${service_user}:g" $nginx_conf
        sed -i '' "s:@SERVICEGROUP@:${service_group}:g" $nginx_conf
        sed -i '' "s:@NGINXWORKERS@:${nginx_workers}:g" $nginx_conf
    else
        sed -i "s:@CONTENTROOT@:${www}:g" $nginx_conf
        sed -i "s:@CONTENTROOT@:${www}:g" $uwsgi_ini
        sed -i "s:@SERVICEUSER@:${service_user}:g" $uwsgi_ini
        sed -i "s:@SERVICEGROUP@:${service_group}:g" $uwsgi_ini
        sed -i "s:@GOOGLE_API_KEY@:${google_api_key}:g" $uwsgi_ini
        sed -i "s:@ANALYZE_MAX_THREADS@:${processing_threads}:g" $uwsgi_ini
        sed -i "s:@UWSGIWORKERS@:${uwsgi_workers}:g" $uwsgi_ini
        sed -i "s:@SERVICEUSER@:${service_user}:g" $nginx_conf
        sed -i "s:@SERVICEGROUP@:${service_group}:g" $nginx_conf
        sed -i "s:@NGINXWORKERS@:${nginx_workers}:g" $nginx_conf
    fi

    # Read in the directory to symlink into our wwww dir
    source_dir=$de_symlink_src
    while [[ ! -d "$source_dir" ]]
    do
        read -p "directory of project accessible by your service worker: " source_dir
        source_dir=${source_dir%/}
    done

    # Make symlink and give it to service user/group
    if [ -d "${www}/eula-aat" ]; then
        rm "${www}/eula-aat"
    fi
    ln -s "${source_dir}" "${www}"
    chown "${service_user}:${service_group}" "${www}/eula-aat"

    # Make directory if not exist and give it to the service user/group
    if [[ ! -d "${www}/socks" ]]; then
        mkdir "${www}/socks"
    fi

    chown "${service_user}:${service_group}" "${www}/socks"
    chmod 750 "${www}/socks"

    read -p "Set nginx to run on start? [y/N]? " nginx_start
    if [[ $nginx_start =~ ^[Yy]$ ]]; then
        systemctl enable nginx
    fi

    read -p "Set uwsgi to run on start [y/N]? " uwsgi_start
    if [[ $uwsgi_start =~ ^[Yy]$ ]]; then
        systemctl enable uwsgi
    fi

    read -p "Set mongod to run on start? [y/N]? " mongod_start
    if [[ $mongod_start =~ ^[Yy]$ ]]; then
        systemctl enable mongod
    fi
fi