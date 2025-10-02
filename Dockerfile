FROM ubuntu:latest
LABEL authors="adminpg"

ENTRYPOINT ["top", "-b"]