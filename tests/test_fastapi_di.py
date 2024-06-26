import typing

import fastapi
from starlette import status
from starlette.testclient import TestClient

from tests import container
from that_depends.providers import DIContextMiddleware


app = fastapi.FastAPI()
app.add_middleware(DIContextMiddleware)


@app.get("/")
async def read_root(
    sync_dependency: typing.Annotated[
        container.AsyncDependentFactory,
        fastapi.Depends(container.DIContainer.async_dependent_factory),
    ],
) -> str:
    return sync_dependency.async_resource


client = TestClient(app)


def test_read_main() -> None:
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == "async resource"
