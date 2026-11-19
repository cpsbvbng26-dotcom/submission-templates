# submission-templates

[English](./README.en.md)

論文やリポジトリを預け先に出したときの欄の文と手順を、預け先ごとに残すリポジトリです。
作品ごとの文を、作品によらない雛形にしてあります。
埋めた例も、作品ごとに残してあります。

## 預け先

預け先は 5 か所です。
どの預け先のフォルダも、欄の雛形（`fields.md`）、手順（`steps.md`）、埋めた例（`examples/`）を持ちます。

| 預け先 | 雛形 | 手順 | 埋めた例 |
| --- | --- | --- | --- |
| Figshare | [fields.md](./venues/figshare/fields.md) | [steps.md](./venues/figshare/steps.md) | [golden-window-resolution の稿](./venues/figshare/examples/golden-window-resolution.md) |
| Sophaxis | [fields.md](./venues/sophaxis/fields.md) | [steps.md](./venues/sophaxis/steps.md) | [golden-window-resolution の稿の投稿の本文](./venues/sophaxis/examples/golden-window-resolution.md) |
| SSRN | [fields.md](./venues/ssrn/fields.md) | [steps.md](./venues/ssrn/steps.md) | [独身論の続編](./venues/ssrn/examples/celibacy-follow-up.md) |
| PhilArchive | [fields.md](./venues/philarchive/fields.md) | [steps.md](./venues/philarchive/steps.md) | [独身論の続編](./venues/philarchive/examples/celibacy-follow-up.md) |
| Zenodo | [fields.md](./venues/zenodo/fields.md) | [steps.md](./venues/zenodo/steps.md) | [sophaxis v1.0.0 の .zenodo.json](./venues/zenodo/examples/sophaxis-v1.0.0.md) |

## 雛形の印

雛形の欄には、どれも確かめ方の印が付いています。
印は、場の頁で確かめた、か、記憶による、のどちらかです。
Figshare、SSRN、PhilArchive、Zenodo の案内の頁は、この作業の環境から届きません。
そのため、それらの欄の大半は記憶によります。
Sophaxis の欄は、sophaxis のリポジトリにある投稿の様式で確かめました。
PhilArchive の分類の名は、philpapers.org の分類の頁で確かめました。
欄に埋める所は `{{TITLE}}` のような大文字の名で示します。

## 開示の段

言語モデルの使い方を開示する段は、[blocks/disclosure.md](./blocks/disclosure.md) に固定してあります。
どの雛形も、この段を一字も変えずに持ちます。
作品ごとに埋めるのは、何に使ったかと、人が何を確かめたかの所だけです。

## メールアドレス

メールアドレスを求める欄には、雛形でも例でも、（本人のものを入力）とだけ書きます。
このリポジトリのどのファイルにも、メールアドレスは書きません。

## 埋めた例

埋めた例は 5 本です。
そのうち、出したものの例は 2 本です。
Figshare の例は、2026-11-18 に出した golden-window-resolution の稿の欄の文です。
Zenodo の例は、Zenodo が記録を作った sophaxis v1.0.0 の `.zenodo.json` です。
Sophaxis の例は投稿の本文で、Sophaxis に載ったという記録は、sophaxis のリポジトリに見つかりません。
SSRN と PhilArchive の例は独身論の続編のために作った欄の文で、出したという記録は見つかりません。
SSRN と PhilArchive の欄の文は、ほかに残っていないので、作った文を例として置きました。
どの例も、作業の控えかリポジトリの版から、一字も変えずに写しました。
写した部分の SHA-256 は `verification/examples.json` にあり、検査が照らします。
例に出てくる DOI は、どれも利用者から受け取った番号か、DataCite か Crossref で確かめた番号です。

## 検査

```
python3 verification/check.py            # 雛形・例・DOI（控えた登録の記録と突き合わせる）・写し・書き方
python3 verification/check.py --online   # DOI を Crossref と DataCite で引き直す
python3 verification/check.py --record   # 引き直して verification/cache/ に書く
python3 verification/check.py --break    # 検査を一つずつ壊し、落ちることを確かめる
```

## 運営者

運営者は、根本卓哉（Takuya Nemoto）です。
ORCID iD は [0009-0000-1406-0547](https://orcid.org/0009-0000-1406-0547) です。
誤りは[誤りの知らせ](https://github.com/cpsbvbng26-dotcom/submission-templates/issues/new?template=error-report.yml)の様式で受けます。
安全の問題は、[SECURITY.md](./SECURITY.md) の入口で受けます。

## 言語モデルの使い方

雛形と検査は、運営者が求め、Claude Code（Anthropic）が書きました。
Claude は著者ではありません。

## ライセンス

文は [CC BY 4.0](./LICENSE)、コードは [MIT](./LICENSE-CODE) です。
