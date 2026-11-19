# Sophaxis：投稿の手順

利用者が手順を求めたので、手順として書きます（cpsbvbng26-dotcom の決めごと 16 の例外）。
2026-11-18 の手順（sophaxis の main、コミット 66e0a01 の様式と規程で確かめたもの）を、作品によらない形にしたものです。
欄の名は、2026-11-19 に sophaxis の main（コミット f4b5fff）の様式で確かめ直しました。
規程の行の番号は、変わりうるので書きません。
欄に貼る文は [fields.md](./fields.md) にあります。

1. 先に預け先（Figshare・Zenodo など）で公開し、DOI を得る。Sophaxis は DOI を持つ預け先の作品だけを扱う。出典：`policies/submission.md`。
2. DOI の登録情報のライセンスが、Sophaxis の受け付けるものかを見る。出典：`policies/submission.md`、`submission.yml` の doi の欄の説明。
3. 投稿の日を決める。2026-11-23 からは、最初の DOI の登録から一定の期間を過ぎた作品だけが載る。期間と数え方は `policies/submission.md` で見る。
4. ORCID の記録に、issue を開く GitHub のアカウントの URL があることを見る。自動の検査が、これで著者であることを確かめる。出典：`submission.yml` の冒頭の説明。
5. sophaxis のリポジトリの Issues で新しい issue を開き、Submit a preprint か日本語の様式を選ぶ。出典：`submission.yml`。
6. 欄を [fields.md](./fields.md) の順に埋める。
7. 印の欄は、それぞれの文が真であるときに付ける。
8. issue を作る。issue は公開され、利用者名と書いた中身はだれにでも見える。出典：`submission.yml` の冒頭の説明。

このあと起きること：

9. 自動の検査が DOI の登録情報と ORCID の記録を読み、結果を issue に書く。出典：`policies/submission.md`。
10. モデレーターがモデレーションの規程に沿って見る。モデレーターが運営者のほかにいない間は、運営者が自分の投稿も判断し、記録の頁にその印が付く。出典：`policies/moderation.md`。
11. 通れば記録の頁が公開される。掲載は査読ではなく、査読として示さない。出典：`submission.yml` の confirm の欄、`policies/moderation.md`。
