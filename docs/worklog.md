# 作業日誌

- まずは、dockerの環境構築
    - wsl2と統合したdocker desktopをインストール
    - そうすれば普通にwsl側でdockerが動く
- grafanaはdocker hubに公式のイメージが上がってるので、それをrunするだけ
    - 初回はhubからダウンロードされる
    - port番号の指定だけすればOK
- 指定したポート番号にlocalhostでブラウザからアクセスすればgrafanaの画面が出てくる
    - この画面でdashboardの設定やdbの設定を行う
- influx dbについても同様にこうしきのdocker imageがあるのでそれを落としてrunすれば動く
    - 指定した番号にブラウザからアクセスすれば初期設定などをする画面になる
- 設定してもろもろやればgrafanaもinflux dbも単体では動く
    - 問題は両社の接続がうまくいかないこと
    - ともにwsl上で動いているのが原因っぽい
    - 同様の報告が上がっている
    - firewall関連なのかなあ？と思いつつ、確認してもよくわからない
- useを考えると、データのuploadはクラウドにして、各自がlocalのPCでアクセスできる方がうれしい
    - 最終的にはgrafanaもサーバ上で動かしてインターネットがあればどこでもテレメを見れる環境が理想だが、これはとりあえずいいや
    - ということで、influxdb cloudとローカルのgrafanaを接続させたい！というのが当面の目標となった
    - 同時に、ラズパイorESPでUARTを読み取ってcloud上のdbにupする、というのもやりたい
- 最終的には、Loraモジュールの刺さったESPorRaspiをネットにつなげて、逐次受け取ったデータをdbにupし、それを各自がgrafanaで閲覧する、というのがベスト
- influxdb cloudを試した
    - 基本的にはlocalhostと変わらない 30日でデータが消える仕様であればタダで利用可能
    - しかしながらgrafanaくんからアクセスが出来ない
    - influxの設定がおかしいのか、wsl上のgrafanaがアクセスを拒まれているのか
    - どっちなのかがいまいち自信がない
    - とにかくまいった
- grafana cloudもためした
    - 当然のようにinflux dbくんと接続されない
    - どうしてだよおお
    - 逆に、cloudとlocalのdbをつなげるのは？
    - ためすのがめんどいのであとで
- cloud同士で接続するとうまくいく
    - けっきょく横着してdockerで環境構築したのが設定がうまくいってないんだと思う
    - いずれちゃんと環境構築をしようね、というお話
### docker
- カーネル上で動作する
- カーネルを共有し、複数の仮想マシンが動いているように見せる
- カーネルはlinuxカーネルに限定　それによりハイパーバイザ型やホストマシン型仮想マシンと比較して軽量
- wsl2はlinuxカーネルで動作するのでdockerも動く
    - wsl1はシステムコールを翻訳してwindowsカーネルで動くからdocker非対応
- 一応decktopを使わないでwsl2上でdockerを構築することも可能らしい
    - 商用利用のときぐらいしかこういうケースはない
### plugin development
- react-flight-indicatorをreact18仕様にしてbuildする
- distをpluginのsrc/libs以下にcp
- plugin dirはtutorialに従って初期化する
- componentはcomponent/simplepanel.tsxに書き加える
- fieldtype=numberを指定すればクエリでもってきた値を自動的にいれてくれる
### server
- 各自のlocalでgrafanaを立ち上げて使わせるのは渋いので、ウェブサービスとしてデプロイしたい
- dockerが使える安価な、出来れば無料のレンタルサーバーを選定
- Google Cloudの無料枠をつかうことにした
- 自前でサーバーを組むのはセキュリティ関連でさすがに自信がないので、その辺をGUIでポチポチすれば設定できるのと、ドキュメントが公式も非公式も充実してたのが選定理由
### google cloud project
- 基本的にはインスタンスを作ってsshすれば普通のlinuxマシンとして扱える
- httpはサービスが走っていないとerror conection refusedを吐く
- https化したい
- 最初のlogin以外はそんなに動作も重くない（いい話
- やはりGrafanaの外部マウントの権限周りが沼
- sshをwslからできるようにしたいね
### 備忘録
- databaseはUSBシリアルデバイスとの通信が必須
- LoramoduleからのUSBシリアル信号を読み取ってdatabase形式に変換して保存する必要があるため
- となるとwsl上にdockerでinflux dbを立てるのはしんどい
    - wslではUSBデバイス非対応だから
- windows上でコードを実行し、そのコードがcloud上のinflux dbと接続されるという仕組みが必要
