"""
Day 3: Object-Oriented Programming (OOP) for AI applications.

Project:
Convert dictionary-based support tickets into structured Python objects.

Concepts:
- Classes
- Objects
- Dataclasses
- Enums
- Instance methods
- Validation
- Agent routing
"""

from dataclasses import dataclass
from enum import Enum


class TicketPriority(str, Enum):
    """
    Defines the allowed priority values for support tickets.

    Using Enum prevents accidental values such as:
    "hgh", "urgenttt", or "HIGHH".
    """

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class TicketStatus(str, Enum):
    """
    Defines the allowed ticket status values.
    """

    OPEN = "open"
    IN_PROGRESS = "in_progress"
    CLOSED = "closed"


@dataclass
class SupportTicket:
    """
    Represents one customer-support ticket.

    A dataclass automatically creates an __init__ method.

    For example, Python automatically allows:

    SupportTicket(
        ticket_id="TKT-1001",
        customer_name="Arun",
        category="password_reset",
        priority=TicketPriority.HIGH,
        status=TicketStatus.OPEN,
        message="I cannot log in."
    )
    """

    ticket_id: str
    customer_name: str
    category: str
    priority: TicketPriority
    status: TicketStatus
    message: str
    requires_human_review: bool = False

    def __post_init__(self) -> None:
        """
        Runs automatically after the object is created.

        We use it to validate important fields.
        """

        if not self.ticket_id.startswith("TKT-"):
            raise ValueError(
                "ticket_id must start with 'TKT-'. "
                "Example: TKT-1001"
            )

        if not self.customer_name.strip():
            raise ValueError("customer_name cannot be empty.")

        if not self.message.strip():
            raise ValueError("message cannot be empty.")

    def is_open(self) -> bool:
        """
        Returns True if the ticket is currently open.
        """
        return self.status == TicketStatus.OPEN

    def is_high_priority(self) -> bool:
        """
        Returns True for HIGH and CRITICAL tickets.
        """
        return self.priority in [
            TicketPriority.HIGH,
            TicketPriority.CRITICAL,
        ]

    def needs_human_review(self) -> bool:
        """
        Returns True if the ticket should be handled by a human.

        In a real AI application, human review can be required for:
        - billing/refund problems
        - legal or compliance requests
        - security incidents
        - low-confidence AI responses
        """
        return self.requires_human_review

    def update_status(self, new_status: TicketStatus) -> None:
        """
        Updates the current ticket status.
        """
        old_status = self.status
        self.status = new_status

        print(
            f"Ticket {self.ticket_id} status changed: "
            f"{old_status.value} -> {new_status.value}"
        )

    def get_agent_route(self) -> str:
        """
        Simulates a simple rule-based agent router.

        Later, we can replace this logic with:
        - an OpenAI LLM classifier
        - LangChain tools
        - LangGraph conditional routing
        """

        if self.needs_human_review():
            return "HUMAN_REVIEW"

        if self.category in ["billing", "refund"]:
            return "BILLING_AGENT"

        if self.category in ["password_reset", "account_access"]:
            return "ACCOUNT_AGENT"

        if self.category == "technical_issue":
            return "TECHNICAL_AGENT"

        return "GENERAL_SUPPORT_AGENT"

    def to_agent_input(self) -> dict[str, str]:
        """
        Converts the object into dictionary data.

        Agent tools, APIs, databases, and JSON responses commonly
        use dictionaries or JSON-like structures.
        """
        return {
            "ticket_id": self.ticket_id,
            "customer_name": self.customer_name,
            "category": self.category,
            "priority": self.priority.value,
            "status": self.status.value,
            "message": self.message,
            "agent_route": self.get_agent_route(),
        }

    def display(self) -> None:
        """
        Prints ticket information in a readable format.
        """
        print(
            f"\nTicket ID: {self.ticket_id}"
            f"\nCustomer: {self.customer_name}"
            f"\nCategory: {self.category}"
            f"\nPriority: {self.priority.value}"
            f"\nStatus: {self.status.value}"
            f"\nMessage: {self.message}"
            f"\nRequires human review: {self.requires_human_review}"
            f"\nAssigned route: {self.get_agent_route()}"
        )


class TicketManager:
    """
    Manages multiple SupportTicket objects.

    This is a simple service class. In future projects,
    similar classes will manage:
    - document ingestion
    - vector databases
    - chat sessions
    - API calls
    - agent workflows
    """

    def __init__(self) -> None:
        """
        Constructor for TicketManager.

        It starts with an empty ticket list.
        """
        self.tickets: list[SupportTicket] = []

    def add_ticket(self, ticket: SupportTicket) -> None:
        """
        Adds a SupportTicket object to the manager.
        """
        self.tickets.append(ticket)
        print(f"Added ticket: {ticket.ticket_id}")

    def get_open_tickets(self) -> list[SupportTicket]:
        """
        Returns every ticket with OPEN status.
        """
        return [
            ticket
            for ticket in self.tickets
            if ticket.is_open()
        ]

    def get_high_priority_open_tickets(self) -> list[SupportTicket]:
        """
        Returns only open tickets with HIGH or CRITICAL priority.
        """
        return [
            ticket
            for ticket in self.tickets
            if ticket.is_open() and ticket.is_high_priority()
        ]

    def get_human_review_tickets(self) -> list[SupportTicket]:
        """
        Returns tickets that need manual human review.
        """
        return [
            ticket
            for ticket in self.tickets
            if ticket.needs_human_review()
        ]

    def get_summary(self) -> dict[str, int]:
        """
        Creates a summary of all managed tickets.
        """
        return {
            "total_tickets": len(self.tickets),
            "open_tickets": len(self.get_open_tickets()),
            "high_priority_open_tickets": len(
                self.get_high_priority_open_tickets()
            ),
            "human_review_tickets": len(
                self.get_human_review_tickets()
            ),
        }

    def display_all_tickets(self) -> None:
        """
        Displays every ticket stored by the manager.
        """
        print("\n--- ALL SUPPORT TICKETS ---")

        for ticket in self.tickets:
            ticket.display()


def main() -> None:
    """
    Main function for the Day 3 practice project.
    """

    # Create a manager object.
    ticket_manager = TicketManager()

    # Create individual ticket objects.
    ticket_1 = SupportTicket(
        ticket_id="TKT-1001",
        customer_name="Arun",
        category="password_reset",
        priority=TicketPriority.HIGH,
        status=TicketStatus.OPEN,
        message="I cannot log in and need to reset my password.",
    )

    ticket_2 = SupportTicket(
        ticket_id="TKT-1002",
        customer_name="Priya",
        category="billing",
        priority=TicketPriority.MEDIUM,
        status=TicketStatus.OPEN,
        message="I was charged twice for my subscription.",
        requires_human_review=True,
    )

    ticket_3 = SupportTicket(
        ticket_id="TKT-1003",
        customer_name="Kumar",
        category="technical_issue",
        priority=TicketPriority.LOW,
        status=TicketStatus.CLOSED,
        message="The dashboard page loads slowly.",
    )

    ticket_4 = SupportTicket(
        ticket_id="TKT-1004",
        customer_name="Meena",
        category="account_access",
        priority=TicketPriority.CRITICAL,
        status=TicketStatus.OPEN,
        message="My account is locked after too many login attempts.",
    )

    # Store ticket objects in TicketManager.
    ticket_manager.add_ticket(ticket_1)
    ticket_manager.add_ticket(ticket_2)
    ticket_manager.add_ticket(ticket_3)
    ticket_manager.add_ticket(ticket_4)

    # Display all ticket details.
    ticket_manager.display_all_tickets()

    # Display ticket summary.
    summary = ticket_manager.get_summary()

    print("\n--- TICKET SUMMARY ---")
    for key, value in summary.items():
        formatted_key = key.replace("_", " ").title()
        print(f"{formatted_key}: {value}")

    # Demonstrate updating a ticket status.
    print("\n--- STATUS UPDATE DEMO ---")
    ticket_1.update_status(TicketStatus.IN_PROGRESS)

    # Convert an object into agent/API-friendly dictionary data.
    print("\n--- AGENT INPUT DATA ---")
    print(ticket_2.to_agent_input())


if __name__ == "__main__":
    main()
