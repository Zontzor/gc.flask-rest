import os.path

if os.path.exists('config.py'):
    from app import app
    app.run(host="0.0.0.0", port=5000)
else:
    print("No config file, exiting...")
