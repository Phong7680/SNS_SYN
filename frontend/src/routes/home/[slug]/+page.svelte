<script>
    import { Avatar, Alert, Button, Textarea, Toolbar, ToolbarButton, Fileupload } from 'flowbite-svelte';
    import ImageOutline from 'flowbite-svelte-icons/ImageOutline.svelte';
    import Main from '$components/Main.svelte';
    
    // 画面遷移時に取得したデータ
    export let data; 

    // apiアクセスurl
    const url_post_image   = "http://127.0.0.1:5000/upload";
    const url_get_post_all = "http://127.0.0.1:5000/all_post";
    const url_add_post     = "http://127.0.0.1:5000/post";

    // 変数
    let new_post_content = "";     // 投稿文
    let new_post_img     = "null"; // 投稿画像
    let new_post_none    = false;  // 投稿文も投稿画像も無い状態で投稿されたときtrueになるフラグ
    let new_post_img_name = "";    // 投稿画像名

    // 画像ファイル入力の関数
    function set_image() {
        // idがpictureである要素のclickイベントを実行
        document.getElementById("picture").click();
    }

    // documentはクライアント側でのみ定義されているのでサーバー側で使えない
    // windowがobjectの状態であればdocumentを扱えるのでそれを用いて条件分岐する
    if (typeof window === 'object') {
        // 画像が選択されたときファイル名を取得する関数
        document.getElementById("picture").addEventListener("change", function(e){
            new_post_img_name = e.target.files.length ? e.target.files[0].name : "";
        });
    }

    // 投稿を送信する関数
    async function add_post() {
        // 投稿文が200文字を超えるとき投稿できない(投稿ボタンも押せないが一応)
        if (new_post_content.length > 200) return;

        // 入力フォームのデータを取得
        const file = document.getElementById("picture").files[0];
        const form_data = new FormData();
        form_data.set("picture", file);

        // 投稿画像の有無で条件分岐
        if (file) {
            // 画像を選択しているとき画像を送信する
            const response_img = await fetch(url_post_image, { method: "POST", body: form_data });
            let result = await response_img.json();
            new_post_img = result.picture;
            if (new_post_content.length == 0) {
                // 画像を選択しているかつ投稿文が無いとき投稿文をスペース1つにする
                new_post_content = " ";
            }
        } else {
            // 画像を選択していないとき画像を送信しない
            new_post_img = "null";          
            if (new_post_content.length == 0) {
                // 画像を選択していないかつ投稿文も無いとき投稿されない(投稿ボタンも押せないが一応)
                new_post_none = true;
                return;
            }
        }

        // 投稿内容と投稿画像を送信
        await fetch(
            url_add_post + "/" + new_post_content + "/" + new_post_img
        );

        // 投稿したら入力内容をクリア
        new_post_content = "";
        new_post_img = "null";
        new_post_none = false;

        // 投稿を取得する
        const response_post = await fetch(url_get_post_all);
        // 投稿リスト更新
        data.post_list = await response_post.json();
    }
</script>

<Main {... data}>
    <div id="post_input_grid">
        <Avatar src={data.account_picture} border class="justify-self-center"/>
        <!-- 投稿文入力部分 -->
        <div id="str_input">
            <Textarea placeholder="What is happening (200 words or less)" rows="4" name="message" bind:value={new_post_content}>
                <Toolbar  slot="footer" embedded>
                    <!-- 投稿ボタン -->
                    <div class="py-1">
                        {#if new_post_content.length > 200 || (new_post_content.length == 0 && new_post_img_name == "")}
                            <!-- 投稿文が200文字を超えるときと,投稿文も投稿画像も無いときボタンを押せなくする -->
                            <Button color="red" class="rounded-full" disabled>post</Button>
                        {:else}             
                            <Button color="red" class="rounded-full" on:click={add_post}>post</Button>
                        {/if}
                    </div>
                    <!-- 投稿画像選択部分 -->
                    <ToolbarButton on:click={set_image}>
                        <ImageOutline class="w-5 h-5" />
                    </ToolbarButton>
                    {new_post_img_name}
                    <!-- 投稿画像入力フォーム(非表示) -->
                    <form  method="POST" enctype="multipart/form-data" class="container_picture">
                        <input type="file" name="picture" id="picture" class="hidden"/>                       
                    </form>
                    {#if new_post_content.length > 200}
                        <!-- 投稿文が200文字を超えるとき警告を出す -->
                        <Alert color="red">投稿文は200文字以内にしてください</Alert>
                    {/if}
                </Toolbar>
            </Textarea>
        </div>
    </div>    
</Main>
  
<!-- 画面の装飾をする -->
<style>
    #post_input_grid {
        display: grid;
        grid-template:
            "user_icon   str_input" auto
            / 50px       1fr;
        padding-top: 10px;
        padding-bottom: 10px;
        border-bottom: solid 1px #eee;
    }
    #str_input {
        grid-area: str_input;
        min-width: 390px;
    }
</style>
  