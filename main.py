from pydantic import BaseModel
import os
from pathlib import Path
import json
from dotenv import load_dotenv
from google import genai
from gtts import gTTS
from twilio.rest import Client
from datetime import date

load_dotenv()

vault_path = Path("C:/Users/ferna/Documents/fjara/Students")

students_per_day = {
    "Monday": ("Sebastian", "Gia", "Kairav", "Diana", "Zaria", "Jory"),
    "Tuesday": ("Toby", "Clara", "Chloe", "Max", "Charlie"),
    "Wednesday": ("Aubrey", "Bodie", "Abraham", "Sydney", "Dylan"),
    "Thursday": ("Luther", "Tue", "Karina"),
    "Friday": ("Shi", "David", "Sara", "Joanna"),
    "Saturday": ("Fabiana", "Faizeen")
}


students_today: tuple[str] = students_per_day[date.today().strftime("%A")]


class Student_context(BaseModel):
    name: str
    context: str


def is_there_a_log(name) -> bool:
    return True if name in os.listdir(path=vault_path.resolve()) else False


def get_student_log(name: str) -> str:
    with open(vault_path / name  / "log.md", "r") as note:
        context = note.read()
    return context

list_of_students: list[Student_context] = []
for student in students_today:
    if is_there_a_log(student):
        list_of_students.append(
            Student_context(
                name=student,
                context=get_student_log(student)
            )
        )

students_context = json.dumps([student.model_dump() for student in list_of_students], 
                separators=(',', ':'), 
                ensure_ascii=False)

prompt = f"""
You are an music teacher specialist with more than 20 years of experience. Use modern pedagogical techniques in order to create good recomendations for each lesson.

I will share list of students in a json format with name and context which is a markdown log file that I write every lesson. You will give me a summary of the their homework and also a short recomendation to cover in todays lesson based on their log. Avoid any introduction such as "As a music pedagogy with over..." go straight to the point. Avoid any markdown sintax keep the response as a plain text response.
Do this for each student you receive in the following json.
{students_context}

Start your response with: "Hi, Fernando. Today you have [students names]. This is your summary.
"""

client = genai.Client()

response = client.models.generate_content(
    model="gemini-3.5-flash",
    contents=prompt + students_context
)

# tts = gTTS(response.text, lang="en", slow=False)

# tts.save("students_agent.mp3")



client = Client(os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN"))

message = client.messages.create(
  from_="whatsapp:+14155238886",
  body=response.text,
  to="whatsapp:+14379869875"
)