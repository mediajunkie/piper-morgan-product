from datetime import datetime
from typing import Any, Dict

import pypdf

from services.analysis.base_analyzer import BaseAnalyzer
from services.analysis.summary_parser import SummaryParser
from services.domain.models import AnalysisResult, AnalysisType
from services.prompts import get_json_summary_prompt
from services.shared_types import TaskType


class DocumentAnalyzer(BaseAnalyzer):
    def __init__(self, llm_client=None):
        self.llm_client = llm_client
        self.summary_parser = SummaryParser()

    async def analyze(self, file_path: str, **kwargs) -> AnalysisResult:
        """Analyze document file using LLM.

        Args:
            file_path: Path to the document
            **kwargs: Additional optional parameters (not used currently)
        """
        try:
            # #1306: bytes via the decrypt seam, never a raw open()
            import io as _io

            from services.file_context.storage import read_file_from_storage

            reader = pypdf.PdfReader(_io.BytesIO(read_file_from_storage(file_path)))
            page_count = len(reader.pages)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""
            metadata = {"page_count": page_count, "text": text}
            # Empty PDF: summary should be empty string if no text and at least one page
            if not text and page_count > 0:
                summary = ""
                metadata["summary"] = summary
                metadata["key_points"] = []
            elif text:
                # Use LLM for summary and key points with JSON mode
                import structlog

                logger = structlog.get_logger()
                if self.llm_client is not None:
                    try:
                        # Use JSON mode for structured output
                        json_prompt = get_json_summary_prompt()
                        json_response = await self.llm_client.complete(
                            task_type=TaskType.SUMMARIZE.value,
                            prompt=json_prompt.format(content=text[:3000]),
                            response_format={"type": "json_object"},
                        )

                        # Parse JSON into domain model
                        document_summary = self.summary_parser.parse_json(json_response)

                        # Generate clean markdown from domain model
                        summary = document_summary.to_markdown()
                        key_points = document_summary.key_findings

                    except Exception as e:
                        logger.error(f"LLM analysis failed: {e}")
                        summary = (
                            f"Summary generation failed. Document contains {len(text)} characters."
                        )
                        key_points = []
                else:
                    summary = f"PDF with {page_count} pages and {len(text)} characters of text."
                    key_points = []
                metadata["summary"] = summary
                metadata["key_points"] = key_points
            else:
                summary = f"PDF with {page_count} pages and {len(text)} characters of text."
                metadata["summary"] = summary
                metadata["key_points"] = []
            # NOTE: key_points kept in metadata for backward compatibility.
            # Low-priority domain model alignment — not blocking any feature.
            return AnalysisResult(
                file_id=file_path,
                analysis_type=AnalysisType.DOCUMENT,
                summary=summary,
                key_findings=key_points,
                recommendations=[],
                generated_at=datetime.now(),
                metadata=metadata,
            )
        except pypdf.errors.PdfReadError:
            return AnalysisResult(
                file_id=file_path,
                analysis_type=AnalysisType.DOCUMENT,
                summary="Unable to analyze PDF document",
                key_findings=["PDF file could not be read - file may be corrupted"],
                metadata={"error": "Unable to read PDF file - file may be corrupted"},
                recommendations=[
                    "Verify the PDF file is not corrupted",
                    "Try re-saving or re-exporting the PDF",
                ],
                generated_at=datetime.now(),
            )

    async def analyze_text(self, text: str, source_id: str = "inline-text") -> AnalysisResult:
        """Analyze already-extracted text through the SAME LLM-summary path
        ``analyze()`` uses for PDF text (#1657).

        Exists for content that lives in the database rather than file storage
        — a saved artifact's markdown (the /files view's second half, #355) has
        no storage_path and nothing for pypdf to parse. Mirrors ``analyze()``'s
        text branch verbatim (JSON-mode summary, SummaryParser, markdown
        render, the same honest fallbacks) so both content sources produce the
        same summary shape.
        """
        metadata: Dict[str, Any] = {"text": text}
        if not text:
            summary = ""
            key_points = []
        elif self.llm_client is not None:
            import structlog

            logger = structlog.get_logger()
            try:
                json_prompt = get_json_summary_prompt()
                json_response = await self.llm_client.complete(
                    task_type=TaskType.SUMMARIZE.value,
                    prompt=json_prompt.format(content=text[:3000]),
                    response_format={"type": "json_object"},
                )
                document_summary = self.summary_parser.parse_json(json_response)
                summary = document_summary.to_markdown()
                key_points = document_summary.key_findings
            except Exception as e:
                logger.error(f"LLM analysis failed: {e}")
                summary = f"Summary generation failed. Document contains {len(text)} characters."
                key_points = []
        else:
            summary = f"Document with {len(text)} characters of text."
            key_points = []
        metadata["summary"] = summary
        metadata["key_points"] = key_points
        return AnalysisResult(
            file_id=source_id,
            analysis_type=AnalysisType.TEXT,
            summary=summary,
            key_findings=key_points,
            recommendations=[],
            generated_at=datetime.now(),
            metadata=metadata,
        )
