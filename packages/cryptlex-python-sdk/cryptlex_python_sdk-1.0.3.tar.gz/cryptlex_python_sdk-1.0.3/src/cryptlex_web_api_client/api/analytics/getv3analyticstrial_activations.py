import datetime
from typing import Any, Dict, List, Optional, Union

import httpx

from ...client import Client
from ...models.activations_by_date_dto import ActivationsByDateDto
from ...models.http_error_response_dto import HttpErrorResponseDto
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    product_id: Union[Unset, None, str] = UNSET,
    start_date: Union[Unset, None, datetime.datetime] = UNSET,
    end_date: Union[Unset, None, datetime.datetime] = UNSET,
) -> Dict[str, Any]:
    url = "{}/v3/analytics/trial-activations".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["productId"] = product_id

    json_start_date: Union[Unset, None, str] = UNSET
    if not isinstance(start_date, Unset):
        json_start_date = start_date.isoformat() if start_date else None

    params["startDate"] = json_start_date

    json_end_date: Union[Unset, None, str] = UNSET
    if not isinstance(end_date, Unset):
        json_end_date = end_date.isoformat() if end_date else None

    params["endDate"] = json_end_date

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[HttpErrorResponseDto, List[ActivationsByDateDto]]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = ActivationsByDateDto.from_dict(response_200_item_data)

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


def _build_response(*, response: httpx.Response) -> Response[Union[HttpErrorResponseDto, List[ActivationsByDateDto]]]:
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
    start_date: Union[Unset, None, datetime.datetime] = UNSET,
    end_date: Union[Unset, None, datetime.datetime] = UNSET,
) -> Response[Union[HttpErrorResponseDto, List[ActivationsByDateDto]]]:
    """Retrieve trial activations by time

     Retrieve trial activations as time series data.

    Args:
        product_id (Union[Unset, None, str]):
        start_date (Union[Unset, None, datetime.datetime]):
        end_date (Union[Unset, None, datetime.datetime]):

    Returns:
        Response[Union[HttpErrorResponseDto, List[ActivationsByDateDto]]]
    """

    kwargs = _get_kwargs(
        client=client,
        product_id=product_id,
        start_date=start_date,
        end_date=end_date,
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
    start_date: Union[Unset, None, datetime.datetime] = UNSET,
    end_date: Union[Unset, None, datetime.datetime] = UNSET,
) -> Optional[Union[HttpErrorResponseDto, List[ActivationsByDateDto]]]:
    """Retrieve trial activations by time

     Retrieve trial activations as time series data.

    Args:
        product_id (Union[Unset, None, str]):
        start_date (Union[Unset, None, datetime.datetime]):
        end_date (Union[Unset, None, datetime.datetime]):

    Returns:
        Response[Union[HttpErrorResponseDto, List[ActivationsByDateDto]]]
    """

    return sync_detailed(
        client=client,
        product_id=product_id,
        start_date=start_date,
        end_date=end_date,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    product_id: Union[Unset, None, str] = UNSET,
    start_date: Union[Unset, None, datetime.datetime] = UNSET,
    end_date: Union[Unset, None, datetime.datetime] = UNSET,
) -> Response[Union[HttpErrorResponseDto, List[ActivationsByDateDto]]]:
    """Retrieve trial activations by time

     Retrieve trial activations as time series data.

    Args:
        product_id (Union[Unset, None, str]):
        start_date (Union[Unset, None, datetime.datetime]):
        end_date (Union[Unset, None, datetime.datetime]):

    Returns:
        Response[Union[HttpErrorResponseDto, List[ActivationsByDateDto]]]
    """

    kwargs = _get_kwargs(
        client=client,
        product_id=product_id,
        start_date=start_date,
        end_date=end_date,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    product_id: Union[Unset, None, str] = UNSET,
    start_date: Union[Unset, None, datetime.datetime] = UNSET,
    end_date: Union[Unset, None, datetime.datetime] = UNSET,
) -> Optional[Union[HttpErrorResponseDto, List[ActivationsByDateDto]]]:
    """Retrieve trial activations by time

     Retrieve trial activations as time series data.

    Args:
        product_id (Union[Unset, None, str]):
        start_date (Union[Unset, None, datetime.datetime]):
        end_date (Union[Unset, None, datetime.datetime]):

    Returns:
        Response[Union[HttpErrorResponseDto, List[ActivationsByDateDto]]]
    """

    return (
        await asyncio_detailed(
            client=client,
            product_id=product_id,
            start_date=start_date,
            end_date=end_date,
        )
    ).parsed
