# marioai-2009
Original source code from https://github.com/morishin/marioai-2009

## 実行環境
Python3.6
## 実行方法
javaのコンパイラーantをインストールした後、最初のディレクトリで
```sh
ant
```
を実行してコンパイルする。

マリオサーバーを立ち上げる。
```sh
java -classpath classes ch.idsia.scenarios.MainRun -server on
```

マリオクライアントを実行

```sh
python src/python/competition/learn.py
```

## 遺伝的アルゴリズムのパラメータ
/src/python/competition内
### 遺伝子座で入力として使われるフィールド情報
ga/individual.pyの変数near_cells
### 各世代の集団数
learn.pyのn_individuals
### エリート個数
learn.pyのnumberOfElites
### 突然変異率
learn.pyのmutation_rate