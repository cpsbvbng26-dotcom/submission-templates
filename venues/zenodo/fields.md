# Zenodo：.zenodo.json の欄の雛形

Zenodo の GitHub の連携は、GitHub の Release から記録を作るときに、リポジトリの根にある `.zenodo.json` を読みます。
欄の名と書き方は、運営者のリポジトリの `.zenodo.json`（cpsbvbng26-dotcom、errata-check、self-correction、sophaxis、deposit-check、trinity-operator など）の書き方に合わせました。
zenodo.org の手引きの頁は、この作業の環境から届きません。
そのため、欄の名はどれも記憶によります。
この書き方の `.zenodo.json` から記録が作られた例は、[examples/sophaxis-v1.0.0.md](./examples/sophaxis-v1.0.0.md) にあります。

## title

確かめ：記憶による

{{REPOSITORY}}: {{ONE_LINE}}

CITATION.cff があれば、その題と同じ語で始めます。

## description

確かめ：記憶による

<p>{{WHAT_IT_HOLDS}}</p>

論文がそれぞれ自分の DOI を持つときは、論文はその DOI で引き、この記録で引かないことを書き添えます。

## upload_type

確かめ：記憶による

{{UPLOAD_TYPE}}

道具は software、記録や台帳は dataset、そのどちらでもないものは other にします。

## license

確かめ：記憶による

{{LICENSE_ID}}

`cc-by-4.0` か `mit` のどちらかにします。欄がどこに掛かるかは、notes に一文で書きます。

## access_right

確かめ：記憶による

open

## creators

確かめ：記憶による

```json
[{ "name": "Nemoto, Takuya", "orcid": "0009-0000-1406-0547" }]
```

所属（affiliation）の欄は置きません。

## keywords

確かめ：記憶による

{{KEYWORDS}}

cpsbvbng26-dotcom の `docs/keywords.json` の語から選びます。言い換えの組は避けます。

## related_identifiers

確かめ：記憶による

{{RELATED_IDENTIFIERS}}

`identifier`・`relation`（isSupplementTo、isDerivedFrom、references など）・`scheme`（doi か url）の組で並べます。
番号は、利用者から受け取ったものか、DataCite や Crossref で確かめたものだけです。

## notes

確かめ：記憶による

notes には、開示の段とライセンスの範囲を、この順に英語で書きます。

<!-- 開示の段：ここから。文は固定。{{LLM_USES}} と {{HUMAN_CHECKS}} だけを作品ごとに埋める -->
Claude Code (Anthropic) was used {{LLM_USES}}. {{HUMAN_CHECKS}} The author is responsible for the content. Claude is not an author.
<!-- 開示の段：ここまで -->

{{PARTS}} is CC BY 4.0 (LICENSE); {{PARTS}} is MIT (LICENSE-CODE). The licence field of this record covers {{PARTS}} only. Texts by others that this repository quotes, or keeps to verify its quotations, are not licensed under CC BY 4.0 or the MIT License and remain their owners'.
