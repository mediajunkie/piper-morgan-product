# test_get_blocks.py
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio

from dotenv import load_dotenv

from services.integrations.mcp.notion_adapter import NotionMCPAdapter


async def test_blocks():
    load_dotenv()

    adapter = NotionMCPAdapter()
    await adapter.connect()

    # Use our test page that we know exists
    page_id = "25c11704-d8bf-8117-ac2f-f3e97b925109"

    blocks = await adapter.get_page_blocks(page_id=page_id)

    if blocks:
        print(f"✅ SUCCESS: Retrieved {len(blocks)} blocks")
        for i, block in enumerate(blocks[:3]):  # Show first 3
            print(f"   Block {i}: {block.get('type', 'unknown')}")
        print("\n🎉 Fourth surgical fix verified!")
    else:
        print("❌ FAILED: No blocks retrieved (might be empty page)")


asyncio.run(test_blocks())
