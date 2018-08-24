#!/usr/bin/env bash


curl -X POST -H 'Content-type:application/json' --data-binary '{
  "add-field":{
     "name":"url",
     "indexed":false,
     "type":"string",
     "stored":true }
}' http://localhost:8983/solr/plotter/schema


curl -X POST -H 'Content-type:application/json' --data-binary '{
  "add-field":{
     "name":"title",
     "indexed":false,
     "type":"string",
     "stored":true }
}' http://localhost:8983/solr/plotter/schema

curl -X POST -H 'Content-type:application/json' --data-binary '{
  "add-field":{
     "name":"vendor",
     "indexed":false,
     "type":"string",
     "stored":true }
}' http://localhost:8983/solr/plotter/schema


curl -X POST -H 'Content-type:application/json' --data-binary '{
  "add-field":{
     "name":"summary",
     "indexed":false,
     "type":"string",
     "stored":true }
}' http://localhost:8983/solr/plotter/schema


curl -X POST -H 'Content-type:application/json' --data-binary '{
  "add-field":{
     "name":"specs",
     "indexed":true,
     "type":"text_general",
     "stored":false }
}' http://localhost:8983/solr/plotter/schema


curl -X POST -H 'Content-type:application/json' --data-binary '{
  "add-field":{
     "name":"price",
     "indexed":true,
     "type":"pfloats",
     "stored":true,
     "docValues":true}
}' http://localhost:8983/solr/plotter/schema


curl -X POST -H 'Content-type:application/json' --data-binary '{
  "add-field":{
     "name":"catogory",
     "indexed":true,
     "type":"text_general",
     "stored":false }
}' http://localhost:8983/solr/plotter/schema


curl -X POST -H 'Content-type:application/json' --data-binary '{
  "add-field":{
     "name":"brand",
     "indexed":true,
     "type":"text_general",
     "stored":false }
}' http://localhost:8983/solr/plotter/schema


curl -X POST -H 'Content-type:application/json' --data-binary '{
  "add-field":{
     "name":"model_id",
     "indexed":true,
     "type":"text_general",
     "stored":false }
}' http://localhost:8983/solr/plotter/schema


curl -X POST -H 'Content-type:application/json' --data-binary '{
  "add-field":{
     "name":"all_data",
     "indexed":true,
     "type":"text_general",
     "stored":true,
     "multiValued":true }
}' http://localhost:8983/solr/plotter/schema


curl -X POST -H 'Content-type:application/json' --data-binary '{
  "add-copy-field":{
     "source":"title",
     "dest":"all_data"}
}' http://localhost:8983/solr/plotter/schema

curl -X POST -H 'Content-type:application/json' --data-binary '{
  "add-copy-field":{
     "source":"summary",
     "dest":"all_data"}
}' http://localhost:8983/solr/plotter/schema


curl -X POST -H 'Content-type:application/json' --data-binary '{
  "add-copy-field":{
     "source":"catogory",
     "dest":"all_data"}
}' http://localhost:8983/solr/plotter/schema


curl -X POST -H 'Content-type:application/json' --data-binary '{
  "add-copy-field":{
     "source":"brand",
     "dest":"all_data"}
}' http://localhost:8983/solr/plotter/schema


curl -X POST -H 'Content-type:application/json' --data-binary '{
  "add-copy-field":{
     "source":"model_id",
     "dest":"all_data"}
}' http://localhost:8983/solr/plotter/schema


curl -X POST -H 'Content-type:application/json' --data-binary '{
  "add-copy-field":{
     "source":"specs",
     "dest":"all_data"}
}' http://localhost:8983/solr/plotter/schema


curl -X POST -H 'Content-type:application/json' --data-binary '{
  "add-copy-field":{
     "source":"vendor",
     "dest":"all_data"}
}' http://localhost:8983/solr/plotter/schema