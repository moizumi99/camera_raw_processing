
# 5 画質を良くする処理

# 5.1 この章について


## はじめに

この章では画像の画質を良くする処理を紹介します。

この章の内容はColabノートブックとして公開してあります。ノートブックを見るには[目次ページ](https://colab.research.google.com/github/moizumi99/camera_raw_processing/blob/master/camera_raw_toc.ipynb)から参照するか、以下のリンクを使ってアクセスしてください。

https://colab.research.google.com/github/moizumi99/camera_raw_processing/blob/master/camera_raw_chapter_5.ipynb


## この章で扱う処理について

前章まででカメラ画像処理に最低限必用な処理の説明を行いました。

ここまででとりあえず見るに耐える画像はできましたが、画像の細部を見ていくとなんとなくぼやっとしていたり、平面のはずのところにノイズがのっていたりしていることに気がつくと思います。この章では、こういった点を解決して見栄えの良い、よりきれいな画像を作り上げる処理をとりあげます。

とりあげるのは以下の処理です。
- ノイズフィルター
- エッジ強調
- トーンカーブ補正

最初のノイズフィルターとしてはよく知られているバイラテラルフィルターという処理をとりあげます。

次のエッジ強調では、これまたアナログの時代から知られているアンシャープマスク処理をとりあげます。

最後のトーンカーブ補正では、ヒストグラムについて簡単に説明したあとで、トーンカーブ補正処理を行ってみます。

この章でも、ラズベリーパイのカメラ(v1.2)で撮影したRAW画像を使用します。

## まとめ

この章で扱う内容について概要を説明しました。次は[ノイズフィルター](https://colab.research.google.com/github/moizumi99/camera_raw_processing/blob/master/camera_raw_chapter_5_2.ipynb)です。
