// ページ遷移時に実行される
export async function load({ params }) {    
    let post_id = params.slug;
    let account_id = params.id;

    // ユーザー情報を取得する
    const response_user = await fetch("http://127.0.0.1:5000/account_info/" + account_id);
    let user_info = await response_user.json();

    // 特定の投稿の情報を取得する
    const response_post = await fetch("http://127.0.0.1:5000/post1/" + post_id);
    let data = await response_post.json();    

    return {
        account_id: account_id,
        account_name: user_info.account_name,
        account_picture: user_info.account_picture,

        post_account_name: data.post.account_name,
        post_account_picture: data.post.account_picture,
        post_id: post_id,
        post_content: data.post.post_content,
        post_picture: data.post.post_picture,
        
        comment_list: data.comment,

        like: data.like,
    };
}