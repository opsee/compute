#!/bin/bash -x

fleetctl='fleetctl -tunnel=cluster1.us-west-1.opsy.co:9122 -strict-host-key-checking=false'

name=$1
if [ -z $name ]; then
	echo "Please provide a GitHub username"
	exit 1
fi

shift 1

pubkey=$(curl https://github.com/${name}.keys)

for machine in $($fleetctl $@ list-machines --no-legend --full | awk '{ print $1;}'); do
	$fleetctl $@ ssh $machine "echo '${pubkey}' | update-ssh-keys -a $name -n"
done
