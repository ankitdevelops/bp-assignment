import logging
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.http import Http404
from .models import Item
from django.utils.text import slugify
from django.core.cache import cache


def get_item_by_name(name=None):

    if name is None:
        return None
    slug = slugify(name)
    cache_key = f"items:slug:{slug}"
    item = cache.get(cache_key)
    if item is not None:
        return item
    item = None
    try:
        item = Item.objects.get(slug=slug)
        cache.set(cache_key, item, timeout=3600)
        return item
    except Item.DoesNotExist:
        return None
    except Exception as e:

        print("Error: ", str(e))
        return None


def get_item_by_id(id=None):
    if id is None:
        raise ValueError("Item ID must be provided.")

    # TODO: hanlde cache error
    cache_key = f"items:id:{id}"
    item = cache.get(cache_key)
    if item is not None:
        return item

    try:
        item = Item.objects.get(id=id)
        cache.set(cache_key, item, timeout=3600)
        return item
    except Item.DoesNotExist:
        raise Http404("Item does not exist")
    except Exception as e:
        raise Exception("An unexpected error occurred: " + str(e))


def create_item(data):
    try:
        slug = slugify(data["name"])
        item = Item(
            name=data["name"],
            slug=slug,
            description=data["description"],
            quantity=data["quantity"],
        )
        item.save()
        cache_key_id = f"items:id:{item.id}"
        cache_key_slug = f"items:slug:{slug}"
        cache.set(cache_key_id, item, timeout=3600)
        cache.set(
            cache_key_slug,
            item,
            timeout=3600,
        )
        return item
    except IntegrityError as e:
        raise ValidationError("Database error: " + str(e))
    except Exception as e:
        raise Exception("An unexpected error occurred: " + str(e))


def update_item(item_id, data):
    try:
        item = get_item_by_id(item_id)
        old_slug = item.slug
        item.name = data.get("name", item.name)
        item.description = data.get("description", item.description)
        item.quantity = data.get("quantity", item.quantity)
        item.save()

        cache_key_id = f"items:id:{item.id}"
        cache_key_new_slug = f"items:slug:{item.slug}"
        cache.set(cache_key_id, item, timeout=3600)
        cache.set(
            cache_key_new_slug,
            item,
            timeout=3600,
        )

        if old_slug != item.slug:
            cache_key_old_slug = f"items:slug:{old_slug}"
            cache.delete(cache_key_old_slug)

        return item
    except IntegrityError as e:
        raise ValidationError("Database error: " + str(e))
    except Exception as e:
        raise Exception("An unexpected error occurred: " + str(e))


def delete_item(item_id):
    try:
        item = get_item_by_id(item_id)
        item.delete()

        cache_key_id = f"items:id:{item_id}"
        cache_key_slug = f"items:slug:{item.slug}"
        cache.delete(cache_key_id)
        cache.delete(cache_key_slug)

        return {"message": "Item deleted successfully."}
    except Http404:
        raise
    except Exception as e:
        raise Exception("An unexpected error occurred: " + str(e))
