# 開発ログ


## 2023-08-19

まずは常用漢字を、学ぶ小学校と中学校の学年ごとに用意する。`scripts/kanji.json` がその結果できたものである。

Wikipedia の日本語記事データから常用漢字に限定した uni-gram (つまり頻度だけ) を取り出し頻度でソートしてみる。ソートするために、最初は dict() で保存していたのに list() 形式で JSON には出力することになった。

```
python ./scripts/populate_kanji_occurrence_from_wikipedia.py
```

(ちなみに公開している JSON ファイル ([wikipedia_joyo_kanji_freq.json](https://github.com/kirameister/aki_code/blob/development/data/wikipedia_joyo_kanji_freq.json)) はその後手動で整形したものである)

その頻度データと、学ぶ漢字の学年 (中学校はまとめて 7 としてカウント) を並べてみる。Linear regression にしてみる。

```
python ./scripts/linear_regression_betweeen_occur_and_year.py
r^2 score: 0.45773262009027904
```

そしてプロットした図がこちらである。

![Wikipeda Kanji occurrence rank vs. educational year](./image/wikipedia_kanji_occur_rank_to_educational_year.png "Wikipedia の頻出漢字ランキングと学習年のプロット")

率直に言うと、「思ったほど correlate してないな」と感じた。もう少し綺麗にまとまっていれば (そこまで分散していなければ) 遠慮なく小学校の低学年で学ぶ漢字を優先して配列に追加できるのにな、ということなのだが、そう簡単な話でもない、ということなのだろう。もう少しどうするか考える。

## 2023-08-20

Wikipedia からのデータも bi-gram 以上の n-gram として抽出しておく。例によって list() としてソートしておく (公開しているファイルは整形済み…と思ったらそのままで 200MB 以上のデータになっていたので (データ件数だけだと 10M いかないぐらい)、1M で cut-off しておく - それでも多すぎるという可能性は大いにあるけれど - [n_gram_to_weight.json](https://github.com/kirameister/aki_code/blob/development/data/n_gram_to_weight.json))。

```
python ./scripts/n_gram_generator.py
head ./data/n_gram_to_weight.json
[
    [
        "日本",
        594779
    ],
    [
        "現在",
        246779
    ],
    [
```

…データを眺めていると、やはりというか、最初は bi-gram ばかり出てくる。しかしこれ、実装方法がなにか間違っている気がしてきた (主に 4-gram 以上のトークンの扱いについて)。それに人間の脳にはそこまで容量があるわけでもないので、高々 (文脈を知るための) tri-gram で十分なのでは、という気がしてきた。後日 script を変更して試してみよう。



