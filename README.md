# website

deeplyrootedhvac.com, the public website for Deeply Rooted Mechanical. Hosted on DRM's own Netlify, separate from Rooted (which holds customer data).

- Edit content in `build.py` (and `assets/`), run `python3 build.py`, commit both. Netlify publishes `public/` as-is.
- Forms: Netlify Forms (`service-request`). Notifications to Service@ are set in Netlify > Forms. Change list #38 moves them into Rooted.
- Old addresses (/home, /Commercial, /Residential, /about-us, /rooted-assurance-program) are kept or redirected so rankings carry over (`_redirects`).
- Legal pages and SMS consent wording match what the Twilio texting campaign was approved with. Do not change them without checking the campaign.
- Plan and decisions: project doc `claude/marketing/website-rebuild-plan.md`.
