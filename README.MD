# GUS
![CI](https://github.com/<KnifeyMoloko>/<GUS>/actions/workflows/test_with_coverage/badge.svg)


GUS is a REST API package for working with the GUS API BDL provided by 
Statistics Poland (Glowny Urzad Statystyczny).
Auhtor: Maciej Cisowski (KnifeyMoloko)

## Design

GUS uses the requests package to pipe requests 
for specific statistical resources to the GUS API BDL, returning the
output in pandas DataFrames (with the optional export to other 
formats).

