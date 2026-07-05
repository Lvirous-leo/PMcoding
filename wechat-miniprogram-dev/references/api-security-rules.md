# API and Security Rules

## Server boundary

- Never store `appSecret`, payment private keys, merchant certificates, service access tokens, long-lived refresh tokens, or privileged credentials in Mini Program client code.
- Perform `code2Session`, payment signing, phone-number decryption, permanent token exchange, and privileged data access on the server.
- Treat the Mini Program client as untrusted. Validate user identity, authorization, ownership, and input again on the server.
- Use HTTPS and configured request/upload/download domains for all network calls.

## Login and sessions

- Use `wx.login` only to obtain a temporary code.
- Send the code to the backend; the backend exchanges it with `code2Session`.
- The client should receive a project-defined session token or cookie, not `session_key`.
- Handle expired sessions with a clear re-login path and retry the original action only when safe.
- Do not use openid or unionid as the only authorization proof for sensitive operations.

## Network requests

- Centralize request handling: base URL, auth injection, timeout, retry policy, error mapping, and response normalization.
- Make request states visible to the user for important flows.
- Avoid silent retries for non-idempotent writes.
- Redact sensitive headers, tokens, phone numbers, addresses, IDs, and payment data from logs.
- Validate backend response shape before updating page state.

## Sensitive capabilities

Use explicit UX and fallback for:

- payment;
- phone number;
- location;
- camera and album;
- microphone;
- files and storage;
- Bluetooth, NFC, clipboard, contacts, calendar;
- subscription messages.

Do not request permissions before the user understands why the capability is needed.

## Payment

- Signing and order creation must happen on the server.
- The client should call payment with server-generated payment parameters only.
- Handle user cancel, duplicate submit, payment pending, callback delay, and reconciliation states.
- Never trust client-side payment success alone; confirm order state with the server.

## Subscription messages

- Ask for subscription at the moment of clear user intent.
- Explain the message purpose in product UI.
- Handle decline gracefully and avoid blocking the core flow unless the subscription is essential and disclosed.

## Storage

- Store only low-risk, necessary client data.
- Do not store secrets, raw identity credentials, decrypted personal information, or payment-sensitive data in local storage.
- Add cache invalidation for user-specific data and clear it on logout.

## Logging

- Keep logs useful but non-sensitive.
- Remove debugging logs before release when they include request payloads, auth state, or personal data.
- For review findings, flag any log that may leak personal or security-sensitive data as Major or Critical depending on impact.
