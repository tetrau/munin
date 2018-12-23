# munin
--------------------------------------------------------------------------------
With munin, you can add http request memorization to your project with no effort.

Once you get one web page from the network, munin automatically save the response
to the disk drive. And after that, when you try to get web page with the same URL,
munin return the response directly from the disk cache.



## Getting Started

First, let's install munin with pip.

```bash
pip3 install https://github.com/tetrau/munin/archive/master.zip
```

Then, just modify your project a little bit.

From

```python
import requests
import time


urls = [...]
session = requests.session()

for url in urls:
    r = session.get(url)
    time.sleep(1)
    # and do some other thing here ...

```

To

```python
import munin


urls = [...]
session = munin.Session("responses.db") # here input the location of database 
                                        # that saves all cached responses
for url in urls:
    r = session.get(url)
    session.sleep(1)                   # change from time.sleep to session.sleep
                                       # here, it will only sleep when a real
                                       # request was sent and will return instantly 
                                       # if the last response was from disk cache

```

