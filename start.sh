#!/bin/bash

# Clear database lock from previous sessions
rm data/fuseki/system/tdb.lock
rm data/fuseki/databases/mydataset/tdb.lock

docker compose up
