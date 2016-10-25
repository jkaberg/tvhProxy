tvhProxy
========

A small flask app to proxy requests between Plex Media Server and Tvheadend.

#### tvhProxy configuration
1. In tvhProxy.py configure options as per your setup.
2. Create a virtual enviroment: ```$ virtualenv venv```
3. Activate the virtual enviroment: ```$ . venv/bin/activate```
4. Install the requirements: ```$ pip install -r requirements.txt```
5. Finally run the app with: ```$ python tvhProxy.py```

#### Virtual host configuration
1. Add an entry in /etc/hosts file (or whatever your OS uses) on the machine running PMS, remember to change the IP if tvhProxy resides on another server:

    ```
    127.0.0.1	localhost
    127.0.0.1	tvhproxy
    ```

#### Configure web server (virtual host)
2. Configure a web server virtual host to listen for PMS on port 80 and proxy to tvhProxy on port 5004, remember to change localhost if tvhProxy resides on another server.
    
    Nginx example:
    ```
    server {
        listen       80;
        server_name  tvhproxy;
        location / {
            proxy_pass http://localhost:5004;
        }
    }
    ```
    
    Apache example:
    ```
    <VirtualHost *:80>
        ServerName tvhProxy

        ProxyPass / http://localhost:5004/
        ProxyPassReverse / http://localhost:5004/    
    </VirtualHost>
    ```

#### systemd service configuration
A startup script for Ubuntu can be found in tvhProxy.service (change paths in tvhProxy.service to your setup), install with:

    $ sudo cp tvhProxy.service /etc/systemd/system/tvhProxy.service
    $ sudo systemctl daemon-reload
    $ sudo systemctl enable tvhProxy.service
    $ sudo systemctl start tvhProxy.service

#### Plex configuration
Enter the virtual host name as the DVR device address (do **not** enter any port) when setting up Plex DVR: ```tvhproxy```
