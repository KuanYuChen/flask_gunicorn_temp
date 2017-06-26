from fgtapp import app

if __name__ == "__main__":
    app.run()
#gunicorn --bind 0.0.0.0:5000 wsgi:app
