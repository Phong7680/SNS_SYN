<script>
  //新規登録画面
  let id = "";
  let password = "";
  let name = "";
  let accountPicture = "";
  let result
  async function createAccount() {
    if(id==""||password==""||name==""||accountPicture==""){
      alert("入力フォームに入力してください") 
    }
    else{
      // データを送信する。
      const file = document.getElementById("picture").files[0];
      const formData = new FormData();
      formData.set("picture", file);
      console.log(file);

      const response_upload = await fetch("http://127.0.0.1:5000/upload", { method: "POST", body: formData });
      result = await response_upload.json()
      accountPicture = result.picture
      const response = await fetch(
        "http://127.0.0.1:5000/signup/" +
          id +
          "/" +
          password +
          "/" +
          accountPicture +
          "/" +
          name
      );
      result = await response.json();
      console.log(result)
      if(result.result == "failure"){
        alert("このIDまたは名前は既に使われています")
        id = ""; // 入力内容クリア
        password = ""; // 入力内容クリア
        name = ""; // 入力内容クリア
        }
      
      else{
        window.location.href = ('/' );

      }
    }

  }

</script>

<main>
  
<div class="create_account">
  <p><a href="/" class = "dli-arrow-left"></a></p>
  <div class="triangle"></div>
  
  <h2 class="header">新規登録</h2>

  <form class="container">
    <p><input type="id" name="userid" bind:value={id} id="uid" placeholder="アカウントID"/></p>
    <p><input type="password" name="pass" id="pass" bind:value={password} placeholder="パスワード"/></p>
    <p><input type="text" name="name" id="name" bind:value={name} placeholder="アカウント名"/></p>
  </form>
  <form  method="POST" enctype="multipart/form-data" class="container_picture">
    <div class = "text"><p class="text_box">アカウント画像</p></div>
    <p><input type="file" name="picture" id = "picture" bind:value={accountPicture}></p>
    <p><button type="button"  on:click = {createAccount}>新規登録</button></p>
  </form>
</div>
</main>

<style>
  .create_account {
width: 400px;
margin: 16px auto;
font-size: 16px;
}

/* Reset top and bottom margins from certain elements */
.header,
.create_account p {
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
.container_picture {
background: #ebebeb;
padding: 0 12px 12px 12px;
}

/* Every row inside .login-container is defined with p tags */
p {
padding: 0 12px 24px 12px;
}

.text{
  text-align: center;
  padding: 0 12px;
}

.text_box{
  padding: 0 16px;
  box-sizing: border-box;
display: block;
width: 100%;
border-width: 1px;
border-style: solid;
outline: 0;
font-family: inherit;
font-size: 0.95em;
background: rgb(255, 66, 66);
border-color: transparent;
color: #fff;
margin-top: 0;
margin-bottom: 0;
}

.create_account input, button {
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

.create_account input[type="id"],
.create_account input[type="password"],
.create_account input[type="text"]{
background: #fff;
border-color: #bbb;
color: #555;
}
.create_account input[type="file"]{
  background: rgb(255, 66, 66);
border-color: transparent;
color: #fff;
cursor: pointer;
}

/* Text fields' focus effect */
.create_account input[type="id"]:focus,
.create_account input[type="password"]:focus,
.create_account input[type="text"]:focus {
border-color: #888;
}

.create_account button {
background: rgb(255, 66, 66);
border-color: transparent;
color: #fff;
cursor: pointer;
}
/* Buttons' focus effect */
.create_account button:hover{
background: rgb(146, 0, 0);
}

.create_account input[type="file"]:hover{
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

