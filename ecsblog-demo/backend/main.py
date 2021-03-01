from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
	return """
          ##         .
    ## ## ##        ==
 ## ## ## ## ##    ===
/\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\___/ ===
{                       /  ===-
\______ O           __/
 \    \         __/
  \____\_______/

Hello from Docker!

"""

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=80)

