"""M3 regression tests tied to docs/trace_case.md."""
import pytest
from pydantic_evals.evaluators import EvaluatorContext

from lab8.shapes import SHAPES
from lab9 import graders
from lab9.trace_case import investigate
from lab9.variant_agent import make_shape

pytestmark = pytest.mark.student


def _ctx(case: dict) -> EvaluatorContext:
    return EvaluatorContext(
        name="regression",
        inputs={},
        metadata=None,
        expected_output=case["label"],
        output=case["trial"],
        duration=0.0,
        _span_tree=None,
        attributes={},
        metrics={},
    )


def test_c002_ticket_trust_regression_and_fixed_control():
    bad = investigate("seeded_regression", "C-002", 11)
    assert bad["trial"]["lab8_pass"] is False
    assert graders.DbFactKept().evaluate(_ctx(bad)).value is False
    assert graders.RefundAmountCorrect().evaluate(_ctx(bad)).value is False

    good = investigate("fixed", "C-002", 11)
    assert good["trial"]["lab8_pass"] is True
    assert graders.DbFactKept().evaluate(_ctx(good)).value is True
    assert graders.RefundAmountCorrect().evaluate(_ctx(good)).value is True


def test_fm08_misreport_caught_by_reply_amount_match():
    SHAPES["test_fm08_misreport"] = make_shape("test_fm08_misreport", {"misreport"})
    bad = investigate("test_fm08_misreport", "C-014", 11)
    assert bad["trial"]["lab8_pass"] is True
    assert graders.ReplyAmountMatch().evaluate(_ctx(bad)).value is False

    good = investigate("fixed", "C-014", 11)
    assert graders.ReplyAmountMatch().evaluate(_ctx(good)).value is True
