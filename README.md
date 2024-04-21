# ML-Agents環境導入用テンプレート
ML-Agentsの環境を導入するためのテンプレートです。

※UnityエディタはUnity Hubから個別でインストールしてください。

- ※ 2024/04 ML-Agents release21のみの対応です。
- ※ 2024/04 Windows + PowerShell環境のみの対応です。

## 使い方
1. このリポジトリをクローンしたディレクトリから、以下のコマンドを実行します。
```powershell
./init.ps1
```
デフォルトの環境構成でML-Agentsの環境が構築されます。※CPU版Pytorch

### (Windows + GPU環境) CUDA版 Pytorchを使う場合
コマンドの引数に`-cuda $ture`を追加します。
```powershell
./init.ps1 -cuda $true
```

# ディレクトリ構成
```
TODO: フォルダツリーを記述
```


