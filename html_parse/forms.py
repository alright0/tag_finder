from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.fields.html5 import URLField
from wtforms.validators import DataRequired, url
from html_parse.models import Main


class InputForm(FlaskForm):
    """Форма ввода данных для ссылок"""

    link = URLField("Введите URL(Полностью):", validators=[DataRequired(), url()])
    submit = SubmitField("Отправить ссылку")


class TagsForm(FlaskForm):
    """Форма ввода данных для id ссылок"""

    id = IntegerField("Введите ID ссылки:", validators=[DataRequired()])
    submit = SubmitField("Получить список тегов")

    def validate_id(self, id):
        """Проверка на попадание числа в диапазон идентификаторов"""

        max_id = Main.query.order_by(Main.id.desc()).first()
        min_id = Main.query.order_by(Main.id).first()

        if max_id is None:
            raise ValueError(f"В БД нет записей")
        else:
            if id.data > max_id.id or id.data < min_id.id or not id.data:
                raise ValueError(
                    f"Идентификатор должен быть в пределах от {min_id.id} до {max_id.id}"
                )
