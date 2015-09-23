#!/bin/bash

fleetctl='fleetctl -tunnel=cluster1.us-west-1.opsy.co:9122 -strict-host-key-checking=false'

for machine in $($fleetctl list-machines --no-legend --full | awk '{ print $1;}'); do
  echo $machine
  $fleetctl ssh $machine "$@"
done
