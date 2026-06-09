"""#952 ARTIFACT-MODEL — Phase 1: the Artifact unifying-lens + lossless round-trip.

Verifies the Arch-ratified invariant `X == to_X(from_X(X))` for each origin type
(Document / UploadedFile / SurfaceableInsight) — Artifact projects each without
flattening (type-specific fields ride verbatim in payload). Pure domain tests.
"""

from datetime import datetime

from services.domain.models import (
    Artifact,
    ArtifactSourceType,
    Document,
    UploadedFile,
)
from services.mux.composting_models import create_insight_learning
from services.mux.composting_pipeline import SurfaceableInsight
from services.mux.lifecycle import LifecycleState


class TestDocumentRoundTrip:
    def _doc(self) -> Document:
        return Document(
            id="doc-1",
            title="Design notes",
            content="The body of the doc.",
            document_type="decision",
            tags=["arch", "mux"],
            topics=["artifact"],
            decisions=["use the lens"],
            file_path="/tmp/x.md",
            file_size=42,
            mime_type="text/markdown",
            summary="a summary",
            key_findings=["finding 1"],
            analysis_metadata={"k": "v"},
            created_at=datetime(2026, 6, 9, 10, 0, 0),
            updated_at=datetime(2026, 6, 9, 11, 0, 0),
            last_accessed=datetime(2026, 6, 9, 12, 0, 0),
        )

    def test_lossless_round_trip(self):
        doc = self._doc()
        assert Artifact.from_document(doc).to_document() == doc

    def test_source_type_and_content_projected(self):
        art = Artifact.from_document(self._doc())
        assert art.source_type == ArtifactSourceType.DOCUMENT
        assert art.content == "The body of the doc."
        assert art.payload["title"] == "Design notes"


class TestUploadedFileRoundTrip:
    def _file(self) -> UploadedFile:
        return UploadedFile(
            id="file-1",
            owner_id="user-9",
            filename="report.pdf",
            file_type="application/pdf",
            file_size=1024,
            storage_path="/store/file-1",
            upload_time=datetime(2026, 6, 9, 9, 0, 0),
            last_referenced=datetime(2026, 6, 9, 9, 30, 0),
            reference_count=3,
            metadata={"a": 1},
            file_metadata={"b": 2},
        )

    def test_lossless_round_trip(self):
        f = self._file()
        assert Artifact.from_uploaded_file(f).to_uploaded_file() == f

    def test_owner_and_source_type_projected(self):
        art = Artifact.from_uploaded_file(self._file())
        assert art.source_type == ArtifactSourceType.UPLOADED_FILE
        assert art.owner_id == "user-9"
        assert art.created_at == datetime(2026, 6, 9, 9, 0, 0)  # = upload_time


class TestInsightRoundTrip:
    def _insight(self) -> SurfaceableInsight:
        learning = create_insight_learning(
            description="user prefers async",
            derived_from=["obj-1"],
            confidence=0.82,
            surprisingness=0.3,
            source_objects=["obj-1"],
            topic_tags=["work_style"],
        )
        return SurfaceableInsight(
            id="ins-1",
            object_id="obj-1",
            user_id="user-7",
            created_at=datetime(2026, 6, 9, 8, 0, 0),
            learning=learning,
            surfaced_count=2,
            last_surfaced=datetime(2026, 6, 9, 8, 30, 0),
            user_response="engaged",
            min_trust_stage=3,
            connected_insights=["ins-2"],
            context_tags=["work_style"],
            is_deleted=False,
            user_correction=None,
        )

    def test_lossless_round_trip(self):
        ins = self._insight()
        assert Artifact.from_insight(ins).to_insight() == ins

    def test_content_projects_learning_expression(self):
        ins = self._insight()
        art = Artifact.from_insight(ins)
        assert art.source_type == ArtifactSourceType.INSIGHT
        assert art.owner_id == "user-7"
        # content is the projection of the learning's expression
        assert art.content == ins.learning.expression


class TestArtifactDefaults:
    def test_generated_is_default_source_type(self):
        art = Artifact(content="hello", owner_id="u1")
        assert art.source_type == ArtifactSourceType.GENERATED
        assert art.lifecycle_state is None
        assert art.payload == {}

    def test_reuses_lifecycle_state_enum(self):
        art = Artifact(lifecycle_state=LifecycleState.RATIFIED)
        assert art.lifecycle_state is LifecycleState.RATIFIED
