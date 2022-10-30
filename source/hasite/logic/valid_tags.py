from django.core.exceptions import ValidationError


def is_valid(tags):
    data = tags.cleaned_data['post_tag']
    if len(data.split(",")) > 3:
        raise ValidationError("No more than 3 tags")
    return True
