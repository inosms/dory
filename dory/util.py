import os
import subprocess

def run_command(command):
    p = subprocess.Popen(command,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT,
                         shell=True)
    return iter(p.stdout.readline, b'')

def remove_end_newline(text):
    if text:
        if text.endswith('\n'):
            return text[:-1]
        else:
            return text
    else:
        return ""
