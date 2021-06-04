#!/usr/bin/bash

## cronjob : At every 6 hours perday
#.0 */6 * * *

webhook="https://discordapp.com/api/webhooks/850260151553359883/a5_fg3be71ADtQD_j--Uj0oIR7tWHyg_4hwEiGKE9rIP9fqmCDmtldXbHKB2ODmMYDkI"

ret_error() {
	p=$(sudo docker inspect --format="{{.Name}}" $1)
	msg="[FAIL:${p}] $1, $(date)"
	curl -H "Content-Type: application/json" -X POST -d '{"content":"'"$msg"'"}'  $webhook
}

sudo docker ps -a | awk '{print $1}' > file1

while IFS= read -r line
do
	if [[ "$line" == "CONTAINER" ]]
	then
		continue
	fi

	if [[ "$(sudo docker inspect ${line} --format='{{.State.ExitCode}}')" == "0" ]]
	then
		continue
	fi

	ret_error "${line}" "..."
done < file1

