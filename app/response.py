class DefaultResponse:
    def __init__(self, success=True, data=None, errors=None):
        self.success = success
        self.errors = errors
        self.data = data

    def to_response(self):
        extra = {}
        if not self.success:
            extra['errors'] = self.errors
        return {
            "success": self.success,
            "results": self.data,
            **extra
        }


class NotificationResponse(DefaultResponse):
    def __init__(self, next_page_token = None, **kwargs):
        super(NotificationResponse, self).__init__(**kwargs)
        self.page_token = next_page_token

    def to_response(self):
        data = super(NotificationResponse, self).to_response()
        return {
            "next_page_token": self.page_token,
            "count": len(self.data),
            **data
        }
