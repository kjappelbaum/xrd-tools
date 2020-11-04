#!/bin/bash

mongod

until mongo --eval "print(\"waited for connection\")"; do
    sleep 60
done

# Restore from dump
mongorestore /home/dump
rm -r /home/dump

# Keep container running
tail -f /dev/null
