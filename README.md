# Data Pipeline Description

This set of scripts is used to enrich citation data with links to dbpedia and wikidata and then transform that citation data into a dynamic GML graph.

# Data Source

The citation data source for this script was downloaded from here:
https://sites.google.com/site/vispubdata/home

It contains information on IEEE Visualization (IEEE VIS) publications from 1990-2020.

Data Citation:
Petra Isenberg, Florian Heimerl, Steffen Koch, Tobias Isenberg, Panpan Xu, Chad Stolper, Michael Sedlmair, Jian Chen, Torsten Möller, and John Stasko. vispubdata.org: A Metadata Collection about IEEE Visualization (VIS) Publications. IEEE Transactions on Visualization and Computer Graphics, 23(9):2199–2206, September 2017. (doi: 10.1109/TVCG.2016.2615308) 

# Data Pipeline Summary

The data pipeline is as follows:

Download from https://sites.google.com/site/vispubdata/home 
    
    ↓
    
[publications.csv](https://github.com/photomedia/citationDataEnrichTransform/blob/main/publications.csv) --> Transform to JSON using [CSVtoJSON.py](https://github.com/photomedia/citationDataEnrichTransform/blob/main/CSVtoJSON.py)

    ↓
    
[publications.json](https://github.com/photomedia/citationDataEnrichTransform/blob/main/publications.json) --> Enrich with DBpedia and WikiData links using [get-concepts.py](https://github.com/photomedia/citationDataEnrichTransform/blob/main/get-concepts.py)

    ↓
    
[enriched-publications.json](https://github.com/photomedia/citationDataEnrichTransform/blob/main/enriched-publications.json) --> Transform JSON to XML using [JSONtoXML.py](https://github.com/photomedia/citationDataEnrichTransform/blob/main/JSONtoXML.py)

    ↓
    
enriched-publications.xml (Intermediate file generated by JSONtoXML.py script)

    ↓
    
[enriched-publications-eprints-model.xml](https://github.com/photomedia/citationDataEnrichTransform/blob/main/enriched-publications-eprints-model.xml) --> Transform to a dynamic co-concept graph in GML format using Pig Latin script [eprints-items-publications-date-merged-edges.pig](https://github.com/photomedia/citationDataEnrichTransform/blob/main/eprints-items-publications-date-merged-edges.pig)

    ↓
  
[OUTPUT/merged-file-co_node-dynamic-gml-with_edge_labels-withheader.gml](https://github.com/photomedia/citationDataEnrichTransform/blob/main/OUTPUT/merged-file-co_node-dynamic-gml-with_edge_labels-withheader.gml) --> Open directly with Gephi, apply layout and visual mappings, save and export renders

    ↓
    
- enriched-dynamic-GML.gephi (saved gephi file)
- [renders folder](https://github.com/photomedia/citationDataEnrichTransform/tree/main/renders) contains exports of visualizations of the graph from Gephi.  

# Renders Folder

- [GC-nodesize-spline.png](https://github.com/photomedia/citationDataEnrichTransform/blob/main/renders/GC-nodesize-spline.png) - Giant Component, Node Size mapped to Betweenness Centrality (BC) on a spline.
- [GC-nodesize-spline-bcGT_01.png](https://github.com/photomedia/citationDataEnrichTransform/blob/main/renders/GC-nodesize-spline-bcGT_01.png) - Giant Component, Node Size mapped to Betweenness Centrality (BC) on a spline, Filter Nodes with BC greater than .01
- [GC-nodesize-spline-degreeGT10.png](https://github.com/photomedia/citationDataEnrichTransform/blob/main/renders/GC-nodesize-spline-degreeGT10.png) - Giant Component, Node Size mapped to Betweenness Centrality (BC) on a spline, Filter Nodes with Degree greater than 10
- [GC-nodesize-spline-multi-conference.png](https://github.com/photomedia/citationDataEnrichTransform/blob/main/renders/GC-nodesize-spline-multi-conference.png) - Giant Component, Node Size mapped to Betweenness Centrality (BC) on a spline, Filter only Concepts that are related by publications from more than 1 conference
- Temporal Filters
  - [NF-nodesize-spline-durationGT25-FS24.png](https://github.com/photomedia/citationDataEnrichTransform/blob/main/renders/NF-nodesize-spline-durationGT25-FS24.png) - Filter leaving only concept relations that span 25 years or longer
  - [NF-nodesize-spline-1990-2000.png](https://github.com/photomedia/citationDataEnrichTransform/blob/main/renders/NF-nodesize-spline-1990-2000.png) - Filter by time (1990-2000)
  - [NF-nodesize-spline-2000-2010-durationLT10-FS24.png](https://github.com/photomedia/citationDataEnrichTransform/blob/main/renders/NF-nodesize-spline-2000-2010-durationLT10-FS24.png) - Filter by time (1990-2000) and Duration of concept relations LESS than 10 years
  - [NF-nodesize-spline-2000-2010.png](https://github.com/photomedia/citationDataEnrichTransform/blob/main/renders/NF-nodesize-spline-2000-2010.png) - Filter by time (2000-2010)
  - [NF-nodesize-spline-2000-2010-durationLT10-FS24.png](https://github.com/photomedia/citationDataEnrichTransform/blob/main/renders/NF-nodesize-spline-2000-2010-durationLT10-FS24.png) - Filter by time (2000-2010) and Duration of concept relations LESS than 10 years
  - [NF-nodesize-spline-2010-2020.png](https://github.com/photomedia/citationDataEnrichTransform/blob/main/renders/NF-nodesize-spline-2010-2020.png) - Filter by time (2010-2010)
  - [NF-nodesize-spline-2010-2020-durationLT10-FS24.png](https://github.com/photomedia/citationDataEnrichTransform/blob/main/renders/NF-nodesize-spline-2010-2020-durationLT10-FS24.png) - Filter by time (2010-2020) and Duration of concept relations LESS than 10 years
  - [NF-nodesize-spline-2015-2020-durationLT5-FS24.png](https://github.com/photomedia/citationDataEnrichTransform/blob/main/renders/NF-nodesize-spline-2015-2020-durationLT5-FS24.png) - Filter by time (2015-2020) and Duration of concept relations LESS than 5 years
  




