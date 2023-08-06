from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.http_error_response_dto import HttpErrorResponseDto
from ...models.release_dto import ReleaseDto
from ...models.release_request_model import ReleaseRequestModel
from ...types import Response


def _get_kwargs(
    id: str,
    *,
    client: Client,
    json_body: ReleaseRequestModel,
) -> Dict[str, Any]:
    url = "{}/v3/releases/{id}".format(client.base_url, id=id)

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


def _parse_response(*, response: httpx.Response) -> Optional[Union[HttpErrorResponseDto, ReleaseDto]]:
    if response.status_code == 200:
        response_200 = ReleaseDto.from_dict(response.json())

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


def _build_response(*, response: httpx.Response) -> Response[Union[HttpErrorResponseDto, ReleaseDto]]:
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
    json_body: ReleaseRequestModel,
) -> Response[Union[HttpErrorResponseDto, ReleaseDto]]:
    """Update a release

     Updates the specified release by setting the values of the parameters passed. Any parameters not
    provided will be left unchanged.

    Args:
        id (str):
        json_body (ReleaseRequestModel):

    Returns:
        Response[Union[HttpErrorResponseDto, ReleaseDto]]
    """

    kwargs = _get_kwargs(
        id=id,
        client=client,
        json_body=json_body,
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
    json_body: ReleaseRequestModel,
) -> Optional[Union[HttpErrorResponseDto, ReleaseDto]]:
    """Update a release

     Updates the specified release by setting the values of the parameters passed. Any parameters not
    provided will be left unchanged.

    Args:
        id (str):
        json_body (ReleaseRequestModel):

    Returns:
        Response[Union[HttpErrorResponseDto, ReleaseDto]]
    """

    return sync_detailed(
        id=id,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    id: str,
    *,
    client: Client,
    json_body: ReleaseRequestModel,
) -> Response[Union[HttpErrorResponseDto, ReleaseDto]]:
    """Update a release

     Updates the specified release by setting the values of the parameters passed. Any parameters not
    provided will be left unchanged.

    Args:
        id (str):
        json_body (ReleaseRequestModel):

    Returns:
        Response[Union[HttpErrorResponseDto, ReleaseDto]]
    """

    kwargs = _get_kwargs(
        id=id,
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    id: str,
    *,
    client: Client,
    json_body: ReleaseRequestModel,
) -> Optional[Union[HttpErrorResponseDto, ReleaseDto]]:
    """Update a release

     Updates the specified release by setting the values of the parameters passed. Any parameters not
    provided will be left unchanged.

    Args:
        id (str):
        json_body (ReleaseRequestModel):

    Returns:
        Response[Union[HttpErrorResponseDto, ReleaseDto]]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            json_body=json_body,
        )
    ).parsed
