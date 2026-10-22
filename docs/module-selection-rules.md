# Module Selection Rules

These rules define how the planner identifies owned modules that can be used
for a target build. They are product rules and can be revised as the planner's
requirements evolve.

## Module identity

A module must match the target on all three identity fields to be an eligible
candidate:

- module type/name
- class/size
- mount type (`G`, `F`, or `T`)

Modules that differ on any identity field are not candidates. The same identity
requirement applies to the informational near-match list.

## Allocation status

The inventory's field 7 indicates whether a module is allocated:

- A value containing `Used on...` means the module is allocated to a ship.
- Any other value, including an empty value, means the module is unallocated.

Allocated modules may be reassigned to the target build, but unallocated
modules are preferred. An inventory module can satisfy only one target slot;
once selected, reserve it and do not use it for another slot.

## Candidate eligibility

For a module with matching identity:

- An exact match has the target modification, target grade, and target
  experimental effect.
- A module with the target modification and target grade but no experimental
  effect is also eligible.
- A module with the target modification at a lower grade is eligible, whether
  it has the target experimental effect or no experimental effect.
- An unmodified module is eligible to be engineered to the target.
- A higher grade than the target, a different modification, or a different
  experimental effect is not an eligible candidate.

Engineering an eligible module to the target modification, grade, or
experimental effect may be assumed possible. This also applies to allocated
modules that are reassigned.

## Candidate priority

Use the first available category in this strict order:

1. Unallocated; target modification, target grade, and target experimental.
2. Unallocated; target modification and target grade, with no experimental.
3. Unallocated; target modification at a lower grade, with the target
   experimental.
4. Unallocated; target modification at a lower grade, with no experimental.
5. Unallocated; no modification or experimental.
6. Allocated; target modification, target grade, and target experimental.
7. Allocated; target modification and target grade, with no experimental.
8. Allocated; target modification at a lower grade, with the target
   experimental.
9. Allocated; target modification at a lower grade, with no experimental.
10. Allocated; no modification or experimental.
11. De-engineer an identity-matching module that has an incorrect Grade 1
    modification and no experimental effect, then apply the target
    engineering. This is permitted only as a last resort, after the preceding
    options and immediately before buying a new module.
12. Buy a new module.

Do not de-engineer a module with an experimental effect. The Grade 1 exception
does not make a module with a different identity eligible.

Within a priority category, prefer the option requiring the fewest changes.
Do not promote a lower-priority category above a higher-priority one.

## When no candidate qualifies

If none of priorities 1–11 yields a module, show the option to buy a new module
and up to three informational near-matches. A near-match must still match all
three identity fields; it is not an eligible candidate and must not be assigned
to the target slot.

Rank near-matches by engineering similarity, in this order:

1. Prefer the target modification.
2. Prefer the closest grade.
3. Prefer the closest experimental effect.

## Details to refine

The rules do not yet specify how to break ties between equally similar
near-matches, or how to measure the distance between experimental effects.
