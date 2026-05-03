# Phase 2: Singpass MyInfo Integration

> Status: **Parked** — pick up when ready to move beyond manual entry.

## Overview

Integrate with Singapore's MyInfo API (via Singpass) to auto-fill income, CPF, family, and NS data into the tax calculator. This eliminates ~70% of manual data entry for the primary user (salaried SC/SPR).

## Architecture

```
Browser (SPA)              Backend (Node.js)           Singpass / MyInfo
     │                            │                          │
     ├── "Login with Singpass" ──►│                          │
     │                            ├── Redirect ─────────────►│
     │   ◄── Singpass QR / login ─┤◄─────────────────────────┤
     │                            │                          │
     │   ◄── Callback + code ─────┤◄── Auth code ────────────┤
     │                            ├── Exchange code ─────────►│
     │                            │◄── Access token ──────────┤
     │                            ├── GET /person ───────────►│
     │                            │◄── JWE (encrypted) ───────┤
     │                            ├── Decrypt + verify        │
     │   ◄── JSON (pre-fill) ─────┤                          │
     └────────────────────────────┘                          │
```

## MyInfo Data Scopes Needed

| Scope | What it provides | Maps to calculator field |
|-------|-----------------|------------------------|
| `cpfcontributions` | Employee + employer CPF contributions | CPF Relief (auto) |
| `cpfbalances` | OA, SA, MA, RA balances | Informational display |
| `noa` | Previous YA Notice of Assessment | Income, past reliefs, past tax |
| `noahistory` | Multi-year NOA | YoY comparison (future) |
| `childrenbirthrecords` | Children DOB, citizenship | QCR, WMCR, PTR auto-fill |
| `marital` | Married / single / divorced | Spouse Relief eligibility |
| `dob` | Date of birth | Age → Earned Income Relief tier |
| `sex` | Gender | WMCR eligibility |
| `residentialstatus` | SC / PR / Foreigner | Tax residency, CPF rates |
| `nsmen` | NSman status + tier | NSman relief auto-fill |
| `cpfrstureliefs` | RSTU relief / top-up amounts | CPF Cash Top-up relief |

## What MyInfo will NOT provide

- **SRS account balances** — no public API from DBS/OCBC/UOB
- **Life insurance premiums paid** — not in MyInfo
- **Spouse's data** — spouse must login separately with their own Singpass
- **Current YA income** — NOA only has previous year; current year income must still be entered manually unless employer has filed IR8A early
- **Voluntary CPF top-ups made this calendar year** — `cpfrstureliefs` may lag

## Tech Stack

### Backend
- **Runtime**: Node.js 20+
- **Framework**: Express.js (minimal)
- **MyInfo SDK**: `myinfo-connector-nodejs` (official GovTech package)
- **Crypto**: Node `crypto` for JWE decryption + JWS verification
- **Hosting**: Vercel (serverless functions) or AWS Lambda + API Gateway

### Frontend changes
- Add a "Login with Singpass" button on Step 1
- On successful callback, pre-fill all form fields from the decrypted response
- Show a "Data from Singpass" badge next to auto-filled fields
- Allow manual override of any pre-filled value

## GovTech Onboarding Steps

1. **Register** at [api.singpass.gov.sg](https://api.singpass.gov.sg)
2. **Create app** — declare scopes, callback URL, environment (sandbox first)
3. **Generate keys** — RSA key pair for JWE decryption, register public key with GovTech
4. **Sandbox testing** — use test personas:
   - `S9812381D` — Mr. ANDY LAU (married, 2 children, SC)
   - `S9812382B` — Ms. JANET TAN (single, SC)
   - `S9812385G` — Mr. DAVID LIM (foreigner)
5. **Security review** — GovTech reviews your app, data handling, PDPA compliance
6. **Production onboarding** — sign agreements, receive production credentials
7. **Go live** — switch from sandbox to production endpoints

## Sandbox Quick Start

```bash
# 1. Clone the official demo
git clone https://github.com/singpass/myinfo-demo-app.git
cd myinfo-demo-app

# 2. Install dependencies
npm install

# 3. Configure (copy sample env)
cp .env.sample .env
# Edit .env with your sandbox app credentials

# 4. Start
npm start
# Opens on http://localhost:3001
```

### Key sandbox URLs
- Authorize: `https://test.api.myinfo.gov.sg/com/v4/authorize`
- Token: `https://test.api.myinfo.gov.sg/com/v4/token`
- Person: `https://test.api.myinfo.gov.sg/com/v4/person`

## Implementation Plan

### Step 1: Backend scaffold
- Express server with 3 routes: `/auth/redirect`, `/auth/callback`, `/api/person`
- MyInfo connector configured for sandbox
- CORS configured for the frontend origin

### Step 2: Frontend integration
- "Login with Singpass" button → redirects to backend `/auth/redirect`
- Backend redirects to Singpass authorize page
- User authenticates → Singpass redirects to `/auth/callback`
- Backend exchanges code → fetches person data → redirects to frontend with session token
- Frontend calls `/api/person` with session token → receives pre-fill data

### Step 3: Field mapping
```javascript
function mapMyInfoToForm(person) {
  return {
    incomeYou: person.noa?.amount?.value || 0,
    ageYou: calculateAge(person.dob?.value),
    citizenYou: mapResidentialStatus(person.residentialstatus?.code),
    genderYou: person.sex?.code === 'M' ? 'M' : 'F',
    married: person.marital?.code === 'M',
    children: (person.childrenbirthrecords || []).map(c => ({
      dob: c.birthcertno?.value ? c.dob?.value : null,
      sgCitizen: c.residentialstatus?.code === 'C',
      disability: false  // not in MyInfo, manual entry
    })),
    nsSelf: mapNSmanTier(person.nsmen),
    cpfContributions: person.cpfcontributions?.history || []
  };
}
```

### Step 4: Production hardening
- HTTPS only (mandatory for Singpass)
- Rate limiting on auth endpoints
- Session management (short-lived tokens, no persistent storage of personal data)
- PDPA compliance: display privacy notice, no data logging beyond session
- Error handling for expired tokens, revoked consent

## Cost

- **MyInfo API**: Free for sandbox, free for production (government service)
- **Hosting**: ~$0–5/month on Vercel free tier or AWS free tier
- **Domain + SSL**: ~$12/year for `.sg` domain + free Let's Encrypt SSL

## Risks & Mitigations

| Risk | Mitigation |
|------|-----------|
| GovTech rejects app registration | Start with sandbox; formal registration only after prototype validated |
| API changes (v4 → v5) | Pin SDK version; GovTech provides migration guides |
| Data sensitivity concerns | No server-side persistence; data lives only in browser session |
| Spouse data requires separate login | Clear UX: "Ask your spouse to scan their Singpass too" |
| NOA income ≠ current year income | Label as "Last year's assessed income" with manual override |

## Decision log

- **2 May 2026**: Decided to park Singpass integration. Current manual-entry calculator covers the core use case. Revisit when user demand or sharing volume justifies the backend complexity.
