const config = require("../../config.json");
const fetch = require("node-fetch");

function client(endpoint = "https://discord.com/api/v6", authorization = config.token) {
  let url = endpoint;
  const fn = function(ep) {
    url += "/" + ep;
    return fn;
  };
  
  fn.get = async (opts) => {
    const resp = await fetch(url, Object.assign({
      method: 'GET',
      headers: {
        'Authorization': `Bot ${authorization}`
      }
    }, opts));
    const json = await resp.json();
    return json;
  };

  fn.post = async (opts) => {
    const resp = await fetch(url, Object.assign({
      method: 'POST',
      headers: {
        'Authorization': `Bot ${authorization}`
      }
    }, opts));
    const json = await resp.json();
    return json;
  };

  fn.put = async (opts) => {
    const resp = await fetch(url, Object.assign({
      method: 'PUT',
      headers: {
        'Authorization': `Bot ${authorization}`
      }
    }, opts));
    const json = await resp.json();
    return json;
  };

  fn.patch = async (opts) => {
    const resp = await fetch(url, Object.assign({
      method: 'PATCH',
      headers: {
        'Authorization': `Bot ${authorization}`
      }
    }, opts));
    const json = await resp.json();
    return json;
  };

  fn.guild = (id) => {
    url += `/guilds/${id ?? ""}`;
    return fn;
  }
  fn.channel = (id) => {
    url += `/channels/${id ?? ""}`;
    return fn;
  }
  fn.emoji = (id) => {
    url += `/emojis/${id ?? ""}`;
    return fn;
  }
  fn.invite = (id) => {
    url += `/invites/${id ?? ""}`;
    return fn;
  }
  fn.user = (id) => {
    url += `/users/${id ?? "@me"}`;
    return fn;
  }
  fn.webhook = (id) => {
    url += `/webhooks/${id ?? ""}`;
    return fn;
  }
  fn.member = (id) => {
    url += `/members/${id ?? ""}`;
    return fn;
  }

  return fn;
}

module.exports = client;