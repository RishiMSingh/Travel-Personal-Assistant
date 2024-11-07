# Warning control
import warnings
warnings.filterwarnings('ignore')
from crewai import Agent, Task, Crew
import os
from crewai_tools import ScrapeWebsiteTool, SerperDevTool
from crewai import Crew, Process
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

os.environ["OPENAI_API_KEY"] = ''
os.environ["OPENAI_MODEL_NAME"] = 'gpt-3.5-turbo'
os.environ["SERPER_API_KEY"] = ''

search_tool = SerperDevTool()
scrape_tool = ScrapeWebsiteTool()

travel_coordinator_agent = Agent(
    role="Travel Coordinator",
    goal=
        """Coordinate all aspects of the user's travel, including planning activities, booking accommodations, and ensuring a smooth experience.
        Gather details such as destination, travel dates, and purpose of the visit, and provide a personalized itinerary.
        Integrate recommendations from all other agents to finalize a cohesive travel plan, including must-see attractions, local dining, and logistical details.
        Continuously adjust the plan based on weather, user preferences, and unforeseen changes.
        """,
    backstory="An experienced travel planner, you synthesize inputs from the entire crew to deliver an optimal and personalized travel experience, ensuring that all elements fit together smoothly.",
    verbose=True,
    allow_delegation=True,
    tools=[scrape_tool, search_tool]
)

weather_specialist_agent = Agent(
    role="Weather Specialist",
    goal=
        """Check the weather forecast for the destination on specified travel dates.
        Provide recommendations on suitable clothing and any weather-specific preparations (e.g., umbrellas, sunblock).
        Adjust the itinerary as needed based on the forecast, suggesting alternative activities in case of unfavorable weather.
        """,
    backstory="With extensive knowledge of meteorological data, you ensure that travelers are prepared for weather conditions at their destination and that their itinerary adapts accordingly.",
    verbose=True,
    allow_delegation=True,
    tools=[scrape_tool, search_tool]
)

local_guide_agent = Agent(
    role="Local Guide",
    goal=
        """Provide recommendations on the best places to visit based on the purpose of the trip, such as leisure, business, or cultural exploration.
        Research popular attractions, hidden gems, and must-see sights at the destination.
        Suggest a mix of activities tailored to user preferences, including cultural spots, shopping, dining, and outdoor activities.
        """,
    backstory="A local expert with a passion for showing travelers the best a destination has to offer, you curate personalized recommendations based on the user's interests and purpose of travel.",
    verbose=True,
    allow_delegation=True,
    tools=[scrape_tool, search_tool]
)

logistics_manager_agent = Agent(
    role="Logistics Manager",
    goal=
        """Ensure the user's travel plans run smoothly by managing logistics like transportation and accommodations.
        Provide recommendations on how to get around the city, including public transportation, taxis, or rentals.
        Suggest accommodations based on user preferences (e.g., budget, luxury, proximity to points of interest).
        Look up real-time fares and timings for transportation options, and assist in making reservations to ensure seamless transit.
        """,
    backstory="With a strong attention to detail and expertise in logistics, you handle all the transportation and accommodation arrangements to ensure a stress-free travel experience for the user.",
    verbose=True,
    allow_delegation=True,
    tools=[scrape_tool, search_tool]
)

culinary_guide_agent = Agent(
    role="Culinary Guide",
    goal=
        """Recommend dining options that suit the user's preferences, including local delicacies, dietary requirements, and must-try dishes.
        Provide options for different meal times, from breakfast to late-night dining.
        Suggest both well-known restaurants and off-the-beaten-path local favorites, tailored to the user's travel purpose.
        """,
    backstory="With a love for culinary experiences, you help travelers explore the local food scene, providing recommendations that match their tastes and dietary needs.",
    verbose=True,
    allow_delegation=True,
    tools=[scrape_tool, search_tool]
)

travel_coordinator_agent_senior = Agent(
    role="Travel Coordinator (Senior)",
    goal=
        """As a senior travel coordinator, you oversee the planning and execution of the entire travel experience, ensuring a seamless and enjoyable trip for the user. You take into account all the information gathered by the other agents and synthesize it into a cohesive travel plan.
        Your role involves coordinating with the user to finalize the itinerary, making real-time adjustments based on feedback and preferences. You are responsible for ensuring that all elements of the trip, from activities to dining and logistics, align with the user's expectations and needs.
        Your experience and expertise in travel planning allow you to anticipate potential issues and provide proactive solutions, creating a stress-free and memorable travel experience for the user.
        You create a final itinerary that reflects the user's preferences, the local culture, and the unique experiences that the destination has to offer, ensuring that every moment of the trip is well-planned and enjoyable with links to your recommendations.
        You create a daily schedule that includes activities, dining options, transportation details, and any special considerations, such as weather updates or last-minute changes. You provide a detailed overview of each day's plan, allowing the user to navigate the destination with ease and make the most of their travel experience.
        You are very specific with the places timings and costs, and you provide a detailed overview of each day's plan, allowing the user to navigate the destination with ease and make the most of their travel experience.
        """,
    backstory="With years of experience in travel planning, you have honed your skills to create unforgettable travel experiences for your clients. Your attention to detail and personalized approach set you apart as a trusted advisor in the world of travel.",
    verbose=True,
    allow_delegation=True,
    tools=[scrape_tool, search_tool]
)

travel_itinerary_task = Task(
    description=(
        "Develop a comprehensive travel itinerary for {destination}. Gather inputs from all agents, including weather updates, local attractions, dining options, logistics, and transportation details."
        "Ensure the itinerary accounts for the user's travel dates ({start_date} to {end_date}), purpose of visit ({travel_purpose}), and preferences for activities ({activity_preferences})."
        "Plan each day to include activities, transportation details (with timings and real-time fares), dining, and accommodation arrangements."
        "Adjust plans based on the latest weather information and user feedback to create a dynamic and enjoyable travel experience."
    ),
    expected_output=(
        "A complete travel itinerary for {destination}, including day-by-day activities, dining suggestions, transportation details with timings and fares, and accommodation details. The itinerary should be flexible, allowing for real-time adjustments based on weather and user feedback."
    ),
    agent=travel_coordinator_agent,
)

weather_analysis_task = Task(
    description=(
        "Analyze the weather forecast for {destination} on the specified travel dates ({start_date} to {end_date})."
        "Provide recommendations on suitable clothing and preparations for the weather conditions, and suggest any adjustments to the planned activities based on the forecast."
    ),
    expected_output=(
        "A weather report for {destination} on the specified dates, including specific recommendations for clothing and activities. The report should also suggest contingency plans in case of unfavorable weather."
    ),
    agent=weather_specialist_agent,
)

local_attractions_task = Task(
    description=(
        "Research and recommend the top attractions in {destination} based on the user's purpose of visit ({travel_purpose})."
        "Provide a diverse selection of activities, including cultural sites, outdoor activities, and unique local experiences, tailored to user preferences. Include opening hours and estimated time for each activity."
    ),
    expected_output=(
        "A curated list of recommended attractions in {destination}, including descriptions, estimated time needed, opening hours, and relevance to the user's travel purpose."
    ),
    agent=local_guide_agent,
)

logistics_planning_task = Task(
    description=(
        "Plan the logistics for {destination}, including transportation options, accommodation recommendations, and real-time transportation fares."
        "Provide details on how to navigate the destination, including public transportation schedules, taxi options, rental suggestions, and accommodation choices."
        "Assist in making reservations and ensure seamless navigation through the destination."
    ),
    expected_output=(
        "A logistics plan for {destination}, including transportation recommendations with real-time fares, accommodation options, and practical travel tips to ensure a comfortable experience."
    ),
    agent=logistics_manager_agent,
)

culinary_recommendations_task = Task(
    description=(
        "Recommend the best dining options in {destination} based on the user's culinary preferences ({dietary_requirements}, {cuisine_preferences})."
        "Suggest places for different meals (breakfast, lunch, dinner) and provide options for both popular and local hidden gems. Include estimated costs and reservation requirements if applicable."
    ),
    expected_output=(
        "A list of dining recommendations in {destination}, tailored to the user's preferences, including descriptions, meal options, estimated costs, and reasons for recommendation."
    ),
    agent=culinary_guide_agent,
)

final_travel_itinerary_task = Task(
    description=(
        "Develop a comprehensive travel itinerary for {destination}. Gather inputs from all agents, including weather updates, local attractions, dining options, logistics, and transportation details. and provide a personalized itinerary."
        "Ensure the itinerary accounts for the user's travel dates ({start_date} to {end_date}), purpose of visit ({travel_purpose}), and preferences for activities ({activity_preferences}) are taken into account and your suggestion is personalized."
        "Plan each day to include activities, transportation details (with timings and real-time fares), dining, and accommodation arrangements along with relevant links for one click and bookings services." 
        "Adjust plans based on the latest weather information and user feedback to create a dynamic and enjoyable travel experience along with taking into account any political issues and other issues that might impact their travel."
    ),
    expected_output=(
        "A complete travel itinerary for {destination}, including day-by-day activities with timings, dining suggestions with food recomendations looking at the menu, transportation details with timings and fares along with website link to book. The itinerary should be flexible, allowing for real-time adjustments based on weather and user feedback."
    ),
    agent=travel_coordinator_agent_senior,
)

# Define the crew with agents and tasks
travel_assistant_crew = Crew(
    agents=[
        travel_coordinator_agent,
        weather_specialist_agent,
        local_guide_agent,
        logistics_manager_agent,
        culinary_guide_agent,
        travel_coordinator_agent_senior
    ],
    
    tasks=[
        travel_itinerary_task,
        weather_analysis_task,
        local_attractions_task,
        logistics_planning_task,
        culinary_recommendations_task,
        final_travel_itinerary_task
    ],
    
    manager_llm=ChatOpenAI(model="gpt-3.5-turbo", 
                           temperature=0.7),
    process=Process.hierarchical,
    verbose=True
)

travel_assistant_inputs = {
    'destination': 'Paris',
    'start_date': '2024-10-20',
    'end_date': '2024-10-27',
    'travel_purpose': ['Leisure', 'Business', 'Adventure', 'Cultural Exploration', 'Wellness Retreat', 'Romantic Getaway', 'Family Vacation'],
    'activity_preferences': ['Museums', 'Historical Sites', 'Local Cuisine'],
    'dietary_requirements': ['Vegetarian', 'Vegan', 'Gluten-Free', 'Halal', 'Kosher'],
    'cuisine_preferences': ['French', 'Mediterranean']
}


#Use different LLMS 
#GCP system smaller LLMS
#Find a metric to evaluate response quality
#Budget-> objective metris 
#Lower the word count simplier it is to understand
#Clickworkers -> llm1, llm2, llm3
# Less expensive solution - Chatbot arena  
