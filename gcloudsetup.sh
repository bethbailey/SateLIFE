#!/bin/bash
if [[  $# -ne 1 || $1 -le 0 ]]; then
	echo "Incorrect input: Supply one argument specifying the number of VM instances to initialize"
else
	for i in `seq 1 $1`; do
		echo "Initializing earth-$i..."
		gcloud compute instances create earth-$i
		gcloud compute scp ~/.ssh/google-cloud-cs123 earth-$i
	done
	


fi

# TO EXTRACT INTERNAL IPs 
#gcloud compute instances list --format=text \
#    | grep '^networkInterfaces\[[0-9]\+\]\.networkIP:' | sed 's/^.* //g'


# TO DELETE VM INSTANCES
#gcloud compute instances delete my-instance --zone us-central1-a


# TO COPY SOMETHING OVER TO VM INSTANCES (combination of two below)
#scp -i .ssh/google-cloud-cs123 .ssh/google-cloud-cs123 username@external-IP-1:~/.ssh/id_rsa
# gcloud compute scp ~/file-1 my-instance:~/remote-destination --zone us-central1-a


# TODO
# configure gcloud with .ssh/google-cloud-cs123
# how to transfer hosts file effectively (i.e., internal IPs)
