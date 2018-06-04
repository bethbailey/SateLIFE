#!/bin/bash
#
# Script to automate nodes' SSH linking for MPI purposes
# This script is called from within gcloudsetup.sh

for i in $(cat hosts); do
	ssh -oStrictHostKeyChecking=no $i "echo connected to $i"
done



