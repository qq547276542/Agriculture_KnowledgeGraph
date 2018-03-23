#!/bin/sh

#　用于文件去重的脚本，输入参数为:待去重文件名
if [ $# -gt 1 ];then
	echo "Too many parameters, requried 1 parameter about filename: inputFileName "
elif [ $# -lt 1 ];then
	echo "Too few papremeter, required 1 parameter about filename: inputFileName "
else
sort $1 | uniq -u >> $1"_deduplication".txt
fi
