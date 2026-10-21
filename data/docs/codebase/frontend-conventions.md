# Frontend Conventions

> Fictional company and content, created for the Ramp-Up Assistant PoC.

Owner: Mei Lin Tan (Tech Lead, Counter Web) · Also ask: Kwame Mensah (Tech Lead, Kitchen Mobile)

These conventions apply to `counter-web` and, where it makes sense, to `kitchen-mobile`. The Node.js version is pinned in each repo's `.nvmrc`.

## Project structure (counter-web)

```
counter-web/src/
├── app/            # Routing, providers, app shell
├── features/       # One folder per feature, e.g. stock-counts/, purchase-orders/
│   └── stock-counts/
│       ├── api.ts          # TanStack Query hooks for this feature
│       ├── components/     # Components used only by this feature
│       ├── pages/          # Route-level components
│       └── __tests__/
├── shared/         # Hooks and utilities used by several features
└── i18n/           # Translation files
```

Code is organized by feature, not by type. A component used by only one feature lives inside that feature's folder; move it to `shared/` only when a second feature needs it.

## Data fetching and state management (no Redux)

- Server data is fetched with **TanStack Query** hooks defined in each feature's `api.ts`. Do not call `fetch` directly from components.
- The API client is generated from the gateway's OpenAPI spec with `npm run generate:api`. Re-run it when a backend endpoint changes.
- Local UI state uses React state and context. We do not use Redux.

## Design system

- Build UIs with **Whisk** components (`@larderly/whisk`) instead of plain HTML elements and custom CSS.
- If Whisk is missing something you need, ask in `#whisk` before building your own; it may already be planned.
- Colours, spacing and fonts come from Whisk design tokens. Hard-coded colour values fail the lint step.

## Translations

Counter and Kitchen are available in English, Brazilian Portuguese and Spanish. Every user-facing string goes through `t('key')`; keys live in `i18n/en.json`. Only add the English text in your PR. The translations are added by the localization vendor before release, and missing translations fall back to English.

## Testing

- **Vitest + Testing Library** for component and hook tests, next to the feature in `__tests__/`.
- **Playwright** end-to-end tests for the critical flows (log in, count stock, submit a purchase order). They run in CI against the dev environment after each merge.
- **Storybook** for Whisk and for complex feature components. Add a story when you add a new reusable component.

## Mobile specifics (kitchen-mobile)

- The app must work offline: stock counts are saved locally in WatermelonDB and synced when the connection returns. Never assume a request will succeed immediately.
- Test on both a small Android device and an iPhone before asking for review on UI changes.
