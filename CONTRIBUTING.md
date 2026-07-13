# Contributing

## Scope

Contributions should improve source accuracy, decision usefulness, trigger boundaries, or validation. Do not add private consultation records, CVs, personal identifiers, local paths, or unverifiable anecdotes.

## Skill Rules

1. Keep one `SKILL.md` per skill directory.
2. Frontmatter may contain only `name` and `description`.
3. Match the frontmatter `name` to the directory name.
4. Put detailed source notes in `references/` and keep `SKILL.md` focused on operational guidance.
5. Label direct evidence, reasonable inference, and insufficient evidence separately.
6. Do not present generated prose as a verbatim quote.
7. Do not add a second persona under an existing persona's name.

## Before Committing

Run:

```powershell
python .\scripts\validate_skills.py
```

Then manually test at least one normal trigger, one negative trigger, one sparse-information case, and one adversarial request for fabricated quotes.
