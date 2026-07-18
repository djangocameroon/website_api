from apps.users.serializers.general_serializers import ErrorResponseSerializer


class BlogNotFoundErrorResponse(ErrorResponseSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['message'].default = "Blog post not found"
        self.fields['status_code'].default = 404