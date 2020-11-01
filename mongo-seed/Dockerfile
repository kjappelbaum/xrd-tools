FROM mongo
COPY $DUMPDIR /home/dump
CMD mongod; mongorestore /home/dump
