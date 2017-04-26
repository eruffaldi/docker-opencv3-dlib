#!/bin/bash
function RUN()
{
$*
}
function ENV()
{
export $1=$2;
}
function WORKDIR()
{
cd $1;
}
function CMD()
{
echo "CMD $*"
}
function FROM()
{
echo "CMD $*"
}
source Dockerfile
