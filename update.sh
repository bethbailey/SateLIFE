#!/bin/bash
#
# Script to automate sending files over to GCloud VM instances for dev purposes
# FIRST ARG IS FILENAME, SECOND ARG IS NUM OF NODES
#  e.g., ./update.sh mpifile.py 3

if [[  $# -ne 2 || $2 -le 0 ]]; then
	echo "Incorrect input: Supply the file to transfer and the number of VM instances"
else
	if [[ -f $1 ]]; then
		for i in `seq 1 $2`; do
			gcloud compute scp $1 earth-$i:~/ --ssh-key-file=~/.ssh/google-cloud-cs123
		done
	else
		for i in `seq 1 $2`; do
			gcloud compute scp --recurse $1 earth-$i:~/ --ssh-key-file=~/.ssh/google-cloud-cs123
		done
	fi
fi

