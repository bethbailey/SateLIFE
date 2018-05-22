#!/bin/bash
if [[  $# -ne 1 || $1 -le 0 ]]; then
	echo "Incorrect input: Supply one argument specifying the number of VM instances to initialize"
else
	for i in `seq 1 $1`; do
		echo "INITIALIZING earth-$i..."
		gcloud compute instances create earth-$i
		gcloud compute scp ./chain.sh earth-$i:~/ --ssh-key-file=~/.ssh/google-cloud-cs123
	done
	gcloud compute instances list --format=text \
	| grep '^networkInterfaces\[[0-9]\+\]\.networkIP:' | sed 's/^.* //g' > hosts
	for i in `seq 1 $1`; do
		gcloud compute scp ~/.ssh/google-cloud-cs123 earth-$i:~/.ssh/id_rsa --ssh-key-file=~/.ssh/google-cloud-cs123
		gcloud compute scp hosts earth-$i:~/ --ssh-key-file=~/.ssh/google-cloud-cs123
		gcloud compute ssh earth-$i --ssh-key-file=~/.ssh/google-cloud-cs123 --command="echo 'Installing dependencies on earth-$i...'; 
		sudo apt-get -y install git-core;
		sudo apt-get -y install mpich; 
		sudo apt-get -y install python-pip; 
		sudo apt-get -y install python-dev; 
		sudo apt-get -y install python3-dev; 
		sudo apt-get -y install python3-pip; 
		yes | sudo pip install mpi4py; 
		yes | sudo pip3 install mpi4py; 
		yes | sudo pip install numpy; 
		yes | sudo pip3 install numpy;
		yes | sudo pip3 install scikit-image;
		yes | sudo pip install scikit-image;
		echo 'Initiating chaining from earth-$i';
		bash ~/chain.sh";
	done
fi
gcloud compute scp --recurse data earth-1:~/ --ssh-key-file=~/.ssh/google-cloud-cs123
gcloud compute ssh earth-1 --ssh-key-file=~/.ssh/google-cloud-cs123

# TO DELETE VM INSTANCES
#gcloud compute instances delete my-instance --zone us-central1-a
