# 設計

-----------------------------------------------------
# システムの概要説明
 Twitterのような投稿を行い、その投稿にコメントをすることで情報発信、情報収集やいいねやコメントでコミュニケーションを取ること また、日常の思い出を写真や言葉で共有することを目的とする。

- 機能
 ・アカウント(ID、名前、パスワード、アカウント画像)の新規登録、IDまたは名前が被ると登録できない

 ・ログイン（IDとパスワード）、パスワードを間違えると警告でやり直し

 ・投稿（画像(１枚のみ)、文字列(200文字まで)）、画像も文字列も何もないと投稿できない

 ・投稿へのコメント（文字列だけ(200文字まで)）、0文字は投稿できない

 ・いいね（１投稿につき一人一回）

 ・アカウント情報（名前、パスワード、アカウント画像）の変更

 ・アカウントの削除（削除したアカウントに関する投稿、コメント、いいねは削除される）




-----------------------------------------------------

# 画面構成


- 新規登録画面
 アカウント名, 写真, ID, パスワードを入力して登録する。

- ログイン画面
 IDとパスワードを入力してログインする。

- メニュー画面
 投稿画面と投稿内容が表示される。
 投稿内容をクリックするとその投稿とコメントが表示される。
 マイページ画面に遷移できる。

- 投稿画面
 投稿, コメント、いいねを表示する画面
 投稿にいいねとコメントをつけれる。

- マイページ画面
 ユーザー削除, アカウント名, 写真, パスワード変更画面への遷移。
 自分の投稿のみ表示。

- アカウント削除画面
 アカウントの削除。
 「はい」で削除、「いいえ」でマイページに戻る

- アカウント名変更画面
 アカウント名の変更。
 新しい名前を入力して変更

- アカウント写真変更画面
 写真の変更。
 新しい画像を入力して変更

- アカウントパスワード変更画面
 パスワードの変更。
 新しいパスワードを2回入力して同じであれば変更


-----------------------------------------------------

# API設計

FrontendとBackendでやり取りするデータの定義
- 新規登録情報
```
{
    user_id: "user01",                  // ユーザID
    password: "abcd1234"               // パースワード
    account_picture: "data:image/.JPEG;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAA"       //　プロフィール写真ファイルのバイナリファイルを文字列にしたもの
    account_name: "Alex"                // 表示する名前
}
```

- ログイン情報
```
{
    user_id: "user01",   // ユーザID
    name: "John"        // 表示する名前
}
```

- ログアウト情報
```
{
    user_id: "user01",   // ユーザID
}
```

- 投稿内容情報
```
{
    post_id : "1"                        // 投稿ID
    post_content: "今日もいい天気"        // 投稿内容
    post_picture: "data:image/.JPEG;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAA"       //　投稿画像ファイルのバイナリファイルを文字列にしたもの
    user_id: "user01",                   // ユーザID
    account_picture: "data:image/.JPEG;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAA"       //　プロフィール写真ファイルのバイナリファイルを文字列にしたもの
    account_name: "Alex"                 // 表示する名前
}
```

- 特定のユーザーの情報
```
{
    user_id: "user01",                  // ユーザID
    account_picture: "data:image/.JPEG;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAA"       //　プロフィール写真ファイルのバイナリファイルを文字列にしたもの
    account_name: "Alex"                // 表示する名前
}
```

- １つの投稿内容情報
```
{
    post:{
        "account_name": "phong",                // 投稿者
        "account_picture": "data:image/.JPEG;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAA"       //　プロフィール写真ファイルのバイナリファイルを文字列にしたもの
        "post_content": "Test!!!!",             // 投稿内容
        "post_id": 1,                           // 投稿ID
        "post_picture": "data:image/.JPEG;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAA"       //　投稿画像ファイルのバイナリファイルを文字列にしたもの
    },
    comment: [
        {
            "account_name": "Phong",            // コメント者
            "account_picture": "data:image/.JPEG;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAA"       //　プロフィール写真ファイルのバイナリファイルを文字列にしたもの
            "comment_content": "Comment Test!", // コメント内容
            "comment_id": 3                     // コメントID
        },
    ],
    like: [
        {
            "account_name": Alex                // いいね者
        }
    ]
}
```

- 全ユーザーの投稿内容情報
```
{
    temp: [
        {
            "account_name": "phong",                // 投稿者
            "account_picture": "data:image/.JPEG;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAA"       //　プロフィール写真ファイルのバイナリファイルを文字列にしたもの
            "post_content": "Test!!!!",             // 投稿内容
            "post_id": 1,                           // 投稿ID
            "post_picture": "data:image/.JPEG;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAA"       //　投稿画像ファイルのバイナリファイルを文字列にしたもの
            "like_number": 100,
        }
    ],
}
```

- 特定のユーザーの情報とそのユーザーの投稿内容情報
```
{
    account_picture: "data:image/.JPEG;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAA"       //　プロフィール写真ファイルのバイナリファイルを文字列にしたもの
    account_name: "Alex"                // 表示する名前
    post_list: [
        {
            "post_content": "Test!!!!",             // 投稿内容
            "post_id": 1,                           // 投稿ID
            "post_picture": "data:image/.JPEG;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAA"       //　投稿画像ファイルのバイナリファイルを文字列にしたもの
            "like_number": 100,
        }
    ],
}
```

- コメント情報
```
{
    comment_id: "1"                      // コメントID
    post_id: "3"                         // 投稿ID
    comment_content: "いい写真だね！"     // コメント内容
    user_id: "user01",                   // ユーザID
    account_picture: "data:image/.JPEG;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAA"       //　プロフィール写真ファイルのバイナリファイルを文字列にしたもの
    account_name: "Linda"                // 表示する名前  
}
```

- いいね情報
```
{
    post_iD: "3"                         // 投稿ID
    account_name: "Linda"                // 表示する名前
}
```

- アカウント名変更
```
{
    new_name: "Kobayashi"                // 新しい名前
}
```

- パスワード名変更
```
{
    new_pass: "1234abcd"                     // パースワード
}
```

- プロフィール写真変更
```
{
    new_account_picture: "data:image/.JPEG;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAA"       //　プロフィール写真ファイルのバイナリファイルを文字列にしたもの
}
```



# Backendでの関数呼び出し

- 新規登録
```
{
    http://localhost:5000/signup/<user_id>/<password>/<account_picture>/<user_name>
}
```
- ログイン
```
{
    http://localhost:5000/login/<user_id>/<password>
}
```
- ログアウト
```
{
    http://localhost:5000/logout
}
```
- 投稿
```
{
    http://localhost:5000/post/<content>/<post_picture>

}
```
- 特定のユーザーの情報を取得
```
{
    http://127.0.0.1:5000/account_info/<user_id>
}
```
- すべての投稿情報を取得
```
{
    http://localhost:5000/all_post
}
```
-   特定のユーザーの投稿情報を取得
```
{
    "http://127.0.0.1:5000/post2/<user_id>
}
```
- １つの投稿情報を取得
```
{
    http://localhost:5000/post1/<post_id>
}
```
- コメント
```
{
    http://localhost:5000/comment/<post_id>/<content>
}
```
- いいね
```
{
    http://localhost:5000/like_data
}
```
- 画像アップロード
```
{
    http://localhost:5000/upload
}
```
- パースワード変更
```
{
    http://localhost:5000/change_info/password/<new_pass>
}
```
- ユーザ名変更
```
{
    http://localhost:5000/change_info/user-name/<new_name>
}
```
- プロフィール写真変更
```
{
    http://localhost:5000/change_profile_picture/<profile_picture>
}
```
- ユーザ削除
```
{
    http://localhost:5000/<delete_account>
}
```
-----------------------------------------------------
