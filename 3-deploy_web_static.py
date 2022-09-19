#!/usr/bin/python3
# task 3:

from datetime import datetime
from os.path import isdir
from fabric.api import put, run, env, local
from os.path import exists


env.hosts = ['web-01.paulinacrespihs.tech', 'web-02.paulinacrespihs.tech']


def do_pack():
    """ tgz file"""
    date = datetime.now().strftime("%Y%m%d%H%M%S")
    if isdir("versions") is False:
        local("mkdir versions")
    resp = "versions/web_static_{}.tgz".format(date)
    local("tar -cvzf {} web_static".format(resp))
    return resp


def do_deploy(archive_path):
    """distributes archive"""
    if exists(archive_path) is False:
        return False
    fname = archive_path.split("/")[-1]
    fnnoext = fname.split(".")[0]
    folder = "/data/web_static/releases/"
    put(archive_path, '/tmp')
    run('mkdir -p {}{}'.format(folder, fnnoext))
    run('tar -xzf /tmp/{} -C {}{}/'.format(fname, folder, fnnoext))
    run('rm /tmp/{}'.format(fname))
    run('mv {0}{1}/web_static/* {0}{1}/'.format(folder, fnnoext))
    run('rm -rf {}{}/web_static'.format(folder, fnnoext))
    run('rm -rf /data/web_static/current')
    run('ln -s {}{}/ /data/web_static/current'.format(folder, fnnoext))
    return True


def deploy():
    """func"""
    path = do_pack()
    if path is None:
        return False
    res = do_deploy(path)
    if res is None:
        return False
    return (res)
