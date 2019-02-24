
<a href="https://colab.research.google.com/github/moizumi99/camera_raw_processing/blob/master/camera_raw_chapter_4.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

#  4. 重要な処理

## 4.1 この章について

### はじめに

この章ではカメラ画像処理の中でも重要な処理を紹介します。

この章の内容はColabノートブックとして公開してあります。ノートブックを見るには[目次ページ](https://colab.research.google.com/github/moizumi99/camera_raw_processing/blob/master/camera_raw_toc.ipynb)から参照するか、以下のリンクを使ってアクセスしてください。

https://colab.research.google.com/github/moizumi99/camera_raw_processing/blob/master/camera_raw_chapter_4.ipynb


### この章で扱う処理について

前章でRAW画像に最低限の処理を行いフルRGBとして表示することができました。
処理が単純な割には以外のきれいな画像ができたのではないでしょうか？

でもこれは画像を随分小さく表示しているせいで粗が目立っていないという面が大きいのです。またRAW現像やカメラ画像処理で扱う画像は常に理想的な状態で撮影されるわけではありません。撮影は室内などの暗いところで扱われることも多いですし、センサーもスマートフォン向けを始め非常に小さい物を使う事が多々あります。そういった画像データにはさまざまな理想的でない特性があり、そういったものは、各種の補正処理を行わないと最終的な画質は低品質になってしまいます。

また、前章で扱ったデモザイクは簡易的なもので出力画像が入力画像の４分の１の大きさになるという重大な問題があります。これも解決しなくてはなりません。

この章ではそういった通常のRAW画像を処理する上で重要な処理を紹介します。

とりあげるのは以下の処理です。
- デモザイク
- 欠陥画素補正
- カラーマトリクス補正
- レンズシェーディング補正

最初に扱うデモザイクでは、出力サイズが入力サイズと同じになる通常のデモザイク処理を取り上げます。

次の欠陥画素補正では、画像センサーにはつきものの欠陥画素を修正する方法を紹介します。

カラーマトリクス補正は色再現性を向上する処理です。

レンズシェーディング補正は画像の周辺で明るさが低下する周辺減光・レンズシェーディングと呼ばれる現象を補正します。

### まとめ

この章で扱う内容について概要を説明しました。次は[線形補間デモザイク処理](https://colab.research.google.com/github/moizumi99/camera_raw_processing/blob/master/camera_raw_chapter_4_2.ipynb)です。
