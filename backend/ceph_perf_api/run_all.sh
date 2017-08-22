#! /bin/bash
./manage.py runserver 0.0.0.0:8866 &>> django.log &
sleep 1
./run_job_conductor.py &>> job_conductor.log &
echo over!
