from datetime import datetime

from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext


def adjust_content_difficulty(tool_context: ToolContext) -> dict:
    """
    Adjusts the difficulty level for the current learning module.
    Updates state with the new difficulty preference.
    """
    course_id = tool_context.args.get("course_id")
    new_difficulty = tool_context.args.get("difficulty")  # "easier", "harder", or "current"
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Get current difficulty preferences
    difficulty_preferences = tool_context.state.get("difficulty_preferences", {})

    # Update difficulty preference for the course
    difficulty_preferences[course_id] = new_difficulty

    # Update state
    tool_context.state["difficulty_preferences"] = difficulty_preferences

    # Update interaction history
    current_interaction_history = tool_context.state.get("interaction_history", [])
    new_interaction_history = current_interaction_history.copy()
    new_interaction_history.append({
        "action": "adjust_difficulty",
        "course_id": course_id,
        "new_difficulty": new_difficulty,
        "timestamp": current_time
    })
    tool_context.state["interaction_history"] = new_interaction_history

    return {
        "status": "success",
        "message": f"Successfully adjusted difficulty for course {course_id} to {new_difficulty}",
        "course_id": course_id,
        "difficulty": new_difficulty,
        "timestamp": current_time,
    }


def adjust_learning_pace(tool_context: ToolContext) -> dict:
    """
    Adjusts the learning pace for the current course.
    Updates state with the new pace preference.
    """
    course_id = tool_context.args.get("course_id")
    new_pace = tool_context.args.get("pace")  # "slower", "faster", or "current"
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Get current pace preferences
    pace_preferences = tool_context.state.get("pace_preferences", {})

    # Update pace preference for the course
    pace_preferences[course_id] = new_pace

    # Update state
    tool_context.state["pace_preferences"] = pace_preferences

    # Update interaction history
    current_interaction_history = tool_context.state.get("interaction_history", [])
    new_interaction_history = current_interaction_history.copy()
    new_interaction_history.append({
        "action": "adjust_pace",
        "course_id": course_id,
        "new_pace": new_pace,
        "timestamp": current_time
    })
    tool_context.state["interaction_history"] = new_interaction_history

    return {
        "status": "success",
        "message": f"Successfully adjusted learning pace for course {course_id} to {new_pace}",
        "course_id": course_id,
        "pace": new_pace,
        "timestamp": current_time,
    }


# Create the adaptive learning agent
adaptive_learning_agent = Agent(
    name="adaptive_learning",
    model="gemini-2.0-flash",
    description="Adaptive learning agent that adjusts content difficulty and pacing in real-time",
    instruction="""
    You are the Adaptive Learning agent for the Personalized Learning Platform.
    Your role is to adjust the learning experience by modifying content difficulty, pacing, and 
    presentation based on student performance and preferences.

    <student_info>
    Name: {student_name}
    Learning Style: {learning_style}
    Current Courses: {current_courses}
    </student_info>

    <learning_preferences>
    Difficulty Preferences: {difficulty_preferences}
    Pace Preferences: {pace_preferences}
    </learning_preferences>

    <learning_history>
    Quiz Results: {quiz_results}
    Learning Time Data: {learning_time_data}
    Engagement Metrics: {engagement_metrics}
    </learning_history>

    Your responsibilities:

    1. Difficulty Adjustment
       - Analyze quiz performance to determine appropriate difficulty levels
       - Suggest easier content when success rate is consistently low (<60%)
       - Recommend more challenging content when success rate is high (>85%)
       - Use adjust_content_difficulty tool to update preferences
       - Balance challenge with achievement to maintain motivation

    2. Pace Modification
       - Monitor learning time metrics to optimize pacing
       - Suggest slower pace when completion times are significantly above average
       - Recommend faster pace when completion times are consistently quick
       - Use adjust_learning_pace tool to update preferences
       - Consider time constraints and learning goals when making recommendations

    3. Content Variation
       - Rotate between different content types based on engagement metrics
       - Suggest alternative presentation formats for difficult concepts
       - Switch between theory and practical application to maintain interest
       - Recommend review sessions when performance indicates knowledge gaps
       - Introduce variety in learning materials to prevent fatigue

    4. Dynamic Recommendations
       - Suggest real-time content modifications based on session performance
       - Provide on-the-spot alternative explanations when confusion is detected
       - Offer additional practice for concepts with low mastery scores
       - Recommend breaks or subject changes when engagement metrics decline
       - Celebrate achievements to build confidence and momentum

    When adapting:
    - Make changes incrementally to avoid overwhelming the student
    - Clearly explain the reasoning behind adaptation recommendations
    - Seek student input on whether adaptations are helpful
    - Balance challenge with achievability to maintain motivation
    - Consider long-term learning goals when making short-term adjustments

    Your outputs:
    - Difficulty adjustment recommendations with clear rationales
    - Pace modification suggestions based on performance data
    - Content variation strategies to optimize engagement
    - Real-time adaptations in response to current session data
    """,
    tools=[adjust_content_difficulty, adjust_learning_pace],
)
