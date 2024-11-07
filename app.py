import streamlit as st
import pandas as pd
from travel_assistant_crew import travel_assistant_crew  # Import the crew from Travel_Crew.py

# Streamlit application
def main():
    st.title("Travel Assistant Crew")

    # Sidebar for user inputs
    with st.sidebar:
        destination = st.text_input("Destination (e.g., Paris)", "Paris")
        start_date = st.date_input("Start Date", value=pd.to_datetime("2024-10-20"))
        end_date = st.date_input("End Date", value=pd.to_datetime("2024-10-27"))
        # Travel Purpose
        default_travel_purpose = ["Leisure", "Business", "Adventure", "Cultural Exploration", "Wellness Retreat", "Romantic Getaway", "Family Vacation", "Solo Travel", "Team Building", "Eco-Tourism", "Spiritual Retreat"]
        travel_purpose = st.multiselect("Travel Purpose", default_travel_purpose, default=["Leisure"])
        new_travel_purpose = st.text_input("Add a new travel purpose")
        if new_travel_purpose and new_travel_purpose not in default_travel_purpose:
            travel_purpose.append(new_travel_purpose)
        # Activity Preferences         
        default_activity_preferences = ["Museums", "Historical Sites", "Local Cuisine", "Outdoor Activities", "Shopping", "Nightlife", "Hiking", "Beach Activities", "Wildlife Safari", "Art Galleries", "Workshops and Classes"]
        activity_preferences = st.multiselect("Activity Preferences", default_activity_preferences, default=["Museums", "Historical Sites", "Local Cuisine"])
        new_activity_preference = st.text_input("Add a new activity preference")
        if new_activity_preference and new_activity_preference not in default_activity_preferences:
            activity_preferences.append(new_activity_preference)
        # Dietary Requirements
        default_dietary_requirements = ["Vegetarian", "Vegan", "Gluten-Free", "Halal", "Kosher", "No Restrictions", "Pescatarian", "Dairy-Free", "Nut-Free", "Low-Carb"]
        dietary_requirements = st.multiselect("Dietary Requirements", default_dietary_requirements, default=["Vegetarian"])
        new_dietary_requirement = st.text_input("Add a new dietary requirement")
        if new_dietary_requirement and new_dietary_requirement not in default_dietary_requirements:
            dietary_requirements.append(new_dietary_requirement)

        # Cuisine Preferences
        default_cuisine_preferences = ["French", "Mediterranean", "Italian", "Asian", "Local Cuisine", "Indian", "Mexican", "Japanese", "Middle Eastern", "American"]
        cuisine_preferences = st.multiselect("Cuisine Preferences", default_cuisine_preferences, default=["French", "Mediterranean"])
        new_cuisine_preference = st.text_input("Add a new cuisine preference")
        if new_cuisine_preference and new_cuisine_preference not in default_cuisine_preferences:
            cuisine_preferences.append(new_cuisine_preference)

    # Main container for the generated itinerary
    itinerary_container = st.container()

    # Button state management
    generate_button_disabled = st.session_state.get("generate_button_disabled", False)
    generate_itinerary_button = st.button("Generate Itinerary", disabled=generate_button_disabled)

    # If the user clicks the "Generate Itinerary" button
    if generate_itinerary_button:
        st.session_state["generate_button_disabled"] = True
        # Prepare the input dictionary
        travel_assistant_inputs = {
            'destination': destination,
            'start_date': start_date,
            'end_date': end_date,
            'travel_purpose': travel_purpose,
            'activity_preferences': activity_preferences,
            'dietary_requirements': dietary_requirements,
            'cuisine_preferences': cuisine_preferences,
        }

        # Execute the crew's process with kickoff method
        result = travel_assistant_crew.kickoff(travel_assistant_inputs)

        # Display the generated itinerary in the container
        with itinerary_container:
            st.subheader("Generated Travel Itinerary")
            if isinstance(result, dict):
                if "daily_schedule" in result:
                    st.write("### Daily Schedule")
                    st.write(result["daily_schedule"])
                if "activities" in result:
                    st.write("### Activities and Attractions")
                    st.write(result["activities"])
                if "accommodations" in result:
                    st.write("### Accommodations")
                    st.write(result["accommodations"])
                if "dining" in result:
                    st.write("### Dining Recommendations")
                    st.write(result["dining"])
                if "logistics" in result:
                    st.write("### Transportation and Logistics")
                    st.write(result["logistics"])
                if "weather" in result:
                    st.write("### Weather Considerations")
                    st.write(result["weather"])
            else:
                st.write(result)

        # Re-enable the button after processing
        st.session_state["generate_button_disabled"] = False

if __name__ == "__main__":
    main()