const operators = [""]
// const redirectUrl = 'https://api.ttvod.lol/gql'
const redirectUrl = 'https://ri8lgur5n4.execute-api.us-west-2.amazonaws.com/'

function onVodListBeforeRequest(details) {
  const dec = new TextDecoder("utf-8");
  let arrayBuffer = details.requestBody.raw[0].bytes;
  let gql = dec.decode(arrayBuffer);
  let queries = JSON.parse(gql);
  if (queries.length == undefined) queries = [queries];
  for (let i=0 ; i<queries.length ; i++) {
    let query = queries[i];
    if((query.operationName == "PlaybackAccessToken_Template" && query.variables.login.endsWith('videos')) || 
        query.operationName == "FilterableVideoTower_Videos" ||
        query.operationName == "ChannelVideoShelvesQuery") {
      console.log("redirecting ", query.operationName);
      return { redirectUrl }
    }
  }
}

chrome.webRequest.onBeforeRequest.addListener(
  onVodListBeforeRequest,
  { urls: ["https://gql.twitch.tv/gql"] },
  ["blocking", "extraHeaders", "requestBody"]
);
