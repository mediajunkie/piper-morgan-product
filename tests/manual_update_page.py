# test_update_page.py
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
from datetime import datetime

from dotenv import load_dotenv

from services.integrations.mcp.notion_adapter import NotionMCPAdapter


async def test_update():
    load_dotenv()

    adapter = NotionMCPAdapter()
    await adapter.connect()

    # Use the page we created at 11:51
    page_id = "25c11704-d8bf-8117-ac2f-f3e97b925109"  # "Adapter Works" page

    # Update its title
    result = await adapter.update_page(
        page_id=page_id,
        properties={
            "title": {
                "title": [
                    {"text": {"content": f"✅ UPDATED - {datetime.now().strftime('%H:%M:%S')}"}}
                ]
            }
        },
    )

    if result and result.get("id"):
        print(f"✅ SUCCESS: Page updated via adapter")
        print(f"   Page ID: {result.get('id')}")
        print(f"   URL: {result.get('url')}")
        print("\n🎉 Second surgical fix verified!")
    else:
        print("❌ FAILED: Update did not work")


asyncio.run(test_update())
