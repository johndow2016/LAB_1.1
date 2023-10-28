# использование модуля numpy для работы с массивами
import numpy as np
# использование модуля фреймворка создания веб-страниц
from flask import Flask
# возможность использования шаблонов веб-страниц
from flask import render_template
# использование модуля отображения формы
from flask_bootstrap import Bootstrap
# возможность использования формы и поля капчи
from flask_wtf import FlaskForm, RecaptchaField
# возможность использования полей ввода и запроса
from wtforms import StringField, SubmitField, FloatField, SelectField, IntegerField
# возможность использования обязательных для заполнения полей
from wtforms.validators import DataRequired
# возможность использования проверки обязательного выбора файла изображения
from flask_wtf.file import FileField, FileAllowed, FileRequired
# использование модуля работы с изображениями
from PIL import Image, ImageFilter
# приложение с использованием фреймворка flask
app = Flask(__name__)
# настройка использования форм
bootstrap = Bootstrap(app)
# настройки применения формы капчи
app.config['RECAPTCHA_USE_SSL'] = False
# настройка открытого ключа
app.config['RECAPTCHA_PUBLIC_KEY'] = '6LcXn_sUAAAAAEbvg1fqCMPOA_pgZiVcteIA9wCy'
# настройка закрытого ключа
app.config['RECAPTCHA_PRIVATE_KEY'] = '6LcXn_sUAAAAAPnsHebESwEcexSbONmIPTcIHVPS'
# настройка темы капчи
app.config['RECAPTCHA_OPTIONS'] = {'theme': 'white'}
# настройка секретного ключа
app.config['SECRET_KEY'] = 'secret'


# класс формы приложения
class WorkForm(FlaskForm):
    # кнопка для выбора исходного файла
    upload = FileField('Выберите зашумленное изображение', validators=[
        FileRequired(),
        FileAllowed(['png', 'jpg', 'jpeg'], 'Требуется указать изображение')])
    # поле для ввода параметра фильтрации
    # капча
    recaptcha = RecaptchaField()
    style = {'style': 'width:200px'}
    filterparam = StringField('Параметр фильтра', validators=[DataRequired()], render_kw=style)
    # кнопка для применения фильтра
    submit = SubmitField(' Применить фильтр для зашумленного изображения ')


# декоратор для вывода страницы по умолчанию
@app.route("/")
def hello():
    return "<html><head><title>Python</title></head><body><a href=""./filter"">Лабораторная работа №1</a></body></html>"


# приложение
@app.route("/filter", methods=['GET', 'POST'])
def transform():
    # создание формы приложени
    form = WorkForm()
    # зашумленное изображение
    noiseimgfile = None
    # фильтрованное изображение
    filtimgfile = None
    col_r = None
    col_g = None
    col_b = None
    # обработка нажатия кнопки фильтрации
    if form.validate_on_submit():
        # указание размещения зашумленного изображения
        noiseimgfile = 'static/noiseimage.png'
        # указание размещения фильтрованного изображения
        filtimgfile = 'static/filterimage.png'
        # загрузка зашумленного изображения
        form.upload.data.save(noiseimgfile)
        # открытие зашумленного изображения
        noiseimg = Image.open(noiseimgfile)
        # вычисление распределения цветов картинки
        col_r = np.zeros(256)
        col_g = np.zeros(256)
        col_b = np.zeros(256)
        for i in range(noiseimg.size[0]):
            for j in range(noiseimg.size[1]):
                r, g, b = noiseimg.getpixel((i, j))
                col_r[r] += 1
                col_g[g] += 1
                col_b[b] += 1
        # выполнение фильтрации картинки
        filtimg = noiseimg.filter(ImageFilter.GaussianBlur(radius=float(form.filterparam.data)))
        # сохранение отфильтрованного изображения
        filtimg.save(filtimgfile)
    # возврат данных в шаблон веб-страницы
    return render_template('index.html', form=form, original=noiseimgfile, filtered=filtimgfile, valr=col_r, valg=col_g, valb=col_b)


# запуск приложения
if __name__ == "__main__":
    app.run()
