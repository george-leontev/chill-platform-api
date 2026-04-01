from sqlalchemy.orm import Session, joinedload
from data_models.profile_data_model import Profile
from data_models.user_data_model import User


class ProfileRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_by_user_id(self, user_id: int) -> Profile | None:
        profile = self.db_session.query(Profile).options(
            joinedload(Profile.user)
        ).filter(Profile.user_id == user_id).one_or_none()

        return profile

    def get_by_id(self, profile_id: int) -> Profile | None:
        profile = self.db_session.query(Profile).options(
            joinedload(Profile.user)
        ).filter(Profile.id == profile_id).one_or_none()

        return profile

    def create(self, user_id: int, profile_data: dict) -> Profile:
        profile = Profile(user_id=user_id, **profile_data)

        self.db_session.add(profile)
        self.db_session.commit()
        self.db_session.refresh(profile)

        return profile

    def update(self, profile: Profile, profile_data: dict) -> Profile:
        for key, value in profile_data.items():
            setattr(profile, key, value)

        self.db_session.commit()
        self.db_session.refresh(profile)

        return profile

    def update_user(self, user: User, user_data: dict) -> User:
        for key, value in user_data.items():
            if value is not None:
                setattr(user, key, value)

        self.db_session.commit()
        self.db_session.refresh(user)

        return user

    def delete(self, profile: Profile) -> Profile:
        self.db_session.delete(profile)
        self.db_session.commit()

        return profile
