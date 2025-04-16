#!/bin/bash
pytest -v -s --html=./reports/report.html --self-contained-html --cov=./ --cov-report=html

if [ $? -ne 0 ]
then
    echo 'pytest failed'
    exit 1
else
    echo 'OK'
fi

open ./reports/report.html &
if [ $? -ne 0 ]
then
    echo 'Failed to open report.html'
    exit 1
else
    echo 'OK'
fi

open ./htmlcov/index.html &
if [ $? -ne 0 ]
then
    echo 'Failed to open report.html'
    exit 1
else
    echo 'OK'
fi


echo 'Success'
exit 0
