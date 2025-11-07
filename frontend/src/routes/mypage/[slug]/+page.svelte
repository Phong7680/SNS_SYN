<script>
    import { Avatar, Button, Dropdown, DropdownItem } from 'flowbite-svelte';
    import { page } from '$app/stores';
    import ArrowLeftOutline from 'flowbite-svelte-icons/ArrowLeftOutline.svelte';
    import Main from '$components/Main.svelte';
    
    // 画面遷移時に取得したデータ
    export let data;

    // このページのパス
    $: activeUrl = $page.url.pathname;

    // ログアウトする関数
    async function logout() {
        await fetch("http://127.0.0.1:5000/logout");
    }
</script>

<Main {... data}>
    <div id="mypage_top_grid">
        <!-- 前のページに戻るボタン -->
        <button id="back_arrow" class="hover:bg-gray-300" onclick="location.href='/home/{data.account_id}'">
            <svelte:component this="{ArrowLeftOutline}" style="margin: 0 auto"/>
        </button>
        <!-- アカウントのアイコン表示 -->
        <Avatar src={data.account_picture} border size="lg" class="place-self-center"/>
        <!-- アカウント設定のボタン -->
        <Button outline color="red" class="w-32 h-10 rounded-full m-3 p-1 justify-self-end self-end">setting</Button>
        <Dropdown {activeUrl}>
            <DropdownItem href="/ChangeAccountName?id={data.account_id}">名前変更</DropdownItem>
            <DropdownItem href="/ChangeAccountPicture?id={data.account_id}">アカウント画像変更</DropdownItem>
            <DropdownItem href="/ChangePassword?id={data.account_id}">パスワード変更</DropdownItem>
            <DropdownItem href="/DeleteAccount?id={data.account_id}">削除</DropdownItem>
            <DropdownItem href="/" on:click={logout}>ログアウト</DropdownItem>
        </Dropdown>
        <!-- アカウント名表示 -->
        <div id="user_name">{data.account_name}</div>
    </div>    
</Main>

<!-- 画面の装飾をする -->
<style>
    #mypage_top_grid {
        display: grid;
        grid-template:
            "back_arrow back_arrow    " 40px
            "user_icon  setting_button" 100px
            "user_name  ...           " 45px
            / 100px      1fr;
        grid-auto-flow: column;
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
        justify-self: center;
    }
</style>