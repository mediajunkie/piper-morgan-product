# test_adapter_final.py - with path fix
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
from datetime import datetime

from dotenv import load_dotenv

from services.integrations.mcp.notion_adapter import NotionMCPAdapter


async def test_adapter():
    load_dotenv()

    adapter = NotionMCPAdapter()
    await adapter.connect()

    # Use first accessible page from search
    parent_id = "25c11704-d8bf-80f4-9bf6-d54b55e784e9"

    result = await adapter.create_page(
        parent_id=parent_id,
        properties={
            "title": {
                "title": [
                    {
                        "text": {
                            "content": f"✅ Adapter Works - {datetime.now().strftime('%H:%M:%S')}"
                        }
                    }
                ]
            }
        },
    )

    if result and result.get("url"):
        print(f"✅ SUCCESS: Adapter create_page WORKS!")
        print(f"   URL: {result.get('url')}")
        print(f"   ID: {result.get('id')}")
        print("\n🎉 First surgical fix complete and verified!")
    else:
        print("❌ FAILED")
        if result:
            print(f"Result: {result}")


asyncio.run(test_adapter())
