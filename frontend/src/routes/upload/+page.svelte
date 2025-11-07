<script>
    let post_id=1;// 投稿ID
    let post_content = "投稿内容テキスト"; // 投稿内容
    let post_picture=// 投稿写真ファイル名
    "https://digitor.jp/textbook/wp-content/uploads/2022/10/%E3%80%90HTML_CSS%E3%80%91%E8%A6%81%E7%B4%A0%E3%82%92%E3%80%8C%E6%A8%AA%E4%B8%A6%E3%81%B2%E3%82%99%E3%80%8D%E3%81%AB%E3%81%99%E3%82%8B%E6%96%B9%E6%B3%95%EF%BC%88%E5%88%9D%E5%BF%83%E8%80%85%E5%90%91%E3%81%91%EF%BC%89.jpg";
    let post_comment = [{Comment_id : 1 , Post_id : 1, Comment_content : "テキスト", Account_name : "名前"},{Comment_id : 2,Post_id : 2,Comment_conten:"テキスト２", Account_name : "名前２"}]; // 投稿についているコメントの情報
    let new_comment;//　新しく投稿につけるコメント
    let post_like = 100 ; //いいね
    let user_id=1; // ユーザID
    let account_picture= //プロフィール写真ファイル名
    "https://thenounproject.com/api/private/icons/3069450/edit/?backgroundShape=SQUARE&backgroundShapeColor=%23000000&backgroundShapeOpacity=0&exportSize=752&flipX=false&flipY=false&foregroundColor=%23000000&foregroundOpacity=1&imageFormat=png&rotation=0";
    let account_name="名前"// 表示する名前

    //テスト用にコメントアウト
    //const commentDB_response = fetch("http://localhost:5000/commentDB");
    //post_comment = commentDB_response.json();

    async function comment(){
        new_comment = document.getElementById("text").value;
        const response = await fetch(
            "http://localhost:5000/comment/"
            +
            post_id
            +
            "/"
            +
            new_comment
        );
        new_comment = "";//同じ投稿を何度もしないようにテキストボックスの中身を空にする
    }

    async function like(){
        const response = await fetch(
            "http://localhost:5000/like/" + {post_id}
        );
        //いいね数を更新
        post_like = await fetch(
            "http://localhost:5000/likeDB"
        )

    }
</script>

<main>
    <div class="container">
        <form action="http://127.0.0.1:5000/upload" method="POST" enctype="multipart/form-data">
            <input type="file" name="picture">
            <input type="submit" value="アップロード">
        </form>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js" integrity="sha384-geWF76RCwLtnZ8qwWowPQNguL3RmwHVBC9FhGdlKrxdiJJigb/j/68SIy3Te4Bkz" crossorigin="anonymous"></script>
    </div>
</main>

<style>
/*アカウントの名前、画像全体用*/
.account_information{
    padding:0% 5%;
}

.account_name {
    color: dodgerblue;
    font: message-box;
}

.account_picture{
    height: 100px;
    width: 100px;
}

/*投稿全体用*/
.post{
    padding: 0% 20%;
}

.post_content{
    color: black;
}

.post_picture{
    padding: 0 5%;
    width:80%; 
}

.post_like{
    color: hotpink;
}

.post_comment{
    padding: 5% 0;
}

.comment_box{
    display: inline-block;
    width: 100%;
    padding: 10px;
    border: 1px solid #999;
    box-sizing: border-box;
    background: #f2f2f2;
    margin: 0.5em 0;
    line-height: 1.5;
    height: 6em;
}



</style>