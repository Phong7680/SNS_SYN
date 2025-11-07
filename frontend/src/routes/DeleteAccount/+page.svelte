

<script>//URLにリクエストパラメータ「?id=<user_id>」を追加してください(例)"/DeleteAccount?id=10"
    //パラメータ取得
    var params = (new URL(document.location)).searchParams;
    let id = params.get('id');
    async function delete_account(){
        const response = await fetch(
            "http://127.0.0.1:5000/delete_account"
        )

        alert("アカウントを削除しました")
        window.location.href = '/';
    }
    function back(){
        window.location.href = ("/mypage/" + id)
    }

</script>

<main>
    <div class = "delete_account">
      <div class="triangle"></div>
      <h2 class="header">本当にアカウントを削除しますか？</h2>
      <form class = "container">
        <p><button on:click={delete_account} >はい</button></p>
        <p><button on:click={back}>いいえ</button></p>
      </form>
    </div>
</main>


<style>
  .delete_account {
width: 400px;
margin: 16px auto;
font-size: 16px;
}

/* Reset top and bottom margins from certain elements */
.header,
.delete_account p {
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

.delete_account  button {
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



.delete_account button {
background: rgb(255, 66, 66);
border-color: transparent;
color: #fff;
cursor: pointer;
}
/* Buttons' focus effect */
.delete_account button:hover{
background: rgb(146, 0, 0);
}


</style>

