#!/bin/bash

sudo docker-compose -f docker-compose-test.yml up --build --abort-on-container-exit
