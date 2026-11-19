# submission-templates

[日本語](./README.md)

The field texts and the steps used when depositing works, one folder per venue.
The texts of each work are turned into templates, and the filled examples are kept.

## Venues

There are 5 venues: Figshare, Sophaxis, SSRN, PhilArchive and Zenodo.
Each folder in `venues/` holds the template of the fields (`fields.md`), the steps (`steps.md`) and filled examples (`examples/`).

Every field of a template is marked either as verified on the venue's page (場の頁で確かめた) or as from memory (記憶による).
The help pages of Figshare, SSRN, PhilArchive and Zenodo cannot be reached from the environment this was written in, so most of their fields are from memory.
The Sophaxis fields were checked against the submission form in the sophaxis repository.
The PhilArchive category names were checked against the category pages of philpapers.org.
Places to fill in are written in capitals, such as `{{TITLE}}`.

The disclosure of the use of a language model is a fixed block, [blocks/disclosure.md](./blocks/disclosure.md), which every template carries unchanged.
Where a venue asks for an e-mail address, the templates and examples say only （本人のものを入力）, "enter one's own", and no file holds an address.

## Filled examples

There are 5 examples, of which 2 are of deposits.
The Figshare example is the paper of golden-window-resolution, deposited on 2026-11-18, and the Zenodo example is the `.zenodo.json` of sophaxis v1.0.0, from which Zenodo made a record.
The Sophaxis example is a submission body, and the sophaxis repository has no record of a listing.
The SSRN and PhilArchive examples are the field texts prepared for the follow-up to the celibacy paper; no deposit is recorded.
They are kept because no other field texts for these venues remain.
Each example is copied unchanged, and `verification/examples.json` holds the SHA-256 of the copied part.
Every DOI in an example was given by the owner or confirmed at DataCite or Crossref.

## Checks

```
python3 verification/check.py
python3 verification/check.py --online
python3 verification/check.py --break
```

## Operator

Takuya Nemoto. ORCID iD [0009-0000-1406-0547](https://orcid.org/0009-0000-1406-0547).
[Report an error](https://github.com/cpsbvbng26-dotcom/submission-templates/issues/new?template=error-report.yml). Security issues go through [SECURITY.md](./SECURITY.md).

## Use of a language model

The templates and the checks were written by Claude Code (Anthropic) at the operator's request.
Claude is not an author.

## Licence

Text is [CC BY 4.0](./LICENSE); code is [MIT](./LICENSE-CODE).
