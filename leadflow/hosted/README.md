# LeadFlow live portfolio demo

Live demo: https://leadflow-bhuvesh.bhuveshchandrakar060.chatgpt.site

Self-built portfolio project by Bhuvesh, developed with AI assistance. Fictional sample data only; no paid client claim.

Cloudflare-compatible Worker with D1 persistence and per-visitor HttpOnly cookie workspaces. Rules scoring, lead capture, deduplication, stages, follow-up dates, activity and export. No AI API or outbound email service is connected. Follow-ups store dates; no automated reminder worker.

Install with npm ci, then npm run build. Configure a D1 binding named DB and apply the included Drizzle migrations before deployment. Worker entrypoint: dist/server/index.js. Public demo limits each visitor to 100 leads. Session cookie lasts seven days; clearing it loses access to that visitor workspace. Not a production CRM account system.

Verified: local Python end-to-end workflow tests; hosted route, origin checks, invalid input and storage failure handling; successful production deployment. Browser UI and WebMCP validation were unavailable in this run.
