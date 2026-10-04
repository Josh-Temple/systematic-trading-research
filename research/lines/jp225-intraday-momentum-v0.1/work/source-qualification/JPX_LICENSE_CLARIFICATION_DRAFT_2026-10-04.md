# JPX DataCube inquiry draft — not sent

Recipient: JPX Market Innovation & Research Client Services via the official J-Quants DataCube contact form:

https://dc.jpx-jquants.com/ja/contact#contact-form

The JPX public DataCube overview identifies Client Services as the contact point. This draft has not been submitted.

## 日本語

**件名:** J-Quants DataCube（日経225mini 歩み値）の個人研究における利用区分と公開範囲の確認

JPX総研 クライアントサービス部 御中

個人の非営利・非業務の研究目的で、J-Quants DataCubeの「金融デリバティブ情報／歩み値（ティック）／日経225mini」の2025年1月から12月までを、月単位で購入することを検討しています。データは個人PC内で分析し、raw CSV/ZIP、行単位の値段、時刻付きの個別レコード、mapped price point、復元可能な抜粋は、公開・第三者提供・クラウドアップロードしません。

公開 repository（public GitHub）に掲載を検討しているのは、rawファイルのSHA-256、公開仕様に基づく列スキーマ、月次・全期間のカバレッジ件数、欠損・重複等の非価格診断、回帰係数・平均return・confidence interval・event count等の非再構成可能な集計研究結果、および研究上の判断のみです。個別行・個別価格を明らかにせず、元データを再現できるような出力もしません。

DataCubeの利用規約では、自己使用目的（個人）は個人による非業務・私的目的、学術使用目的は非営利研究機関またはその所属者を対象としています。一方、DataCube FAQには「分析した判定結果のみの提供」であれば自己使用の範囲とあり、元データを分析根拠として提供する場合や再現可能な形で提供する場合は外部配信に該当し得ると記載されています。私は非営利研究機関に所属していません。

上記の事実関係では、購入時に「自己使用目的（個人）」を選択してよいでしょうか。それとも、public GitHubでの掲載により「外部配信目的」を選択する必要がありますか。特に、SHA-256、公開仕様のスキーマ、集計カバレッジ件数、非再構成可能な統計結果が、それぞれFAQの「分析結果のみ」に含まれるかをご教示ください。外部配信に該当する項目がある場合は、該当する項目と、購入時に必要な利用区分を明示いただけると助かります。

併せて、①すでにローカルPCへダウンロードしたファイルの保存期間またはローカルバックアップ制限、②tick仕様のTime（HHMMSSmmm）のタイムゾーンがJSTであるか、についても確認をお願いします。

この確認が取れるまで購入・公開は行いません。rawデータはローカル環境から外へ出しません。

よろしくお願いいたします。

## English

**Subject:** Confirmation of use category and publication scope for individual research using J-Quants DataCube Nikkei 225 mini ticks

Dear JPX Market Innovation & Research Client Services,

I am considering purchasing the J-Quants DataCube product “Financial Derivatives Information / Tick / Nikkei 225 mini” for each calendar month from January through December 2025 for an individual, non-commercial research project. I would analyze the files only on my personal computer. I would not publish or provide the raw CSV/ZIP files, row-level prices, timestamped records, mapped price points, or reconstructable extracts, and would not upload them to cloud services.

The only items I am considering publishing on a public GitHub repository are SHA-256 hashes of the raw files, the schema already described in public specifications, monthly and full-period coverage counts, non-price diagnostics such as missing/duplicate counts, non-reconstructable aggregate research outputs such as regression coefficients, mean returns, confidence intervals and event counts, and research decisions. No row-level observations or individual prices would be disclosed, and the outputs would not permit reconstruction of the source data.

The DataCube terms define individual self-use as an individual's non-business private purpose, and academic use as research by a non-profit research institution or a person belonging to one. I am not affiliated with such an institution. The DataCube FAQ says that providing analysis/judgment results alone is within self-use, while providing source data as supporting evidence or in reconstructable form may be external distribution.

Given these facts, may I select “self-use (individual)” when purchasing, or does publication on public GitHub require “external distribution”? In particular, please confirm whether SHA-256 hashes, the public schema, aggregate coverage counts, and non-reconstructable statistical results each fall within the FAQ's “analysis results only” scope. If any item requires external distribution, please identify that item and the use category that must be selected.

Please also confirm (1) whether a downloaded local copy may be retained or backed up locally after the download window expires, and (2) whether the tick specification's Time field (HHMMSSmmm) is expressed in JST.

I will not purchase or publish pending this clarification. Raw data will remain on my local computer.

Sincerely,

## 確認が取れれば十分な回答

JPXの回答が次を明示すれば、利用区分と公開境界の問い合わせは解決扱いにできる。

1. この個人・非業務研究に申告すべき購入区分（個人自己使用／学術／外部配信）。
2. 上記の各公開項目（hash、schema、coverage counts、aggregate statistics）がその区分で public GitHub に掲載可能か。
3. 外部配信扱いとなる項目があれば、その対象と必要区分。
4. ローカル保存・ローカルバックアップの保持条件。
5. Time欄のタイムゾーン。

回答は手動で確認し、資格判断を validator の自動推測で置き換えない。
