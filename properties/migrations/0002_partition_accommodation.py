# File: properties/migrations/0002_partition_accommodation.py

from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('properties', '0001_initial'),  # Replace with the actual previous migration
    ]

    operations = [
        migrations.RunSQL(
            sql="""
            -- Drop existing table if it exists
            DROP TABLE IF EXISTS properties_accommodation CASCADE;

            -- Create parent table with partitioning
            CREATE TABLE properties_accommodation (
                id VARCHAR(20),
                feed SMALLINT NOT NULL,
                title VARCHAR(100) NOT NULL,
                country_code CHAR(2) NOT NULL,
                bedroom_count INTEGER NOT NULL,
                review_score NUMERIC(3, 1) DEFAULT 0,
                usd_rate NUMERIC(10, 2) NOT NULL,
                center GEOMETRY(Point, 4326) NOT NULL,
                amenities JSONB,
                user_id INTEGER,
                location_id VARCHAR(20) NOT NULL,
                published BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP WITH TIME ZONE NOT NULL,
                updated_at TIMESTAMP WITH TIME ZONE NOT NULL,
                
                -- Primary key now includes feed
                PRIMARY KEY (id, feed),
                
                -- Add foreign key constraints
                FOREIGN KEY (user_id) REFERENCES auth_user(id),
                FOREIGN KEY (location_id) REFERENCES properties_location(id)
            ) PARTITION BY RANGE (feed);

            -- Create partition ranges
            -- Example partitions, adjust based on your expected feed ranges
            CREATE TABLE properties_accommodation_feed_0_1000 
                PARTITION OF properties_accommodation
                FOR VALUES FROM (0) TO (1000);

            CREATE TABLE properties_accommodation_feed_1001_5000 
                PARTITION OF properties_accommodation
                FOR VALUES FROM (1001) TO (5000);

            CREATE TABLE properties_accommodation_feed_5001_10000 
                PARTITION OF properties_accommodation
                FOR VALUES FROM (5001) TO (10000);

            -- Optional: Add a default partition for feeds outside specified ranges
            CREATE TABLE properties_accommodation_feed_default 
                PARTITION OF properties_accommodation DEFAULT;

            -- Recreate indexes
            CREATE INDEX idx_accommodation_feed ON properties_accommodation (feed);
            CREATE INDEX idx_accommodation_location ON properties_accommodation (location_id);
            CREATE INDEX idx_accommodation_user ON properties_accommodation (user_id);
            CREATE INDEX idx_accommodation_created_at ON properties_accommodation (created_at);
            """,
            reverse_sql="""
            -- Reverse the partitioning
            DROP TABLE IF EXISTS properties_accommodation CASCADE;
            
            -- Recreate the original table if needed
            CREATE TABLE properties_accommodation (
                id VARCHAR(20) PRIMARY KEY,
                feed SMALLINT NOT NULL,
                title VARCHAR(100) NOT NULL,
                -- Add other columns as necessary
            );
            """
        )
    ]