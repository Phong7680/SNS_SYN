<script>
    import { Avatar } from 'flowbite-svelte';
    import HeartOutline from 'flowbite-svelte-icons/HeartOutline.svelte'
    export let account_id, account_name, account_picture, post_list;
</script>

<!-- 画面右下のボタン -->
<div id="mypage_button">
    <button onclick="location.href='/mypage/{account_id}'">
        <Avatar src={account_picture} size="md" border class="ring-red-400 dark:ring-red-300"/>
    </button>
</div>

<div class="grid" style="grid-template-columns: minmax(0, 700px); justify-content: center;">
    <div>
        <slot></slot>
    </div>
    <!-- 投稿を縦に表示させる -->   
    <div id="post_layout">
        <!-- 繰り返し処理 post_listの各行をpostとして取り出し -->
        {#each post_list as post}
            <button class="hover:bg-gray-100" onclick="location.href='/post/{post.post_id}-{account_id}'">
                <div class="post">
                    <!--
                    全てのユーザーの投稿を表示する場合と特定のユーザーの投稿を表示する場合の2パターンある
                    全てのユーザーの投稿を表示する場合,投稿データ1つ1つに投稿者の情報が載っている
                    特定のユーザーの投稿を表示する場合,投稿データの中に投稿者の情報は載せていない
                    -->
                    <!-- 投稿データに投稿者名の情報があるかで条件分岐 -->
                    {#if "account_name" in post}
                        <Avatar src={post.account_picture} border />             <!-- ユーザー画像 -->          
                        <div class="user_name">{post.account_name}</div>         <!-- ユーザー名 -->
                    {:else}
                        <Avatar class="user_img" src={account_picture} border /> <!-- ユーザー画像 -->
                        <div class="user_name">{account_name}</div>              <!-- ユーザー名 -->
                    {/if}
                    <!-- 投稿文 -->
                    <div class="post_content">{post.post_content}</div>
                    <!-- 投稿画像があるかないか判定 -->
                    {#if post.post_picture != "null"}
                        <!-- 投稿画像 -->                  
                        <img class="post_picture" src={post.post_picture} alt="post img"/>  
                    {/if}
                    <!-- いいね -->
                    <div class="post_like">
                        <svelte:component this="{HeartOutline}" /> <!-- ハートアイコン -->
                        <div>{post.like_number}</div>              <!-- いいね数 -->
                    </div>
                </div>
            </button>
        {/each}
    </div>
    <!-- 画面右下のボタンで一番下の投稿が隠れるのを防ぐための空白 -->
    <div style="height: 70px;"></div>
</div>
    
<!-- 画面の装飾をする -->
<style>
    #mypage_button {
        position: fixed;
        width: 60px;
        height: 60px;
        bottom: 0;
        right: 0;
        opacity: 1;
    }
    #post_layout {
        display: grid; /* グリッドレイアウト */
        grid-template-columns: 1fr;
    }
    .post {
        display: grid;
        grid-template:
            "user_img user_name   " 45px
            "...      post_content" auto
            "...      post_picture" auto
            "...      post_like   " 30px
            / 45px     1fr;
        padding-top: 5px;
        padding-bottom: 5px;
        padding-left: 5px;
        border-top: solid 1px #eee;
        background: transparent;
        grid-row-gap: 10px;
        grid-column-gap: 10px;
    }
    .user_name {
        grid-area: user_name;
        font-weight: bold;
        justify-self: left;
        align-self: center;
    }
    .post_content {
        grid-area: post_content;
        min-height: 0px;
        text-align: left;
        word-break: break-all;
        justify-self: left;
    }
    .post_picture {
        grid-area: post_picture;
        max-width: 200px;
        justify-self: center;
        border: 1px solid #eee;
    }
    .post_like {
        grid-area: post_like;
        display: grid;
        grid-template:
            "hert_icon like_num" auto
            / 30px     auto;       
        justify-self: left;
        align-items: center;
    }
</style>
    