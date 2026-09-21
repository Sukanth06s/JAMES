const API_BASE_URL="http://127.0.0.1:8000"

export async function sendMessage(message, conversation=[]){
    const response=await fetch(`${API_BASE_URL}/chat`,{
        method:"POST",
        headers:{
            "Content-Type":"application/json",
        },
        body:JSON.stringify({
            message,
            conversation,
        }),
    });
    if(!response.ok)
    {
        throw new Error(`Chat request failed: ${response.status}`);
    }
    return response.json();
}

export async function getEpisode(){
    const response=await fetch(`${API_BASE_URL}/episodes`);

    if (!response.ok) {
    throw new Error(`Failed to load episodes: ${response.status}`);
  }

  return response.json();
}

export async function getEpisodeById(episodeId) {
  const response = await fetch(
    `${API_BASE_URL}/episodes/${episodeId}`
  );

  if (!response.ok) {
    throw new Error(`Failed to load episode: ${response.status}`);
  }

  return response.json();
}

export async function getEpisodeObservations(episodeId) {
  const response = await fetch(
    `${API_BASE_URL}/episodes/${episodeId}/observations`
  );

  if (!response.ok) {
    throw new Error(
      `Failed to load observations: ${response.status}`
    );
  }

  return response.json();
}

export async function checkHealth() {
  const response = await fetch(`${API_BASE_URL}/health`);

  if (!response.ok) {
    throw new Error("Backend unavailable");
  }

  return response.json();
}