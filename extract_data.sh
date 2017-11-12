#!/bin/bash

usage="$(basename "$0") [-h] data_folder -- Extracts a csv file from the binary el4000 data."

while getopts ':h' option; do
  case "$option" in
    h) echo "$usage"
       exit
       ;;
   \?) echo "$usage"
       exit
       ;;
  esac
done
shift $((OPTIND - 1))

if [ $# -eq 0 ]; then
  echo "$usage"
  exit
fi

data_folder=${1%/}

if [ ! -d "$data_folder" ]; then
  echo "Directory $data_folder does not exist!"
  exit
fi

data_name=${data_folder##*/}

# print the header (the first line of input)
# and then run the specified command on the body (the rest of the input)
# use it in a pipeline, e.g. ps | body grep somepattern
body() {
    IFS=`read - r header`
    printf '%s\n' "$header"
    "$@"
}

# First sort reverse to get all headers ontop, then uniq the file, then sort it again without the first line
el4000 -o -p csv "$data_folder"/* | sort -r | uniq | (read -r; printf "%s\n" "$REPLY"; sort) > "$data_name".csv


