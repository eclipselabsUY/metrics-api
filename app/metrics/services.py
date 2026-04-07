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
        f"""
        INSERT INTO events (service_id, event_type, method, url, client_ip, metadata, timestamp)
        VALUES ({int(event_data.get("service_id", 0))}, '{_esc(event_data.get("event_type", ""))}', '{_esc(event_data.get("method", ""))}', '{_esc(event_data.get("url", ""))}', '{_esc(event_data.get("client_ip", ""))}', '{_esc(str(event_data.get("metadata", {})))}', now())
        """
    )


def _esc(s: str) -> str:
    return s.replace("'", "\\'").replace("\\", "\\\\")


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

    if service_id is not None:
        conditions.append(f"service_id = {int(service_id)}")

    if event_type:
        conditions.append(f"event_type = '{_esc(event_type)}'")

    if start_date:
        conditions.append(f"timestamp >= '{start_date}'")

    if end_date:
        conditions.append(f"timestamp <= '{end_date}'")

    where_clause = " AND ".join(conditions) if conditions else "1=1"

    query = f"""
        SELECT id, service_id, event_type, method, url, client_ip, metadata, timestamp
        FROM events
        WHERE {where_clause}
        ORDER BY timestamp DESC
        LIMIT {int(limit)} OFFSET {int(offset)}
    """

    rows = await client.fetch(query)
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

    if service_id is not None:
        conditions.append(f"service_id = {int(service_id)}")

    if event_type:
        conditions.append(f"event_type = '{_esc(event_type)}'")

    if start_date:
        conditions.append(f"timestamp >= '{start_date}'")

    if end_date:
        conditions.append(f"timestamp <= '{end_date}'")

    where_clause = " AND ".join(conditions) if conditions else "1=1"

    query = f"SELECT count() FROM events WHERE {where_clause}"
    result = await client.fetchrow(query)
    return result[0] if result else 0
