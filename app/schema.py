from marshmallow import Schema, fields


class NotificationSchema(Schema):
    message = fields.String()
    img_url = fields.String(required=False, allow_none=True)
    id = fields.UUID()

    class Meta:
        fields = ('message', 'img_url', 'id')


class UserNotificationSchema(Schema):
    user_id = fields.Integer()
    lesson_id = fields.Integer()
    show_after = fields.DateTime()
    read = fields.Boolean()
    notification = fields.Nested(NotificationSchema, required=False)


default_schema = UserNotificationSchema()
ntf_schema = NotificationSchema()