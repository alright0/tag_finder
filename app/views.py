from flask.templating import render_template
from marshmallow import fields
from flask_apispec import marshal_with, use_kwargs
from flask import Blueprint, jsonify, request
from app.schemas import LinkSchema
from app.logic import count_tags
from app.models import Main
from app.forms import InputForm, TagsForm
from app import docs

link_parser = Blueprint("link_parser", __name__)
ui = Blueprint("user-interface", __name__)


@link_parser.route("/api/send", methods=["POST"])
@use_kwargs({"link": fields.Url()})
@marshal_with(LinkSchema)
def send_a_link(**kwargs):
    """API функция принимает POST запрос клиента на запись в базу"""
    try:
        new_record = Main(**kwargs)
        new_record.save()

        return new_record, 200
    except Exception as e:
        return jsonify({"error": e}), 400


@link_parser.route("/api/<int:link_id>", methods=["GET"])
def get_tags(link_id):
    """API функция принимает id и возвращает json c уникальными тегами"""

    try:
        answer = Main.query.filter(Main.id == link_id).first()
        tags_answer, status_code = count_tags(answer.link)

        return tags_answer, status_code

    except Exception as e:
        return {"error": str(e)}, 400


@ui.route("/", methods=["GET", "POST"])
@ui.route("/index", methods=["GET", "POST"])
def send_link_in_browser():
    """Эта форма принимает ссылку и возвращает уникальный идентификатор записи"""

    input_form = InputForm()

    if request.method == "POST":
        if input_form.validate_on_submit():

            new_rec = Main(**{"link": input_form.link.data})
            new_rec.save()

            returned_id = f"Уникальный идентификатор ссылки: {new_rec.id}"

            return render_template("index.html", form=input_form, id=returned_id)

    return render_template("index.html", form=input_form, id="")


@ui.route("/tags", methods=["GET", "POST"])
def read_tags_in_browser():
    """Эта форма принимает номер записи и возвращает список уникальных тегов"""

    tags_form = TagsForm()

    if request.method == "POST":
        if tags_form.validate_on_submit():

            answer = Main.query.filter(Main.id == tags_form.id.data).first()
            if answer:

                tags_answer, status_code = count_tags(answer.link)
                link = f"Ссылка: {answer.link}"

            return render_template(
                "/tags.html",
                form=tags_form,
                tags_answer=tags_answer,
                link=link,
                status_code=status_code,
            )

    return render_template(
        "/tags.html",
        form=tags_form,
        tags_answer="",
        link="",
        status_code="",
    )


docs.register(send_a_link, blueprint="link_parser")
docs.register(get_tags, blueprint="link_parser")
