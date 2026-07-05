# Privacy and Compliance Rules

## Core principle

Collect the minimum personal information needed for the user-visible purpose. Explain the purpose before requesting sensitive capability or personal data.

## Before using privacy-sensitive APIs

Verify:

- the feature has a clear user-facing purpose;
- the user can understand why the data or permission is needed;
- the Mini Program privacy configuration and privacy policy cover the data type;
- there is a denial path that does not trap the user;
- data is sent only to approved domains and necessary backend endpoints.

## Authorization UX

- Request permission at the moment of intent, not at app launch.
- Show a plain-language explanation before system authorization prompts when context is not obvious.
- Handle deny, later enablement, and partial capability gracefully.
- Provide alternate flows when possible.

## Personal information

Treat the following as sensitive:

- phone number, identity information, address, precise location;
- images, voice, video, files, contacts, clipboard content;
- payment/order data;
- user profile, identifiers, behavior logs tied to a user;
- health, education, finance, minors, or other high-risk data.

Do not log, cache, or transmit sensitive data unless necessary.

## User profile and phone number

- Do not assume profile or phone information is available.
- Use explicit user action and current platform APIs.
- Decrypt or exchange sensitive data on the server when required.
- Store only the normalized data needed for the business flow.

## Location

- Ask only when the user chooses a location-dependent feature.
- Explain whether the app needs one-time location, continuous location, or selected address.
- Provide manual entry or city selection when practical.

## Submission readiness

Before preview/upload/submission, check:

- privacy policy and platform privacy configuration match actual API usage;
- permission descriptions are accurate and not overbroad;
- demo/test accounts are available if review needs login;
- no hidden debug page exposes internal data;
- no mock data, staging domain, or unsupported capability remains in production config.

## Finding severity

- Critical: undisclosed collection, client-side secrets enabling personal data access, payment/privacy data leakage.
- Major: missing permission denial path, inaccurate privacy description, unnecessary sensitive data collection.
- Minor: unclear copy, excessive but non-sensitive logging, incomplete alternate states.
