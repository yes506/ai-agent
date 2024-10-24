from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

from agents.agent_steven import plan
from agents.travel_topic_tool import search_wiki_page_and_store_raw
from agents.agent_chatbot import chat


class Question(BaseModel):
    startPoint: str
    radius: int
    numberOfMember: int
    relationship: str
    purpose: str
    travelDate: str
    startTime: str
    endTime: str
    mealLunchStartTime: str
    mealLunchEndTime: str
    mealDinnerStartTime: str
    mealDinnerEndTime: str
    members: list


class TravelTopics(BaseModel):
    travelSpots: list


class ChatMessage(BaseModel):
    message: str


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/plan-travel")
def make_a_travel_plan(question: Question):
    result = plan(question.startPoint,
                  question.radius,
                  question.numberOfMember,
                  question.relationship,
                  question.purpose,
                  question.travelDate,
                  question.startTime,
                  question.endTime,
                  question.mealLunchStartTime,
                  question.mealLunchEndTime,
                  question.mealDinnerStartTime,
                  question.mealDinnerEndTime,
                  question.members)
    return result


@app.get("/routes-map")
def get_travel_routes_maps(path: str):
    flow_order = (path.split("/")[-1]).split("_")[0]
    file_name = f"routes_map_{flow_order}.png"
    return FileResponse(path, filename=file_name, media_type="image/png")


@app.post("/travel-topics/preprocess")
def pre_proceed_travel_topic(travel_topics: TravelTopics):
    topics = travel_topics.travelSpots
    search_wiki_page_and_store_raw(topics)
    return {
        "data":
            {
                "result: ": "success",
                "count": len(topics)
            }
    }


@app.post("/chatbot/chat")
def chat_with_chatbot(chat_message: ChatMessage):
    return chat(chat_message.message)
