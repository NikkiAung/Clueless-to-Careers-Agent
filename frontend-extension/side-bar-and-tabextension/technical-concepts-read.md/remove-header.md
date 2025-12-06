# Bypassing iframe limitation 🤷‍♂️⚔️

The declarativeNetRequestWithHostAccess permission and the declarative_net_request section in your manifest work together to enable the header modifications that bypass iframe restrictions. Here’s how they support each other:

## 1. declarativeNetRequestWithHostAccess Permission

- What it does:
  This permission allows your extension to use the Declarative Net Request API, which lets you modify network requests and responses without injecting scripts into the page.
- Why it matters:
  It’s a more secure and efficient way to handle network modifications compared to older methods (like webRequest), as it runs in a separate process and doesn’t require full access to the page’s JavaScript.

## 2. declarative_net_request Section in Manifest

- What it does:
  This section tells Chrome to load a set of rules from removeHeader.json. These rules define how to modify network requests and responses.
- Why it matters:
  It’s where you specify the exact changes you want to make (like removing headers or setting new ones) and when they should apply.

```
"declarative_net_request": {
  "rule_resources": [
    {
      "id": "removeHeader",
      "enabled": true,
      "path": "removeHeader.json"
    }
  ]
}
```

## How They Work Together

- Step 1: The declarativeNetRequestWithHostAccess permission enables the Declarative Net Request API for your extension.
- Step 2: The declarative_net_request section in your manifest points to - removeHeader.json, which contains the rules for modifying headers.
- Step 3: When a network request is made, Chrome applies these rules:
  - It sets the sec-fetch-dest header to "document" on outgoing requests (making the request look like a normal page load).
  - It removes the x-frame-options and content-security-policy headers from the response (preventing the browser from blocking iframe embedding).
- Result: The combination of these two parts allows your extension to bypass iframe restrictions by modifying both the request and response headers.

## Request Header Modification

```
"requestHeaders": [
  { "header": "sec-fetch-dest", "operation": "set", "value": "document" }
]
```

- What it does:
  This sets the sec-fetch-dest header to "document" for outgoing requests.

- Why it matters:
  Some websites check this header to determine if a request is for a top-level page ("document") or for an embedded resource like an iframe ("iframe").
  By forcing it to "document", you make the request look like a normal page load, not an iframe, which can trick the server into serving the content without restrictions.

## Response Header Removal

```
"responseHeaders": [
  { "header": "x-frame-options", "operation": "remove" },
  { "header": "content-security-policy", "operation": "remove" }
]
```

- What it does:
  This removes the x-frame-options and content-security-policy headers from the server’s response.
- Why it matters:
  x-frame-options is a security header that tells the browser whether a page can be displayed in an iframe. If it’s set to DENY or SAMEORIGIN, the browser will block the page from being embedded.
  content-security-policy can also include rules (like frame-ancestors) that prevent embedding in iframes.
  By removing these headers, you prevent the browser from enforcing these restrictions, allowing the page to be loaded in an iframe.

## How They Work Together

- Step 1: The outgoing request is modified to look like a normal page load (not an iframe) by setting sec-fetch-dest: document.

- Step 2: When the server responds, any headers that would block iframe embedding (x-frame-options and content-security-policy) are stripped out.

- Result: The browser receives a response that looks like a normal page load and has no headers telling it to block iframe embedding, so it allows the page to be displayed inside an iframe.

## Summary:

### - DeclarativeNetRequestWithHostAccess

The declarativeNetRequestWithHostAccess permission enables the API, while the declarative_net_request section in your manifest specifies the rules (loaded from removeHeader.json) that actually perform the header modifications. Together, they allow your extension to bypass iframe restrictions by altering network traffic in a secure and efficient way.

### - ModificationtWithHostAccess

These two modifications, one on the request, & one on the response-work together to bypass both server-side and browser-side restrictions on iframe usage, making it possible to embed pages that would otherwise block being loaded in an iframe.
