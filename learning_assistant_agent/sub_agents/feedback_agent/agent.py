from datetime import datetime

from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext


def submit_feedback(tool_context: ToolContext) -> dict:
    """
    Submits student feedback on courses, resources, or the learning experience.
    Updates state with the feedback information.
    """
    feedback_type = tool_context.args.get("type")  # "course", "resource", "recommendation", "general"
    feedback_content = tool_context.args.get("content")
    feedback_rating = tool_context.args.get("rating", 0)  # 1-5 scale
    item_id = tool_context.args.get("item_id", "")  # Course ID, resource ID, etc.
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    feedback_id = f"feedback_{current_time.replace(' ', '_').replace(':', '_').replace('-', '_')}"
    
    # Get current feedback list
    feedback_list = tool_context.state.get("feedback_list", [])
    
    # Add new feedback
    new_feedback_list = feedback_list.copy()
    new_feedback_list.append({
        "id": feedback_id,
        "type": feedback_type,
        "content": feedback_content,
        "rating": feedback_rating,
        "item_id": item_id,
        "timestamp": current_time
    })
    
    # Update state
    tool_context.state["feedback_list"] = new_feedback_list
    
    # Update interaction history
    current_interaction_history = tool_context.state.get("interaction_history", [])
    new_interaction_history = current_interaction_history.copy()
    new_interaction_history.append({
        "action": "submit_feedback",
        "feedback_id": feedback_id,
        "feedback_type": feedback_type,
        "timestamp": current_time
    })
    tool_context.state["interaction_history"] = new_interaction_history
    
    return {
        "status": "success",
        "message": f"Successfully recorded your feedback",
        "feedback_id": feedback_id,
        "timestamp": current_time,
    }


def update_recommendation_relevance(tool_context: ToolContext) -> dict:
    """
    Updates the relevance score for a recommendation based on student feedback.
    This helps improve future recommendations.
    """
    recommendation_id = tool_context.args.get("recommendation_id")
    relevance_score = tool_context.args.get("relevance_score")  # 1-5 scale
    feedback_note = tool_context.args.get("feedback_note", "")
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Get current recommendation feedback
    recommendation_feedback = tool_context.state.get("recommendation_feedback", {})
    
    # Update feedback for the specific recommendation
    recommendation_feedback[recommendation_id] = {
        "relevance_score": relevance_score,
        "feedback_note": feedback_note,
        "timestamp": current_time
    }
    
    # Update state
    tool_context.state["recommendation_feedback"] = recommendation_feedback
    
    # Update interaction history
    current_interaction_history = tool_context.state.get("interaction_history", [])
    new_interaction_history = current_interaction_history.copy()
    new_interaction_history.append({
        "action": "update_recommendation_relevance",
        "recommendation_id": recommendation_id,
        "relevance_score": relevance_score,
        "timestamp": current_time
    })
    tool_context.state["interaction_history"] = new_interaction_history
    
    return {
        "status": "success",
        "message": f"Thank you for rating this recommendation",
        "recommendation_id": recommendation_id,
        "relevance_score": relevance_score,
        "timestamp": current_time,
    }


# Create the feedback agent
feedback_agent = Agent(
    name="feedback",
    model="gemini-2.0-flash",
    description="Feedback agent that gathers and integrates student feedback to improve the learning experience",
    instruction="""
    You are the Feedback Integration agent for the Personalized Learning Platform.
    Your role is to collect, analyze, and incorporate student feedback to continuously improve 
    the learning experience and recommendations.

    <student_info>
    Name: {student_name}
    Subject Interests: {subject_interests}
    Learning Style: {learning_style}
    </student_info>

    <feedback_data>
    Previous Feedback: {feedback_list}
    Recommendation Feedback: {recommendation_feedback}
    </feedback_data>

    <learning_history>
    Completed Courses: {completed_courses}
    Current Courses: {current_courses}
    </learning_history>

    Your responsibilities:

    1. Feedback Collection
       - Encourage students to provide feedback on learning materials
       - Ask specific questions about content quality, difficulty, and relevance
       - Use submit_feedback tool to record feedback in various categories
       - Gather input on recommendation quality and learning experience
       - Create a positive feedback culture that emphasizes improvement

    2. Feedback Analysis
       - Identify patterns in student feedback across materials
       - Track sentiment trends over time
       - Correlate feedback with student performance and engagement
       - Recognize recurring themes in positive and negative feedback
       - Use feedback to identify knowledge gaps in available content

    3. Recommendation Refinement
       - Use update_recommendation_relevance tool to record recommendation quality
       - Incorporate feedback into future content and resource suggestions
       - Adjust recommendation strategies based on feedback patterns
       - Filter out consistently low-rated resources
       - Prioritize highly-rated content in similar contexts

    4. Learning Experience Improvement
       - Suggest platform improvements based on feedback trends
       - Identify content areas needing expansion or revision
       - Connect student feedback to specific learning outcomes
       - Recommend experiential adjustments to other agents
       - Track the impact of changes made in response to feedback

    When collecting and using feedback:
    - Create a safe, non-judgmental environment for honest input
    - Acknowledge all feedback positively, even when critical
    - Close the feedback loop by explaining how input will be used
    - Balance individual preferences with evidence-based best practices
    - Distinguish between subjective preferences and objective quality issues

    Your outputs:
    - Thoughtful feedback prompts that encourage specific, actionable input
    - Analysis of feedback trends with clear patterns and insights
    - Recommendation adjustments based on feedback data
    - Improvement suggestions for the overall learning experience
    """,
    tools=[submit_feedback, update_recommendation_relevance],
)
