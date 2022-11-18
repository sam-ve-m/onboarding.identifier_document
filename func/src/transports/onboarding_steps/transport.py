from http import HTTPStatus

from decouple import config
from httpx import AsyncClient

from ...domain.exceptions.exceptions import OnboardingStepsStatusCodeNotOk


class OnboardingSteps:
    @staticmethod
    async def _get_user_current_step(host: str, jwt: str) -> str:
        headers = {"x-thebes-answer": jwt}
        async with AsyncClient() as httpx_client:
            request_result = await httpx_client.get(host, headers=headers)
            if not request_result.status_code == HTTPStatus.OK:
                raise OnboardingStepsStatusCodeNotOk
            user_current_step = (
                request_result.json().get("result", {}).get("current_step")
            )
        return user_current_step

    @classmethod
    async def get_user_current_step_br(cls, jwt: str) -> str:
        host = config("ONBOARDING_STEPS_BR_URL")
        user_current_step = await cls._get_user_current_step(host, jwt)
        return user_current_step

    @classmethod
    async def get_user_current_step_us(cls, jwt: str) -> str:
        host = config("ONBOARDING_STEPS_US_URL")
        user_current_step = await cls._get_user_current_step(host, jwt)
        return user_current_step
