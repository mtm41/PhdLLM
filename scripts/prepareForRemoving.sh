#!/bin/bash

FILES=$(ls *.png)
for file in $FILES; do sha256sum $file >> hashes.txt; done
cut -d ' ' -f 1 hashes.txt > only_hashes.txt
sort only_hashes.txt | uniq -d > duplicated_hashes.txt
