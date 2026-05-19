// Cloudflare Worker — 反向代理 + 缓存加速
// 部署后: daily-motto.yzdsoul.workers.dev
// 后端:  yzdsoul-daily-motto.hf.space

const BACKEND = 'https://yzdsoul-daily-motto.hf.space'

const CACHE_TTL = {
  '/static/': 3600,       // CSS/JS 1h
  '/api/daily': 86400,    // 每日格言 24h
  '/api/joke/daily': 86400,
  '/api/categories': 300, // 分类 5min
  '/api/jokes/categories': 300,
}

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url)

    // 计算缓存时间
    let ttl = 0
    for (const [prefix, sec] of Object.entries(CACHE_TTL)) {
      if (url.pathname.startsWith(prefix)) { ttl = sec; break }
    }

    // GET 请求尝试读 Cloudflare 缓存
    const cache = caches.default
    if (ttl > 0 && request.method === 'GET') {
      const hit = await cache.match(request)
      if (hit) return hit
    }

    // 透传到 HF Spaces
    const backendUrl = BACKEND + url.pathname + url.search
    const headers = new Headers(request.headers)
    headers.set('Host', new URL(BACKEND).host)

    const resp = await fetch(backendUrl, {
      method: request.method,
      headers,
      body: request.method === 'GET' ? null : request.body,
    })

    // 构造响应 + 缓存头
    const newResp = new Response(resp.body, {
      status: resp.status,
      statusText: resp.statusText,
      headers: resp.headers,
    })

    if (ttl > 0) {
      newResp.headers.set('Cache-Control', `public, max-age=${ttl}`)
      if (request.method === 'GET') {
        ctx.waitUntil(cache.put(request, newResp.clone()))
      }
    } else {
      newResp.headers.set('Cache-Control', 'no-cache')
    }

    newResp.headers.set('X-Proxy', 'Cloudflare Worker')
    return newResp
  },
}
