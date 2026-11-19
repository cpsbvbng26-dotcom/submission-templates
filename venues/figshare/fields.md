# Figshare：登録の欄に貼る文の雛形

golden-window-resolution の稿を出したとき（2026-11-18）の欄の文を、作品によらない形にしたものです。
埋めた例は [examples/golden-window-resolution.md](./examples/golden-window-resolution.md) にあります。
Figshare の手引きの頁（help.figshare.com、figshare.com、docs.figshare.com）は、この作業の環境から届きません。
そのため、どの欄も記憶によります。
必須かどうかの印も記憶によります。

## Title

確かめ：記憶による（必須）

{{TITLE}}

PDF の題、PDF の登録情報、README、CITATION.cff と同じ文字列にします。

## Authors

確かめ：記憶による（必須）

Takuya Nemoto（ORCID 0009-0000-1406-0547）

所属は書きません。

## Item type

確かめ：記憶による（必須）

Preprint

## Categories

確かめ：記憶による（必須。語は Figshare の一覧から選ぶ）

{{CATEGORIES}}

## Keywords

確かめ：記憶による（必須）

{{KEYWORDS}}

## Description

確かめ：記憶による（必須）

要旨、状態の行、開示の段をこの順に置きます。
要旨は PDF の要旨と同じ文です。

{{ABSTRACT}}

Status. Known: {{KNOWN}}. Not found in the texts read: {{NOT_FOUND}}. Conditional: {{CONDITIONAL}}. "Not found in the texts read" is the strongest novelty claim made.

<!-- 開示の段：ここから。文は固定。{{LLM_USES}} と {{HUMAN_CHECKS}} だけを作品ごとに埋める -->
Claude Code (Anthropic) was used {{LLM_USES}}. {{HUMAN_CHECKS}} The author is responsible for the content. Claude is not an author.
<!-- 開示の段：ここまで -->

## License

確かめ：記憶による（必須）

CC BY 4.0

## Funding

確かめ：記憶による

None. (The work had no funding.)

## References

確かめ：記憶による

DOI か arXiv の URL を、行ごとに置きます。
DOI は、紙面の文献の欄と reading-ledger の台帳にある綴りだけを使います。

{{REFERENCE_URLS}}

## Related materials

確かめ：記憶による（欄の名と、関係の種類の選び方）

| 関係 | 識別子 |
| --- | --- |
| References | {{EARLIER_DOI}} |
| IsSupplementedBy | https://github.com/cpsbvbng26-dotcom/{{REPOSITORY}} |

関係の種類の名（References、IsSupplementedBy など）は DataCite の語です。
前の稿の新しい版として出すのか、別の項目として出すのかを、ここに書き添えます。
