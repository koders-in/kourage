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

git_branch=`git branch 2>/dev/null | grep '^*' | colrm 1 2 | tr -d '\n' && echo  -n`
run_cmd "docker build -t ${git_branch} ." "Docker file built."
run_cmd "docker run -e TOKEN ${git_branch}" "Run"
