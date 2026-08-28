"""
Day 2: Python lists, dictionaries, loops, conditions, and functions.

Project:
Process fake customer-support tickets.

This represents a simplified version of data that an AI support
agent may receive before it decides what action to take.
"""

from typing import Any
# A list contains multiple items 
# Each tickets is represented by dictionary 
from typing import Any

support_ticket: list[dict[str, Any]] = [
    {
        "ticket_id": "TKT-1001",
        "customer_name": "Arun",
        "category": "password_reset",
        "priority": "high",
        "status": "open",
        "message": "I cannot log in and need to reset my password.",
        "require_human_review": False,
    },  # <-- comma added here
    {
        "ticket_id": "TKT-1002",
        "customer_name": "Priya",
        "category": "billing",
        "priority": "medium",
        "status": "open",
        "message": "I was charged twice for my subscription.",
        "require_human_review": True,
    },
    {
        "ticket_id": "TKT-1003",
        "customer_name": "Kumar",
        "category": "technical_issue",
        "priority": "low",
        "status": "closed",
        "message": "The dashboard page loads slowly.",
        "require_human_review": False,
    },
    {
        "ticket_id": "TKT-1004",
        "customer_name": "Meena",
        "category": "account_access",
        "priority": "high",
        "status": "open",
        "message": "My account is locked after too many login attempts.",
        "require_human_review": False,
    },
    {
        "ticket_id": "TKT-1005",
        "customer_name": "Rahul",
        "category": "refund",
        "priority": "high",
        "status": "open",
        "message": "I need a refund for an accidental purchase.",
        "require_human_review": True,
    },
]


def display_all_ticket(tickets:list[dict[str,any]])->None:
    """
    Prints all tickets in a readable format.

    """
    print("\n--- ALL SUPPORT TICKETS ---")

    for ticket in tickets:
        print(
            f"\nTicket ID: {ticket['ticket_id']}"
            f"\nCustomer: {ticket['customer_name']}"
            f"\nCategory: {ticket['category']}"
            f"\nPriority: {ticket['priority']}"
            f"\nStatus: {ticket['status']}"
            f"\nMessage: {ticket['message']}"
        )
def get_open_tickets(tickets:list[dict[str,Any]])->list[dict[str, Any]]:
    """
    Returns only tickets whose status is 'open'.

    In an AI application, this can represent filtering tickets
    that still need an agent or employee action.
    """
    open_tickets=[]
    for ticket in tickets:
        if ticket["status"]=="open":
            open_tickets.append(ticket)

    return open_tickets

def get_high_priority_tickets(
    tickets: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    """
    Returns open tickets with high priority.
    """
    high_priority_tickets = []
    for ticket in tickets:
        is_open = ticket["status"] == "open"
        is_high_priority = ticket["priority"] == "high"

        if is_open and is_high_priority:
            high_priority_tickets.append(ticket)

    return high_priority_tickets

def get_human_review_tickets(tickets:list[dict[str,any]])->list[dict[str,any]]:
    """
    Returns tickets that must be reviewed by a human.

    Agentic AI systems should not automatically handle every request.
    Refunds, payment disputes, legal issues, medical decisions,
    and security issues may require human approval.
    """
    review_tickets=[]
    for ticket in tickets:
        if ticket["require_human_review"]:
            review_tickets.append(ticket)
    return review_tickets

def create_ticket_summary(tickets: list[dict[str, Any]]) -> dict[str, int]:

    """
    Creates a summary dictionary containing ticket counts.
    """
    total_tickets = len(tickets)
    open_count = 0
    closed_count = 0
    high_priority_count = 0
    human_review_count = 0

    for ticket in tickets:
        if ticket["status"] == "open":
            open_count += 1

        if ticket["status"] == "closed":
            closed_count += 1

        if ticket["priority"] == "high":
            high_priority_count += 1

        if ticket["require_human_review"]:
            human_review_count += 1

    return {
        "total_tickets": total_tickets,
        "open_tickets": open_count,
        "closed_tickets": closed_count,
        "high_priority_tickets": high_priority_count,
        "human_review_tickets": human_review_count,
    }
def decide_ticket_route(ticket: dict[str, Any]) -> str:
    """
    Simulates a simple AI agent router.

    Later, you will replace this rule-based function with an LLM
    or LangGraph routing workflow.

    Possible routes:
    - HUMAN_REVIEW
    - BILLING_AGENT
    - ACCOUNT_AGENT
    - TECHNICAL_AGENT
    - GENERAL_SUPPORT_AGENT
    """
    category = ticket["category"]
    if ticket["require_human_review"]:
        return "HUMAN_REVIEW"

    if category in ["billing", "refund"]:
        return "BILLING_AGENT"

    if category in ["password_reset", "account_access"]:
        return "ACCOUNT_AGENT"

    if category == "technical_issue":
        return "TECHNICAL_AGENT"

    return "GENERAL_SUPPORT_AGENT"

def display_routing_decisions(tickets: list[dict[str, Any]]) -> None:
    """
    Prints the route selected for each open ticket.
    """
    print("\n--- AGENT ROUTING DECISIONS ---")

    for ticket in tickets:
        if ticket["status"] == "open":
            route = decide_ticket_route(ticket)

            print(
                f"Ticket {ticket['ticket_id']} "
                f"({ticket['category']}) "
                f"--> {route}"
            )
def main() -> None:
    """
    Main function that executes the Day 2 practice project.
    """
    display_all_ticket(support_ticket)

    open_tickets = get_open_tickets(support_ticket)
    high_priority_tickets = get_high_priority_tickets(support_ticket)
    human_review_tickets = get_human_review_tickets(support_ticket)
    summary = create_ticket_summary(support_ticket)

    print("\n--- FILTERED RESULTS ---")
    print(f"Open tickets: {len(open_tickets)}")
    print(f"High-priority open tickets: {len(high_priority_tickets)}")
    print(f"Tickets requiring human review: {len(human_review_tickets)}")

    print("\n--- TICKET SUMMARY ---")
    for key, value in summary.items():
        formatted_key = key.replace("_", " ").title()
        print(f"{formatted_key}: {value}")

    display_routing_decisions(support_ticket)


if __name__ == "__main__":
    main()