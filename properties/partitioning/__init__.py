from django.db import connections

PARTITION_TABLES = {
    'en': 'localize_accommodation_en',
    'ar': 'localize_accommodation_ar',
    'fr': 'localize_accommodation_fr',
    'de': 'localize_accommodation_de',
}

def insert_into_partition(instance):
    """
    Insert the instance into the correct partition based on the language.
    """
    language = instance.language
    table_name = PARTITION_TABLES.get(language)

    if table_name:
        with connections['default'].cursor() as cursor:
            cursor.execute(
                f"""
                INSERT INTO {table_name} (accommodation_id, language, description, policy)
                VALUES (%s, %s, %s, %s)
                """,
                [instance.accommodation_id, instance.language, instance.description, instance.policy]
            )
    else:
        raise ValueError(f"No partition defined for language '{language}'")
