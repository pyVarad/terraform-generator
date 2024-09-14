from fastapi import APIRouter

from tf_generator.cloudformation2terraform.api import router as ct2tf_router

api_router = APIRouter()

include_api = api_router.include_router
routers = (
    (ct2tf_router, "cloudformation2terraform", "cloudformation2terraform"),
)

for router_item in routers:
    router, prefix, tag = router_item

    if tag:
        include_api(router, prefix=f"/{prefix}", tags=[tag])
    else:
        include_api(router, prefix=f"/{prefix}")