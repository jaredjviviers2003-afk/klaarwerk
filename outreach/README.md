# Klaarwerk outreach kit

Used by the daily scheduled check of the Klaarwerk Call List sheet.

- `proposal-template.html`: the branded proposal email. Fill in the `{{...}}` placeholders. HEADLINE_START is usually "A website as good as" and HEADLINE_HIGHLIGHT is "your work." (or "your reviews.", "your garden." and so on).
- `email-logo.png`: the white Klaarwerk logo on green. Attach it **inline** as the first attachment, and the template references it as `cid:att0`.
- Gmail strips `background:`, so colours must use `background-color` plus `bgcolor`. The template already does this.
- Rules: one email approach per business (POPIA), always include the NO opt-out line, never invent facts about a business, and only mention site problems you have actually seen.
