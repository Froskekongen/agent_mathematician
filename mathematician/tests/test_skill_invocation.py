from __future__ import annotations

import re
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
SKILLS = REPO_ROOT / "mathematician" / "skills"
EXPECTED_SKILLS = {
    "audit-assumptions",
    "consolidate-math-documents",
    "destroy-theory",
    "explain-mathematics",
    "explore-mathematical-structure",
    "explore-proof-strategies",
    "formalize-concepts",
    "research-mathematics",
    "write-proof-exposition",
}
MODEL_WORKERS = {"audit-assumptions", "destroy-theory"}
MEMORY_WRITERS = EXPECTED_SKILLS - {"formalize-concepts"}
SKILL_REFERENCE = re.compile(r"`\$([a-z0-9-]+)`")


class SkillInvocationTest(unittest.TestCase):
    def skill_texts(self) -> dict[str, str]:
        skills = {
            path.parent.name: path.read_text(encoding="utf-8")
            for path in SKILLS.glob("*/SKILL.md")
        }
        self.assertEqual(set(skills), EXPECTED_SKILLS)
        return skills

    def frontmatter(self, name: str, text: str) -> dict[str, str]:
        lines = [line for line in text.split("---", 2)[1].splitlines() if line]
        fields = [line.split(":", 1) for line in lines]
        keys = [key for key, _ in fields]
        self.assertEqual(len(keys), len(set(keys)), name)
        self.assertLessEqual(
            set(keys), {"name", "description", "disable-model-invocation"}
        )
        parsed = {key: value.strip() for key, value in fields}
        self.assertEqual(parsed.get("name"), name)
        self.assertTrue(parsed.get("description"), name)
        return parsed

    def test_every_named_handoff_resolves(self) -> None:
        skills = self.skill_texts()
        for caller, text in skills.items():
            for callee in SKILL_REFERENCE.findall(text):
                self.assertIn(callee, skills, f"{caller} names missing skill {callee}")

    def test_only_cold_review_workers_are_model_invokable(self) -> None:
        actual: set[str] = set()
        for name, text in self.skill_texts().items():
            frontmatter = self.frontmatter(name, text)
            openai = (SKILLS / name / "agents" / "openai.yaml").read_text(
                encoding="utf-8"
            )
            policy = [
                line.strip()
                for line in openai.splitlines()
                if line.strip().startswith("allow_implicit_invocation:")
            ]
            self.assertEqual(len(policy), 1, name)
            self.assertIn(
                policy[0],
                {
                    "allow_implicit_invocation: true",
                    "allow_implicit_invocation: false",
                },
            )
            model_invokable = "disable-model-invocation" not in frontmatter
            implicitly_available = policy[0].endswith("true")
            self.assertEqual(model_invokable, implicitly_available, name)
            if not model_invokable:
                self.assertEqual(frontmatter["disable-model-invocation"], "true")
            if model_invokable:
                actual.add(name)
        self.assertEqual(actual, MODEL_WORKERS)

    def test_research_invokes_both_cold_review_workers(self) -> None:
        skills = self.skill_texts()
        research = skills["research-mathematics"]
        challenge_start = research.index("## 4.")
        challenge_end = research.index("## 5.", challenge_start)
        challenge = research[challenge_start:challenge_end]
        normalized = " ".join(challenge.split()).lower()
        self.assertIn("dispatch two fresh, mutually isolated", normalized)
        self.assertIn("the first prompt invokes `$destroy-theory`", normalized)
        self.assertIn("the second invokes `$audit-assumptions`", normalized)
        self.assertIn("that candidate, digest, and no peer report", normalized)
        self.assertIn("mismatched `candidate_digest`", normalized)
        self.assertIn("at most one fresh call to each worker", normalized)
        self.assertIn(
            "the coordinator routes review work and integrates or repairs findings "
            "as sole writer",
            normalized,
        )
        self.assertIn("specialists only review", normalized)

        automatic = re.compile(
            r"(?:\b(?:invoke|invokes|dispatch|dispatches|call|calls|run|runs)\b"
            r"[^.;]{0,80}|\broute(?:s)?\b[^.;]{0,80}\bto\s+)"
            r"`\$(audit-assumptions|destroy-theory)`"
        )
        for caller, text in skills.items():
            if caller != "research-mathematics":
                self.assertIsNone(automatic.search(" ".join(text.split())), caller)

    def test_integrity_is_shared_and_claim_resolution_is_research_only(self) -> None:
        skills = self.skill_texts()
        integrity_path = (
            SKILLS
            / "research-mathematics"
            / "references"
            / "mathematical-integrity.md"
        )
        resolution_path = (
            SKILLS
            / "research-mathematics"
            / "references"
            / "claim-resolution.md"
        )
        self.assertTrue(integrity_path.is_file())
        self.assertTrue(resolution_path.is_file())
        self.assertFalse(
            (SKILLS / "research-mathematics" / "references" / "rigor.md").exists()
        )

        integrity_text = integrity_path.read_text(encoding="utf-8").lower()
        integrity = " ".join(integrity_text.split())
        for heading in (
            "keep the object and claim fixed",
            "say what the evidence establishes",
            "make intuition recoverable",
            "state the mathematical status plainly",
        ):
            self.assertIn(f"## {heading}", integrity_text)
        self.assertIn("conversion obligation", integrity)
        self.assertIn("it is not a proof protocol", integrity)
        self.assertIn("use these rules behind the scenes", integrity)
        self.assertIn("workflow labels", integrity)
        self.assertLessEqual(
            len(integrity_path.read_text(encoding="utf-8").splitlines()), 90
        )

        for name, text in skills.items():
            self.assertIn("mathematical-integrity.md", text, name)
            if name == "research-mathematics":
                self.assertIn("claim-resolution.md", text, name)
            else:
                self.assertNotIn("claim-resolution.md", text, name)

    def test_every_skill_inherits_the_research_key_contract(self) -> None:
        for name, text in self.skill_texts().items():
            self.assertIn("research-memory.md", text, name)

        protocol = (
            SKILLS
            / "research-mathematics"
            / "references"
            / "research-memory.md"
        ).read_text(encoding="utf-8")
        normalized = " ".join(protocol.split()).lower()
        self.assertIn("stable identity of one durable mathematical referent", normalized)
        for check in ("necessity", "granularity", "stability"):
            self.assertIn(f"**{check}:**", normalized)
        self.assertIn("keys are document-scoped", normalized)
        self.assertIn("remap every card and artifact link", normalized)
        self.assertLess(
            normalized.index("audit every marker for necessity"),
            normalized.index("freeze the resulting canonical digest"),
        )

    def test_exactly_eight_skills_have_writable_memory_roles(self) -> None:
        skills = self.skill_texts()
        self.assertEqual(len(MEMORY_WRITERS), 8)
        for name in MEMORY_WRITERS:
            normalized = " ".join(skills[name].split()).lower()
            self.assertRegex(normalized, r"\b(?:writable|file-backed)\b", name)
        formalize = " ".join(skills["formalize-concepts"].split()).lower()
        self.assertIn("this skill does not create companions", formalize)
        self.assertNotIn("sole writer", formalize)

    def test_explanation_rewrite_uses_shared_memory_contract(self) -> None:
        explain = " ".join(
            self.skill_texts()["explain-mathematics"].split()
        ).lower()
        protocol_path = (
            SKILLS / "research-mathematics" / "references" / "research-memory.md"
        )
        protocol = " ".join(
            protocol_path.read_text(encoding="utf-8").split()
        ).lower()

        self.assertRegex(
            explain,
            r"(?:supplying|naming).{0,80}(?:does not authorize|is not authorization)",
        )
        self.assertIn("named canonical target", explain)
        self.assertRegex(explain, r"in-place.{0,80}only.{0,80}markdown/sqlite pair")
        self.assertRegex(
            explain,
            r"separate explanation.{0,100}own.{0,30}companion.{0,100}source pair"
            r".{0,30}read-only",
        )
        self.assertRegex(
            explain,
            r"(?:no two markdown documents share|never share).{0,20}"
            r"(?:one )?(?:sqlite )?database",
        )
        self.assertRegex(
            explain,
            r"(?:before writing|for writable work).{0,80}rules.{0,80}sole writer",
        )

        for invariant in (
            r"same close transaction.{0,100}remap every card and artifact link",
            r"apply one (?:optimistic (?:memory )?)?transaction",
            r"run `check`",
            r"exactly (?:re)?read every changed key, card, and artifact",
        ):
            self.assertRegex(protocol, invariant)

        terminology = protocol[protocol.index("canonical terminology") :]
        for invariant in (
            r"(?:update|synchronize) (?:every )?affected card field",
            r"`term`.{0,20}`symbol`.{0,20}facet",
            r"refresh affected links",
        ):
            self.assertRegex(terminology, invariant)

    def test_proof_exposition_has_distinct_scope_and_memory_ownership(self) -> None:
        exposition = " ".join(
            self.skill_texts()["write-proof-exposition"].split()
        ).lower()
        self.assertIn("reconstruct an established proof", exposition)
        self.assertIn("outside the specialty", exposition)
        self.assertRegex(
            exposition,
            r"status.{0,80}does not.{0,40}prove.{0,20}repair.{0,20}strengthen",
        )
        self.assertIn("named canonical target", exposition)
        self.assertRegex(exposition, r"in-place.{0,80}only.{0,80}markdown/sqlite pair")
        self.assertRegex(
            exposition,
            r"separate proof exposition.{0,100}own.{0,30}companion.{0,100}source pair"
            r".{0,30}read-only",
        )
        self.assertRegex(
            exposition,
            r"no two markdown documents share.{0,20}(?:one )?(?:sqlite )?database",
        )
        self.assertIn("$explain-mathematics", exposition)
        self.assertIn("$research-mathematics", exposition)
        self.assertRegex(
            exposition,
            r"publish only after.{0,80}(?:source )?comparison succeeds",
        )

    def test_skills_preserve_task_local_rigor_and_internal_handoffs(self) -> None:
        skills = {
            name: " ".join(text.split()).lower()
            for name, text in self.skill_texts().items()
        }
        for name in ("explore-mathematical-structure", "explore-proof-strategies"):
            self.assertIn("proof handoff", skills[name])
            self.assertRegex(
                skills[name],
                r"internal.{0,100}conversion obligation",
            )
        self.assertRegex(skills["explain-mathematics"], r"proof.{0,20}optional")
        self.assertIn("$write-proof-exposition", skills["explain-mathematics"])

        audit = skills["audit-assumptions"]
        for distinction in (
            "well-posedness",
            "present proof",
            "necessary for the theorem",
        ):
            self.assertIn(distinction, audit)
        self.assertRegex(audit, r"necessity.{0,80}checked example")
        self.assertRegex(audit, r"redundancy.{0,100}(?:derivation|checked proof)")
        self.assertIn("candidate_digest", audit)
        self.assertIn("requested_attacks", audit)

        destroy = skills["destroy-theory"]
        for outcome in (
            r"the theorem.{0,20}false",
            r"(?:this|the) proof.{0,20}fails",
            r"encoding.{0,40}fails",
            r"no defect.{0,30}(?:found|tested scope)",
        ):
            self.assertRegex(destroy, outcome)
        self.assertIn("candidate_digest", destroy)
        self.assertIn("requested_assumption_audits", destroy)
        self.assertIn("refuted", destroy)
        self.assertIn("not falsified in scope", destroy)

    def test_formalization_hands_off_only_a_suggested_key(self) -> None:
        formalize = " ".join(
            self.skill_texts()["formalize-concepts"].split()
        ).lower()
        self.assertRegex(formalize, r"plain description.{0,30}mathematical subject")
        self.assertRegex(formalize, r"suggested.{0,20}research key")
        self.assertRegex(formalize, r"next writable skill.{0,80}(?:reuse|new one)")
        self.assertRegex(formalize, r"does not.{0,20}create companions")


if __name__ == "__main__":
    unittest.main()
