#!/bin/bash

while !</dev/tcp/web/8000; do sleep 10; done;
celery -A test1 worker -l info
