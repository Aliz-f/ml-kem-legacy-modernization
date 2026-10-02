"""Application fault selection, independent of cryptographic fault execution."""

from edge_gateway.failure.injector import APPLICATION_FAILURE_MODES, FailureInjector

__all__ = ["APPLICATION_FAILURE_MODES", "FailureInjector"]
