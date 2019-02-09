
# 3.1 準備と簡易デモザイク

## この節について

この節ではまずRAW画像を準備し、簡易的なデモザイクを行ってみます。

この節のの内容はColabノートブックとして公開してあります。ノートブックを見るには[目次ページ](https://colab.research.google.com/github/moizumi99/camera_raw_processing/blob/master/camera_raw_toc.ipynb)から参照するか、以下のリンクを使ってアクセスしてください。

https://colab.research.google.com/github/moizumi99/camera_raw_processing/blob/master/camera_raw_chapter_3_1.ipynb

## RAW画像の準備

まずRAW画像を用意します。今回はSony α 7 IIIで撮影したこの画像を使います。

  ![最終的な画像](https://github.com/moizumi99/camera_raw_processing/raw/master/fig2_1.png "最終的な画像")

ここで表示している画像は使用するRAWファイルから作成したRGB画像（PNGファイル）です。

元になるRAWファイルはこのURLにあります。

https://raw.githubusercontent.com/moizumi99/raw_process/master/sample.ARW

では、colab上にダウンロードしてみましょう。


```python
!if [ ! -f sample.ARW ]; then wget https://raw.githubusercontent.com/moizumi99/camera_raw_process/master/sample.ARW; fi
```

自分で撮影したRAWデータを使用する場合は次のコマンド利用してください。


```python
# from google.colab import files
# uploaded = files.upload()
```

使いやすいようにRAWファイル名を変数に保存しておきます。

自分でアップロードしたファイルを使用する場合は、ファイル名を対象のファイルに書き換えてください。


```python
raw_file  = "sample.ARW"
```

## RAW画像の読み込み

まず必用なモジュールをインストールします。

まずインストールするのはrawpyです。

rawpyはpythonでRAW画像を操作するためのモジュールです。

https://pypi.org/project/rawpy/

rawpyを使うとRAW画像からRAW画像データを取り出したり、画像サイズなどのパラメータを読み出したり、また簡易現像をすることができます。

rawpyの使用法については実際に使う時に説明します。


```python
!pip install rawpy
```

    Requirement already satisfied: rawpy in /home/moiz/anaconda3/lib/python3.7/site-packages (0.13.0)
    Requirement already satisfied: numpy in /home/moiz/anaconda3/lib/python3.7/site-packages (from rawpy) (1.15.1)


colabではコマンドの最初に!をつけると、linuxコマンドが実行できます。pipはpythonのモジュール管理用のコマンドです。

次にimageioをインストールします。

imageioは画像の表示やロード・セーブなどを行うモジュールです。


```python
!pip install imageio
```

    Requirement already satisfied: imageio in /home/moiz/anaconda3/lib/python3.7/site-packages (2.4.1)


次にこれらのモジュールをインポートします。


```python
import rawpy, imageio
```

他に必用なモジュールがある場合はその都度importすることにします。

では先程ダウンロードしたRAWファイルをrawpyを使って読み出してみましょう。

`imread()`はrawデータをファイルから読み込むrawpyのメソッドです。


```python
raw = rawpy.imread(raw_file)
```

読み込みがうまくいったか確認を兼ねてRAWデータの情報を見てみましょう。

まず、画像サイズを確認します。読み込んだRAWデータは、sizesというアトリビュートでサイズ確認ができます。


```python
print(raw.sizes)
```

    ImageSizes(raw_height=4024, raw_width=6048, height=4024, width=6024, top_margin=0, left_margin=0, iheight=4024, iwidth=6024, pixel_aspect=1.0, flip=0)


raw_heightとraw_widthはRAWデータのサイズです。この画像のサイズは縦4024ライン、横6048画素、ということになります。

heightとwidthは、画像処理後の出力画像のサイズです。

他の値についてはrawpyのページで解説されています。

https://letmaik.github.io/rawpy/api/rawpy.RawPy.html#rawpy.RawPy.sizes

この画像を処理しやすくするために、numpyを使用します。

numpyはpython用の数値計算ライブラリーです。行列処理の機能が豊富なので画像処理にも向いています。

まず、numpyをnpという名前でインポートします。


```python
import numpy as np
```

次にraw画像データから数値データのみをnumpyの配列に読み込みます。


```python
raw_array = raw.raw_image
```

raw_imageはRAW画像データをnumpyの配列して渡すアトリビュートです。

縦横の大きさを取得しておきます。


```python
h, w = raw_array.shape
print(h, w)
```

    4024 6048


これでraw_arrayは4024 x 6048の２次元配列になりました。
画像データを表示するコマンドimshowを使って、画像として確認してみましょう。

まずキャプション用に日本語フォントを用意します。


```python
# 日本語フォントをインストール
!apt -y install fonts-ipafont-gothic

# 画像表示用ライブラリpyplotのインポート。
import matplotlib.pyplot as plt
# 日本語フォントを設定
plt.rcParams['font.family'] = 'IPAPGothic'
```

    E: Could not open lock file /var/lib/dpkg/lock-frontend - open (13: Permission denied)
    E: Unable to acquire the dpkg frontend lock (/var/lib/dpkg/lock-frontend), are you root?


実際に画像を表示します。


```python
# 画像表示サイズを設定。figsizeの中身は横サイズ、縦サイズ。
# 単位はインチだが実際の表示サイズはディスプレイ解像度によって異なる。
plt.figure(figsize=(8, 6))
# raw_arrayの中のデータをグレースケールで表示します。
plt.imshow(raw_array, cmap='gray')
# 軸を非表示にします。
plt.axis('off')
# 画像タイトルの設定
plt.title(u"Bayer画像をそのまま表示")
# 実際に表示します。
plt.show()
```


![png](camera_raw_chapter_3_1_files/camera_raw_chapter_3_1_35_0.png)


ここでmatplotlibはnumpy用描画ライブラリーです。その中でpyplotは各種グラフを表示するモジュールです。ここではpltという名前でインポートしています。

もし日本語のタイトルが文字化けしている場合は、もし日本語が文字化けしている場合は
`! rm /content/.cache/matplotlib/fontList.json`を実行して、
Runtime->Restart Runtimeで再実行してみてください。


```python
# もし日本語が文字化けしている場合次の行の#を削除して実行。
# ! rm /content/.cache/matplotlib/fontList.json
# その後、Runtime->Restart and run allで再実行
```

## この節のまとめ

必用なモジュールをインポートしてRAW画像をcolab上に読み込みました。
次は[簡易デモザイク処理](https://colab.research.google.com/github/moizumi99/camera_raw_processing/blob/master/camera_raw_chapter_3_2.ipynb)を行います。
