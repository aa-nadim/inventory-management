from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0002_partition_accommodation'),
    ]

    operations = [
        migrations.RunSQL(
            """
            -- Drop the existing primary key constraint if any
            DROP TABLE IF EXISTS properties_localizeaccommodation CASCADE;

            -- Create a new partitioned table with the correct primary key
            CREATE TABLE properties_localizeaccommodation (
                id SERIAL NOT NULL,
                accommodation_id CHAR(20) NOT NULL,  -- Ensure this is the correct type for accommodation_id
                language CHAR(2) NOT NULL,  -- Ensure that language is consistent with partitioning
                description TEXT,
                policy JSONB,
                PRIMARY KEY (id, language)  -- Include language in the primary key
            ) PARTITION BY LIST (language);


            -- Create partitions for different languages (ensure lowercase language codes)
            CREATE TABLE properties_localizeaccommodation_en PARTITION OF properties_localizeaccommodation FOR VALUES IN ('en');
            CREATE TABLE properties_localizeaccommodation_ar PARTITION OF properties_localizeaccommodation FOR VALUES IN ('ar');
            CREATE TABLE properties_localizeaccommodation_fr PARTITION OF properties_localizeaccommodation FOR VALUES IN ('fr');
            CREATE TABLE properties_localizeaccommodation_de PARTITION OF properties_localizeaccommodation FOR VALUES IN ('de');
            -- Add more partitions if needed for other languages (e.g., 'es', 'it', etc.)
            """
        )
    ]
