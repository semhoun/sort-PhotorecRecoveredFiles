#!/bin/bash

file_lst=$(mktemp /tmp/dup-lst.XXXXXX)
file_md5=$(mktemp /tmp/dup-md5.XXXXXX)
file_dup=$(mktemp /tmp/dup-dup.XXXXXX)

> $file_lst
find $1 -type f | while read file; do
	MD5=`dd count=20 bs=4k if="$file" 2> /dev/null|md5sum`
	SIZE=`ls -ltr "$file" | awk '{print $5}'`
	printf "$MD5 %010d ;$file\n" $SIZE >> ${file_lst}
done

cat $file_lst | sort -r > $file_md5
cat $file_md5 | uniq -D -w 36 > $file_dup
CUR_MD5=""
cat $file_dup | while read line; do
	MD5=`echo $line | cut -d " " -f 1`
	if [ "$MD5" != "$CUR_MD5" ]; then
		CUR_MD5="$MD5"
	else 
		FILE=`echo $line | cut -d ";" -f 2`
		rm -f "$FILE"
	fi
done
