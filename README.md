tvhProxy
========

An small flask app to proxy requests between Plex Media Server and Tvheadend


In tvhProxy.py configure options as per your setup, then create a 
virtual enviroment
```virtualenv venv```

Activate the virtual enviroment
```. venv/bin/activate```

Install the requirements
```pip install -r requirements.txt```

Finally run the app with
```python tvhProxy.py```

An startup script for Ubuntu can be found in tvhProxy.service (change 
paths to your setup), install with
```
cp tvhProxy.service /etc/systemd/system/tvhProxy.service
systemctl daemon-reload
systemctl enable tvhProxy.service
```

When in PMS setting the DVR up, use the url <ip/localhost>:5004
