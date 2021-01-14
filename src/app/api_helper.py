import requests
import os
import src.app.codec_helper

HOST = 'http://localhost:8089/'

def req_password(passval):
    resp = requests.post(f'{HOST}hash', data=passval)
    return resp

def lookup_pass_hash(job_num):
    resp = requests.get(f'{HOST}hash/{job_num}')
    return resp

def get_stats(self):
    resp = requests.get(f'{HOST}stats')
    return resp

def req_shutdown(self):
    resp = requests.post(f'{HOST}hash', data='shutdown')
    return resp