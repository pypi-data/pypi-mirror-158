from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.user_metadata_request_model import UserMetadataRequestModel
from ..types import UNSET, Unset

T = TypeVar("T", bound="Postv3UsersJsonBody")


@attr.s(auto_attribs=True)
class Postv3UsersJsonBody:
    """
    Attributes:
        first_name (Union[Unset, str]): First name of the user.
        last_name (Union[Unset, str]): Last name of the user.
        email (Union[Unset, str]): Email address of the user.
        company (Union[Unset, None, str]): Company of the user.
        allow_customer_portal_access (Union[Unset, None, bool]): Allow customer portal access.
        metadata (Union[Unset, None, List[UserMetadataRequestModel]]): List of metdata key/value pairs.
        tags (Union[Unset, None, List[str]]): List of tags.
        password (Union[Unset, str]): Password of the user.
        role (Union[Unset, None, str]): Role of the user.
    """

    first_name: Union[Unset, str] = UNSET
    last_name: Union[Unset, str] = UNSET
    email: Union[Unset, str] = UNSET
    company: Union[Unset, None, str] = UNSET
    allow_customer_portal_access: Union[Unset, None, bool] = UNSET
    metadata: Union[Unset, None, List[UserMetadataRequestModel]] = UNSET
    tags: Union[Unset, None, List[str]] = UNSET
    password: Union[Unset, str] = UNSET
    role: Union[Unset, None, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        first_name = self.first_name
        last_name = self.last_name
        email = self.email
        company = self.company
        allow_customer_portal_access = self.allow_customer_portal_access
        metadata: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.metadata, Unset):
            if self.metadata is None:
                metadata = None
            else:
                metadata = []
                for metadata_item_data in self.metadata:
                    metadata_item = metadata_item_data.to_dict()

                    metadata.append(metadata_item)

        tags: Union[Unset, None, List[str]] = UNSET
        if not isinstance(self.tags, Unset):
            if self.tags is None:
                tags = None
            else:
                tags = self.tags

        password = self.password
        role = self.role

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if first_name is not UNSET:
            field_dict["firstName"] = first_name
        if last_name is not UNSET:
            field_dict["lastName"] = last_name
        if email is not UNSET:
            field_dict["email"] = email
        if company is not UNSET:
            field_dict["company"] = company
        if allow_customer_portal_access is not UNSET:
            field_dict["allowCustomerPortalAccess"] = allow_customer_portal_access
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if tags is not UNSET:
            field_dict["tags"] = tags
        if password is not UNSET:
            field_dict["password"] = password
        if role is not UNSET:
            field_dict["role"] = role

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        first_name = d.pop("firstName", UNSET)

        last_name = d.pop("lastName", UNSET)

        email = d.pop("email", UNSET)

        company = d.pop("company", UNSET)

        allow_customer_portal_access = d.pop("allowCustomerPortalAccess", UNSET)

        metadata = []
        _metadata = d.pop("metadata", UNSET)
        for metadata_item_data in _metadata or []:
            metadata_item = UserMetadataRequestModel.from_dict(metadata_item_data)

            metadata.append(metadata_item)

        tags = cast(List[str], d.pop("tags", UNSET))

        password = d.pop("password", UNSET)

        role = d.pop("role", UNSET)

        postv_3_users_json_body = cls(
            first_name=first_name,
            last_name=last_name,
            email=email,
            company=company,
            allow_customer_portal_access=allow_customer_portal_access,
            metadata=metadata,
            tags=tags,
            password=password,
            role=role,
        )

        postv_3_users_json_body.additional_properties = d
        return postv_3_users_json_body

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
