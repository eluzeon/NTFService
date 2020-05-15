from flask_restful import Resource
from flask import request

from app.forms import ListForm, PostForm
from app.notification import for_user, create_notification
from app.response import NotificationResponse
from app.schema import default_schema, ntf_schema



class NotificationResource(Resource):
    def get(self):
        form = ListForm(request.args)
        if not form.validate():
            return form.errors, 400
        data, page_token = for_user(form.user_id.data, True, form.page_token.data)
        rsp = NotificationResponse(page_token, data=default_schema.dump(data, many=True))
        return rsp.to_response(), 200

    def post(self):
        form = PostForm.from_json(request.json)
        if not form.validate():
            return form.errors, 400
        ntf = create_notification(
            form.user_ids.data,
            form.message.data,
            form.img_url.data,
            form.show_at.data,
            form.lesson_id.data,
            form.expire.data)
        return ntf_schema.dump(ntf), 200