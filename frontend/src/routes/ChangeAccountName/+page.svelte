<script>//URLにリクエストパラメータ「?id=<user_id>」を追加してください(例)"/DeleteAccount?id=10"
    //パラメータ取得
    var params = (new URL(document.location)).searchParams;
    let id = params.get('id');

    let new_name = "";
    async function change_name(){
        if(new_name == ""){
           alert("入力フォームに入力してください") 
        }
        else{
            await fetch(
                "http://localhost:5000/change_info/user_name/"+
                new_name
                )
            alert("アカウント名を変更しました")
            window.location.href = "/mypage/" + id
        }
    }

</script>

<main>
    <div class = "change_name">
        <p><a href="/mypage/{id}" class = "dli-arrow-left"></a></p>
        <div class = "triangle"></div>
        <h2 class = "header">アカウント名変更</h2>
        <form class="container">
            <p><input type="text" bind:value={new_name} placeholder="新しいアカウント名"></p>
            <p><button on:click={change_name}>変更</button></p>
        </form>
    </div>
</main>

<style>
.change_name{
width: 400px;
margin: 16px auto;
font-size: 16px;
}

.triangle {
width: 0;
margin-right: auto;
margin-left: auto;
border: 12px solid transparent;
border-bottom-color: rgb(255, 66, 66);
}

.header,
.change_name p {
margin-top: 0;
margin-bottom: 0;
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

p {
padding: 12px;
}

.change_name  input, button {
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

.change_name  input[type="text"] {
    background: #fff;
border-color: #bbb;
color: #555;
}



.change_name button {
background: rgb(255, 66, 66);
border-color: transparent;
color: #fff;
cursor: pointer;
}
/* Buttons' focus effect */
.change_name button:hover{
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