#!/usr/bin/python3
from fabric.api import put, run, local, env
import os

env.hosts = ["52.86.204.80", "34.202.158.153"]
env.user = 'ubuntu'
env.key_filename = '~/.ssh/school'


def do_deploy(archive_path):
    """Fabric script that distributes
    an archive to your web server"""
    runned_locally = os.getenv("runned_locally", None) # None the first time
    if runned_locally is None: # run the local commands
        ...
        os.environ["runned_locally"] = "True" # this must be a string
    # run the remaining local codes
    # use run outside the if statement
    # to access the remote hosts

    if not os.path.exists(archive_path):
        return False
    try:
        tgzfile = archive_path.split("/")[-1]
        print(tgzfile)
        filename = tgzfile.split(".")[0]
        print(filename)
        pathname = "/data/web_static/releases/" + filename
        put(archive_path, '/tmp/')
        run("mkdir -p /data/web_static/releases/{}/".format(filename))
        run("tar -zxvf /tmp/{} -C /data/web_static/releases/{}/"
            .format(tgzfile, filename))
        run("rm /tmp/{}".format(tgzfile))
        run("mv /data/web_static/releases/{}/web_static/*\
            /data/web_static/releases/{}/".format(filename, filename))
        run("rm -rf /data/web_static/releases/{}/web_static".format(filename))
        run("rm -rf /data/web_static/current")
        run("ln -s /data/web_static/releases/{}/ /data/web_static/current"
            .format(filename))
        return True
    except Exception as e:
        return False
