# 開発ログ


## 2023-08-19

まずは常用漢字を、学ぶ小学校と中学校の学年ごとに用意する。`scripts/kanji.json` ができたものである。

Wikipedia の日本語記事データから常用漢字に限定した uni-gram (つまり頻度だけ) を取り出し頻度でソートしてみる。ソートするために、最初は dict() で保存していたのに list() 形式で JSON には出力することになった。

```
python ./scripts/populate_kanji_occurrence_from_wikipedia.py
```

その頻度データと、学ぶ漢字の学年 (中学校はまとめて 7 としてカウント) を並べてみる。Linear regression にしてみる。

```
python ./scripts/linear_regression_betweeen_occur_and_year.py
r^2 score: 0.45773262009027904
```

そしてプロットした図がこちらである。

![Wikipeda Kanji occurrence rank vs. educational year](./image/wikipedia_kanji_occur_rank_to_educational_year.png "Wikipedia の頻出漢字ランキングと学習年のプロット")

率直に言うと、「思ったほど correlate してないな」と感じた。もう少し綺麗にまとまっていれば (そこまで分散していなければ) 遠慮なく小学校の低学年で学ぶ漢字を優先して配列に追加できるのにな、ということなのだが、そう簡単な話でもない、ということなのだろう。もう少しどうするか考える。

