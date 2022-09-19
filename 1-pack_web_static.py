#!/usr/bin/python3
# task 1
from fabric.api import local
from datetime import datetime
from os.path import isdir


def do_pack():
    """ tgz file"""
    try:
        date = datetime.now().strftime("%Y%m%d%H%M%S")
        if isdir("versions") is False:
            local("mkdir versions")
        resp = "versions/web_static_{}.tgz".format(date)
        local("tar -cvzf {} web_static".format(resp))
        return resp
    except:
        return None
