import subprocess
import json
import os

class Rclone:
    def __init__(self, rclone_path="rclone", config_file=None):
        self.rclone_path = rclone_path
        self.config_file = config_file

    def _run_command(self, args):
        command = [self.rclone_path]
        if self.config_file:
            command.extend(["--config", self.config_file])
        command.extend(args)
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode != 0:
            raise Exception(f"RClone command failed: {result.stderr}")
        return result.stdout

    def list_remotes(self):
        return self._run_command(["listremotes"]).splitlines()

    def list_files(self, remote_path):
        output = self._run_command(["lsjson", remote_path])
        return json.loads(output)

    def copy(self, source, destination):
        self._run_command(["copy", source, destination])

    def move(self, source, destination):
        self._run_command(["move", source, destination])

    def sync(self, source, destination):
        self._run_command(["sync", source, destination])

    def delete(self, path):
        self._run_command(["delete", path])

    def deletefile(self, path):
        self._run_command(["deletefile", path])

    def mkdir(self, path):
        self._run_command(["mkdir", path])

    def rmdir(self, path):
        self._run_command(["rmdir", path])

    def purge(self, path):
        self._run_command(["purge", path])

    def check(self, source, destination):
        return self._run_command(["check", source, destination])

    def version(self):
        return self._run_command(["version"]).strip()

    def set_config_file(self, config_file):
        self.config_file = config_file

    def get_config_file(self):
        return self.config_file

    def get_remote_info(self, remote: str) -> dict:
        try:
            output = self._run_command(["about", remote, "--json"])
            return json.loads(output)
        except Exception as e:
            print(f"Failed to get remote info: {e}")
            return {}