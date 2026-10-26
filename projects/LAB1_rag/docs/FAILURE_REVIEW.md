# Failure and citation review — AI editorial inspection

The 20 stored outputs were inspected against the authored fictional policies. This is Codex review, not independent human annotation. The automatic reference-substring metric is intentionally retained unchanged so its weakness is visible.

- **Weekday opening time:** retrieval missed `hours.txt`. Raw generation invented “11:30 AM”. The guard abstained, which prevents an unsupported answer but does not answer the available question. The high retrieval score (about .93) did not establish relevance.
- **Book returns:** retrieval chose digital/loans documents, omitting the returns policy. The generated phrase “Lumen Library” occurs in those documents and passed the guard, but it does not specify the required main desk. Source-substring support is insufficient for correctness.
- **Damaged-book replacement fee:** the corpus explicitly leaves the fee unspecified. The answer “a librarian” was copied from the source and passed the guard despite being irrelevant. This is an unanswerable case falsely answered with a citation.
- **Phone number, director and parking fee:** raw generation invented a marker, a name or a price. The guard converted these to UNKNOWN. Generated names and numbers are not verified facts or actual contacts.
- **Outdoor return box:** “No” is correct, but the guard cites both returns and loans because the word also appears in an unrelated loan condition. Citation presence is not citation precision.

On semantic inspection, the no-RAG baseline has two acceptable answers that the reference substring test misses: “no” for Sunday opening and “No” for digital renewal. Its semantic result is therefore 2/20 (10%), not the automatic 0/20. Raw RAG is 14/20; guarded RAG is 17/20 under the task's answer-or-UNKNOWN criterion. Among 16 non-abstained guarded responses, 14 are correct (87.5%). Of four unanswerable questions, three are correctly refused and one is falsely answered. These are diagnostics on this exact set, not generalization estimates.

Do not deploy this guard as a semantic faithfulness validator. A next version should improve retrieval, require answer-type and citation entailment checks, and be assessed on a newly authored untouched question set. The present set must not become a repeatedly tuned test benchmark.
