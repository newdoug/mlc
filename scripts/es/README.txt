Elasticsearch basic usage stuff for beginners like me.
These are obtained when starting elasticsearch, I just like them here as well.

Pretty much everything is in `./elasticsearch`.
Configure other nodes to join this cluster:
• On this node:
  ⁃ Create an enrollment token with `bin/elasticsearch-create-enrollment-token -s node`.
  ⁃ Uncomment the transport.host setting at the end of config/elasticsearch.yml.
  ⁃ Restart Elasticsearch.
• On other nodes:
  ⁃ Start Elasticsearch with `bin/elasticsearch --enrollment-token <token>`, using the enrollment token that you generated.

Mostly need to run `./download_and_set_up.sh` and it'll try to install things appropriately into `/opt`
