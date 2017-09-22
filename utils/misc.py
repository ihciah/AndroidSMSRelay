# -*- coding: utf-8 -*-

import os
import time

from config import MEM_SAVE_PATH, FREE_SIZE, SAVE_PATH, LAST_FILE, MAX_LOCK_WAIT, LOCK

__author__ = 'ihciah'


def clean_env():
    to_delete = ['/dev/shm/mmssms.db', '/dev/shm/mmssms.db-journal',
                 '/tmp/mmssms.db', '/tmp/mmssms.db-journal']
    for f in to_delete:
        if os.path.exists(f):
            os.remove(f)


def get_db_save_path():
    statvfs = os.statvfs('/dev/shm')
    free = statvfs.f_frsize * statvfs.f_bavail / 1024 / 1024
    return MEM_SAVE_PATH if free > FREE_SIZE else SAVE_PATH


class LastFile:
    def __init__(self):
        self.last_time = self.get_last_time_on_disk()

    def get_last_time_on_disk(self):
        if os.path.isfile(LAST_FILE):
            with open(LAST_FILE) as f:
                last = f.read().strip()
            if last.isdigit() and len(last) > 9:
                return int(last)
        last = int(time.time() * 1000)
        self.dump_to_disk(last)
        return last

    def get_last_time(self):
        return self.last_time

    def dump_to_disk(self, t):
        with open(LAST_FILE, "w") as fw:
            fw.write(str(t))

    def update_time(self, t):
        if self.last_time >= t:
            return
        self.last_time = t
        self.dump_to_disk(t)


class FileLock:
    @staticmethod
    def wait_lock():
        wait_time = 0.0
        while True:
            if wait_time > MAX_LOCK_WAIT:
                FileLock.delete_lock()
            if os.path.isfile(LOCK):
                time.sleep(0.5)
                wait_time += 0.5
            else:
                break

    @staticmethod
    def create_lock():
        open(LOCK, 'a').close()

    @staticmethod
    def delete_lock():
        try:
            os.remove(LOCK)
        finally:
            pass
