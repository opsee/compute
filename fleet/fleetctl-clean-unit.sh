#!/bin/bash -x

fleetctl='fleetctl -tunnel=cluster1.us-west-1.opsy.co:9122 -strict-host-key-checking=false'

name=$1
if [ -z $name ]; then
	echo "Please provide a busted unit name"
	exit 1
fi

shift 1

$fleetctl stop $name
$fleetctl destroy $name

for machine in $($fleetctl $@ list-machines --no-legend --full | awk '{ print $1;}'); do
	$fleetctl $@ ssh $machine "sudo rm -f /run/fleet/units/$name && sudo systemctl daemon-reload && sudo systemctl restart fleet"
done
