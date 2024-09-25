import logging
from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
from utils.api_response import APIResponse
from .serializers import ItemInputSerializer, ItemOutputSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from django.db import IntegrityError
from . import services

logger = logging.getLogger(__name__)


class ItemView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ItemInputSerializer(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data.get("name")
            check_item = services.get_item_by_name(name=name)
            if check_item:
                logger.error(
                    f"An item with the name '{name}' already exists.",
                )
                return APIResponse.error(
                    f"An item with the name '{name}' already exists.",
                    status_code=status.HTTP_400_BAD_REQUEST,
                )
            try:
                item = services.create_item(serializer.validated_data)
                output_serializer = ItemOutputSerializer(item)
                logger.info("New Item added")
                return APIResponse.success(
                    "Record added successfully",
                    data=output_serializer.data,
                    status_code=status.HTTP_201_CREATED,
                )
            except ValidationError as e:
                logger.warning(f"Validation error during item creation: {str(e)}")
                return APIResponse.error(
                    str(e),
                    status_code=status.HTTP_400_BAD_REQUEST,
                )
            except Exception as e:
                logger.error(f"Unexpected error during item creation: {str(e)}")
                return APIResponse.error(
                    "An unexpected error occurred: " + str(e),
                    status_code=status.HTTP_400_BAD_REQUEST,
                )
        logger.warning(f"Invalid data received: {serializer.errors}")
        return APIResponse.error(
            "Validation error",
            data=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    def get(self, request, item_id):
        try:
            item = services.get_item_by_id(item_id)
            serializer = ItemOutputSerializer(item)
            logger.info(f"Item with ID {item_id} fetched successfully.")
            return APIResponse.success(
                "Record fetched successfully",
                data=serializer.data,
                status_code=status.HTTP_200_OK,
            )
        except Http404 as e:
            logger.error(f"Item with ID {item_id} not found.")
            return APIResponse.error(
                str(e),
                status_code=status.HTTP_404_NOT_FOUND,
            )
        except ValueError as e:
            logger.warning(
                f"Value error while fetching item with ID {item_id}: {str(e)}"
            )
            return APIResponse.error(
                str(e),
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            logger.error(
                f"Unexpected error during fetching item with ID {item_id}: {str(e)}"
            )
            return APIResponse.error(
                "An unexpected error occurred: " + str(e),
                status_code=status.HTTP_400_BAD_REQUEST,
            )

    def put(self, request, item_id):
        try:
            item = services.get_item_by_id(id=item_id)
            serializer = ItemInputSerializer(item, data=request.data)
            if serializer.is_valid(raise_exception=True):
                item = services.update_item(
                    item_id=item_id, data=serializer.validated_data
                )
                output_serializer = ItemOutputSerializer(item)
                logger.info(f"Item with ID {item_id} updated successfully.")
                return APIResponse.success(
                    "Record fetched successfully",
                    data=output_serializer.data,
                    status_code=status.HTTP_200_OK,
                )
        except Http404 as e:
            logger.error(f"Item with ID {item_id} not found.")
            return APIResponse.error(
                str(e),
                status_code=status.HTTP_404_NOT_FOUND,
            )
        except ValidationError as e:
            logger.warning(
                f"Validation error during update of item ID {item_id}: {str(e)}"
            )
            return APIResponse.error(
                str(e),
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        except IntegrityError as e:
            logger.error(
                f"Integrity error during update of item ID {item_id}: {str(e)}"
            )
            return APIResponse.error(
                str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        except Exception as e:
            logger.error(
                f"Unexpected error during update of item ID {item_id}: {str(e)}"
            )
            return APIResponse.error(
                str(e),
                status_code=status.HTTP_400_BAD_REQUEST,
            )

    def delete(self, request, item_id):
        try:
            response = services.delete_item(item_id)
            logger.info(f"Item with ID {item_id} deleted successfully.")
            return APIResponse.success(
                "Record deleted successfully",
                data=response,
                status_code=status.HTTP_204_NO_CONTENT,
            )
        except Http404:
            logger.error(f"Item with ID {item_id} not found.")
            return APIResponse.error(
                "Item not found",
                status_code=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            logger.error(
                f"Unexpected error during deletion of item ID {item_id}: {str(e)}"
            )
            return APIResponse.error(
                str(e),
                status_code=status.HTTP_400_BAD_REQUEST,
            )
