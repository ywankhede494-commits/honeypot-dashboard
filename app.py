from flask import Flask, render_template
import json

app = Flask(__name__)

LOG_FILE = "/home/cowrie/cowrie/var/log/cowrie/cowrie.json"

def parse_logs():
    events = []
    try:
        with open(LOG_FILE, "r") as f:
            for line in f:
                events.append(json.loads(line))
    except Exception as e:
        print(e)

    return events

@app.route("/")
def dashboard():
    events = parse_logs()

    # Successful + Failed logins
    logins = [
        e for e in events
        if "login" in e.get("eventid", "")
    ]

    # Commands executed by attacker
    commands = [
        e for e in events
        if e.get("eventid", "") == "cowrie.command.input"
    ]

    return render_template(
        "index.html",
        logins=logins,
        commands=commands
    )

if  __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
