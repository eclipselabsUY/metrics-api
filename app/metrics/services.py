from aiochclient import ChClient
from datetime import datetime
from typing import Optional
import json
import re


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

    await client.execute("""
        CREATE TABLE IF NOT EXISTS page_views (
            id UUID DEFAULT generateUUIDv4(),
            service_id UInt32,
            path String,
            referrer String,
            user_agent String,
            viewport String,
            document_title String,
            client_ip String,
            timestamp DateTime64(3) DEFAULT now()
        ) ENGINE = MergeTree()
        ORDER BY (timestamp, service_id, path)
    """)


async def create_event(client: ChClient, event_data: dict):
    metadata_json = json.dumps(event_data.get("metadata", {}), ensure_ascii=False)
    await client.execute(
        "INSERT INTO events (service_id, event_type, method, url, client_ip, metadata, timestamp) VALUES",
        query_params={
            "service_id": int(event_data.get("service_id", 0)),
            "event_type": _validate_string(event_data.get("event_type", ""), 255),
            "method": _validate_string(event_data.get("method", ""), 16),
            "url": _validate_string(event_data.get("url", ""), 2048),
            "client_ip": _validate_string(event_data.get("client_ip", ""), 45),
            "metadata": _validate_string(metadata_json, 65535),
            "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
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
    params = {}

    if service_id is not None:
        conditions.append("service_id = {service_id:UInt32}")
        params["service_id"] = int(service_id)

    if event_type:
        conditions.append("event_type = {event_type:String}")
        params["event_type"] = _validate_string(event_type, 255)

    if start_date:
        conditions.append("timestamp >= {start_date:DateTime64(3)}")
        params["start_date"] = start_date.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

    if end_date:
        conditions.append("timestamp <= {end_date:DateTime64(3)}")
        params["end_date"] = end_date.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

    where_clause = " AND ".join(conditions) if conditions else "1=1"

    query = f"""
        SELECT id, service_id, event_type, method, url, client_ip, metadata, timestamp
        FROM events
        WHERE {where_clause}
        ORDER BY timestamp DESC
        LIMIT {{limit:UInt32}} OFFSET {{offset:UInt32}}
    """
    params["limit"] = min(int(limit), 1000)
    params["offset"] = max(int(offset), 0)

    rows = await client.fetch(query, query_params=params)
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
        conditions.append("service_id = {service_id:UInt32}")
        params["service_id"] = int(service_id)

    if event_type:
        conditions.append("event_type = {event_type:String}")
        params["event_type"] = _validate_string(event_type, 255)

    if start_date:
        conditions.append("timestamp >= {start_date:DateTime64(3)}")
        params["start_date"] = start_date.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

    if end_date:
        conditions.append("timestamp <= {end_date:DateTime64(3)}")
        params["end_date"] = end_date.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

    where_clause = " AND ".join(conditions) if conditions else "1=1"

    query = f"SELECT count() FROM events WHERE {where_clause}"
    result = await client.fetchrow(query, query_params=params)
    return result[0] if result else 0


def _validate_string(value: str, max_length: int) -> str:
    if not isinstance(value, str):
        value = str(value)
    if len(value) > max_length:
        value = value[:max_length]
    return value


async def create_view_event(client: ChClient, view_data: dict):
    await client.execute(
        "INSERT INTO page_views (service_id, path, referrer, user_agent, viewport, document_title, client_ip, timestamp) VALUES",
        query_params={
            "service_id": int(view_data.get("service_id", 0)),
            "path": _validate_string(view_data.get("path", ""), 2048),
            "referrer": _validate_string(view_data.get("referrer", ""), 2048),
            "user_agent": _validate_string(view_data.get("user_agent", ""), 512),
            "viewport": _validate_string(view_data.get("viewport", ""), 20),
            "document_title": _validate_string(
                view_data.get("document_title", ""), 512
            ),
            "client_ip": _validate_string(view_data.get("client_ip", ""), 45),
            "timestamp": view_data.get(
                "timestamp", datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
            ),
        },
    )


async def get_views(
    client: ChClient,
    limit: int = 100,
    offset: int = 0,
    service_id: Optional[int] = None,
    path: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
):
    conditions = []
    params = {}

    if service_id is not None:
        conditions.append("service_id = {service_id:UInt32}")
        params["service_id"] = int(service_id)

    if path:
        conditions.append("path = {path:String}")
        params["path"] = _validate_string(path, 2048)

    if start_date:
        conditions.append("timestamp >= {start_date:DateTime64(3)}")
        params["start_date"] = start_date.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

    if end_date:
        conditions.append("timestamp <= {end_date:DateTime64(3)}")
        params["end_date"] = end_date.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

    where_clause = " AND ".join(conditions) if conditions else "1=1"

    query = f"""
        SELECT id, service_id, path, referrer, user_agent, viewport, document_title, client_ip, timestamp
        FROM page_views
        WHERE {where_clause}
        ORDER BY timestamp DESC
        LIMIT {{limit:UInt32}} OFFSET {{offset:UInt32}}
    """
    params["limit"] = min(int(limit), 1000)
    params["offset"] = max(int(offset), 0)

    rows = await client.fetch(query, query_params=params)
    return [
        {
            "id": row[0],
            "service_id": row[1],
            "path": row[2],
            "referrer": row[3],
            "user_agent": row[4],
            "viewport": row[5],
            "document_title": row[6],
            "client_ip": row[7],
            "timestamp": row[8],
        }
        for row in rows
    ]


async def get_view_stats(
    client: ChClient,
    service_id: Optional[int] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
) -> dict:
    conditions = []
    params = {}

    if service_id is not None:
        conditions.append("service_id = {service_id:UInt32}")
        params["service_id"] = int(service_id)

    if start_date:
        conditions.append("timestamp >= {start_date:DateTime64(3)}")
        params["start_date"] = start_date.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

    if end_date:
        conditions.append("timestamp <= {end_date:DateTime64(3)}")
        params["end_date"] = end_date.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

    where_clause = " AND ".join(conditions) if conditions else "1=1"

    total_query = f"SELECT count() FROM page_views WHERE {where_clause}"
    total_result = await client.fetchrow(total_query, query_params=params)
    total_views = total_result[0] if total_result else 0

    unique_query = f"SELECT uniqExact(client_ip) FROM page_views WHERE {where_clause}"
    unique_result = await client.fetchrow(unique_query, query_params=params)
    unique_visitors = unique_result[0] if unique_result else 0

    by_path_query = f"""
        SELECT path, count() as cnt
        FROM page_views
        WHERE {where_clause}
        GROUP BY path
        ORDER BY cnt DESC
        LIMIT 20
    """
    by_path_rows = await client.fetch(by_path_query, query_params=params)
    views_by_path = {row[0]: row[1] for row in by_path_rows}

    by_ref_query = f"""
        SELECT referrer, count() as cnt
        FROM page_views
        WHERE {where_clause} AND referrer != ''
        GROUP BY referrer
        ORDER BY cnt DESC
        LIMIT 20
    """
    by_ref_rows = await client.fetch(by_ref_query, query_params=params)
    top_referrers = {row[0]: row[1] for row in by_ref_rows}

    return {
        "total_views": total_views,
        "unique_visitors": unique_visitors,
        "views_by_path": views_by_path,
        "top_referrers": top_referrers,
    }


async def get_view_count(
    client: ChClient,
    service_id: Optional[int] = None,
    path: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
) -> int:
    conditions = []
    params = {}

    if service_id is not None:
        conditions.append("service_id = {service_id:UInt32}")
        params["service_id"] = int(service_id)

    if path:
        conditions.append("path = {path:String}")
        params["path"] = _validate_string(path, 2048)

    if start_date:
        conditions.append("timestamp >= {start_date:DateTime64(3)}")
        params["start_date"] = start_date.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

    if end_date:
        conditions.append("timestamp <= {end_date:DateTime64(3)}")
        params["end_date"] = end_date.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

    where_clause = " AND ".join(conditions) if conditions else "1=1"

    query = f"SELECT count() FROM page_views WHERE {where_clause}"
    result = await client.fetchrow(query, query_params=params)
    return result[0] if result else 0
