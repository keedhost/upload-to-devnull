#!/usr/bin/env python

"""
upload-to-devnull is the utility for the test upload perfomance for the CPE.

This script receive files that not related to size and redirect it to /dev/null on the server side. 

According to this you can upload 1G, 10G, 100G or 1T file and don't think about size.

usage:
    $ chmod +x ./upload-to-devnull.py
    $ ./upload-to-devnull.py

    $ curl --form file=@10G-TestFile.bin http://server:8000/upload


If the port is busy, you can change it.

Also you can check the updates by the URL: https://github.com/keedhost/upload-to-devnull
"""

import os
import sys
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import mimetypes as memetypes
import shutil
import cgi
import random
import string
import json

SV_HOST="0.0.0.0"
SV_PORT=8000
SITE_ROOT="http://0.0.0.0:8000"

BASE62_CHARSET=string.ascii_lowercase + string.digits + string.ascii_uppercase

def rand_string(n=8, charset=BASE62_CHARSET):
    res = ""
    for i in range(n):
        res += random.choice(charset)
    return res


class Handler(BaseHTTPRequestHandler):

    def do_HEAD(self):
        self.send_headers()


    def send_headers(self):
        npath = os.path.normpath(self.path)
        npath = npath[1:]
        path_elements = npath.split('/')

        if path_elements[0] == "f":
            reqfile = path_elements[1]

            if not os.path.isfile(reqfile) or not os.access(reqfile, os.R_OK):
                self.send_error(404, "file not found")
                return None

            content, encoding = memetypes.MimeTypes().guess_type(reqfile)
            if content is None:
                content = "application/octet-stream"

            info = os.stat(reqfile)

            self.send_response(200)
            self.send_header("Content-Type", content)
            self.send_header("Content-Encoding", encoding)
            self.send_header("Content-Length", info.st_size)
            self.end_headers()

        elif path_elements[0] == "upload":
            self.send_response(200)
            self.send_header("Content-Type", "text/json; charset=utf-8")
            self.end_headers()

        else:
            self.send_error(404, "fuck you :)")
            return None

        return path_elements


    def do_GET(self):
        elements = self.send_headers()
        if elements is None:
            return

        reqfile = elements[1]
        f = open(reqfile, 'rb')
        shutil.copyfileobj(f, self.wfile)
        f.close()


    def do_POST(self):
        elements = self.send_headers()
        if elements is None or elements[0] != "upload":
            return

        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={
                "REQUEST_METHOD": "POST",
                "CONTENT_TYPE":   self.headers['Content-Type']
            })

        _, ext = os.path.splitext(form["file"].filename)

        # fname = rand_string() + ext
        # while os.path.isfile(fname):
        #    fname = rand_string() + ext

        fdst = open(os.devnull, "wb")
        shutil.copyfileobj(form["file"].file, fdst)
        fdst.close()

        result = {
            "data": { "result": "File was uploaded to /dev/null"},
            "success": True,
            "status": 200,
        }

        self.wfile.write(json.dumps(result))



HTTPServer((SV_HOST, SV_PORT), Handler).serve_forever()

