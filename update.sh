#!/bin/bash
if [[  $# -ne 2 || $2 -le 0 ]]; then
	echo "Incorrect input: Supply the file to transfer and the number of VM instances"
else
	for i in `seq 1 $1`; do
		gcloud compute scp $2 earth-$i:~/ --ssh-key-file=~/.ssh/google-cloud-cs123
	done
fi

