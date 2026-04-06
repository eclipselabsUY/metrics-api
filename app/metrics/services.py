from aiochclient import ChClient
from datetime import datetime
from typing import Optional


async def init_clickhouse(client: ChClient):
    await client.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id UUID DEFAULT generateUUIDv4(),
            service_id UInt32,
            event_type String,
            method String,
            url String,
            client_ip String,
            metadata String,
            timestamp DateTime64(3) DEFAULT now()
        ) ENGINE = MergeTree()
        ORDER BY (timestamp, service_id, event_type)
    """)


async def create_event(client: ChClient, event_data: dict):
    await client.execute(
        """
        INSERT INTO events (service_id, event_type, method, url, client_ip, metadata, timestamp)
        VALUES (%(service_id)s, %(event_type)s, %(method)s, %(url)s, %(client_ip)s, %(metadata)s, %(timestamp)s)
        """,
        {
            "service_id": event_data.get("service_id", 0),
            "event_type": event_data.get("event_type", ""),
            "method": event_data.get("method", ""),
            "url": event_data.get("url", ""),
            "client_ip": event_data.get("client_ip", ""),
            "metadata": str(event_data.get("metadata", {})),
            "timestamp": datetime.utcnow(),
        },
    )


async def get_events(
    client: ChClient,
    limit: int = 100,
    offset: int = 0,
    service_id: Optional[int] = None,
    event_type: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
):
    conditions = []
    params = {"limit": limit, "offset": offset}

    if service_id is not None:
        conditions.append("service_id = %(service_id)s")
        params["service_id"] = service_id

    if event_type:
        conditions.append("event_type = %(event_type)s")
        params["event_type"] = event_type

    if start_date:
        conditions.append("timestamp >= %(start_date)s")
        params["start_date"] = start_date

    if end_date:
        conditions.append("timestamp <= %(end_date)s")
        params["end_date"] = end_date

    where_clause = " AND ".join(conditions) if conditions else "1=1"

    query = f"""
        SELECT id, service_id, event_type, method, url, client_ip, metadata, timestamp
        FROM events
        WHERE {where_clause}
        ORDER BY timestamp DESC
        LIMIT %(limit)s OFFSET %(offset)s
    """

    rows = await client.fetch(query, params)
    return [
        {
            "id": row[0],
            "service_id": row[1],
            "event_type": row[2],
            "method": row[3],
            "url": row[4],
            "client_ip": row[5],
            "metadata": row[6],
            "timestamp": row[7],
        }
        for row in rows
    ]


async def get_event_count(
    client: ChClient,
    service_id: Optional[int] = None,
    event_type: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
) -> int:
    conditions = []
    params = {}

    if service_id is not None:
        conditions.append("service_id = %(service_id)s")
        params["service_id"] = service_id

    if event_type:
        conditions.append("event_type = %(event_type)s")
        params["event_type"] = event_type

    if start_date:
        conditions.append("timestamp >= %(start_date)s")
        params["start_date"] = start_date

    if end_date:
        conditions.append("timestamp <= %(end_date)s")
        params["end_date"] = end_date

    where_clause = " AND ".join(conditions) if conditions else "1=1"

    query = f"SELECT count() FROM events WHERE {where_clause}"
    result = await client.fetchrow(query, params)
    return result[0] if result else 0
