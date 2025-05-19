from datetime import datetime

from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext


def add_learning_goal(tool_context: ToolContext) -> dict:
    """
    Adds a new learning goal for the student.
    Updates state with the new goal information.
    """
    goal_title = tool_context.args.get("title")
    goal_description = tool_context.args.get("description", "")
    goal_target_date = tool_context.args.get("target_date", "")
    goal_type = tool_context.args.get("type", "knowledge")  # "knowledge", "skill", "project"
    goal_related_subjects = tool_context.args.get("related_subjects", [])
    
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    goal_id = f"goal_{current_time.replace(' ', '_').replace(':', '_').replace('-', '_')}"

    # Get current learning goals
    learning_goals = tool_context.state.get("learning_goals", [])

    # Add the new goal
    new_goals = learning_goals.copy()
    new_goals.append({
        "id": goal_id,
        "title": goal_title,
        "description": goal_description,
        "type": goal_type,
        "status": "active",
        "progress": 0,
        "created_date": current_time,
        "target_date": goal_target_date,
        "related_subjects": goal_related_subjects
    })

    # Update state
    tool_context.state["learning_goals"] = new_goals

    # Update interaction history
    current_interaction_history = tool_context.state.get("interaction_history", [])
    new_interaction_history = current_interaction_history.copy()
    new_interaction_history.append({
        "action": "add_goal",
        "goal_id": goal_id,
        "goal_title": goal_title,
        "timestamp": current_time
    })
    tool_context.state["interaction_history"] = new_interaction_history

    return {
        "status": "success",
        "message": f"Successfully added new learning goal: {goal_title}",
        "goal_id": goal_id,
        "timestamp": current_time,
    }


def update_goal_progress(tool_context: ToolContext) -> dict:
    """
    Updates the progress of an existing learning goal.
    Updates state with the new progress information.
    """
    goal_id = tool_context.args.get("goal_id")
    new_progress = tool_context.args.get("progress")  # 0-100 percentage
    progress_note = tool_context.args.get("note", "")
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Get current learning goals
    learning_goals = tool_context.state.get("learning_goals", [])
    
    # Find and update the specific goal
    updated = False
    new_goals = []
    for goal in learning_goals:
        if isinstance(goal, dict) and goal.get("id") == goal_id:
            updated_goal = goal.copy()
            updated_goal["progress"] = new_progress
            
            # If progress is 100%, mark as completed
            if new_progress >= 100:
                updated_goal["status"] = "completed"
                updated_goal["completion_date"] = current_time
            
            # Add progress note if provided
            if progress_note:
                if "progress_notes" not in updated_goal:
                    updated_goal["progress_notes"] = []
                updated_goal["progress_notes"].append({
                    "note": progress_note,
                    "timestamp": current_time,
                    "progress": new_progress
                })
                
            new_goals.append(updated_goal)
            updated = True
        else:
            new_goals.append(goal)

    if not updated:
        return {
            "status": "error",
            "message": f"Goal with ID {goal_id} not found"
        }

    # Update state
    tool_context.state["learning_goals"] = new_goals

    # Update interaction history
    current_interaction_history = tool_context.state.get("interaction_history", [])
    new_interaction_history = current_interaction_history.copy()
    new_interaction_history.append({
        "action": "update_goal_progress",
        "goal_id": goal_id,
        "new_progress": new_progress,
        "timestamp": current_time
    })
    tool_context.state["interaction_history"] = new_interaction_history

    # Status message
    message = f"Updated progress for goal to {new_progress}%"
    if new_progress >= 100:
        message = f"Congratulations! Goal marked as completed with 100% progress"

    return {
        "status": "success",
        "message": message,
        "goal_id": goal_id,
        "progress": new_progress,
        "timestamp": current_time,
    }


# Create the goal setting agent
goal_setting_agent = Agent(
    name="goal_setting",
    model="gemini-2.0-flash",
    description="Goal setting agent that helps students set and track personalized learning goals",
    instruction="""
    You are the Goal Setting agent for the Personalized Learning Platform.
    Your role is to help students set meaningful learning goals, track progress, and celebrate achievements.

    <student_info>
    Name: {student_name}
    Subject Interests: {subject_interests}
    Learning Style: {learning_style}
    Career Aspirations: {career_aspirations}
    </student_info>

    <learning_goals>
    Current Goals: {learning_goals}
    </learning_goals>

    <learning_history>
    Completed Courses: {completed_courses}
    Current Courses: {current_courses}
    Quiz Results: {quiz_results}
    </learning_history>

    Your responsibilities:

    1. Goal Creation
       - Help students create SMART goals (Specific, Measurable, Achievable, Relevant, Time-bound)
       - Suggest appropriate goal types (knowledge, skill, project, certification)
       - Use add_learning_goal tool to add new goals to the system
       - Connect goals to career aspirations when relevant
       - Ensure goals are challenging but achievable

    2. Progress Tracking
       - Monitor goal progress through regular check-ins
       - Use update_goal_progress tool to record progress updates
       - Help students identify and overcome obstacles
       - Suggest resources to aid in goal achievement
       - Maintain an appropriate timeline for each goal

    3. Achievement Celebration
       - Acknowledge completed goals and milestones
       - Highlight the impact of achievements on overall learning journey
       - Connect completed goals to future opportunities
       - Encourage reflection on the learning process
       - Suggest appropriate next goals after completion

    4. Goal Refinement
       - Help students adjust goals when necessary
       - Recognize when goals need modification based on changing interests
       - Break down overly ambitious goals into manageable steps
       - Combine related goals when appropriate
       - Suggest timeline adjustments when progress is faster or slower than expected

    When helping with goals:
    - Focus on intrinsic motivation rather than just completion
    - Connect goals to students' interests and larger aspirations
    - Maintain a positive and encouraging tone
    - Recognize effort as well as achievement
    - Help students learn from both successes and setbacks

    Example Goal Types:
    - Knowledge: "Understand key machine learning algorithms and their applications"
    - Skill: "Build a functional web application using React"
    - Project: "Create a data visualization portfolio piece using Python"
    - Certification: "Complete and pass the AWS Cloud Practitioner certification"

    Your outputs:
    - SMART goal suggestions tailored to the student
    - Progress tracking updates with encouraging feedback
    - Achievement celebrations that recognize effort and impact
    - Goal refinement recommendations when necessary
    """,
    tools=[add_learning_goal, update_goal_progress],
)
