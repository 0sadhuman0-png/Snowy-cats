from flask import Flask, render_template
from whitenoise import WhiteNoise

app = Flask(__name__)

# Эта строка нужна, чтобы сервер видел картинки и CSS
app.wsgi_app = WhiteNoise(app.wsgi_app, root='static/', prefix='static/')

@app.route('/')
def home():
    my_pins = [
        {"id": "1", "title": "Snow Cat (Black Edition)", "image": "Snow_cat_blackl.jpg", "likes": 0},
        {"id": "2", "title": "Snow Cat (White Edition)", "image": "Snow_cat_white.jpg", "likes": 0},
        {"id": "3", "title": "Snow Cat V1 Edition", "image": "Snow_cat.jpg", "likes": 0},
        {"id": "4", "title": "Snow Cat V2 Edition", "image": "Snow_cat_v2.jpg", "likes": 0},
        {"id": "5", "title": "Snow Cat (Red Edition)", "image": "Snow_cat_Red_edition.jpg", "likes": 0},
        {"id": "6", "title": "Snow Cat (Green Edition)", "image": "Snow_cat_Green.jpg", "likes": 0},
        {"id": "7", "title": "Snow Cat (Orange Edition)", "image": "orange.jpg", "likes": 0},
        {"id": "8", "title": "Snow Cat (Pink Edition)", "image": "Snow_cat_pink.jpg", "likes": 0},
        {"id": "9", "title": "Snow Cat (Purple Edition)", "image": "Snow_cat_Purple.jpg", "likes": 0},
        {"id": "10", "title": "Snow Cat (Yellow Edition)", "image": "Snow_cat_Yellow.jpg", "likes": 0}
    ]
    return render_template('index.html', pins=my_pins)

if __name__ == '__main__':
    app.run()