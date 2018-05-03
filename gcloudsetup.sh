#!/bin/bash
if [[  $# -ne 1 || $1 -le 0 ]]; then
	echo "Incorrect input: Supply one argument specifying the number of VM instances to initialize"
else
	for i in `seq 1 $1`; do
		echo "Initializing earth-$i..."
		gcloud compute instances create earth-$i
		gcloud compute scp ~/.ssh/google-cloud-cs123 earth-$i:~/.ssh/id_rsa --ssh-key-file=~/.ssh/google-cloud-cs123
	done
	gcloud compute instances list --format=text \
    | grep '^networkInterfaces\[[0-9]\+\]\.networkIP:' | sed 's/^.* //g' >> intIPs
    for i in `seq 1 $1`; do
    	gcloud compute scp intIPs earth-$i:~/ --ssh-key-file=~/.ssh/google-cloud-cs123
    	gcloud compute ssh earth-$i --ssh-key-file=~/.ssh/google-cloud-cs123
    	cat intIPs >> hosts
    	rm intIPs
    	echo "Installing dependencies on earth-$i..."
    	sudo apt-get -y install mpich
    	sudo apt-get -y install python-pip
    	sudo apt-get -y install python-dev
    	yes | sudo pip install mpi4py
    	sudo apt-get -y install python3-dev
    	sudo apt-get -y install python3-pip
    	yes | sudo pip3 install mpi4py
		yes | sudo pip install numpy
		yes | sudo pip3 install numpy
		logout
		for i in `seq 1 $(($1-1))`; do
			gcloud compute ssh earth-$i --ssh-key-file=~/.ssh/google-cloud-cs123
			echo "SSHing from earth-$i..."
			for j in `seq $(($i+1)) $1`; do
				echo "...to earth-$j"
				gcloud compute ssh earth-$j --ssh-key-file=~/google-cloud-cs123
			done
		done
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
#
