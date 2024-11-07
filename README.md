# Travel Assistant Project

This Travel Assistant is a personalized travel planning tool that leverages AI agents to create customized itineraries based on user preferences and travel details. The project is structured to showcase skills in developing user-centered applications and deploying collaborative AI models for real-world scenarios.

## Project Overview

The Travel Assistant uses CrewAI, a framework for creating AI agents that collaborate to provide travel recommendations. Users can input details such as their destination, travel dates, and activity preferences, and the system generates a comprehensive itinerary, making travel planning seamless and interactive.

### Key Features

- **Personalized Itineraries**: Based on destination and user preferences, the assistant generates a day-by-day itinerary that includes recommended activities, dining options, and local attractions.
- **CrewAI Collaboration**: Multiple AI agents work together, each specializing in different aspects of travel planning, such as weather adaptation, logistics, and local attractions, to create a comprehensive and flexible itinerary.

## Project Structure

- **app.py**: Main application interface, capturing user inputs through a streamlined UI and displaying the generated travel itinerary.
- **travel_assistant_crew.py**: Contains the CrewAI setup, where specialized agents are defined for tasks like itinerary planning, weather forecasting, and logistics management. Note - please add your own OPENAI api key and serper api key. 

## Technologies Used

- **Python**: Core language for application logic and AI integration.
- **CrewAI**: Framework used for building and managing collaborative AI agents, allowing complex, multi-agent interactions for itinerary generation.
- **Streamlit** (optional): For deploying the application with a user-friendly web interface.


