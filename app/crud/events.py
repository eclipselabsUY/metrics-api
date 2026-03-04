from fastapi import Request, Depends
from fastcrud import crud_router, EndpointCreator, FastCRUD
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_async_db
from app.schemas.event import EventCreate, EventRead, EventUpdate
from app.models.event import Event


class EventEndpointCreator(EndpointCreator):
    def _create_event_auto_ip(self):
        async def create_event(
            request: Request,
            data: EventCreate,
            db: AsyncSession = Depends(get_async_db),
        ):
            from datetime import datetime

            client_ip = request.client.host if request.client else ""

            # Crear con timestamp explícito
            event = Event(
                event_type_id=data.event_type_id,
                client_ip=client_ip,
                event_metadata=data.event_metadata or {},
                timestamp=datetime.utcnow(),
            )
            db.add(event)
            await db.commit()
            await db.refresh(event)

            # Recargar desde BD para cargar relaciones
            result = await db.execute(select(Event).where(Event.id == event.id))
            event = result.scalars().unique().one()
            return event

        return create_event

    def add_routes_to_router(
        self,
        create_deps=[],
        read_deps=[],
        read_multi_deps=[],
        update_deps=[],
        delete_deps=[],
        db_delete_deps=[],
        included_methods=None,
        deleted_methods=None,
        **kwargs,
    ):
        self.router.add_api_route(
            path="/create",
            endpoint=self._create_event_auto_ip(),
            methods=["POST"],
            response_model=EventRead,
            tags=self.tags,
            dependencies=[Depends(dep) for dep in create_deps] if create_deps else [],
        )

        super().add_routes_to_router(
            create_deps=create_deps,
            read_deps=read_deps,
            read_multi_deps=read_multi_deps,
            update_deps=update_deps,
            delete_deps=delete_deps,
            db_delete_deps=db_delete_deps,
            included_methods=included_methods,
            deleted_methods=deleted_methods,
        )


event_crud = FastCRUD(Event)

event_router = crud_router(
    session=get_async_db,
    model=Event,
    create_schema=EventCreate,
    update_schema=EventUpdate,
    select_schema=EventRead,
    crud=event_crud,
    path="",
    endpoint_creator=EventEndpointCreator,
    endpoint_names={
        "read": "get",
        "read_multi": "get",
        "update": "update",
        "delete": "delete",
    },
    deleted_methods=["create"],
    tags=["Event"],
)
