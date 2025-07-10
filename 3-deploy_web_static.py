from fabric.api import env, run, put, local
from datetime import datetime
import os

# Define your web server IPs (replace with actual IPs)
env.hosts = ['xx.xx.xx.xx', 'yy.yy.yy.yy']
env.user = 'ubuntu'  # or whatever user you're using

def do_pack():
    """
    Generates a .tgz archive from the web_static folder.
    Stores archive in versions/ folder with timestamp.
    Returns the archive path if successful, else None.
    """
    try:
        if not os.path.isdir("versions"):
            os.mkdir("versions")
        now = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_path = f"versions/web_static_{now}.tgz"
        print(f"Packing web_static to {archive_path}")
        result = local(f"tar -cvzf {archive_path} web_static", capture=True)
        if result.failed:
            return None
        return archive_path
    except Exception:
        return None

def do_deploy(archive_path):
    """
    Distributes an archive to the web servers.
    """
    if not os.path.exists(archive_path):
        return False

    try:
        file_name = archive_path.split('/')[-1]
        no_ext = file_name.split('.')[0]
        release_path = f"/data/web_static/releases/{no_ext}"

        put(archive_path, f"/tmp/{file_name}")
        run(f"mkdir -p {release_path}")
        run(f"tar -xzf /tmp/{file_name} -C {release_path}")
        run(f"rm /tmp/{file_name}")
        run(f"mv {release_path}/web_static/* {release_path}/")
        run(f"rm -rf {release_path}/web_static")
        run("rm -rf /data/web_static/current")
        run(f"ln -s {release_path} /data/web_static/current")

        print("New version deployed!")
        return True
    except Exception:
        return False

def deploy():
    """
    Creates and deploys a new archive to the web servers.
    """
    archive = do_pack()
    if archive is None:
        return False
    return do_deploy(archive)
