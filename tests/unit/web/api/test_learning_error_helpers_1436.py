"""#1436 B4: learning routes' error branches return clean 422/404, not TypeError-500.

Regression: ten ``validation_error``/``not_found_error`` calls passed
``error_id=`` (once ``error_code=``) — kwargs those helpers don't accept — so
every error branch raised TypeError and surfaced as a raw 500 instead of the
intended structured 422/404. (``internal_error`` DOES accept ``error_id``;
those calls were always fine.) Identifiers now ride ``details={"error_id":…}``,
the file's own later-route convention.
"""

import json

from web.api.routes.learning import PatternRequest, learn_pattern


async def test_invalid_pattern_type_returns_422_not_typeerror():
    resp = await learn_pattern(
        PatternRequest(
            pattern_type="not_a_real_type",
            source_feature="test",
            pattern_data={"k": "v"},
        )
    )
    # Old behavior: TypeError("unexpected keyword argument 'error_id'") -> 500.
    assert resp.status_code == 422
    body = json.loads(resp.body)
    assert body["details"]["error_id"] == "INVALID_PATTERN_TYPE"
    assert body["status"] == "error"
