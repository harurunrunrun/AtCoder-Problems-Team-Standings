# AtCoder-Problems-Team-Standings (alpha ver.)
This script create a team standings on AtCoder Problems.(alpha ver. lang. is only japanese)

## 仕様上削除されている機能一覧
- Auto Refresh (beta ver.で復活予定)
- Pin me

## 導入方法
- (方法1 推奨) greasy forkに同様のスクリプトを投稿しているので、そこからダウンロードする。(リンク:)
- (方法2 非推奨) alpha フォルダ内にあるスクリプトをTampermonkey(他は未確認)などに保存して使う

## 使い方 
1. {[user_id]:[team名],[user_id]:[team名].....}というユーザとチーム名の対応が書かれたファイル(形式はjsonやtxtなど)を作成する。
2. 画面上部にあるファイルを選択から上記のファイルを読み込む
3. リロードすると、チームスコアが表示されます。
4. コンテスト終了後、上部にresultというリンクが表れるので、そこを押すと get_standings.py 用のjsonファイルがダウンロードできます。

## 注意点
1. このスクリプトは、WEBの表面的な情報しか収集していない(APIを使用しているわけではない)ので、ペナ数の表示は各チームのユーザの合計となります。
2. script内にあるget_standings.pyはAtCoder Problems のAPIを使用し、より正確な順位表を出力しますが、負荷軽減の観点から、代表者のみが行うようにしてください。
3. alpha ver.なので本家の順位表に比べてかなり見辛いです。ご了承ください。

## 確認されているバグ一覧
- ロードしないと表示されない
- 稀に、スコアが0になる
- 他のProblems内のページに行っても残っている => リロードすると治ります
- save時にtrがずれる => 現在はリロードすることで回避
