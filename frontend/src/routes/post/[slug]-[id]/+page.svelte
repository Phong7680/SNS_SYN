<script>
    import { Alert, Avatar, Button, Textarea, Toolbar} from 'flowbite-svelte';
    import ArrowLeftOutline from 'flowbite-svelte-icons/ArrowLeftOutline.svelte';
    import HeartOutline from 'flowbite-svelte-icons/HeartOutline.svelte'

    // 画面遷移時に取得したデータ
    export let data;

    // apiアクセスurl
    const url_add_comment = "http://127.0.0.1:5000/comment";
    const url_add_like = "http://127.0.0.1:5000/like";
    const url_get_post = "http://127.0.0.1:5000/post1"

    // 変数
    let comment_list = data.comment_list;  // この投稿についたコメントのリスト
    let post_like_info = data.like;        // この投稿にいいねしたユーザーのリスト 
    let post_like = post_like_info.length; // 投稿についているいいねの数
    let new_comment = "";                  // 新しいコメント

    // コメントを投稿する関数
    async function add_comment(){
        // コメント送信
        await fetch (
            url_add_comment +
            "/" +
            data.post_id + 
            "/" + 
            new_comment
        );
        //同じ投稿を何度もしないようにテキストボックスの中身を空にする
        new_comment = "";
        // コメント取得
        const response = await fetch (
            url_add_comment +
            "/" +
            data.post_id
        );
        // コメントリストを更新
        comment_list = await response.json();
    }

    // いいねする関数
    async function add_like() {
        await fetch(
            url_add_like + "/" + data.post_id
        );
        // いいねの数を更新
        const response = await fetch(
            url_get_post  + "/" + data.post_id
        );
        const res = await response.json();
        post_like_info = res.like;
        post_like = post_like_info.length;
    }
</script> 

<main class="grid" style="grid-template-columns: minmax(0, 700px); justify-content: center;">
    <div id="post_grid">
        <!-- 前のページに戻るボタン -->
        <button id="back_arrow" class="hover:bg-gray-300" onclick="location.href='/home/{data.account_id}'">
            <svelte:component this="{ArrowLeftOutline}" style="margin: 0 auto"/>
        </button>
        <!-- 投稿者画像 -->
        <Avatar src={data.post_account_picture} border size="lg" class="place-self-center"/>
        <!-- 投稿者の名前 -->
        <div id="user_name">{data.post_account_name}</div>
        <!-- 投稿文 -->
        <div id="post_content">{data.post_content}</div>
        <!-- 投稿画像があるかないか判定 -->
        {#if data.post_picture != "null"}
            <!-- 投稿画像 -->                  
            <img id="post_picture" src={data.post_picture} alt="post img"/>  
        {/if}
        <!-- いいね -->
        <div id="post_like">
            <button on:click={add_like}>
                <!-- ハートアイコン -->
                <svelte:component this="{HeartOutline}" />
            </button>
            <!-- いいね数 -->
            <div>{post_like}</div>
        </div>
    </div>
    <div id="post_input_grid">
        <Avatar src={data.account_picture} border/>
        <!-- コメント文入力部分 -->
        <div id="str_input">
            <Textarea placeholder="comment (200 words or less)" rows="4" name="message" bind:value={new_comment}>
                <Toolbar slot="footer" embedded class="justify-between">
                    <!-- コメントボタン -->
                    <div id="post_button" style="grid-column: 2; grid-row: 1;">
                        {#if new_comment.length > 200 || (new_comment.length == 0 && new_comment == "")}
                            <!-- コメントが200文字を超えるときと,コメントが無いときボタンを押せなくする -->
                            <Button color="red" class="rounded-full" disabled>comment</Button>
                        {:else}             
                            <Button color="red" class="rounded-full" on:click={add_comment}>comment</Button>
                        {/if}
                    </div>
                    {#if new_comment.length > 200}
                        <!-- コメント文が200文字を超えるとき警告を出す -->
                        <Alert color="red">コメントは200文字以内にしてください</Alert>
                    {/if}
                </Toolbar>
            </Textarea>
        </div>
    </div> 
    <div>  
        <div id="post_layout">
            <!-- 繰り返し処理 comment_listの各行をdataとして取り出し -->
            {#each comment_list as comment}
                <!-- dataに含まれる要素を取り出して表示 -->
                    <div class="comment">
                        <Avatar src={comment.account_picture} border />              <!-- コメント者画像 -->
                        <div class="comment_user_name">{comment.account_name}</div>  <!-- コメント者名 -->
                        <div class="comment_content">{comment.comment_content}</div> <!-- コメント文 -->
                    </div>
            {/each}
        </div>
    </div>   
</main>

<!-- 画面の装飾をする -->
<style>
    #post_grid {
        display: grid;
        grid-template:
            "back_arrow   back_arrow  " 40px
            "user_icon    user_name   " 100px
            "post_content post_content" auto
            "post_picture post_picture" auto
            "post_like    ...         " auto
            / 100px        1fr;
        padding: 10px;
        border-bottom: solid 1px #eee;
    }
    #back_arrow {
        grid-area: back_arrow;
        width: 40px;
        justify-self: first baseline;
        border-radius: 50%;
    }
    #user_name {
        grid-area: user_name;
        font-weight: bold;
        font-size: 1.5rem;
        line-height: 2rem;
        justify-self: left;
        align-self: center;
    } 
    #post_content{
        grid-area: post_content;
        word-break: break-word;
        padding-left: 40px;
    }
    #post_picture {
        grid-area: post_picture;
        max-width: 200px;
        justify-self: center;
        border: 1px solid #eee;
    }
    #post_like {
        grid-area: post_like;
        display: grid;
        grid-template:
            "hert_icon like_num" auto
            / 30px     auto;       
        justify-self: left;
        align-items: center;
        padding-left: 40px;
    }
    #post_layout {
        display: grid;
        grid-template-columns: 1fr;
    }
    #post_input_grid {
        display: grid;
        grid-template:
            "user_icon   str_input" auto
            "...         button   " 45px
            / 50px       1fr;
        padding-top: 10px;
        border-bottom: solid 1px #eee;
    }
    #str_input {
        grid-area: str_input;
        min-width: 390px;
    }
    #post_button {
        grid-area: button;
        justify-self: last baseline;
        align-self: center;
    }
    .comment {
        display: grid;
        grid-template:
            "user_img comment_user_name" 45px
            "...      comment_content  " auto
            / 45px     1fr;
        padding-top: 5px;
        padding-bottom: 5px;
        padding-left: 5px;
        border-top: solid 1px #eee;
        background: transparent;
        grid-row-gap: 10px;
        grid-column-gap: 10px;
    }
    .comment_user_name {
        grid-area: comment_user_name;
        font-weight: bold;
        justify-self: left;
        align-self: center;
    }
    .comment_content {
        grid-area: comment_content;
        min-height: 0px;
        word-break: break-word;
        justify-self: left;
    }
</style>