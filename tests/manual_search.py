# test_search.py
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio

from dotenv import load_dotenv

from services.integrations.mcp.notion_adapter import NotionMCPAdapter


async def test_search():
    load_dotenv()

    adapter = NotionMCPAdapter()
    await adapter.connect()

    # Search for our test pages
    results = await adapter.search_notion("Adapter", filter_type="page")

    if results:
        print(f"✅ SUCCESS: Search found {len(results)} results")
        for i, result in enumerate(results[:3]):
            title = "Untitled"
            if "properties" in result and "title" in result["properties"]:
                title_prop = result["properties"]["title"]
                if "title" in title_prop and len(title_prop["title"]) > 0:
                    title = title_prop["title"][0]["text"]["content"]
            print(f"   {i+1}. {title}")
        print("\n🎉 search_notion verified!")
    else:
        print("❌ FAILED: No results found")


asyncio.run(test_search())
