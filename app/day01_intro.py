"""
Day 1: Python setup check for the Gen AI and Agentic AI learning journey
"""

def introduce_developer(name:str,goal:str)->str:
    """
        Returns a message describing the learner's goal.

    Args:
        name: Developer's name.
        goal: Learning objective.

    Returns:
        A formatted introductory message.
    """
    return(
        f'hello,{name}!\n'
        f"Your learning goal is: {goal}\n"
        "You are starting your Generative AI and Agentic AI journey today."
    )

def calculate_study_process(
        completed_days:int,
        total_days:int=90
)->float:
    """
    Calculates completion percentage for the learning roadmap.
    """
    if total_days<=0:
        raise ValueError("total_days must be greater than zero.")

    progress=(completed_days/total_days)*100
    return round(progress,2)

if __name__=="__main__":
        message=introduce_developer(name="soundar",goal="Learning_goal")
        process=calculate_study_process(completed_days=1)
print(message)
print(f"\nLearning progress: {process}%")