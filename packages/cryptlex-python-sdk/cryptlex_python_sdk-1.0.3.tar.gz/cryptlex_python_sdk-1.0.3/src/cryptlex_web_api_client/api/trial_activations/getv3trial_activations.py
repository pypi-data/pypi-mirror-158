from typing import Any, Dict, List, Optional, Union

import httpx

from ...client import Client
from ...models.http_error_response_dto import HttpErrorResponseDto
from ...models.trial_activation_dto import TrialActivationDto
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    product_id: Union[Unset, None, str] = UNSET,
    page: Union[Unset, None, int] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    sort: Union[Unset, None, str] = UNSET,
    query: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/v3/trial-activations".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["productId"] = product_id

    params["page"] = page

    params["limit"] = limit

    params["sort"] = sort

    params["query"] = query

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[HttpErrorResponseDto, List[TrialActivationDto]]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = TrialActivationDto.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if response.status_code == 401:
        response_401 = HttpErrorResponseDto.from_dict(response.json())

        return response_401
    if response.status_code == 403:
        response_403 = HttpErrorResponseDto.from_dict(response.json())

        return response_403
    if response.status_code == 429:
        response_429 = HttpErrorResponseDto.from_dict(response.json())

        return response_429
    if response.status_code == 500:
        response_500 = HttpErrorResponseDto.from_dict(response.json())

        return response_500
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[HttpErrorResponseDto, List[TrialActivationDto]]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    product_id: Union[Unset, None, str] = UNSET,
    page: Union[Unset, None, int] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    sort: Union[Unset, None, str] = UNSET,
    query: Union[Unset, None, str] = UNSET,
) -> Response[Union[HttpErrorResponseDto, List[TrialActivationDto]]]:
    """List all trial activations

     Returns a list of trial activations. The trial activations are returned sorted by creation date in
    ascending order.

    Args:
        product_id (Union[Unset, None, str]):
        page (Union[Unset, None, int]):
        limit (Union[Unset, None, int]):
        sort (Union[Unset, None, str]):
        query (Union[Unset, None, str]):

    Returns:
        Response[Union[HttpErrorResponseDto, List[TrialActivationDto]]]
    """

    kwargs = _get_kwargs(
        client=client,
        product_id=product_id,
        page=page,
        limit=limit,
        sort=sort,
        query=query,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    product_id: Union[Unset, None, str] = UNSET,
    page: Union[Unset, None, int] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    sort: Union[Unset, None, str] = UNSET,
    query: Union[Unset, None, str] = UNSET,
) -> Optional[Union[HttpErrorResponseDto, List[TrialActivationDto]]]:
    """List all trial activations

     Returns a list of trial activations. The trial activations are returned sorted by creation date in
    ascending order.

    Args:
        product_id (Union[Unset, None, str]):
        page (Union[Unset, None, int]):
        limit (Union[Unset, None, int]):
        sort (Union[Unset, None, str]):
        query (Union[Unset, None, str]):

    Returns:
        Response[Union[HttpErrorResponseDto, List[TrialActivationDto]]]
    """

    return sync_detailed(
        client=client,
        product_id=product_id,
        page=page,
        limit=limit,
        sort=sort,
        query=query,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    product_id: Union[Unset, None, str] = UNSET,
    page: Union[Unset, None, int] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    sort: Union[Unset, None, str] = UNSET,
    query: Union[Unset, None, str] = UNSET,
) -> Response[Union[HttpErrorResponseDto, List[TrialActivationDto]]]:
    """List all trial activations

     Returns a list of trial activations. The trial activations are returned sorted by creation date in
    ascending order.

    Args:
        product_id (Union[Unset, None, str]):
        page (Union[Unset, None, int]):
        limit (Union[Unset, None, int]):
        sort (Union[Unset, None, str]):
        query (Union[Unset, None, str]):

    Returns:
        Response[Union[HttpErrorResponseDto, List[TrialActivationDto]]]
    """

    kwargs = _get_kwargs(
        client=client,
        product_id=product_id,
        page=page,
        limit=limit,
        sort=sort,
        query=query,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    product_id: Union[Unset, None, str] = UNSET,
    page: Union[Unset, None, int] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    sort: Union[Unset, None, str] = UNSET,
    query: Union[Unset, None, str] = UNSET,
) -> Optional[Union[HttpErrorResponseDto, List[TrialActivationDto]]]:
    """List all trial activations

     Returns a list of trial activations. The trial activations are returned sorted by creation date in
    ascending order.

    Args:
        product_id (Union[Unset, None, str]):
        page (Union[Unset, None, int]):
        limit (Union[Unset, None, int]):
        sort (Union[Unset, None, str]):
        query (Union[Unset, None, str]):

    Returns:
        Response[Union[HttpErrorResponseDto, List[TrialActivationDto]]]
    """

    return (
        await asyncio_detailed(
            client=client,
            product_id=product_id,
            page=page,
            limit=limit,
            sort=sort,
            query=query,
        )
    ).parsed
