### Start containers
```
$ docker-compose up -d
```

### Stop containers
```
$ docker-compose down
```

### Sample request-response
```
$ curl -XPUT localhost:8000 -d "url=www.santanukar.com"
"2713"%     
```      
```
$ curl -v localhost:8000/2713                          
* Host localhost:8000 was resolved.
* IPv6: ::1
* IPv4: 127.0.0.1
*   Trying [::1]:8000...
* Connected to localhost (::1) port 8000
> GET /2713 HTTP/1.1
> Host: localhost:8000
> User-Agent: curl/8.7.1
> Accept: */*
> 
* Request completely sent off
< HTTP/1.1 302 Found
< date: Wed, 14 Jan 2026 17:21:32 GMT
< server: uvicorn
< content-length: 4
< content-type: application/json
< location: www.santanukar.com
< 
* Connection #0 to host localhost left intact
```