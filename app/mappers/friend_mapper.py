from data_models.friend_data_model import Friend
from models.friend_model import FriendModel, FriendsModel


class FriendMapper:
    @staticmethod
    def to_model(friend: Friend) -> FriendModel:
        result = FriendModel(
            id=friend.id,
            user_id=friend.user_id,
            friend_id=friend.friend_id,
            status_id=friend.status_id,
            created_at=friend.created_at
        )

        return result

    @staticmethod
    def to_list_model(friends: list[Friend]) -> FriendsModel:
        result = FriendsModel(
            items=[FriendMapper.to_model(friend) for friend in friends]
        )

        return result