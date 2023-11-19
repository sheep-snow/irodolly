# basic



# advanced

**articles**

* [画像処理 - 画像の性質と色空間](https://note.com/branch_it_sol205/n/na235045591c5)
* [Illustrated Characters Classification with Color Information](https://db-event.jpn.org/deim2013/proceedings/pdf/p4-5.pdf)
  * LBP (Local Binary Pattern)
    * [Local Binary Patternの理論と実装](https://qiita.com/tancoro/items/959ae9c14048c06bea8e)
* [Region-Based Image Retrieval using L\*a\*b\* Color
Histogram Features applied to ImageNet Database](https://www.lab.kochi-tech.ac.jp/yoshilab/thesis/1160346.pdf)
  * 色特徴抽出法
    * RGB色ヒストグラムを得る方法
    * L\*a\*b\*色特徴の平均・分散・歪度を得る方法
  * 類似画像検索の特徴抽出法
    * SIFT, SURF, ORB などがあり、ORBが精度と消費資源面で優秀
* [RGB-HSV-XYZ-L\*a\*b\*の対応表](https://qiita.com/fate_shelled/items/f466065f3fb1e99b0201)

# tools

* managed services
  * [AWS Rekogniton](https://docs.aws.amazon.com/ja_jp/rekognition/?id=docs_gateway)
    * [content moderation](https://aws.amazon.com/jp/machine-learning/ml-use-cases/content-moderation/)
  * [AWS Sagemaker Canvas](https://aws.amazon.com/jp/about-aws/whats-new/2023/10/amazon-sagemaker-canvas-content-information-extraction/)
  * [GCP CLoud Natural Language API](https://cloud.google.com/natural-language/docs/analyzing-sentiment?hl=ja)
    * [content moderation](https://cloud.google.com/natural-language/docs/classifying-text?hl=ja)
    * [analyzing sentiment](https://cloud.google.com/natural-language/docs/analyzing-sentiment?hl=ja)
* libraries
  * OpenCV
  * scikit-image
  * PyTorch

# usecase ideas

画像の特徴を教えてくれるお楽しみツール

* ユーザが分析したい画像をアップロードする
* サービスが画像の次の内容をユーザに表示する
  * キーカラー - 画像を特徴づけるキーカラー5～10色程度のHexCode表現
  * 言語化 - 画像にかかれている内容を言語化した数種類の単語のキーワードマップ表現
  * 感情 - 言語化結果をもとに、画像の表現内容がポジティブ・ネガティブどちらにどの程度寄るかを示すチャート
  * スタイル - 予め定義済(how?)の画像の作風・スタイルを示す単語のリストまたはHexChart表現
  * センシティブ

# implements ideas

どのように実装するか

* アップロード機能
  * streamlit, Figma
* 分析
  * Workload
    * CDK - S3, APIGateway, Lambda
  * キーカラー
    * OpenCVまたはscikit-image
  * 言語化
    * Rekognitionによるlabeling
  * 感情
    * GCP Natural Language API
  * スタイル
    * TBD, 多分OpenCV, Rekognition + animeface-character-datasetなどによるモデル作成が必要
  * センシティブ
    * Rekognition
* プレゼンテーション
  * streamlit, Figma
