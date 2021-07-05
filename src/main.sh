#!/usr/bin/bash

###################
# Run this shell in detach mode. It'll start the docker in case of the stdin
# (dce_stdin) file is found.

###################

FLOC=stream/dce_stdin

docker pull tyrrrz/discordchatexporter
function file_get(){
	local out=$(cat "$FLOC" | grep "$1" | sed "s/$1: //g")
	echo "$out"
}
while true
do
	if [ -f "$FLOC" ]
	then
		echo "~"
		cat "$FLOC"
		echo "~"
		token=$(file_get "token")
		echo "Token : $token"

		p=$(cat "$FLOC" | grep "guild")
		if [[ -z "$p" ]]
		then
			channel=$(file_get "channel")
			echo "Channel : $channel"
			docker run -t -v $(pwd)/stream/files:/app/out tyrrrz/discordchatexporter export --channel "$channel" --token "$token"
		else
			guild=$(file_get "guild")
			echo "Guild : $guild"
			docker run -t -v $(pwd)/stream/files:/app/out tyrrrz/discordchatexporter exportguild --guild "$guild" --token "$token"
		fi

		echo "Done" > stream/o_stdin
		rm "$FLOC"
		while true
		do
			if [ -f "$FLOC" ]
			then
				rm stream/files/*
				rm "$FLOC"
				break
			fi
			sleep 1
		done
	fi
	sleep 1
done
