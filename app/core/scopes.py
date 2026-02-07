from app.core.enums import ServiceKind

SERVICE_KIND_SCOPES: dict[ServiceKind, set[str]] = {
    ServiceKind.FRONTEND: {
        "metrics:write",
    },
    ServiceKind.BACKEND: {
        "metrics:write",
        "metrics:read",
        "events:write",
    },
}