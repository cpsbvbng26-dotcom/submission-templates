# Zenodo：GitHub の連携で記録を作る手順

利用者が手順を求めたので、手順として書きます（cpsbvbng26-dotcom の決めごと 16 の例外）。
zenodo.org の手引きの頁は、この作業の環境から届きません。
画面の名前とボタンの名前は、どの段も記憶によります。
Zenodo での公開と新しい版の作成は、利用者が行います（cpsbvbng26-dotcom の決めごと 12）。
Claude は `.zenodo.json` を書き、番号を受け取って記録に書くだけです。

1. リポジトリの根に `.zenodo.json` を置き、main にマージする。欄は [fields.md](./fields.md) の形にする。
2. Zenodo に GitHub のアカウントでサインインし、GitHub の連携の頁でそのリポジトリを有効にする。
3. GitHub でタグと Release を作る。Zenodo は Release を受けて記録を作る。
4. 記録の頁に出る版の DOI（10.5281/zenodo.… の形）と、すべての版に共通する DOI を写す。
5. 番号を受け取ったら、DataCite の記録で、版の関係（IsVersionOf）・種類・著者の ORCID iD・ライセンスを確かめてから、cpsbvbng26-dotcom の `docs/doi-index.md` に書く。番号を推測で書かない（決めごと 1）。
