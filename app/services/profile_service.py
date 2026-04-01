from http import HTTPStatus
from fastapi import HTTPException
from mappers.profile_mapper import ProfileMapper
from models.profile_model import ProfileModel, CreateOrUpdateProfileModel
from repositories.profile_repository import ProfileRepository


class ProfileService:
    def __init__(self, profile_repository: ProfileRepository):
        self.profile_repository = profile_repository
        self.mapper = ProfileMapper()

    def get_profile(self, user_id: int) -> ProfileModel:
        profile = self.profile_repository.get_by_user_id(user_id)

        if not profile:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Профиль не найден.")

        result = self.mapper.to_model(profile)

        return result

    def get_profile_by_id(self, profile_id: int) -> ProfileModel:
        profile = self.profile_repository.get_by_id(profile_id)

        if not profile:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Профиль не найден.")

        result = self.mapper.to_model(profile)

        return result

    def create_profile(self, user_id: int, profile_data: CreateOrUpdateProfileModel) -> ProfileModel:
        existing = self.profile_repository.get_by_user_id(user_id)

        if existing:
            raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="Профиль уже существует.")

        data = self.mapper.from_input_model(profile_data)
        profile = self.profile_repository.create(user_id, data)

        result = self.mapper.to_model(profile)

        return result

    def update_profile(self, user_id: int, profile_data: CreateOrUpdateProfileModel) -> ProfileModel:
        profile = self.profile_repository.get_by_user_id(user_id)

        if not profile:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Профиль не найден.")

        # Update profile fields
        data = self.mapper.from_input_model(profile_data)
        updated_profile = self.profile_repository.update(profile, data)

        # Update user fields if provided
        if profile_data.user:
            user_data = self.mapper.from_user_input_model(profile_data.user)
            self.profile_repository.update_user(profile.user, user_data)

        # Refresh to get updated user data
        updated_profile = self.profile_repository.get_by_user_id(user_id)

        result = self.mapper.to_model(updated_profile)

        return result

    def delete_profile(self, user_id: int) -> ProfileModel:
        profile = self.profile_repository.get_by_user_id(user_id)

        if not profile:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Профиль не найден.")

        deleted = self.profile_repository.delete(profile)

        result = self.mapper.to_model(deleted)

        return result
