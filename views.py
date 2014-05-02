from flask import Flask, render_template, redirect, request, g, session, url_for, flash
import config
import portscanner
import subprocess
import daemon
import os
from portscanner import LOCKFILE
import psutil

app = Flask(__name__)
app.config.from_object(config)



@app.route("/")
def index():
    message = 'Portscanner is not running.'
    try:
        pid = os.readlink(LOCKFILE)
        if psutil.pid_exists(int(pid)):
            message = 'Portscanner already running.'
    except OSError:
        pass
    return render_template("index.html", message=message)

@app.route("/scan")
def scan():
    daemon.main("python portscanner.py")
    return redirect("/", code=302)
# to do: allow user to override these in a web form
# portscanner.main(portscanner.NETMASK, portscanner.IP, portscanner.FILENAME)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
