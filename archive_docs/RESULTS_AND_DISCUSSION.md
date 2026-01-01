# 7. Results and Discussion

This chapter is organised to help you add screenshots and a simple accuracy chart, and to present clear discussion points about benefits (including suggested local/Pakistan-focused talking points). It is written so you can drop in screenshots and numbers later.

## 7.1 How to present results (screenshots)

Include screenshots that show the real UI and flows. Save images in `assets/screenshots/` and use these suggested filenames and captions:

- `dashboard.png` — "User dashboard: points balance and history".
- `scan_screen.png` — "QR disposal screen (scanner + session status)".
- `capture_preview.png` — "Camera capture preview shown before inference".
- `disposal_confirm.png` — "Confirmation screen after successful disposal".
- `rewards_store.png` — "Rewards store and redemption screen".

Insert each screenshot using standard markdown image links. Example markdown you can paste:

`![User dashboard](assets/screenshots/dashboard.png)`

Below each image add a one-line caption describing what the reader should look for (e.g., "Shows awarded points and recent disposals").

## 7.2 ML training accuracy chart

Add a training/validation accuracy chart for the waste classifier. Save the chart as `assets/charts/ml_accuracy.png` and include it like:

`![Model accuracy](assets/charts/ml_accuracy.png)`

Suggested caption: "Model training and validation accuracy across epochs — used to select the final classifier and the stopping epoch." 

If you don't have the chart image yet, you can create a simple placeholder image with the same filename and replace it later.

## 7.3 Results summary (text to include alongside screenshots)

Use short, clear bullets that pair with your screenshots and chart. Example text you can paste and edit with your numbers:

- End-to-end flow verified: QR → session → capture → classify → bin control → record.
- Demonstration success rate (example): 85–95% in controlled conditions. (Replace with your measured value.)
- Average capture-to-decision latency: ~2–4 seconds (local network). (Replace with your measured value.)
- Model classification accuracy (validation): XX% at selected epoch. (Insert value from your accuracy chart.)

## 7.4 Discussion — Benefits (general and Pakistan-focused)

Use this section to explain why the project matters and how it can help local governments, communities, and the environment. Replace placeholders with local statistics if you have them.

General benefits:

- Increased recycling rates: by routing waste correctly and making recycling rewarding, the system encourages proper sorting at source.
- Reduced operational costs: better sorting at collection points can reduce landfill volumes and lower transport and processing costs.
- Transparent rewards and audit trail: each disposal is recorded, enabling traceability and community engagement.
- Community engagement and behaviour change: gamified points and rewards motivate users to participate regularly.

Pakistan-focused benefits and suggested talking points (insert local figures where available):

- Municipal waste burden: municipal solid waste management represents a significant line item in municipal budgets. Insert a local annual cost figure here and a citation if available (for example: "City X spends Rs. Y per year on solid waste collection and disposal").
- Potential savings: estimate savings by projecting diversion rates — for example, if a city diverts Z tonnes/year to recycling and the average processing cost is Rs. C per tonne, annual savings ≈ Z * C. Replace Z and C with local values.
- Employment and informal sector uplift: the system can help integrate informal waste pickers by creating verified collection points and incentive mechanisms, reducing loss of recyclable materials to landfill.
- Environmental benefits: fewer items landfilled => reduced greenhouse gas emissions and reduced need for landfill expansion (quote local impacts if available).

Template paragraph you can use in reports and presentations:

"Municipalities often spend a substantial portion of their sanitation budgets on collection, transport, and landfill operation. By increasing correct sorting at the point of disposal and incentivising recycling through a transparent rewards program, our system can reduce landfill volumes, lower operating costs, and create value for communities. For example, if a municipal area diverts X tonnes of recyclable material annually, and the average cost saving per tonne is Y, the projected annual saving is X × Y — funds that can be reinvested into improved services."

## 7.5 Suggested figures and tables to include

- Figure: `assets/screenshots/dashboard.png` — user dashboard.
- Figure: `assets/screenshots/scan_screen.png` — QR disposal screen.
- Figure: `assets/charts/ml_accuracy.png` — training/validation accuracy chart.
- Table: "Field trial summary" — columns: `Test Type | Attempts | Successes | Success Rate | Avg Latency | Notes`.
- Table: "Projected savings" — columns: `Metric | Value (local currency) | Notes` (fill in city-level figures if available).

## 7.6 How to present this chapter

1. Start with the user-facing screenshots and short captions to orient the reader.
2. Show the ML accuracy chart and state the chosen model and epoch briefly.
3. Present the key performance numbers (success rate, latency) in a short table.
4. Use the discussion section to explain benefits and include a short local projection using local numbers.

---

Document created: November 13, 2025
