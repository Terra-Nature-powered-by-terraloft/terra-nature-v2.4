"""
Regressionstests: Fail-Closed-Verhalten des Expert-Validators.

Grundsatz: Eine Aussage darf nur dann "approved" sein, wenn sie tatsächlich
geprüft wurde. Kein API-Schlüssel, Modellfehler, Timeout oder eine unlesbare
Modellantwort führen zu "not_validated" (bzw. "requires_review" bei Teilausfall),
niemals zu "approved".

Die Tests rufen kein echtes Modell auf: Das Paket "anthropic" wird durch ein
Testdouble ersetzt.
"""

import asyncio
import sys
import types
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from kappa.main import app
from kappa.services import expert_validator as validator_module
from kappa.services.expert_validator import ExpertValidator, NOT_VALIDATED

# Bewusst unbelegte, physikalisch unplausible Aussage
UNBELEGTE_AUSSAGE = "Die K-Cascade wandelt 99 % der Abwärme bei 80 °C in Strom um."


def _fake_anthropic(responder):
    """Baut ein Ersatzmodul für 'anthropic'.

    responder(prompt) liefert entweder den Antworttext oder wirft eine Exception.
    """

    class _Messages:
        def create(self, model, max_tokens, messages):
            text = responder(messages[0]["content"])
            return types.SimpleNamespace(content=[types.SimpleNamespace(text=text)])

    class Anthropic:
        def __init__(self, api_key=None, timeout=None):
            self.messages = _Messages()

    module = types.ModuleType("anthropic")
    module.Anthropic = Anthropic
    return module


def _validator_with_key():
    v = ExpertValidator()
    v.api_key = "test-key"
    v.available = True
    return v


def _run(coro):
    return asyncio.run(coro)


class TestOhneApiSchluessel:
    def test_unbelegte_aussage_wird_nicht_freigegeben(self):
        v = ExpertValidator()
        v.api_key = None
        v.available = False

        result = _run(v.validate_statement(UNBELEGTE_AUSSAGE, ["cto", "mrv"]))

        assert result.overall_approved is False
        assert result.approval_level == NOT_VALIDATED
        assert set(result.expert_opinions) == {"cto", "mrv"}
        for opinion in result.expert_opinions.values():
            assert opinion.approved is False
            assert opinion.validated is False

    def test_api_validate_endpoint_gibt_nicht_frei(self, monkeypatch):
        monkeypatch.setattr(validator_module.expert_validator, "available", False)
        monkeypatch.setattr(validator_module.expert_validator, "api_key", None)
        client = TestClient(app)

        response = client.post(
            "/api/kappa/validate",
            json={"statement": UNBELEGTE_AUSSAGE, "modes": ["cto"]},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["overall_approved"] is False
        assert data["approval_level"] == NOT_VALIDATED
        assert all(r["approved"] is False for r in data["results"].values())


class TestModellfehler:
    def test_exception_und_timeout_fuehren_zu_not_validated(self, monkeypatch):
        def responder(prompt):
            raise TimeoutError("Zeitüberschreitung beim Modellaufruf")

        monkeypatch.setitem(sys.modules, "anthropic", _fake_anthropic(responder))
        v = _validator_with_key()

        result = _run(v.validate_statement(UNBELEGTE_AUSSAGE, ["cto", "bank"]))

        assert result.overall_approved is False
        assert result.approval_level == NOT_VALIDATED
        assert all(not op.validated for op in result.expert_opinions.values())

    def test_antwort_ohne_json_wird_nicht_als_freigabe_gewertet(self, monkeypatch):
        # Früher reichte das Wort "approved" im Text für eine Freigabe -
        # auch in "not approved".
        monkeypatch.setitem(
            sys.modules, "anthropic", _fake_anthropic(lambda p: "This is not approved.")
        )
        v = _validator_with_key()

        result = _run(v.validate_statement(UNBELEGTE_AUSSAGE, ["cto"]))

        assert result.overall_approved is False
        assert result.approval_level == NOT_VALIDATED
        assert result.expert_opinions["cto"].approved is False

    @pytest.mark.parametrize("approved_value", ['"false"', '"true"', "1", "null"])
    def test_approved_muss_echter_boolean_sein(self, monkeypatch, approved_value):
        body = '{"approved": %s, "confidence": 0.9, "feedback": "x"}' % approved_value
        monkeypatch.setitem(sys.modules, "anthropic", _fake_anthropic(lambda p: body))
        v = _validator_with_key()

        result = _run(v.validate_statement(UNBELEGTE_AUSSAGE, ["cto"]))

        assert result.overall_approved is False
        assert result.approval_level == NOT_VALIDATED

    def test_teilausfall_fuehrt_zu_requires_review(self, monkeypatch):
        def responder(prompt):
            if "Bankfähigkeit" in prompt:
                raise RuntimeError("Modellfehler")
            return '{"approved": true, "confidence": 0.9, "feedback": "ok"}'

        monkeypatch.setitem(sys.modules, "anthropic", _fake_anthropic(responder))
        v = _validator_with_key()

        result = _run(v.validate_statement(UNBELEGTE_AUSSAGE, ["cto", "bank"]))

        assert result.overall_approved is False
        assert result.approval_level == "requires_review"


class TestEchtePruefung:
    def test_freigabe_nur_bei_vollstaendiger_positiver_pruefung(self, monkeypatch):
        body = '{"approved": true, "confidence": 0.8, "feedback": "plausibel"}'
        monkeypatch.setitem(sys.modules, "anthropic", _fake_anthropic(lambda p: body))
        v = _validator_with_key()

        result = _run(v.validate_statement("Aussage", ["cto", "mrv"]))

        assert result.overall_approved is True
        assert result.approval_level == "approved"
        assert all(op.validated for op in result.expert_opinions.values())

    def test_ablehnung_bleibt_ablehnung(self, monkeypatch):
        body = '{"approved": false, "confidence": 0.9, "feedback": "unbelegt"}'
        monkeypatch.setitem(sys.modules, "anthropic", _fake_anthropic(lambda p: body))
        v = _validator_with_key()

        result = _run(v.validate_statement(UNBELEGTE_AUSSAGE, ["cto"]))

        assert result.overall_approved is False
        assert result.approval_level == "requires_review"


class TestQueryEndpoint:
    def test_query_antwort_ist_nicht_als_freigegeben_markiert(self):
        client = TestClient(app)

        response = client.post(
            "/api/kappa/query", json={"text": "Test query", "mode": "default"}
        )

        assert response.status_code == 200
        assert response.json()["approval_level"] == NOT_VALIDATED
