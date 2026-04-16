import mimetypes
from pathlib import Path

from services.domain.models import AnalysisType, FileTypeInfo


class FileTypeDetector:
    """Detects file types and maps them to appropriate analyzers"""

    def __init__(self):
        # Map extensions to analyzer types
        self.extension_map = {
            # Text files
            ".md": AnalysisType.TEXT,
            ".txt": AnalysisType.TEXT,
            ".log": AnalysisType.TEXT,
            # Documents
            ".pdf": AnalysisType.DOCUMENT,
            ".docx": AnalysisType.DOCUMENT,
            ".doc": AnalysisType.DOCUMENT,
            # Data files
            ".csv": AnalysisType.DATA,
            ".xlsx": AnalysisType.DATA,
            ".xls": AnalysisType.DATA,
        }

    def detect(self, file_path: str) -> FileTypeInfo:
        """Detect file type from path"""
        path = Path(file_path)
        extension = path.suffix.lower()

        # Get MIME type
        mime_type, _ = mimetypes.guess_type(file_path)
        if not mime_type:
            mime_type = "application/octet-stream"

        # Determine analyzer type
        analyzer_type = self.extension_map.get(
            extension,
            AnalysisType.TEXT,  # Default to text for unknown types
        )

        return FileTypeInfo(
            mime_type=mime_type,
            extension=extension,
            analyzer_type=analyzer_type.value,  # Convert enum to string
            confidence=0.9 if extension in self.extension_map else 0.5,
        )
