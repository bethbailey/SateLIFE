#!/bin/bash
if [[  $# -ne 1 || $1 -le 0 ]]; then
	echo "Incorrect input: Supply one argument specifying the number of VM instances to initialize"
else
	location=""
	while [[ $location != "root" ]] && [[ $location != "all" ]]
	do
		read -p "Specify data location ('all' or 'root') followed by [ENTER]: " location
		echo "Enter a valid location"
	done
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
	if [[ $location == "root" ]]; then
		echo "Sending to root..."
		gcloud compute scp --recurse data earth-1:~/ --ssh-key-file=~/.ssh/google-cloud-cs123
	else
		echo "Sending to..."
		for i in `seq 1 $1`; do
			echo "...node $i"
			gcloud compute scp --recurse data earth-$i:~/. --ssh-key-file=~/.ssh/google-cloud-cs123
		done
	fi
	gcloud compute ssh earth-1 --ssh-key-file=~/.ssh/google-cloud-cs123
fi



# TO DELETE VM INSTANCES
#gcloud compute instances delete my-instance --zone us-central1-a

## TODOs
## allow for 'none' sending condition
## customize node specifications (e.g., memory, CPU, etc.)
## 
