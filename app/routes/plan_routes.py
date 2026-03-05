from fastapi import APIRouter
from app.utils.plans import PLANS

router = APIRouter()


@router.get("/plans")
def get_plans():

    return PLANS