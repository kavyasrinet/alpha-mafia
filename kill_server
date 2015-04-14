server_file=alpha_mafia_server_pid
if [ -e $server_file ]; then
    echo "Killing server"
    server_pid=$(cat $server_file)
    kill $server_pid
else
    echo "No server file"
fi
