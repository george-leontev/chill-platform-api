from models.app_base_model import AppBaseModel

class StatsModel(AppBaseModel):
    users_count: int
    posts_count: int
    messages_count: int
    friends_count: int
