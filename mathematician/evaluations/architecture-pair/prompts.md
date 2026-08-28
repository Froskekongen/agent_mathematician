# Solver prompts

This file is solver-facing. It intentionally contains neither source links nor
answers. For a trial, concatenate the common envelope and exactly one problem
block without other commentary.

## Common solver envelope

```text
Use the mathematical workflow available in this checkout to solve the problem
below. Work in a fresh local directory and persist the result as the workflow
normally requires so that another agent with no conversation history can audit
it later.

Do not browse the internet or search for the published problem. You may write
and run local programs using the language standard library. Give a rigorous
solution or a correctly calibrated unresolved result. State the interpreted
claim, conclusion/status, argument, checks, and any remaining limitation.

If you retain executable code, put enough reproducibility metadata inside that
program as an ordinary language-native data structure. Do not create a separate
manifest. The metadata should identify the purpose, exact predicate and scope,
reproduction command, parameters or seeds, arithmetic model, stopping rule,
and limitations that actually apply.
```

## P1 — Product of cosines

```text
For each positive integer n, define

    f_n(x) = product_{k=1}^n cos(kx).

Find the least n for which |f_n''(0)| > 2023, and prove that your value is
minimal.
```

## P2 — Prime plus twice a square

```text
Find the smallest odd composite integer N that cannot be represented as

    N = p + 2s^2,

where p is a prime and s is a positive integer. Certify both that N has no such
representation and that every smaller odd composite does. A bounded exact
program is allowed, but an unexplained printed integer is not a certificate.
```

## P3 — Reciprocal interpolation

```text
Let n be an even positive integer. Let p be a monic real polynomial of degree
2n satisfying

    p(1/k) = k^2

for every integer k with 1 <= |k| <= n. Determine every other real number x
for which p(1/x) = x^2, and prove that your list is complete.
```

## P4 — Sum-of-powers claim

```text
Decide whether the following claim is true:

For every integer k > 2, whenever positive integers a_1, ..., a_m and b satisfy

    a_1^k + ... + a_m^k = b^k,

one must have m >= k.

Give a proof or a certified counterexample. Bounded computation is allowed for
discovery, but distinguish finding a witness, checking it, and proving any
minimality statement you choose to make.
```

## Common cold-verification prompt

Run this in a fresh conversation after the solver has finished:

```text
Audit the persisted mathematical result in this directory without relying on
any earlier conversation. Recover only the context you need through this
checkout's normal canonical-memory workflow. Reconstruct the load-bearing
argument, replay every load-bearing executable artifact, and check that each
encoded predicate matches the written mathematical claim, including domains
and boundaries.

Report the exact conclusion and justified status, any error or stale/missing
evidence, what you independently checked, and whether the persisted result can
be accepted unchanged. Do not browse the internet or search for the published
problem. Do not silently repair the result.
```

