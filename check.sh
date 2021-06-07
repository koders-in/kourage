#!/usr/bin/bash

## cronjob : At every 6 hours perday
#.0 */6 * * *
webhook="https://discordapp.com/api/webhooks/850260151553359883/a5_fg3be71ADtQD_j--Uj0oIR7tWHyg_4hwEiGKE9rIP9fqmCDmtldXbHKB2ODmMYDkI"
ret_error() {
	if [[ $2 = "true" ]]
	then
		status="PASS"
		color=65280
	else
		status="FAIL"
		color=16711680
	fi

	### Name seperation
	tmp=$(sudo docker inspect --format="{{.Name}}" "$1")
	IFS='/' read -ra tmp <<< "$tmp"

	name=""
	for i in "${tmp[@]}"
	do
		name="${name} ${i}"
	done

	msg="𝗡𝗮𝗺𝗲 : ${name}\n𝗖𝗼𝗻𝘁𝗮𝗶𝗻𝗲𝗿 𝗜𝗗 : $1\n𝗖𝗿𝗲𝗮𝘁𝗲𝗱 𝗔𝘁 : $(date -d $(sudo docker inspect --format='{{.State.StartedAt}}' "$1"))"
	if [[ ! $2 == "true" ]]
	then
	msg="$msg\n𝗙𝗮𝗶𝗹𝗲𝗱 𝗔𝘁 : $(date -d $(sudo docker inspect --format='{{.State.FinishedAt}}' "$1"))\n𝗘𝘅𝗶𝘁 𝗖𝗼𝗱𝗲 : $(sudo docker inspect --format='{{.State.ExitCode}}' "$1")\n"
	fi

	fmsg="{ \"wait\": true, \"embeds\": [{ \"_\": \"_\", \"title\": \"${status}\", \"description\": \"\", \"color\": \"16711680\", \"timestamp\": \"$(date -u --iso-8601=seconds)\", \"author\": { \"_\": \"_\", \"name\":\"Docker Report\", \"icon_url\": \"https://imgur.com/axp9PKK.png\"}, \"thumbnail\": {  }, \"image\": { \"_\": \"_\" }, \"footer\": { \"_\":\"_\" } }], \"embeds\": [{ \"_\": \"_\", \"title\": \"${status}\", \"description\": \"${msg}\", \"color\":\"${color}\", \"timestamp\": \"$(date -u --iso-8601=seconds)\", \"author\": { \"_\": \"_\", \"name\":\"Docker Report\", \"icon_url\": \"https://imgur.com/axp9PKK.png\"}, \"thumbnail\": {  }, \"image\": { \"_\": \"_\" }, \"footer\": { \"_\":\"_\", \"text\": \"Made with ❤️  by Koders\"} }] }"


#	fmsg="{ "wait": true, "embeds": [{ "_": "_", "title": "Fail", "description": "..", "author": { "_": "_" }, "thumbnail": {  }, "image": { "_": "_" }, "footer": { "_":"_" } }], "embeds": [{ "_": "_", "title": "Fail", "description": "..", "author": { "_": "_" }, "thumbnail": {  }, "image": { "_": "_" }, "footer": { "_":"_" } }] }

	curl -H "Content-Type: application/json" -H "Expect: application/json" -X POST "${webhook}" -d "${fmsg}" 2>/dev/null
}

#sudo docker ps -qa --filter='status=running' > running.log
#sudo docker ps -qa --filter='status=exited' > exited.log

sudo docker ps -aq > file1

while IFS= read -r line
do
	ret_error "${line}" "$(sudo docker inspect "${line}" --format='{{.State.Running}}')"
done < file1
