#!/bin/bash
input="summarize_app.pid"
while IFS= read -r line
do
  echo "killing $line"
  kill -9 "$line"
done < "$input"
rm "$input"