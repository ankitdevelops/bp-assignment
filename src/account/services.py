import logging
from django.contrib.auth.models import User
from django.db import IntegrityError

logger = logging.getLogger(__name__)


def create_user(username, email, password):
    try:
        user = User.objects.create_user(
            username=username, email=email, password=password
        )
        logger.info(f"User created successfully: {username}")
        return user, None
    except IntegrityError as e:
        logger.error(f"Error creating user: {str(e)}")
        return None, "Failed to create user due to a database error."
    except Exception as e:
        logger.error(f"Unexpected error in create_user: {str(e)}")
        return None, "An unexpected error occurred."
