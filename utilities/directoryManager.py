import glob
import os


class DirectoryManager:
    @staticmethod
    def get_latest_file(directory):
        return max(glob.glob(os.path.join(directory, '*')), key=os.path.getmtime)
