#!/usr/bin/bash

NC='\033[0m'
BOLD=$(tput bold)
NT=$(tput sgr0)
FAIL='\033[1;31m'
SUCCESS='\033[1;32m'

# Error checking
run_cmd() {
	if ! eval $1; then
		printf "[${BOLD}${FAIL}FATAL ERROR${NC}] ${FAIL}$2 failed with $?${NC}${NT}"
		exit 0
	fi
	printf "${BOLD}[${SUCCESS}Success${NC}] ${SUCCESS}$2${NC}${NT}\n"
}

run_cmd "docker build -t kourage ." "Docker file built."
run_cmd "docker run -e TOKEN -e OWN_TOKEN kourage" "Run"
