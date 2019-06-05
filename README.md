`upload-to-devnull` is the simple python utility for the testing upload perfomance for the CPE.

This script starts a simply web server that can receive files not related to any size and redirect it to `/dev/null` on the server side. 

According to this you can upload 1G, 10G, 100G or 1T file and don't think about size.

usage:
```
pip install -r requirements.txt
chmod +x ./upload-to-devnull.py
./upload-to-devnull.py
curl --form file=@10G-TestFile.bin http://server:8000/upload
```

If the port is busy, you can change it

The usage example:
![The usage example](https://raw.githubusercontent.com/keedhost/upload-to-devnull/master/example.png "The usage example")

_Best regards,_<br />
_Andrii Kondratiev_
