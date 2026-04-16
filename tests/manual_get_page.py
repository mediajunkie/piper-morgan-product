# test_get_page.py
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio

from dotenv import load_dotenv

from services.integrations.mcp.notion_adapter import NotionMCPAdapter


async def test_get():
    load_dotenv()

    adapter = NotionMCPAdapter()
    await adapter.connect()

    # Use the page we've been testing with
    page_id = "25c11704-d8bf-8117-ac2f-f3e97b925109"

    result = await adapter.get_page(page_id=page_id)

    if result and result.get("id"):
        print(f"✅ SUCCESS: Page retrieved via adapter")
        print(f"   Title: {result.get('title')}")
        print(f"   ID: {result.get('id')}")
        print(f"   URL: {result.get('url')}")
        print(f"   Created: {result.get('created_time')}")
        print("\n🎉 Third surgical fix verified!")
    else:
        print("❌ FAILED: Could not retrieve page")


asyncio.run(test_get())
