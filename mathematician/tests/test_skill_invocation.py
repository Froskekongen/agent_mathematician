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
        challenge = research.split("## 4. Challenge the unchanged candidate", 1)[1]
        challenge = challenge.split("## 5. Verify freshly", 1)[0]
        normalized = " ".join(challenge.split()).lower()
        self.assertIn("dispatch two fresh, mutually isolated", normalized)
        self.assertIn("the first prompt invokes `$destroy-theory`", normalized)
        self.assertIn("the second invokes `$audit-assumptions`", normalized)
        self.assertIn("that candidate, digest, and no peer report", normalized)
        self.assertIn("reject a mismatched `candidate_digest`", normalized)
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

    def test_exactly_seven_skills_have_writable_memory_roles(self) -> None:
        skills = self.skill_texts()
        self.assertEqual(len(MEMORY_WRITERS), 7)
        for name in MEMORY_WRITERS:
            normalized = " ".join(skills[name].split()).lower()
            self.assertRegex(normalized, r"\b(?:writable|file-backed)\b", name)
        formalize = " ".join(skills["formalize-concepts"].split()).lower()
        self.assertIn("this skill does not create companions", formalize)
        self.assertNotIn("sole writer", formalize)

    def test_explanation_rewrite_requires_explicit_authorization(self) -> None:
        explain = " ".join(
            self.skill_texts()["explain-mathematics"].split()
        ).lower()
        self.assertIn("merely supplying or naming a file does not authorize", explain)
        self.assertIn(
            "explicit request that names an existing canonical target and asks to "
            "update or rewrite it",
            explain,
        )
        self.assertIn("two markdown documents never share one sqlite database", explain)
        self.assertIn("apply one optimistic memory transaction", explain)

    def test_formalization_hands_off_only_a_proposed_key(self) -> None:
        formalize = " ".join(
            self.skill_texts()["formalize-concepts"].split()
        ).lower()
        self.assertIn("durable mathematical subject in words", formalize)
        self.assertIn("proposed semantic key", formalize)
        self.assertIn("proposed key is not authoritative", formalize)
        self.assertIn("receiving writable coordinator reads the target outline", formalize)

    def test_live_complexity_metrics_are_reproducible(self) -> None:
        skill_paths = sorted(SKILLS.glob("*/SKILL.md"))
        reference_paths = sorted(SKILLS.glob("*/references/*.md"))
        reference_paths = [
            path for path in reference_paths if path.name != "evidence-based-methods.md"
        ]
        public = "".join(path.read_text(encoding="utf-8") for path in skill_paths)
        runtime = public + "".join(
            path.read_text(encoding="utf-8") for path in reference_paths
        )
        skills = self.skill_texts()
        worker_descriptions = [
            self.frontmatter(name, skills[name])["description"]
            for name in sorted(MODEL_WORKERS)
        ]
        pilot = (
            REPO_ROOT
            / "mathematician"
            / "evaluations"
            / "architecture-pair"
            / "pilot-results.md"
        ).read_text(encoding="utf-8")
        self.assertIn(
            f"| Public skill lines | 939 | 633 | {public.count(chr(10)):,} |", pilot
        )
        self.assertIn(
            f"| Public skill words | 8,440 | 3,958 | {len(public.split()):,} |", pilot
        )
        self.assertIn(
            f"| Full routed-runtime lines | 1,621 | 1,167 | {runtime.count(chr(10)):,} |",
            pilot,
        )
        self.assertIn(
            f"| Full routed-runtime words | 14,012 | 7,210 | {len(runtime.split()):,} |",
            pilot,
        )
        self.assertIn(
            f"{sum(len(value.encode()) for value in worker_descriptions)}\nbytes "
            f"({sum(len(value.split()) for value in worker_descriptions)} words)",
            pilot,
        )


if __name__ == "__main__":
    unittest.main()
