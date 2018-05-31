#!/bin/bash
for i in $(cat hosts); do
	ssh -oStrictHostKeyChecking=no $i "echo connected to $i"
done



