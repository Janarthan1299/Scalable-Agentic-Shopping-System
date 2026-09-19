import pytest
from app.services.validator import ParameterValidator
from app.services.permission_service import PermissionDenied, PermissionService


def test_parameter_validation():
    assert ParameterValidator().validate("track_order", {"order_id": "O10025"}) == {"order_id": "O10025"}
    with pytest.raises(ValueError): ParameterValidator().validate("track_order", {})


def test_permission_validation():
    with pytest.raises(PermissionDenied): PermissionService().check("C001", "payment:refund")
    PermissionService().check("ADMIN", "payment:refund")
