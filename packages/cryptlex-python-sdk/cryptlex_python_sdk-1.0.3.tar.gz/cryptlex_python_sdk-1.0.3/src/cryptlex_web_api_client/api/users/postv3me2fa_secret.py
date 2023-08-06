from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.http_error_response_dto import HttpErrorResponseDto
from ...models.two_factor_secret_dto import TwoFactorSecretDto
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
) -> Dict[str, Any]:
    url = "{}/v3/me/2fa-secret".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[HttpErrorResponseDto, TwoFactorSecretDto]]:
    if response.status_code == 200:
        response_200 = TwoFactorSecretDto.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = HttpErrorResponseDto.from_dict(response.json())

        return response_400
    if response.status_code == 401:
        response_401 = HttpErrorResponseDto.from_dict(response.json())

        return response_401
    if response.status_code == 403:
        response_403 = HttpErrorResponseDto.from_dict(response.json())

        return response_403
    if response.status_code == 409:
        response_409 = HttpErrorResponseDto.from_dict(response.json())

        return response_409
    if response.status_code == 429:
        response_429 = HttpErrorResponseDto.from_dict(response.json())

        return response_429
    if response.status_code == 500:
        response_500 = HttpErrorResponseDto.from_dict(response.json())

        return response_500
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[HttpErrorResponseDto, TwoFactorSecretDto]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
) -> Response[Union[HttpErrorResponseDto, TwoFactorSecretDto]]:
    """Generate the 2FA secret

     Generates the 2FA secret for Authenticator app.

    Returns:
        Response[Union[HttpErrorResponseDto, TwoFactorSecretDto]]
    """

    kwargs = _get_kwargs(
        client=client,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
) -> Optional[Union[HttpErrorResponseDto, TwoFactorSecretDto]]:
    """Generate the 2FA secret

     Generates the 2FA secret for Authenticator app.

    Returns:
        Response[Union[HttpErrorResponseDto, TwoFactorSecretDto]]
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
) -> Response[Union[HttpErrorResponseDto, TwoFactorSecretDto]]:
    """Generate the 2FA secret

     Generates the 2FA secret for Authenticator app.

    Returns:
        Response[Union[HttpErrorResponseDto, TwoFactorSecretDto]]
    """

    kwargs = _get_kwargs(
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
) -> Optional[Union[HttpErrorResponseDto, TwoFactorSecretDto]]:
    """Generate the 2FA secret

     Generates the 2FA secret for Authenticator app.

    Returns:
        Response[Union[HttpErrorResponseDto, TwoFactorSecretDto]]
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
