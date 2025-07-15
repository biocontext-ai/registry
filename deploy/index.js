export default {
  async fetch(request, env) {
    const originHeader = request.headers.get("Origin");

    const allowedOrigins = [
      /^https?:\/\/localhost:\d+$/,
      "https://biocontext.ai",
    ];

    let isOriginAllowed = false;
    let actualOriginForHeader = null;

    if (originHeader) {
      for (const pattern of allowedOrigins) {
        if (typeof pattern === "string" && originHeader === pattern) {
          isOriginAllowed = true;
          actualOriginForHeader = originHeader;
          break;
        } else if (pattern instanceof RegExp && pattern.test(originHeader)) {
          isOriginAllowed = true;
          actualOriginForHeader = originHeader;
          break;
        }
      }
    }

    // Define the CORS headers that will be applied if the origin is allowed
    const corsPolicyHeaders = {
      "Access-Control-Allow-Methods": "GET, OPTIONS",
      "Access-Control-Allow-Headers":
        "Content-Type, Authorization, X-Requested-With",
    };

    // Handle preflight OPTIONS requests
    if (request.method === "OPTIONS") {
      if (isOriginAllowed) {
        return new Response(null, {
          status: 204,
          headers: {
            ...corsPolicyHeaders,
            "Access-Control-Allow-Origin": actualOriginForHeader,
          },
        });
      } else {
        if (originHeader) {
          return new Response("CORS policy: Origin not allowed.", {
            status: 403,
          });
        }
        return new Response(null, {
          status: 204,
          headers: { Allow: "GET, OPTIONS" },
        });
      }
    }

    const response = await env.ASSETS.fetch(request);

    // If the origin is allowed, add appropriate CORS headers to the actual response
    if (isOriginAllowed) {
      const newHeaders = new Headers(response.headers);
      newHeaders.set("Access-Control-Allow-Origin", actualOriginForHeader);

      // Add other CORS policy headers to the actual response
      for (const [key, value] of Object.entries(corsPolicyHeaders)) {
        if (key !== "Access-Control-Allow-Origin") {
          newHeaders.set(key, value);
        }
      }
      return new Response(response.body, {
        status: response.status,
        statusText: response.statusText,
        headers: newHeaders,
      });
    }

    return response;
  },
};
