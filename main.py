"""
Piper Morgan 1.0 - Main Application
Bootstrap version to prove the architecture
"""
import asyncio
import uvicorn
from fastapi import FastAPI, HTTPException, BackgroundTasks
from contextlib import asynccontextmanager
from pydantic import BaseModel
from typing import Optional, Dict, Any
import logging
from dotenv import load_dotenv
import os
from fastapi import File, UploadFile, Form
import tempfile
import shutil
from services.knowledge_graph import get_document_service

# Load environment variables FIRST
load_dotenv()

from services.domain.models import Product, Feature, Intent, IntentCategory
from services.intent_service import classifier
from services.orchestration import engine, WorkflowType, WorkflowStatus

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Request/Response models
class IntentRequest(BaseModel):
    message: str

class IntentResponse(BaseModel):
    message: str
    intent: dict
    response: str
    workflow_id: Optional[str] = None

class WorkflowResponse(BaseModel):
    workflow_id: str
    status: str
    type: str
    tasks: list
    message: str

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("🚀 Starting Piper Morgan 1.0...")
    logger.info("✅ Domain models loaded")
    logger.info("✅ LLM clients initialized")
    logger.info("✅ Intent classifier ready")
    logger.info("✅ Orchestration engine ready")
    yield
    # Shutdown
    logger.info("Shutting down...")

# Create FastAPI app
app = FastAPI(
    title="Piper Morgan Platform 1.0",
    version="1.0.0-bootstrap",
    description="Intelligent Product Management Assistant",
    lifespan=lifespan
)

@app.get("/")
async def root():
    return {
        "name": "Piper Morgan Platform 1.0",
        "version": "1.0.0-bootstrap",
        "status": "healthy",
        "message": "Ready to be your AI PM assistant! 🤖"
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "services": {
            "postgres": "connected",
            "redis": "connected",
            "chromadb": "connected", 
            "temporal": "connected",
            "llm": "ready",
            "orchestration": "ready"
        }
    }

@app.post("/api/v1/intent", response_model=IntentResponse)
async def process_intent(request: IntentRequest, background_tasks: BackgroundTasks):
    """Process a natural language message with real AI and optionally create workflow"""
    try:
        # Use real intent classifier
        intent = await classifier.classify(request.message)
        
        # Try to create a workflow from the intent
        workflow = await engine.create_workflow_from_intent(intent)
        workflow_id = None
        
        if workflow:
            # Execute workflow in background
            workflow_id = workflow.id
            background_tasks.add_task(engine.execute_workflow, workflow_id)
            response_text = f"I understand you want to {intent.action}. I've started a workflow to handle this."
        else:
            # No workflow needed, just respond
            response_text = f"I understand you want to {intent.action}. "
            
            if intent.category == IntentCategory.EXECUTION:
                response_text += "I'll help you execute that task."
            elif intent.category == IntentCategory.ANALYSIS:
                response_text += "Let me analyze that for you."
            elif intent.category == IntentCategory.SYNTHESIS:
                response_text += "I'll help you create that."
            elif intent.category == IntentCategory.STRATEGY:
                response_text += "Let's think strategically about this."
            else:
                response_text += "I'll help you learn from this."
        
        return IntentResponse(
            message=request.message,
            intent={
                "category": intent.category.value,
                "action": intent.action,
                "confidence": intent.confidence,
                "context": intent.context
            },
            response=response_text,
            workflow_id=workflow_id
        )
    except Exception as e:
        logger.error(f"Intent processing failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to process intent")

@app.get("/api/v1/workflows/{workflow_id}", response_model=WorkflowResponse)
async def get_workflow(workflow_id: str):
    """Get workflow status and details"""
    workflow = engine.workflows.get(workflow_id)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    workflow_dict = workflow.to_dict()
    
    # Create user-friendly message based on status
    if workflow.status == WorkflowStatus.COMPLETED:
        message = "Workflow completed successfully!"
    elif workflow.status == WorkflowStatus.RUNNING:
        completed_tasks = sum(1 for t in workflow.tasks if t.status.value == "completed")
        message = f"Workflow in progress... ({completed_tasks}/{len(workflow.tasks)} tasks completed)"
    elif workflow.status == WorkflowStatus.FAILED:
        message = f"Workflow failed: {workflow.error}"
    else:
        message = "Workflow is pending"
    
    return WorkflowResponse(
        workflow_id=workflow_id,
        status=workflow_dict["status"],
        type=workflow_dict["type"],
        tasks=workflow_dict["tasks"],
        message=message
    )

@app.get("/api/v1/workflows")
async def list_workflows():
    """List all workflows"""
    workflows = []
    for wf_id, workflow in engine.workflows.items():
        workflows.append({
            "id": wf_id,
            "type": workflow.type.value,
            "status": workflow.status.value,
            "created_at": workflow.created_at.isoformat()
        })
    return {"workflows": workflows}

@app.get("/api/v1/products")
async def list_products():
    """List all products"""
    # TODO: Real database integration
    sample_product = Product(
        name="Sample Product",
        vision="Make PMs more effective",
        strategy="AI-first approach"
    )
    return [sample_product]

# Add these endpoints to main.py right before the if __name__ == "__main__": line

@app.post("/api/v1/knowledge/upload")
async def upload_document(
    file: UploadFile = File(...),
    title: Optional[str] = Form(None),
    author: Optional[str] = Form(None),
    source_type: Optional[str] = Form("reference"),
    knowledge_domain: Optional[str] = Form("pm_fundamentals")
):
    """Upload a document to the knowledge base"""
    
    # Validate knowledge domain
    valid_domains = ["pm_fundamentals", "business_context", "product_context", "task_context"]
    if knowledge_domain not in valid_domains:
        raise HTTPException(status_code=400, detail=f"Invalid knowledge domain. Must be one of: {valid_domains}")
    
    # Prepare metadata
    metadata = {
        "title": title or file.filename,
        "author": author or "Unknown",
        "source_type": source_type,
        "knowledge_domain": knowledge_domain,
        "original_filename": file.filename
    }
    
    try:
        # Use document service - clean abstraction!
        result = await get_document_service().upload_pdf(file, metadata)
        
        # Emit event for learning system
        if hasattr(app.state, 'event_bus'):
            await app.state.event_bus.emit("knowledge.document_added", {
                "document_id": result.get("details", {}).get("document_id"),
                "title": metadata["title"],
                "knowledge_domain": knowledge_domain,
                "chunks": result.get("details", {}).get("chunks_created", 0)
            })
        
        return result
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Document upload failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to process document")

@app.get("/api/v1/knowledge/search")
async def search_knowledge(query: str, limit: int = 5):
    """
    Search the knowledge base
    
    Args:
        query: Search query
        limit: Maximum number of results
    """
    try:
        results = await get_ingester().search(query, n_results=limit)
        return {
            "query": query,
            "results": results,
            "count": len(results)
        }
    except Exception as e:
        logger.error(f"Knowledge search failed: {e}")
        raise HTTPException(status_code=500, detail="Search failed")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
        log_level="info"
    )