from flask import Flask

app = Flask("mattermost hook helper")

@app.route("/")
def hello_world() -> str:
    return "<p>Hello, World!</p>"

