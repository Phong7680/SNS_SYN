// ページ遷移時に実行される
export async function load({ params }) {
    let account_id = params.slug;

    //  アカウントIDからアカウント情報を取得する
    const response_account = await fetch("http://127.0.0.1:5000/account_info/" + account_id);
    const account_info = await response_account.json();

    // 全ての投稿を取得する
    const response_post = await fetch("http://127.0.0.1:5000/all_post");
    const post_list = await response_post.json();

    return {
        account_id: account_id,
        account_name: account_info.account_name,
        account_picture: account_info.account_picture,
        post_list: post_list,
    };
}