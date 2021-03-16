const username = /^[A-Za-z0-9_-]{1,32}$/g;

const actor = /^[A-Za-z0-9_-]{1,32}$/g;

const password = /^.{12,255}/g;

const actorHandle = /@[\w]{1,}@[\w.]{1,}.[\w]{1,}/g;

export {actorHandle, username, actor, password}

