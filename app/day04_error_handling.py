"""
Day 4: Error handling, custom exceptions, validation, and logging.

Project:
Safely process support-ticket data.

Concepts:
- try
- except
- finally
- raise
- custom exceptions
- logging
- safe API-style response dictionaries
"""

from dataclasses import dataclass
from enum import Enum
from typing import Any
import logging


# Logging helps developers understand what happens in an application.
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s - %(message)s"
)


class TicketPriority(str, Enum):
    """
    Allowed ticket priorities.
    """

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"



class TicketStatus(str, Enum):
    """
    Allowed ticket statuses.
    """

    OPEN = "open"
    CLOSED = "closed"


class TicketValidationError(Exception):
    """
    Custom exception for invalid support-ticket data.

    We create a custom exception so we can clearly identify
    validation-related errors.
    """

    pass


@dataclass
class SupportTicket:
    """
    Represents one valid support ticket.
    """

    ticket_id: str
    customer_name: str
    category: str
    priority: TicketPriority
    status: TicketStatus
    message: str

    def to_dict(self) -> dict[str, str]:
        """
        Converts the ticket object into a dictionary.

        Dictionaries are commonly returned from APIs and agent tools.
        """
        return {
            "ticket_id": self.ticket_id,
            "customer_name": self.customer_name,
            "category": self.category,
            "priority": self.priority.value,
            "status": self.status.value,
            "message": self.message,
        }


def validate_text_field(ticket_data: dict[str, Any], field_name: str) -> str:
    """
    Validates a required text field.

    Raises:
        TicketValidationError:
            If the field is missing, not text, or empty.
    """
    value = ticket_data.get(field_name)

    if not isinstance(value, str):
        raise TicketValidationError(
            f"'{field_name}' is required and must be text."
        )

    if not value.strip():
        raise TicketValidationError(
            f"'{field_name}' cannot be empty."
        )

    return value.strip()


def create_ticket_from_data(ticket_data: dict[str, Any]) -> SupportTicket:
    """
    Converts raw dictionary data into a validated SupportTicket object.

    Raw data might come from:
    - a web form
    - FastAPI request JSON
    - a database
    - an LLM structured response
    - another API
    """

    ticket_id = validate_text_field(ticket_data, "ticket_id")
    customer_name = validate_text_field(ticket_data, "customer_name")
    category = validate_text_field(ticket_data, "category")
    message = validate_text_field(ticket_data, "message")

    # Get priority and status from incoming dictionary data.
    priority_text = ticket_data.get("priority")
    status_text = ticket_data.get("status")

    try:
        # Convert normal strings into Enum values.
        priority = TicketPriority(priority_text)
        status = TicketStatus(status_text)

    except ValueError as error:
        # This runs if priority/status is not one of the allowed values.
        raise TicketValidationError(
            "Invalid priority or status value. "
            "Priority must be: low, medium, or high or Critical. "
            "Status must be: open or closed."
        ) from error

    # Create and return a valid SupportTicket object.
    return SupportTicket(
        ticket_id=ticket_id,
        customer_name=customer_name,
        category=category,
        priority=priority,
        status=status,
        message=message,
    )


def process_ticket(ticket_data: dict[str, Any]) -> dict[str, Any]:
    """
    Processes one ticket safely.

    Returns a dictionary similar to an API response.
    The program does not crash when ticket data is invalid.
    """

    try:
        logging.info("Starting ticket processing.")

        ticket = create_ticket_from_data(ticket_data)

        logging.info(
            "Ticket %s was processed successfully.",
            ticket.ticket_id
        )

        return {
            "success": True,
            "message": "Ticket processed successfully.",
            "ticket": ticket.to_dict(),
        }

    except TicketValidationError as error:
        logging.warning("Validation failed: %s", error)

        return {
            "success": False,
            "message": "Ticket validation failed.",
            "error": str(error),
        }

    except Exception as error:
        # Unexpected errors should be logged.
        # In production, do not expose internal error details to users.
        logging.exception("Unexpected application error: %s", error)

        return {
            "success": False,
            "message": "An unexpected error occurred.",
        }

    finally:
        # finally runs whether the code succeeds or fails.
        logging.info("Ticket processing attempt finished.")


def main() -> None:
    """
    Tests valid and invalid ticket data.
    """

    valid_ticket_data = {
        "ticket_id": "TKT-2001",
        "customer_name": "Arun",
        "category": "password_reset",
        "priority": "high",
        "status": "open",
        "message": "I cannot reset my password.",
    }

    invalid_priority_ticket_data = {
        "ticket_id": "TKT-2002",
        "customer_name": "Priya",
        "category": "billing",
        "priority": "urgent",  # Invalid: not in TicketPriority Enum
        "status": "open",
        "message": "I was charged twice.",
    }

    missing_message_ticket_data = {
        "ticket_id": "TKT-2003",
        "customer_name": "Kumar",
        "category": "technical_issue",
        "priority": "low",
        "status": "open",
        # "message" is intentionally missing
    }

    critical_ticket_data = {
    "ticket_id": "TKT-2004",
    "customer_name": "Meena",
    "category": "account_access",
    "priority": "critical",
    "status": "open",
    "message": "My account may have been accessed by someone else.",
}


    print("\n--- VALID TICKET TEST ---")
    valid_result = process_ticket(valid_ticket_data)
    print(valid_result)

    print("\n--- INVALID PRIORITY TEST ---")
    invalid_priority_result = process_ticket(invalid_priority_ticket_data)
    print(invalid_priority_result)

    print("\n--- MISSING MESSAGE TEST ---")
    missing_message_result = process_ticket(missing_message_ticket_data)
    print(missing_message_result)
    print("\n--- CRITICAL TICKET TEST ---")
    critical_result = process_ticket(critical_ticket_data)
    print(critical_result)



if __name__ == "__main__":
    main()
