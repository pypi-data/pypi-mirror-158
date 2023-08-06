from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.access_token_dto import AccessTokenDto
from ...models.http_error_response_dto import HttpErrorResponseDto
from ...models.postv_3_accountslogin_google_json_body import Postv3AccountsloginGoogleJsonBody
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    json_body: Postv3AccountsloginGoogleJsonBody,
) -> Dict[str, Any]:
    url = "{}/v3/accounts/login-google".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[AccessTokenDto, HttpErrorResponseDto]]:
    if response.status_code == 200:
        response_200 = AccessTokenDto.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = HttpErrorResponseDto.from_dict(response.json())

        return response_400
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


def _build_response(*, response: httpx.Response) -> Response[Union[AccessTokenDto, HttpErrorResponseDto]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    json_body: Postv3AccountsloginGoogleJsonBody,
) -> Response[Union[AccessTokenDto, HttpErrorResponseDto]]:
    """Log into the account using Google

     Returns an access token.

    Args:
        json_body (Postv3AccountsloginGoogleJsonBody):

    Returns:
        Response[Union[AccessTokenDto, HttpErrorResponseDto]]
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
    json_body: Postv3AccountsloginGoogleJsonBody,
) -> Optional[Union[AccessTokenDto, HttpErrorResponseDto]]:
    """Log into the account using Google

     Returns an access token.

    Args:
        json_body (Postv3AccountsloginGoogleJsonBody):

    Returns:
        Response[Union[AccessTokenDto, HttpErrorResponseDto]]
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    json_body: Postv3AccountsloginGoogleJsonBody,
) -> Response[Union[AccessTokenDto, HttpErrorResponseDto]]:
    """Log into the account using Google

     Returns an access token.

    Args:
        json_body (Postv3AccountsloginGoogleJsonBody):

    Returns:
        Response[Union[AccessTokenDto, HttpErrorResponseDto]]
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
    json_body: Postv3AccountsloginGoogleJsonBody,
) -> Optional[Union[AccessTokenDto, HttpErrorResponseDto]]:
    """Log into the account using Google

     Returns an access token.

    Args:
        json_body (Postv3AccountsloginGoogleJsonBody):

    Returns:
        Response[Union[AccessTokenDto, HttpErrorResponseDto]]
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
