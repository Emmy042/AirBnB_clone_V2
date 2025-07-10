from fabric.api import env, run, put
import os

# Hosts will be passed manually via CLI or defined statically
env.hosts = ['172.17.0.12']  # Replace with your server IP or set via CLI 

def do_deploy(archive_path):
    """
    Distributes an archive to the web server. 
    - archive_path: path to the .tgz file
    """
    if not os.path.exists(archive_path):
        print("Archive path does not exist")
        return False

    try:
        file_name = archive_path.split('/')[-1]
        no_ext = file_name.split('.')[0]
        release_path = "/data/web_static/releases/{}".format(no_ext)

        # Upload archive to /tmp/
        put(archive_path, "/tmp/{}".format(file_name))

        # Create release directory
        run("mkdir -p {}".format(release_path))

        # Extract archive
        run("tar -xzf /tmp/{} -C {}".format(file_name, release_path))

        # Move contents up one level
        run("mv {}/web_static/* {}/".format(release_path, release_path))
        run("rm -rf {}/web_static".format(release_path))

        # Delete archive from /tmp/
        run("rm /tmp/{}".format(file_name))

        # Update symbolic link
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(release_path))

        print("New version deployed!")
        return True

    except Exception as e:
        print("Deployment failed: {}".format(e))
        return False
