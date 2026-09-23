"""#1718 — Settings -> LLM API Keys renders the SPECIFIC save-time failure reason,
not a flat "Key saved" claim regardless of outcome.

templates/settings_llm_keys.html has no server-side conditional for this — the
status line is built client-side from the /api/v1/keys/store JSON response. A
render test of the Jinja template alone (or a curl 200 on the route) would pass
even if the shipped JS ignored `is_validated`/`message` entirely and always
printed "Key saved" (the exact bug this issue is about) — that's the m-43 trap:
checking a layer that can't fail the way the real bug fails. So the layer that
actually matters here is the JS SOURCE shipped to the browser: this pins that the
save handler branches on `data.is_validated` and renders `data.message` (the
honest, provider-diagnosed sentence) instead of unconditionally claiming success.
"""

TEMPLATE_PATH = "templates/settings_llm_keys.html"


def _script_block() -> str:
    src = open(TEMPLATE_PATH).read()
    start = src.index("saveBtn.addEventListener")
    end = src.index("tbody.addEventListener")
    return src[start:end]


def test_save_handler_checks_is_validated_before_claiming_success():
    block = _script_block()
    assert "data.is_validated" in block, (
        "save handler no longer inspects is_validated — it would render 'Key saved' "
        "for every outcome again (#1718's original bug)"
    )


def test_save_handler_renders_the_server_supplied_message_on_failure():
    block = _script_block()
    # The false-branch must use data.message (the honest, provider-specific
    # sentence from the route), not a hardcoded "invalid" string.
    false_branch_start = block.index("is_validated === false")
    false_branch = block[false_branch_start : false_branch_start + 300]
    assert "data.message" in false_branch


def test_save_handler_does_not_unconditionally_claim_saved_ok():
    """The pre-fix shape, pinned so the defect stays understood: a bare
    `setStatus("Key saved for " + provider + ".", true)` with no gate at all,
    right after the fetch resolves, is exactly the bug (#1718)."""
    block = _script_block()
    # The success-claim line must sit inside a branch (an `else` off the
    # is_validated check), not be the first thing after the response parses.
    validated_check_index = block.index("data.is_validated")
    saved_claim_index = block.index('"Key saved for "')
    assert (
        validated_check_index < saved_claim_index
    ), "the honest-outcome check must run BEFORE the success message can be shown"
