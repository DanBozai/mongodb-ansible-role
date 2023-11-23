#!/bin/bash

initialValue=$(echo ${1} | tr -d " []'")
bkpIFS=$IFS
IFS=","
port=${2}

read -ra ip_array <<< "${initialValue}"
IFS=$bkpIFS

array_len=${#ip_array[@]}
last_index=$((array_len - 1))
build_members_string=""

for i in "${!ip_array[@]}"; do
    if [ $i -ne $last_index ]; then
        build_members_string+="{'_id': $i, 'host': '${ip_array[$i]}:${port}', 'priority': 1 }, "
    else
        build_members_string+="{'_id': $i, 'host': '${ip_array[$i]}:${port}', 'priority': 2 }"
    fi
done

config="{'_id':'cfg1svr', 'configsvr':true, 'members':[${build_members_string}]}"




mongosh --username ${3} --password ${4} --port ${port} --eval "rs.initiate(${config})"

exit 0
