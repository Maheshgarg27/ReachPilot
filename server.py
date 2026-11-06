from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from starlette.concurrency import run_in_threadpool

from research import search_web
from extractor import extract_founders
from enrichment import enrich_leads
from personalizer import generate_message


app = FastAPI(title="ReachPilot API")

# Development configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class SearchRequest(BaseModel):
    prompt: str
    number_of_leads: int = 3
    message_template: str


@app.get("/health")
def health_check():
    return {
        "status": "running",
        "application": "ReachPilot"
    }


@app.post("/api/leads")
async def discover_leads(request: SearchRequest):

    try:

        # 1. Search the web
        results = await run_in_threadpool(
            search_web,
            request.prompt,
            10
        )

        if not results:
            raise HTTPException(
                status_code=404,
                detail="No search results found."
            )

        # 2. Extract founders
        leads = await run_in_threadpool(
            extract_founders,
            results,
            request.number_of_leads
        )

        if not leads:
            raise HTTPException(
                status_code=404,
                detail="No founders could be extracted."
            )

        # 3. Enrich leads
        leads = await run_in_threadpool(
            enrich_leads,
            leads
        )

        # 4. Generate personalized messages
        for lead in leads:

            lead["message"] = await run_in_threadpool(
                generate_message,
                lead,
                request.message_template
            )

            lead["status"] = "Pending"

        return {
            "success": True,
            "total": len(leads),
            "leads": leads
        }

    except HTTPException:
        raise

    except Exception as e:

        print("Backend error:", e)

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )