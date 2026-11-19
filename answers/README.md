# Working copies for the labs

From the folder you cloned, run `python3 tools/start.py STAGE --agent "$agent"`
with a stage from the table. Open the path it prints. When the folder
already exists, use it or add `--at` and a new path.

| Lab | First run | Working copy | What to check |
| --- | --- | --- | --- |
| 1. Skill | `1-before` | `1-solved` | The kit question leads to the product guide. The double-charge ticket still triggers the order skill. |
| 2. Script | `2-before` | `2-solved` | Order 1042 has 2500 cents captured and 2500 cents pending. |
| 3. Rule | `3-before` | `3-solved` | Ask why the save goes into `drafts/` on a request for an already-written note. |
| 4. Hook | `4-before` | `4-solved` | The root write is denied after the hook is installed. The file under `drafts/` opens. |
| 5. Clef | `5-before` | `5-solved` | The routing script and the two logs show the cases that need reasoning. |
| 6. Package | `6-before` | `6-solved` | `acr validate` lists the package files. The clean consumer can find the installed script. |
| 7. Eval | `clean` twice | [Saved runs](../evidence/README.md#eval) | Score both runs with the same criteria and find the evidence for each point. |
