# Compare the three saves

These were fresh local Codex sessions using the Brickbox practice tool.

| Request | What the tool or hook did | File check |
| --- | --- | --- |
| Save `1042.md` before installing the hook | Tool reported `Saved 1042.md`. | The file existed in the project root. |
| Save `1042.md` with the hook active | The hook denied the attempted write. It told the agent to use `drafts/<order-number>.md`. | The root file was absent. |
| Save `drafts/1042.md` with the hook active | Tool reported `Saved drafts/1042.md`. | The file contained `Order 1042. Forward to Billing.` |

Ask your agent why each call ended where it did. The hook checks this
practice tool. Its result says what happened to that attempted write.
