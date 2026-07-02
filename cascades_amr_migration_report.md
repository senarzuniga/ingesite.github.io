---
title: Migration from Fixed Transfer Car (BHS) to an AMR Fleet — Cascades
author: INGECART Engineering
date: 2026-07-02
version: 0.1 (draft)
---

# Migration from Fixed Transfer Car (BHS) to an AMR Fleet

Prepared for: Cascades — Engineering & Operations

Prepared by: INGECART — Systems & Solutions

Date / Version: 2026-07-02 / v0.1 (draft)

## Executive summary

This report evaluates the strategic migration from a fixed transfer-car based Bulk Handling System (BHS) to an autonomous mobile robot (AMR) fleet for reel handling in a corrugated packaging plant. The proposal preserves corrugator throughput while increasing floor-space efficiency, reducing single points of failure, and decoupling logistics flows from mechanical conveyors. The recommended solution combines AMR transport with local Trident handoff stations and a high-density WIP allocation strategy to deliver measurable gains in availability, flexibility and OPEX.

## Current vs Proposed (high-level)

| Operational variable | Current system (BHS transfer / belts) | Proposed system (AMR + Trident stations) | Operational impact |
|---|---|---|---|
| Space density | Fixed rails and conveyors consume continuous linear floor area | Flexible AMR lanes + concentrated WIP blocks reduce continuous footprint | Increase usable floor area; easier reconfiguration |
| Flow flexibility | Deterministic but rigid routing; rework costly | Dynamic routing, multi-destination deliveries | Faster adaptation to changes in demand |
| Mechanical maintenance | Heavy dependence on conveyors and transfer car | Fewer continuous-movement mechanical subsystems; AMRs are modular | Lower preventive maintenance and faster part replacement |
| Flow bottlenecks | Single transfer carriage creates queuing and SPoF | Multiple AMRs provide redundancy; Trident stations parallelise handoff | Reduced starvation & downtime |
| Expandability | Requires costly rail extensions and civil works | Scale by adding AMRs and scalable stations | Phased investment with smaller CAPEX steps |
| Routing adaptability | Limited to rails and fixed tracks | Omnidirectional AMR routing with traffic orchestration | Better handling of production variability |
| Operational resilience | High impact from single carriage failure | Redundant AMR fleet and rerouting | Lower systemic risk |
| Product handling quality | Precise but constrained by transfer mechanics | Trident stations ensure gentle handoff; AMRs maintain orientation | Equal or improved product protection |

## Key value drivers

1. Maximised floor space / High‑density WIP

- Executive statement: Concentrate WIP into compact, managed blocks and free continuous conveyorways to increase productive area.
- Technical explanation: Use dense storage racks and buffer islands adjacent to a dual-lane AMR highway; AMRs shuttle reels between dense WIP and Trident handoff points.
- Operational consequence: More production cells and staging areas fit within the same footprint; shorter walking distances for operators and simplified maintenance zones.

2. Elimination of single point of failure

- Executive statement: Replace the transfer carriage single‑point with a redundant fleet architecture.
- Technical explanation: Multiple AMRs coordinated by fleet manager; Trident stations accept inputs from any AMR and decouple delivery from single-vehicle timing.
- Operational consequence: Fault tolerance; degraded-but-serviceable operation during maintenance.

3. Decoupled operational flows

- Executive statement: Separate long‑distance transport from line feeding and returns.
- Technical explanation: AMRs operate on dual‑lane highways for bulk transfer; Trident stations and local conveyors provide fast line insertion and return paths.
- Operational consequence: Increased throughput predictability; easier scheduling and job change handling.

4. Reduced mechanical maintenance

- Executive statement: Replace continuously running conveyors with scheduled AMR movements and short local conveyors.
- Technical explanation: Mechanical wear limited to short pick/drop conveyors and station actuators; AMRs follow modular maintenance cycles.
- Operational consequence: Lower OPEX and simpler spare‑parts management.

5. Improved board protection / waste reduction

- Executive statement: Minimise handling shocks and mis‑drops through standardised Trident handoff logic and gentle transfer profiles.
- Technical explanation: Controlled pick/drop sequences and job-level friction/velocity profiles at Trident stations.
- Operational consequence: Fewer damaged rolls and lower waste.

## Layout blueprint

See `cascades_amr_migration_report_assets/layout_blueprint.svg` for a scaled diagram of the proposed layout. The blueprint shows:

- Corrugator take‑off and immediate induction.
- A central AMR dual‑lane highway with directional lanes.
- Main evacuation Trident station serving the corrugator.
- Six converting lines on the left with local Trident feed stations.
- High‑density WIP block (right) for staged reels and buffer capacity.
- Shipping / finished goods outbound on the far right.

The asset is included both as an inline SVG in the HTML and as a standalone file for print or further editing.

## Material flow dynamics (4 steps)

1. Inbound induction from corrugator

- Operational description: Reels exiting the corrugator are staged at an induction buffer where they are tagged and assigned.
- AMR action: AMRs pick assigned reels and transport them to the high‑density WIP block or directly to Trident stations depending on demand.
- Control layer: WMS/WCS assigns priorities, updates fleet tasks, and reserves Trident slots.
- Why it matters: Prevents unmanaged accumulation at the corrugator and avoids upstream starvation.

2. Deep‑lane WIP allocation

- Operational description: Concentrated buffers store reels in high density, minimising occupied linespace.
- AMR action: Shuttle reels between the dense block and line‑side Trident stations as scheduled or on demand.
- Control layer: WIP model triggers replenishment when local buffers fall below thresholds.
- Why it matters: Smooths peaks and allows just‑in‑time feeding.

3. JIT converting line feeding

- Operational description: Trident stations decouple AMR arrival from local drop timing, enabling synchronous delivery.
- AMR action: Prepositioned AMRs release reels to Trident stations which deliver onto short conveyors to the roll stand.
- Control layer: Line demand signals and MES interface trigger drop sequences.
- Why it matters: Keeps the corrugator fed continuously with minimized delay.

4. Reverse logistics / overruns handling

- Operational description: Partial reels or overruns are returned to WIP or warehouse.
- AMR action: Collects return reels and places them back into the dense block or return aisle.
- Control layer: Exception workflows in WCS manage returns and reconcile inventory.
- Why it matters: Rapid handling of overruns reduces manual interventions and avoids line blockage.

## Engineering & integration considerations

- WCS / Fleet Manager coordination: Use a message‑based API to coordinate job dispatch, real‑time reservation of Trident slots and fleet health monitoring.
- Trident station integration: Electrical/IO and semantic event model for pick/drop handshake, presence sensors, and fast‑eject confirmation.
- Buffering logic: Short local conveyors at Trident with gentle acceleration profiles; station timeouts to avoid deadlocks.
- Line demand signals: MES integration required to receive job changes and preemptive refills.
- Traffic orchestration: Dual‑lane highway with lane discipline (left/right) and dynamic lane reconfiguration during maintenance.
- Exception handling: Clear fallbacks for blocked stations (reroute to alternate station) and controlled human takeover procedures.

## Recommended next phase: Concept validation & layout engineering

Suggested work packages:

- Site survey and dimensional validation.
- Throughput simulation and WIP capacity modelling.
- AMR fleet sizing and charging strategy.
- Trident station interface & mechanical definition.
- Phased migration concept and pilot cell design.
- ROI / OPEX vs CAPEX analysis.

---

## Appendix — assumptions

- The plant layout allows installation of a central dual‑lane AMR highway parallel to the corrugator.
- Typical reel sizes and weights are within standard ranges (≤ 3,500 kg). Large outliers require special handling.
- Integration with MES/WCS is feasible via standard APIs or OPC‑UA gateways.
