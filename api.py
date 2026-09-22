from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from core.processor import process_input
from storage.db import load_all_episodes,load_all_observations,load_all_candidates

app=FastAPI(
    title="JAMES API",
    description="API for the JAMES Persistent Adaptive Assistant",
    version="1.0.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message:str
    conversation:list=[]

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "JAMES API"
    }

@app.post("/chat")
def chat(request: ChatRequest):
    result=process_input(request.message)
    return result

@app.get("/episodes")
def get_episode():
    return load_all_episodes()

@app.get("/episodes/{episode_id}")
def get_episode(episode_id:str):
    episodes=load_all_episodes()

    for episode in episodes:
        if episode.get("episode_id")==episode_id:
            return episode

    raise HTTPException(
        status_code=404,
        detail=f"Episode '{episode_id}' not found"
    )

@app.get("/episodes/{episode_id}/observations")
def get_episode_observations(episode_id:str):
    episodes=load_all_episodes()

    episode=next(
        (
            episode
            for episode in episodes
            if episode.get("episode_id")==episode_id
        ),
        None
    )

    if episode is None:
        raise HTTPException(
            status_code=404,
            detail=f"Episode '{episode_id}' not found"
        )

    observation_ids=set(
        episode.get("related_observations",[])
    )
    observations=load_all_observations()
    return [
        observation
        for observation in observations
        if observation.get("id") in observation_ids
    ]

@app.get("/candidates")
def get_candidates():
    return load_all_candidates()