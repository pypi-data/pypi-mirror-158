from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.email_template_dto import EmailTemplateDto
from ...models.email_template_request_model import EmailTemplateRequestModel
from ...models.http_error_response_dto import HttpErrorResponseDto
from ...types import Response


def _get_kwargs(
    id: str,
    *,
    client: Client,
    json_body: EmailTemplateRequestModel,
) -> Dict[str, Any]:
    url = "{}/v3/email-templates/{id}".format(client.base_url, id=id)

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


def _parse_response(*, response: httpx.Response) -> Optional[Union[EmailTemplateDto, HttpErrorResponseDto]]:
    if response.status_code == 200:
        response_200 = EmailTemplateDto.from_dict(response.json())

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


def _build_response(*, response: httpx.Response) -> Response[Union[EmailTemplateDto, HttpErrorResponseDto]]:
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
    json_body: EmailTemplateRequestModel,
) -> Response[Union[EmailTemplateDto, HttpErrorResponseDto]]:
    """Update an email template

     Updates the specified email template by setting the values of the parameters passed. Any parameters
    not provided will be left unchanged.

    Args:
        id (str):
        json_body (EmailTemplateRequestModel):

    Returns:
        Response[Union[EmailTemplateDto, HttpErrorResponseDto]]
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
    json_body: EmailTemplateRequestModel,
) -> Optional[Union[EmailTemplateDto, HttpErrorResponseDto]]:
    """Update an email template

     Updates the specified email template by setting the values of the parameters passed. Any parameters
    not provided will be left unchanged.

    Args:
        id (str):
        json_body (EmailTemplateRequestModel):

    Returns:
        Response[Union[EmailTemplateDto, HttpErrorResponseDto]]
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
    json_body: EmailTemplateRequestModel,
) -> Response[Union[EmailTemplateDto, HttpErrorResponseDto]]:
    """Update an email template

     Updates the specified email template by setting the values of the parameters passed. Any parameters
    not provided will be left unchanged.

    Args:
        id (str):
        json_body (EmailTemplateRequestModel):

    Returns:
        Response[Union[EmailTemplateDto, HttpErrorResponseDto]]
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
    json_body: EmailTemplateRequestModel,
) -> Optional[Union[EmailTemplateDto, HttpErrorResponseDto]]:
    """Update an email template

     Updates the specified email template by setting the values of the parameters passed. Any parameters
    not provided will be left unchanged.

    Args:
        id (str):
        json_body (EmailTemplateRequestModel):

    Returns:
        Response[Union[EmailTemplateDto, HttpErrorResponseDto]]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            json_body=json_body,
        )
    ).parsed
