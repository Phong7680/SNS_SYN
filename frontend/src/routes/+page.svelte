<script>
  let id ="";
  let password ="";
  let result = [];//ログインの結果
  async function login(){
      if(id=="" || password==""){
        alert("入力フォームに入力して下さい")
      }
      else{
        const response = await fetch(
          "http://127.0.0.1:5000/login/"
          +
          id
          +"/"+
          password
        )
        result = await response.json()
        console.log(result)
        if (result.result == "true") {
            window.location.href = "/home/" + id;
          }
        else if(result.result = "false"){
            alert("パスワードが違います");
          }
        }
    }

</script>

<main>
  <div class="login">
      <div class="login-triangle"></div>
      
      <h2 class="login-header">ログイン</h2>
    
      <form class="login-container">
        <p><input type="id" placeholder="アカウントID" bind:value={id}></p>
        <p><input type="password" placeholder="パスワード" bind:value={password}></p>
        <p><button on:click={login}>ログイン</button></p>
        <p><button onclick = "window.location.href = '/CreateAccount'" >新規登録</button></p>
      </form>
    </div>



    
    
</main>

<style>
  /* class=testとなっている箇所に適用されるスタイル */



.login {
width: 400px;
margin: 16px auto;
font-size: 16px;
}

/* Reset top and bottom margins from certain elements */
.login-header,
.login p {
margin-top: 0;
margin-bottom: 0;
}

/* The triangle form is achieved by a CSS hack */
.login-triangle {
width: 0;
margin-right: auto;
margin-left: auto;
border: 12px solid transparent;
border-bottom-color: rgb(255, 66, 66);
}

.login-header {
background: rgb(255, 66, 66);
padding: 20px;
font-size: 1.4em;
font-weight: normal;
text-align: center;
text-transform: uppercase;
color: #fff;
}

.login-container {
background: #ebebeb;
padding: 12px;
}

/* Every row inside .login-container is defined with p tags */
.login p {
padding: 12px;
}

.login input, button {
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

.login input[type="id"],
.login input[type="password"] {
background: #fff;
border-color: #bbb;
color: #555;
}

/* Text fields' focus effect */
.login input[type="id"]:focus,
.login input[type="password"]:focus {
border-color: #888;
}

.login button {
background: rgb(255, 66, 66);
border-color: transparent;
color: #fff;
cursor: pointer;
}
/* Buttons' focus effect */
.login button:hover{
background: rgb(146, 0, 0);
}



</style>
