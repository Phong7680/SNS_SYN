<script>//URLにリクエストパラメータ「?id=<user_id>」を追加してください(例)"/DeleteAccount?id=10"
    //パラメータ取得
    var params = (new URL(document.location)).searchParams;
    let id = params.get('id');

    let result = [];
    let new_picture = "";
    async function change_picture(){
      if(new_picture==""){
        alert("画像を選択してください")
      }
      else{
        const file = document.getElementById("picture").files[0];
        const formData = new FormData();
        formData.set("picture", file);
        console.log(file);
        const response = await fetch("http://127.0.0.1:5000/upload", { method: "POST", body: formData });
        result = await response.json()
        new_picture = result.picture
        console.log( new_picture);8/
        await fetch(
            "http://127.0.0.1:5000/change_profile_picture/none",{method:"GET"}
            )

            alert("変更が完了しました");
            window.location.href = "/mypage/" + id
        
      }
    }

</script>

<main>

    <div class="change_picture">
        <p><a href="/mypage/{id}" class = "dli-arrow-left"></a></p>
        <div class="triangle"></div>
        
        <h2 class="header">アカウント画像変更</h2>
      
        <form enctype="multipart/form-data" class = "container">
          <div class = "text"><p class="text_box">アカウント画像</p></div>
            <p><input type="file" name="picture" accept="image/*" id="picture" bind:value={new_picture}></p>
            <p><button  on:click = {change_picture}>変更</button></p>
        </form>

    </div>
</main>

<style>
  .change_picture {
width: 400px;
margin: 16px auto;
font-size: 16px;
}

/* Reset top and bottom margins from certain elements */
.header,
.change_picture p {
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
padding: 0 12px 24px 12px;
}

.change_picture input, button {
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


.change_picture input[type="file"]{
  background: rgb(255, 66, 66);
border-color: transparent;
color: #fff;
cursor: pointer;
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

.change_picture button {
background: rgb(255, 66, 66);
border-color: transparent;
color: #fff;
cursor: pointer;
}
/* Buttons' focus effect */
.change_picture button:hover{
background: rgb(146, 0, 0);
}


.change_picture input:hover{
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