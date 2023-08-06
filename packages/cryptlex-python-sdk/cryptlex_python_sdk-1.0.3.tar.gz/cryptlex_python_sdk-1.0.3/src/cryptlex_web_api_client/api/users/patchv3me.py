from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.http_error_response_dto import HttpErrorResponseDto
from ...models.me_update_request_model import MeUpdateRequestModel
from ...models.user_dto import UserDto
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    json_body: MeUpdateRequestModel,
) -> Dict[str, Any]:
    url = "{}/v3/me".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_json_body = json_body.to_dict()

    return {
        "method": "patch",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[HttpErrorResponseDto, UserDto]]:
    if response.status_code == 200:
        response_200 = UserDto.from_dict(response.json())

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


def _build_response(*, response: httpx.Response) -> Response[Union[HttpErrorResponseDto, UserDto]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    json_body: MeUpdateRequestModel,
) -> Response[Union[HttpErrorResponseDto, UserDto]]:
    """Update profile

     Updates the currently authenticated user by setting the values of the parameters passed. Any
    parameters not provided will be left unchanged.

    Args:
        json_body (MeUpdateRequestModel):

    Returns:
        Response[Union[HttpErrorResponseDto, UserDto]]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    json_body: MeUpdateRequestModel,
) -> Optional[Union[HttpErrorResponseDto, UserDto]]:
    """Update profile

     Updates the currently authenticated user by setting the values of the parameters passed. Any
    parameters not provided will be left unchanged.

    Args:
        json_body (MeUpdateRequestModel):

    Returns:
        Response[Union[HttpErrorResponseDto, UserDto]]
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    json_body: MeUpdateRequestModel,
) -> Response[Union[HttpErrorResponseDto, UserDto]]:
    """Update profile

     Updates the currently authenticated user by setting the values of the parameters passed. Any
    parameters not provided will be left unchanged.

    Args:
        json_body (MeUpdateRequestModel):

    Returns:
        Response[Union[HttpErrorResponseDto, UserDto]]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    json_body: MeUpdateRequestModel,
) -> Optional[Union[HttpErrorResponseDto, UserDto]]:
    """Update profile

     Updates the currently authenticated user by setting the values of the parameters passed. Any
    parameters not provided will be left unchanged.

    Args:
        json_body (MeUpdateRequestModel):

    Returns:
        Response[Union[HttpErrorResponseDto, UserDto]]
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
