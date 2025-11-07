<script>//URLにリクエストパラメータ「?id=<user_id>」を追加してください(例)"/DeleteAccount?id=10"
    //パラメータ取得
    var params = (new URL(document.location)).searchParams;
    let id = params.get('id');
    
    let new_password = "";
    let check_password = "";


    async function change_password(){
        if(new_password==""||check_password==""){
            alert("入力フォームに入力してください")
        }
        else{
            if(new_password == check_password){
            await fetch(
            "http://localhost:5000/change_info/password/"
            +
            new_password
            )
            alert("パスワードを変更しました")
            window.location.href = "/mypage/" + id
            }
            else{
                alert("パスワードが異なります")
                new_password = ""
                check_password = ""
            }
        }


    }

</script>

<main>

    <div class="change_password">
        <p><a href="/mypage/{id}" class = "dli-arrow-left"></a></p>
        <div class="triangle"></div>
        <h2 class="header">パスワード変更</h2>
        <form class = "container">
            <p><input type="password" bind:value={new_password} placeholder="新しいパスワード"></p>
            <p><input type="password" bind:value={check_password} placeholder="確認のためもう一度入力してください"></p>
            <p><button on:click={change_password}>変更</button></p>

        </form>
    </div>
</main>

<style>

.change_password {
width: 400px;
margin: 16px auto;
font-size: 16px;
}

/* Reset top and bottom margins from certain elements */
.header,
.change_password p {
margin-top: 0;
margin-bottom: 0;
}

/* The triangle form is achieved by a CSS hack */
.triangle {
width: 0;
margin-right: auto;
margin-left: auto;
border: 12px solid transparent;
border-bottom-color: rgb(255, 66, 66);
}

.header {
background: rgb(255, 66, 66);
padding: 20px;
font-size: 1.4em;
font-weight: normal;
text-align: center;
text-transform: uppercase;
color: #fff;
}

.container {
background: #ebebeb;
padding: 12px 12px 0 12px;
}

/* Every row inside .login-container is defined with p tags */
p {
padding: 12px;
}

.change_password input, button {
box-sizing: border-box;
display: block;
width: 100%;
border-width: 1px;
border-style: solid;
padding: 16px;
outline: 0;
font-family: inherit;
font-size: 0.95em;
}

.change_password input[type="password"]{
background: #fff;
border-color: #bbb;
color: #555;
}

/* Text fields' focus effect */
.change_password input[type="password"]:focus{
border-color: #888;
}

.change_password button {
background: rgb(255, 66, 66);
border-color: transparent;
color: #fff;
cursor: pointer;
}
/* Buttons' focus effect */
.change_password button:hover{
background: rgb(146, 0, 0);
}

.dli-arrow-left {
  display: inline-block;
  vertical-align: middle;
  color: rgb(255, 66, 66);
  line-height: 1;
  position: relative;
  width: 1.5em;
  height: 0.5em;
  background: currentColor;
}

.dli-arrow-left::before {
  content: '';
  width: 1em;
  height: 1em;
  border: 0.3em solid currentColor;
  border-right: 0;
  border-bottom: 0;
  transform: rotate(-45deg);
  transform-origin: top left;
  position: absolute;
  top: 50%;
  left: -0.4em;
  box-sizing: border-box;
}

</style>