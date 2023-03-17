import asyncio
import time

from api.database.cosmo_db import form_submits_container

SECONDS_IN_ONE_DAY = 24 * 60 * 60


async def delete_expired_form_submissions():
    """
    Background task that runs daily, to delete submissions that are past the data retention period.
    """

    query = """SELECT form.id, form.submission_expiration_time FROM c form"""

    while True:
        # Fetch all the submissions from the database
        results = form_submits_container.query_items(query=query,
                                                     enable_cross_partition_query=True)

        items = list(results)

        # Get the current time
        current_time = int(time.time())

        # Delete all the expired submissions
        for item in items:
            if item['submission_expiration_time'] <= current_time:
                form_submits_container.delete_item(item)

        await asyncio.sleep(SECONDS_IN_ONE_DAY)
