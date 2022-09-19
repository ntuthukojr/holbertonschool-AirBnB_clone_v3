#!/usr/bin/python3
# task 2


from fabric.api import put, run, env
from os.path import exists
env.hosts = ['web-01.paulinacrespihs.tech', 'web-02.paulinacrespihs.tech']


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
