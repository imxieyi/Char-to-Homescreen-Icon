### Char-to-Homescreen-Icon

This is a simple CGI server based on [flup](https://pypi.python.org/pypi/flup?). It works with iOS App [Workflow](http://workflow.is/). It converts any character into an image.

Download workflow: [https://workflow.is/workflows/184ad62a65714c93a00169d3e668c74e](https://workflow.is/workflows/184ad62a65714c93a00169d3e668c74e).

## Server Installation

**Remember to set absolute path of a ttf font in api.py**

Start CGI server command:
```sh
python api.py --method=prefork/threaded minspare=1 maxspare=3 maxchildren=5
```

Sample nginx config:
```
server {
    listen       0.0.0.0:80;
    listen       [::]:80;
    server_name  localhost;

    location / {
        fastcgi_pass  127.0.0.1:3456;
        fastcgi_param SCRIPT_FILENAME "";
        fastcgi_param PATH_INFO $fastcgi_script_name;
        include fastcgi.conf;
    }

}
```

Sample systemd script:
```
[Unit]
Description=Image API to Generate Icon for Workflow

[Service]
TimeoutStartSec=0
ExecStart=/usr/bin/python /home/user/imgapi/api.py --method=prefork/threaded minspare=1 maxspare=3 maxchildren=5

[Install]
WantedBy=multi-user.target
```
