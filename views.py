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
def main(request):
    current_user = request.user
    print(current_user)

    if request.method=="POST":
        #Mp3 operations
        musicLink = request.POST.get("musicLink")
        mp3Title,id,poster=getMp3Title(musicLink)
        downloadMp3(musicLink,mp3Title,id,poster)

    #ListMp3

    mp3List=getMusicList()

    return render(request, 'freetify/Clear.html',{'mp3List':mp3List})
def downloadMp3(musicLink,mp3Title,id,poster):
    try:
        folder = absPath()
        subprocess.Popen(
            ('youtube-dl --write-info-json   --no-playlist -o "{}/static/music/%(id)s.%(ext)s" -f 140 ' + musicLink).format(folder))
        con = lite.connect('freetify/freetify.db')
        cur = con.cursor()
        command=("""INSERT INTO downloadedSongs VALUES(%r,%r,%r);""" %(id,mp3Title,poster))
        cur.execute(command)
        con.commit()

        return True
    except:
        return False
def getMp3Title(musicLink):
    ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s%(ext)s'})
    with ydl:
        result = ydl.extract_info(
            musicLink,
            download=False  # We just want to extract the info
        )

    if 'entries' in result:
        video = result['entries'][0]

    else:
        video = result
    print(video)
    video['title'] = video['title'].replace(" ", "")
    return (video['title'],video['id'],video['thumbnail'])
def getMusicList():
    con = lite.connect('freetify/freetify.db')
    cur = con.cursor()
    command =( """select * from downloadedSongs """)
    cur.execute(command)
    data =[{'mp3': "/static/music/" + row[0] +".m4a",
            'title': row[1],
            'poster':row[2]}
               for row in cur.fetchall()]

    return data
def jsonResponse(request):
    con = lite.connect('freetify/freetify.db')
    cur = con.cursor()
    command =( """select * from downloadedSongs """)
    cur.execute(command)
    data =[{'mp3': "/static/music/" + row[0] +".m4a",
            'title': row[1] }
               for row in cur.fetchall()]

    json_data=json.dumps(data)

    return HttpResponse(json_data, content_type='application/json')