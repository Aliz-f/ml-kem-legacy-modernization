"""Workflow constants and validation helpers."""

from __future__ import annotations

from enum import StrEnum


class Status(StrEnum):
    IN_PROGRESS = "In Progress"
    AWAITING_REVIEW = "Awaiting Human Review"
    REVISION_REQUESTED = "Revision Requested"
    AWAITING_VERIFICATION = "Awaiting Final Verification"
    COMPLETE = "Complete"
    REJECTED = "Rejected"


ACTIVE_STATUSES = {
    Status.IN_PROGRESS,
    Status.AWAITING_REVIEW,
    Status.REVISION_REQUESTED,
    Status.AWAITING_VERIFICATION,
}


def state_name(status: Status) -> str:
    return status.lower().replace(" ", "_")
