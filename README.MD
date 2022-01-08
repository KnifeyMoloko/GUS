# GUS
[![CI](https://github.com/KnifeyMoloko/GUS/actions/workflows/test_with_coverage.yml/badge.svg)](https://github.com/KnifeyMoloko/GUS/actions/workflows/test_with_coverage.yml)


GUS is a REST API package for working with the GUS API BDL provided by 
Statistics Poland (Glowny Urzad Statystyczny).
Auhtor: Maciej Cisowski (KnifeyMoloko)

## Project Goals

GUS started out as a simple project aiming to pipe requests 
for specific statistical resources to the GUS API BDL, returning the
output in pandas DataFrames (with the optional export to other 
formats).

Since feature creep is great, I decided to extend the scope of the project to be
more about dynamically creating working Python code from parsing a swagger JSON 
file. Currently the aim is to:
* retrieve the swagger JSON doc from GUS
* build a model of the paths, endpoints and params
* create Python modules with classes and methods covering the GUS API
* make the modules structured in a directory hierarchy reflecting the API model
* the end results should be similar to a Flask / Djando app, just built from 
parsing a JSON file

