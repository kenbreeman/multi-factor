curl -X PUT 'http://localhost:9999/api/user' -H 'Cookie: dev_appserver_login="test@example.com:False:185804764220139124118"'
curl -X PUT  -H 'Cookie: dev_appserver_login="test@example.com:False:185804764220139124118"' -H "Content-Type: application/json" http://localhost:9999/api/token -d '{"name":"token1","desc":"foooo","secret":"base32secret3232"}'
curl -X PUT  -H 'Cookie: dev_appserver_login="test@example.com:False:185804764220139124118"' -H "Content-Type: application/json" http://localhost:9999/api/token -d '{"name":"token2","desc":"foooo","secret":"base32secret3232"}'
curl -X GET  -H 'Cookie: dev_appserver_login="test@example.com:False:185804764220139124118"' http://localhost:9999/api/tokens
