#!/bin/bash

nosetests --with-coverage --cover-package=external_ingestor unit_test/*
nosetests -sv --rednose --force-color unit_test/