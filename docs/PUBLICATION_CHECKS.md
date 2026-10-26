# Publication review

The public edition has an independent history. Original Python source and tests are byte-identical to the locally reviewed/tested source. Metadata, licences, private-reference redaction and presentation were changed for release; no model was retrained.

- The preceding private history was inspected across its single commit before any publication decision; private transfer receipts and machine/private-page references were excluded from the new public history. The private repository was not rewritten or made public.
- Explicit output allowlists and a content review exclude raw data, CFPB complaint narratives/IDs/vocabulary/models, runtime/weights, private snapshots and secrets. The only email-pattern finding in source is an example.org synthetic privacy-scrubbing test fixture.
- Seven executed companion notebooks retain matching evidence hashes. Original raw evidence is kept locally and is not published. Public logs redact local machine paths; these redactions are not new computations.
- Thirty-five Python files parse and match the previously tested source. Forty-five local Markdown targets were checked before release; new public links and final tracking links are checked after upload.
- GitHub visibility, remote Git blob hashes and selected raw files were verified anonymously. GitHub Actions is disabled.
- Ten Notion pages were published through the official Share → Publish interface. All ten URLs returned HTTP 200 without cookies/authentication, and all ten contents were checked in the read-only visitor layout. Native links stay on the public Notion domain; a home-to-Retail and Docker-to-home round trip passed.

Code-only MIT scope and source-specific data rights are in LICENSING.md and ATTRIBUTIONS.md. Olist derived material remains CC BY-NC-SA 4.0 and noncommercial. Technical limits and AI assistance remain visible in README and each case. No cloud, profile changes, offers, applications or client outcome claims.
