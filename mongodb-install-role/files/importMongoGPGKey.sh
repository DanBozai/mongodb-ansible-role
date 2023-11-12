#!/bin/bash

if [ ! -e /usr/share/keyrings/mongodb-server-7.0.gpg ]; then

curl -fsSL https://pgp.mongodb.com/server-7.0.asc | \
   sudo gpg -o /usr/share/keyrings/mongodb-server-7.0.gpg \
   --dearmor
fi

if [ ! -e /etc/apt/sources.list.d/mongodb-org-7.0.list ]; then
    echo "deb [ signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg ] http://repo.mongodb.org/apt/debian bullseye/mongodb-org/7.0 main" | sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list
fi

exit 0
