// ページ遷移時に実行される
export const ssr = false; // ssrを無効にする
export async function load({ params }) {    
    // 特定ユーザーの投稿を取得する
    const response = await fetch("http://127.0.0.1:5000/post2/" + params.slug);
    const res_json = await response.json();

    return {
        account_id: params.slug,
        account_name: res_json.account_name,
        account_picture: res_json.account_picture,
        post_list: res_json.post_list,
    };
}