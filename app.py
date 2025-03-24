import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=api_key)
import requests
import json
from typing import List

st.set_page_config(page_title="Zovy's Multi-agent Vegetarian Assistant 🤖")
st.title("Zovy's Multi-agent Vegetarian Assistant 🤖")

# Input Fields
api_key = st.text_input("Enter your OpenAI API Key", type="password")
restaurant_query = st.text_area("Enter the name or description of the restaurant")

# Trigger
if st.button("Run Multi-Agent AI") and api_key and restaurant_query:

    def call_gpt(prompt: str) -> str:
        response = client.chat.completions.create(model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful vegetarian food assistant."},
            {"role": "user", "content": prompt}
        ])
        return response.choices[0].message.content.strip()

    # Agent 1 - Review Article and Google Review
    with st.spinner("Generating review article and Google review..."):
        review_prompt = f"Write a short blog article and a Google-style review for a vegetarian-friendly restaurant called: {restaurant_query}"
        review_output = call_gpt(review_prompt)
        st.subheader("📝 Blog Article and Google Review")
        st.write(review_output)

    # Agent 2 - Social Media Posts
    with st.spinner("Creating social media posts..."):
        social_prompt = f"Create 3 fun, engaging social media posts about the vegetarian restaurant {restaurant_query}. Include hashtags and emojis."
        social_output = call_gpt(social_prompt)
        st.subheader("📣 Social Media Posts")
        st.write(social_output)

    # Agent 3 - Vegetarian Sampler Menu
    with st.spinner("Creating vegetarian sampler menu..."):
        menu_prompt = f"Generate a typical 3-course sampler vegetarian menu (starter, main, dessert) for the restaurant {restaurant_query}."
        menu_output = call_gpt(menu_prompt)
        st.subheader("🥗 Vegetarian Sampler Menu")
        st.write(menu_output)

    # Agent 4 - Booking Aggregators
    with st.spinner("Fetching booking links and phone number..."):
        search_url = f"https://nominatim.openstreetmap.org/search?q={restaurant_query}&format=json"
        response = requests.get(search_url)
        booking_output = ""

        if response.status_code == 200 and len(response.json()) > 0:
            location = response.json()[0]
            address = location['display_name']
            lat, lon = location['lat'], location['lon']
            booking_output += f"**Address**: {address}\n\n"
            booking_output += f"Try booking on [OpenTable](https://www.opentable.com) or [TheFork](https://www.thefork.com). Search with the name: **{restaurant_query}**.\n\n"
            booking_output += f"If available, you can call them directly or visit their website."
        else:
            booking_output = "Sorry, couldn't fetch the booking info. Try searching manually on Google."

        st.subheader("📞 Booking Info and Links")
        st.write(booking_output)

    # Agent 5 - Map + Small Photos
    with st.spinner("Showing map and images..."):
        if response.status_code == 200 and len(response.json()) > 0:
            lat, lon = location['lat'], location['lon']
            st.subheader("🗺️ Map View")
            st.map({"lat": [float(lat)], "lon": [float(lon)]})

            # Use Google Custom Search API or Unsplash for images (mocked for now)
            st.subheader("📸 Restaurant Images")
            st.image([
                "https://source.unsplash.com/400x300/?vegetarian-restaurant",
                "https://source.unsplash.com/400x300/?plant-based-food",
                "https://source.unsplash.com/400x300/?vegan-meal"
            ], width=250)
        else:
            st.warning("Couldn't fetch location details for map or images.")

else:
    st.info("Please enter your OpenAI API Key and a restaurant query to begin.")
