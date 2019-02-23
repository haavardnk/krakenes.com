#!/bin/bash
chmod 600 ~/.travis/id_rsa
cat .travis/update.sh | ssh -o StrictHostKeyChecking=no -o BatchMode=yes -i ~/.travis/id_rsa "$SSHUSER@$IP"