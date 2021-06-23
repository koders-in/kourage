#!/usr/bin/bash

# Color and Syntax Globals
NC='\033[0m'
BOLD=$(tput bold)
NT=$(tput sgr0)
FAIL='\033[1;31m'
SUCCESS='\033[1;32m'

######################################################################
# Run a command, with error handling
# ARGUMENTS:
#	Single command to run
# NOTE:
#	In case of an error, this function would exit instead of
#	returning some error code.
######################################################################
run_cmd() {
	if ! eval $1; then
		printf "[${BOLD}${FAIL}FATAL ERROR${NC}] ${FAIL}$2 failed with $?${NC}${NT}"
		exit 0
	fi
	printf "${BOLD}[${SUCCESS}Success${NC}] ${SUCCESS}$2${NC}${NT}\n"
}

# Package checking.
# -Docker check
docker --version >/dev/null 2>&1
docker_ok=$?

[[ "$docker_ok" -eq 127 ]] && \
	printf "[${BOLD}${FAIL}ERROR${NC}] ${FAIL}Docker Not found!!!${NC}${NT}" && \
	exit 2

# -Git check
git --version >/dev/null 2>&1
git_ok=$?

[[ "$git_ok" -eq 127 ]] && \
	printf "[${BOLD}${FAIL}ERROR${NC}] ${FAIL}Git Not found!!!${NC}${NT}" && \
	exit 2

# -Directory check
git_branch=`git branch 2>/dev/null | grep '^*' | colrm 1 2 | tr -d '\n' && echo  -n`

[[ -z "${git_branch}" ]] && \
	printf "[${BOLD}${FAIL}ERROR${NC}] ${FAIL}Not a github branch!!!\nPlease clone again and don't remove the '.git' file.${NC}${NT}" && \
	exit 2

run_cmd "docker build -t ${git_branch} ." "Docker file built."
run_cmd "docker run -e TOKEN -e ADMIN_CHANNEL_ID ${git_branch}" "Run"
