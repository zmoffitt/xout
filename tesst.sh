#!/bin/bash
if [[ ! -e "big1.txt" ]]; then
	echo "making big file"
	for i in {1..500}; do cat b6.txt >> big1.txt; done
fi

fgrep --ignore-case --color=always sanchez big1.txt | head
python3 xout.py big1.txt clean.big1.txt
fgrep --ignore-case --color=always sanchez clean.big1.txt | head
