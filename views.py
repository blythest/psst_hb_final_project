from flask import Flask, render_template, redirect, request, g, session, url_for, flash
import config
import portscanner
import subprocess
import daemon


app = Flask(__name__)
app.config.from_object(config)




@app.route("/")
def index():
    # daemon.main("python portscanner.py")
    # to do: allow user to override these in a web form
    # portscanner.main(portscanner.NETMASK, portscanner.IP, portscanner.FILENAME)
    return render_template("index.html")



if __name__ == "__main__":
    app.run(debug=True)
