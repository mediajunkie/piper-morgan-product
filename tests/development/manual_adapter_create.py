# test_adapter_create.py
import asyncio
import os
from datetime import datetime

from dotenv import load_dotenv

from services.integrations.mcp.notion_adapter import NotionMCPAdapter


async def test_adapter():
    load_dotenv()

    # Initialize adapter
    adapter = NotionMCPAdapter()
    await adapter.connect()

    # Use the Piper Morgan page ID from your screenshot
    parent_id = "25c11704-d8bf-812d-9738-cd3726ec22d5"  # Your "Piper Morgan - Test Page"

    # Create test page through adapter
    result = await adapter.create_page(
        parent_id=parent_id,
        properties={
            "title": {
                "title": [
                    {"text": {"content": f"Adapter Test - {datetime.now().strftime('%H:%M:%S')}"}}
                ]
            }
        },
    )

    if result and result.get("url"):
        print(f"✅ SUCCESS: Page created via adapter")
        print(f"   URL: {result.get('url')}")
        print(f"   ID: {result.get('url')}")
    else:
        print("❌ FAILED: Adapter did not create page")
        if result:
            print(f"   Result: {result}")


# Run the test
asyncio.run(test_adapter())
