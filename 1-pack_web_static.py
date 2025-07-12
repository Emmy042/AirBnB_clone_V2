from fabric.api import local
from datetime import datetime
import os

def do_pack():
    """
    Generates a .tgz archive from the web_static folder.
    The archive is saved in the versions folder with a timestamped filename.
    Returns the archive path if successful, or None if failed.
    """
    try:
        if not os.path.isdir("versions"):
            os.mkdir("versions")

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_path = "versions/web_static_{}.tgz".format(timestamp)

        print("Packing web_static to {}".format(archive_path))
        result = local("tar -cvzf {} web_static".format(archive_path))

        if result.failed:
            return None
        return archive_path
    except Exception:
        return None
