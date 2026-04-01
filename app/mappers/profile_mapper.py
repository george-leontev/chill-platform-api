from data_models.profile_data_model import Profile
from models.profile_model import ProfileModel, CreateOrUpdateProfileModel, UserInfoInputModel
from models.user_info_model import UserInfoModel
from datetime import date


class ProfileMapper:
    @staticmethod
    def _calculate_age(birth_date: date) -> int:
        today = date.today()
        age = today.year - birth_date.year
        if (today.month, today.day) < (birth_date.month, birth_date.day):
            age -= 1
        return age

    @staticmethod
    def to_model(profile: Profile) -> ProfileModel:
        user_info = None
        if hasattr(profile, 'user') and profile.user:
            user_info = UserInfoModel(
                id=profile.user.id,
                username=profile.user.username,
                first_name=profile.user.first_name,
                last_name=profile.user.last_name,
                email=profile.user.email
            )

        calculated_age = None
        if profile.birth_date:
            calculated_age = ProfileMapper._calculate_age(profile.birth_date.date())

        result = ProfileModel(
            id=profile.id,
            user_id=profile.user_id,
            user=user_info,
            avatar_url=profile.avatar_url,
            bio=profile.bio,
            phone=profile.phone,
            location=profile.location,
            birth_date=profile.birth_date,
            gender=profile.gender,
            age=calculated_age,
            created_at=profile.created_at,
            updated_at=profile.updated_at
        )

        return result

    @staticmethod
    def from_input_model(model: CreateOrUpdateProfileModel) -> dict:
        return {
            "avatar_url": model.avatar_url,
            "bio": model.bio,
            "phone": model.phone,
            "location": model.location,
            "birth_date": model.birth_date,
            "gender": model.gender,
        }

    @staticmethod
    def from_user_input_model(model: UserInfoInputModel) -> dict:
        return {
            "username": model.username,
            "first_name": model.first_name,
            "last_name": model.last_name,
        }
