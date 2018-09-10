from __future__ import unicode_literals
from django.shortcuts import render
import subprocess
import os
import sys
import sqlite3 as lite
import youtube_dl
import json
from django.http import HttpResponse

def absPath():
    return os.path.dirname(os.path.realpath(__import__("__main__").__file__))

def downloadMp3(musicLink,mp3Title,id,poster):

        folder = absPath()
        subprocess.Popen(
            ('youtube-dl --no-playlist --write-info-json  -o "{}/static/music/%(id)s.%(ext)s" -f 140 ' + musicLink).format(folder))

        current_user = request.user
        print(current_user.id)

