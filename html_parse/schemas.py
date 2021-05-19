from marshmallow import Schema, validate, fields


class LinkSchema(Schema):
    """Простейшая схема присваивания уникальных значений ссылкам"""

    id = fields.Integer(dump_only=True)
    link = fields.Url(dump_only=True)
