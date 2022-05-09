#!/bin/bash -e

# To add component just append names to the components array
components=(
    animal 
    body
    format
)

components_num=${#components[@]}
shell_pids=()
PYTHON3=$(which python3)


on_exit () {
    for PID in ${shell_pids[@]} ; do
        /bin/kill $(ps -o pid= --ppid $PID)
    done
    
    exit 0
}
trap on_exit SIGINT

for i in `seq 1 $components_num` ;
do
    comp_name=${components[$(($i - 1))]}
    echo "Running... ${comp_name}"
    bash -c "$PYTHON3 -m $comp_name 2>&1 | sed -e \"s/^/[$comp_name] /\"" 2> /dev/null &
    shell_pids[$i]=$!
    echo "Done"
done
echo "All started!"

$PYTHON3 -m core

on_exit
