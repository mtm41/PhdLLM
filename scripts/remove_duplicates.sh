#!/bin/bash

hash=$(echo $1 | cut -d ' ' -f 1)
file=$(echo $1 | cut -d ' ' -f 2)

while read -r line; do
		if [ "$line" == "$hash" ]; then
			echo "removing $2"
			rm $2
		fi;			
done < duplicated_hashes.txt
