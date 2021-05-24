/*

方法是:

1. 去 https://pretalx.com/orga/me 拿 token
2.  發 request 到 https://pretalx.com/api/events/coscup-2021/submissions?limit=300&offset=0&page=1&q=&state=, 設定 Header: Authorization: Token xxxxxxxxx
3. 留下裡面的 array, 拿去 json to csv, 下載後把 csv 要再存一次 UTF8 with BOM

reference: [submissions-api](https://docs.pretalx.org/api/resources/submissions.html)


執行這個腳本:
1. 到 Pretalx 網站，開 F12 ，貼上下面整串
2. 在 F12 打上: download_all_submissions('請貼上你的 token', '貼上活動 id (網址上應該可以辨別)')
3. 按下 Enter，等一陣子它會自己下載好

examples:
download_all_submissions('s5s5s5s5s55s5s5s55s5s5s5s55s5s', 'coscup-2021')

*/
const blob_download_with_bom = (content, fileName, contentType) => {
    const a = document.createElement("a");
    // add new Uint8Array([0xEF, 0xBB, 0xBF]) is for utf8-with-bom
    const file = new Blob([new Uint8Array([0xEF, 0xBB, 0xBF]), content], {type: contentType});
    a.href = URL.createObjectURL(file);
    a.download = fileName;
    a.click();
}

const download_all_submissions = (auth_token, event_id="coscup-2021") => {

  const myHeaders = new Headers();
  myHeaders.append("Accept", "application/json, text/javascript");
  myHeaders.append("Authorization", `Token ${auth_token}`);

  const requestOptions = {
    method: 'GET',
    headers: myHeaders,
    redirect: 'follow'
  };

  fetch(`https://pretalx.com/api/events/${event_id}/submissions?limit=300&offset=0&page=1&q=&state=`, requestOptions)
    .then(response => response.json())
    .then(({ results }) => {
        blob_download_with_bom(JSON.stringify(results), `${event_id}-submissions.json`, 'application/json;charset=utf-8');
    })
    .catch(error => console.log('error', error));
}

