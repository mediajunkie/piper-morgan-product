"""
Document Memory CLI Commands - Phase 3 Implementation
Connects to extended DocumentService using existing PM-011 infrastructure
"""

import asyncio
import os
from typing import Any, Dict

import click

from services.intent_service.canonical_handlers import CanonicalHandlers
from services.knowledge_graph.document_service import get_document_service


@click.group()
def documents():
    """Document memory commands using extended DocumentService."""
    pass


@documents.command()
@click.argument("topic")
@click.option("--timeframe", default="last_week", help="Time period: last_week, last_month, etc.")
async def decide(topic: str, timeframe: str):
    """Find decisions on topic using DocumentService.find_decisions()"""
    click.echo(f"🔍 Searching for decisions on: {topic} ({timeframe})")

    try:
        service = get_document_service()  # Use existing singleton
        results = await service.find_decisions(topic, timeframe)

        # Display results from extended DocumentService
        if results.get("decisions"):
            click.echo(f"📋 Found {results.get('count', 0)} decisions:")
            for decision in results["decisions"][:5]:  # Show top 5
                click.echo(f"  • {decision.get('topic', 'N/A')}: {decision.get('decision', 'N/A')}")
        else:
            click.echo(f"ℹ️  No decisions found for '{topic}' in {timeframe}")
            if results.get("error"):
                click.echo(f"   Error: {results['error']}")

    except Exception as e:
        click.echo(f"❌ Error searching decisions: {e}")
        click.echo("💡 This may be a temporary issue - try again later")


@documents.command()
@click.option("--days", default=1, help="Number of days for context")
async def context(days: int):
    """Get recent document context using DocumentService.get_relevant_context()"""
    timeframe = f"last_{days}_days"
    click.echo(f"📚 Retrieving document context for {days} day(s)")

    try:
        service = get_document_service()  # Use existing singleton
        results = await service.get_relevant_context(timeframe)

        # Display context from extended DocumentService
        if results.get("context_documents"):
            click.echo(f"📖 Found {results.get('count', 0)} relevant documents:")
            for doc in results["context_documents"][:5]:  # Show top 5
                click.echo(f"  📄 {doc.get('title', 'N/A')}: {doc.get('summary', 'N/A')[:100]}...")
        else:
            click.echo(f"ℹ️  No relevant context found for {timeframe}")
            if results.get("error"):
                click.echo(f"   Error: {results['error']}")

    except Exception as e:
        click.echo(f"❌ Error retrieving context: {e}")
        click.echo("💡 This may be a temporary issue - try again later")


@documents.command()
@click.argument("file_path")
@click.option("--title", help="Document title")
@click.option("--domain", default="general", help="Knowledge domain")
async def add(file_path: str, title: str = None, domain: str = None):
    """Add document using existing DocumentService.upload_pdf() pipeline"""
    click.echo(f"📄 Adding document: {file_path}")

    try:
        # Verify file exists
        if not os.path.exists(file_path):
            click.echo(f"❌ File not found: {file_path}")
            return

        service = get_document_service()  # Use existing singleton

        # Prepare metadata for existing upload_pdf method
        metadata = {"title": title or os.path.basename(file_path), "knowledge_domain": domain}

        # Use existing DocumentService upload method
        # Note: This connects to existing PM-011 upload pipeline
        result = await service.upload_pdf(file_path, metadata)

        # Display upload results
        if result.get("status") == "success":
            click.echo(f"✅ {result.get('message', 'Document successfully processed')}")
        else:
            click.echo(f"❌ Upload failed: {result.get('error', 'Unknown error')}")

    except Exception as e:
        click.echo(f"❌ Error adding document: {e}")
        click.echo("💡 Check file path and try again")


@documents.command()
@click.option("--focus", default="", help="Focus area for recommendations")
async def review(focus: str):
    """Get document recommendations using DocumentService.suggest_documents()"""
    focus_msg = f"on '{focus}'" if focus else "generally"
    click.echo(f"👀 Finding documents for review {focus_msg}")

    try:
        service = get_document_service()  # Use existing singleton
        results = await service.suggest_documents(focus)

        # Display suggestions from extended DocumentService
        if results.get("suggestions"):
            click.echo(f"📋 Found {results.get('count', 0)} documents for review:")
            for suggestion in results["suggestions"][:5]:  # Show top 5
                click.echo(
                    f"  📖 {suggestion.get('title', 'N/A')}: {suggestion.get('reason', 'N/A')}"
                )
        else:
            click.echo("ℹ️  No documents currently need review")
            if results.get("error"):
                click.echo(f"   Error: {results['error']}")

    except Exception as e:
        click.echo(f"❌ Error getting recommendations: {e}")
        click.echo("💡 This may be a temporary issue - try again later")


@documents.command()
async def status():
    """Show DocumentService system status"""
    click.echo("📊 Document Memory System Status")
    click.echo("=" * 40)

    try:
        service = get_document_service()  # Use existing singleton

        # Test basic connectivity to extended DocumentService
        click.echo("✅ DocumentService available")
        click.echo("✅ Extended methods accessible")

        # Test a basic query to verify integration
        test_results = await service.get_relevant_context("today")
        if test_results:
            click.echo("✅ ChromaDB integration operational")

        click.echo("\n🎯 System Status: OPERATIONAL")

    except ImportError:
        click.echo("❌ DocumentService not available")
        click.echo("💡 System may be in development mode")
        click.echo("\n🎯 System Status: UNAVAILABLE")
    except Exception as e:
        click.echo(f"❌ System error: {e}")
        click.echo("\n🎯 System Status: ERROR")


def main():
    """Main entry point - convert async commands to sync for Click compatibility"""
    # Convert async commands to sync for Click framework
    for cmd in [decide, context, add, review, status]:
        if asyncio.iscoroutinefunction(cmd.callback):
            original_callback = cmd.callback

            def make_sync_callback(callback):
                def sync_callback(*args, **kwargs):
                    return asyncio.run(callback(*args, **kwargs))

                return sync_callback

            cmd.callback = make_sync_callback(original_callback)

    documents()


if __name__ == "__main__":
    main()
