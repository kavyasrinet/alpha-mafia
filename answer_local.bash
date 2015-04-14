#!/usr/bin/env bash
server_file='alpha_mafia_server_pid'

function ensure_server {
    should_start=0
    if [ -e $server_file ]; then
        server_pid=$(cat $server_file)
        if ps --pid $server_pid | grep -q "[j]ava"; then
            >&2 echo "Server already running"
            should_start=0
        else
            >&2 echo "File exists, but no server at pid $server_pid"
            should_start=1
        fi
    else
        >&2 echo "Server does not exist"
        should_start=1
    fi

    if ((should_start == 1)); then
        >&2 echo "Starting server"
        pushd dependencies/BART
        source setup.sh
        java -Xmx1024m elkfed.webdemo.BARTServer >> bart_server.log 2>&1 &
        server_pid=$!
        >&2 echo "Started server on $server_pid"
        popd
        echo $server_pid > $server_file
        sleep 10
    fi
}

export NLTK_DATA="$PWD/dependencies/nltk-data:${NLTK_DATA}"
ensure_server
#source dependencies/venv/bin/activate
arg1=$(readlink -f $1 2>/dev/null)
arg2=$(readlink -f $2 2>/dev/null)
cd src
./answer.py $arg1 $arg2
