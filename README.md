# Students agent

This is a personal project to develop my skills on agents.

It consists on an agent that reads my logs in obsidian (I am using Obsidian Sync to keep everything updated everywhere) and based on the students I have booked every day it sends me a summary of their homework and a suggested topic we can do in the lesson using Gemini (currently Gemini Flash 3.5). Then it is sent to my personal whatapp through Twilio.

## Stack
- Python 13.3
- Pydantic for base model
- Google genai
- Google calendar API
- Twilio API to send me messages
- Obsidian notes https://obsidian.md/