from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="Postv3UsersidupdatePasswordJsonBody")


@attr.s(auto_attribs=True)
class Postv3UsersidupdatePasswordJsonBody:
    """
    Attributes:
        old_password (Union[Unset, str]): Old password of the user.
        new_password (Union[Unset, str]): New password of the user.
    """

    old_password: Union[Unset, str] = UNSET
    new_password: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        old_password = self.old_password
        new_password = self.new_password

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if old_password is not UNSET:
            field_dict["oldPassword"] = old_password
        if new_password is not UNSET:
            field_dict["newPassword"] = new_password

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        old_password = d.pop("oldPassword", UNSET)

        new_password = d.pop("newPassword", UNSET)

        postv_3_usersidupdate_password_json_body = cls(
            old_password=old_password,
            new_password=new_password,
        )

        postv_3_usersidupdate_password_json_body.additional_properties = d
        return postv_3_usersidupdate_password_json_body

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
