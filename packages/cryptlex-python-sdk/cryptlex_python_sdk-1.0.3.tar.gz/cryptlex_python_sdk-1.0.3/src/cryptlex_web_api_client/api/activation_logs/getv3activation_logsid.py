from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.activation_log_dto import ActivationLogDto
from ...models.http_error_response_dto import HttpErrorResponseDto
from ...types import Response


def _get_kwargs(
    id: str,
    *,
    client: Client,
) -> Dict[str, Any]:
    url = "{}/v3/activation-logs/{id}".format(client.base_url, id=id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[ActivationLogDto, HttpErrorResponseDto]]:
    if response.status_code == 200:
        response_200 = ActivationLogDto.from_dict(response.json())

        return response_200
    if response.status_code == 401:
        response_401 = HttpErrorResponseDto.from_dict(response.json())

        return response_401
    if response.status_code == 403:
        response_403 = HttpErrorResponseDto.from_dict(response.json())

        return response_403
    if response.status_code == 404:
        response_404 = HttpErrorResponseDto.from_dict(response.json())

        return response_404
    if response.status_code == 429:
        response_429 = HttpErrorResponseDto.from_dict(response.json())

        return response_429
    if response.status_code == 500:
        response_500 = HttpErrorResponseDto.from_dict(response.json())

        return response_500
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[ActivationLogDto, HttpErrorResponseDto]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    id: str,
    *,
    client: Client,
) -> Response[Union[ActivationLogDto, HttpErrorResponseDto]]:
    """Retrieve an activation log

     Retrieves the details of an existing activation log.

    Args:
        id (str):

    Returns:
        Response[Union[ActivationLogDto, HttpErrorResponseDto]]
    """

    kwargs = _get_kwargs(
        id=id,
        client=client,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    id: str,
    *,
    client: Client,
) -> Optional[Union[ActivationLogDto, HttpErrorResponseDto]]:
    """Retrieve an activation log

     Retrieves the details of an existing activation log.

    Args:
        id (str):

    Returns:
        Response[Union[ActivationLogDto, HttpErrorResponseDto]]
    """

    return sync_detailed(
        id=id,
        client=client,
    ).parsed


async def asyncio_detailed(
    id: str,
    *,
    client: Client,
) -> Response[Union[ActivationLogDto, HttpErrorResponseDto]]:
    """Retrieve an activation log

     Retrieves the details of an existing activation log.

    Args:
        id (str):

    Returns:
        Response[Union[ActivationLogDto, HttpErrorResponseDto]]
    """

    kwargs = _get_kwargs(
        id=id,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    id: str,
    *,
    client: Client,
) -> Optional[Union[ActivationLogDto, HttpErrorResponseDto]]:
    """Retrieve an activation log

     Retrieves the details of an existing activation log.

    Args:
        id (str):

    Returns:
        Response[Union[ActivationLogDto, HttpErrorResponseDto]]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
        )
    ).parsed
