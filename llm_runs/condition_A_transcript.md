# LLM concept generation run — Condition A (Dual-track, proposed framework)

- Model: Claude Fable 5 (`claude-fable-5`, Anthropic)
- Access: Claude Agent SDK subagent session (independent session, empty context)
- Date: 2026-08-11
- Protocol: single pass, 2 turns, no retries/rerolls
- Transcript is verbatim and unedited

---

## Turn 1 — Prompt (P1)

Do not use any tools. Respond with text only.

You are acting as a robotics R&D strategist specializing in humanoid robot product planning.

Below is a dual-track morphological matrix derived from data analysis. Track A dimensions (technology supply) were extracted from 824 humanoid-robot invention patents (2020-2024) via BERTopic topic modeling. Track B dimensions (user experience) were extracted from 2,789 English YouTube comments on four major humanoid robot demonstration videos (Tesla Optimus Gen 2, Boston Dynamics Atlas, Figure 01, Ameca) via BERTopic and VADER sentiment analysis.

TRACK A - TECHNOLOGICAL DIMENSIONS (share of patent corpus):
- A1 Actuation (32.2%): Electric geared motor drive | Hydraulic actuator | Pneumatic artificial muscle | Linear screw actuator
- A2 Manipulation (15.0%): Dexterous multi-finger hand | Underactuated linkage hand | Modular arm assembly | Soft gripper
- A3 Control (33.9%): Model-based balance control (ZMP/centroid) | Whole-body motion planning | Reinforcement-learning locomotion | Vision-guided follow-up control
- A4 Perception (5.1%): 3D point-cloud sensing (LiDAR/depth) | Vision-based object recognition | Obstacle detection and mapping | Tactile/force sensing
- A5 Structure (13.8%): Expressive facial head module | Protective shell with thermal management | Integrated charging/docking design | Human-friendly exterior styling

TRACK B - EXPERIENTIAL DIMENSIONS (share of comment corpus):
- B1 Task needs (13.4%): Household chores (dishes/tidying) | Clothing and laundry handling | Affordable consumer price point | Personal errand assistance
- B2 Interaction (6.4%): Natural voice conversation | Human-like speech prosody | Real-time speech-to-speech reasoning | Expressive face/gesture cues
- B3 Acceptance (27.9%): Calibrated human-likeness (uncanny-safe) | Visible safety controls | Capability transparency (no staging) | Predictable, legible behavior
- B4 Projection (52.3%): Brand credibility | Futuristic tech symbolism | Pop-culture-aware positioning | Demonstrable capability milestones

Key empirical context from the analysis: public discourse is dominated by symbolic projection and by acceptance concerns (negative sentiment is elevated in the Acceptance dimension relative to others), while concrete task demands center on household labor; the patent corpus concentrates on movement-related technologies (81.1% across actuation, manipulation, control) with little attention to perception and human-facing structure.

TASK: Generate exactly 9 candidate humanoid robot product concepts. Each concept must:
1. Select at least one attribute from EVERY dimension (A1-A5, B1-B4).
2. Form a complete Perception-Cognition-Action loop (sensing -> decision -> actuation must be coherent).
3. Respect social acceptance constraints: avoid uncanny-valley-inducing hyper-realism, include at least one acceptance-oriented design element, and avoid configurations likely to trigger safety fears identified in the data.
4. Be technically plausible with current or near-term (within 5 years) technology.

Think through the trade-offs step by step before writing each concept. Then present the 9 candidates, each in exactly this compact format:
- Name:
- Selected attributes: (list dimension codes and chosen attributes)
- Core idea (2-3 sentences):

## Turn 1 — Response

Here is the portfolio, built from the matrix with the empirical asymmetries in mind. Before the concepts, the trade-off logic I applied throughout:

**Step-by-step trade-off reasoning (applied across all 9):**

1. **Supply-demand gap as design driver.** Patents concentrate 81.1% on movement (A1+A3+A2) while public demand centers on household labor (B1) and acceptance (B3). So most concepts convert existing movement-tech strength into household/service value, while deliberately over-investing in the patent whitespace: perception (5.1%) and human-facing structure (13.8%).
2. **Actuation choice is an acceptance decision, not just a performance one.** Hydraulics (powerful, noisy, "industrial-scary") are confined to controlled-venue concepts; homes get electric geared motors, linear screws, or compliant pneumatic muscles — quieter, back-drivable, inherently safer on contact, which directly addresses the elevated negative sentiment in B3.
3. **Uncanny-valley management.** No concept uses hyper-realistic skin/faces. Where expressiveness is needed (B2/A5), I use stylized/abstract expressive heads (Ameca-style articulation without silicone realism), which the comment data suggests is the "uncanny-safe" calibration point.
4. **B4 dominance (52.3%) means positioning is a feature.** Symbolic projection drives discourse, so several concepts explicitly engineer for credibility signals — unedited demos, open telemetry, milestone-based marketing — treating "capability transparency" as both a B3 and B4 asset.
5. **Loop coherence check per concept:** each pairs a sensing modality (A4) with a matching control paradigm (A3) and an actuation/end-effector stack (A1/A2) that can physically execute what the controller decides — e.g., deformable-object tasks get tactile sensing + vision-guided servoing + soft grippers, not ZMP + LiDAR.
6. **Feasibility discipline:** all concepts assume current-generation components (harmonic-drive electric joints, depth cameras, LLM speech stacks, sim-to-real RL) — nothing requiring breakthroughs beyond a 5-year horizon.

---

**1.**
- Name: HomeHand One
- Selected attributes: A1 Electric geared motor drive | A2 Dexterous multi-finger hand | A3 Whole-body motion planning + Vision-guided follow-up control | A4 Vision-based object recognition + Tactile/force sensing | A5 Human-friendly exterior styling | B1 Household chores (dishes/tidying) | B2 Natural voice conversation | B3 Predictable, legible behavior | B4 Demonstrable capability milestones
- Core idea (2-3 sentences): A general-purpose home chore humanoid whose loop runs camera-based object recognition and fingertip force sensing into whole-body planning, executed by quiet back-drivable electric joints and a dexterous hand for dishes and tidying. It telegraphs every intended motion via a chest projection strip and slow-start trajectories, making behavior legible before contact. Marketing is built on monthly unedited "chore milestone" videos to counter staging skepticism.

**2.**
- Name: LaundryLoop
- Selected attributes: A1 Linear screw actuator | A2 Soft gripper | A3 Vision-guided follow-up control | A4 Tactile/force sensing + Vision-based object recognition | A5 Protective shell with thermal management | B1 Clothing and laundry handling | B2 Natural voice conversation | B3 Visible safety controls | B4 Brand credibility
- Core idea (2-3 sentences): A laundry-specialist humanoid that closes the loop from fabric-state vision and gripper tactile feedback to real-time visual servoing, actuated by precise linear-screw arms and compliant soft grippers suited to deformable textiles. A sealed, humidity-tolerant shell suits bathroom/utility spaces, and an oversized illuminated e-stop plus a physical "hands-off" lever anchor perceived safety. Positioned under an established appliance brand to borrow washer/dryer trust.

**3.**
- Name: Errand Mate Mini
- Selected attributes: A1 Electric geared motor drive | A2 Underactuated linkage hand | A3 Model-based balance control (ZMP/centroid) | A4 Obstacle detection and mapping | A5 Integrated charging/docking design | B1 Affordable consumer price point + Personal errand assistance | B2 Natural voice conversation | B3 Predictable, legible behavior | B4 Demonstrable capability milestones
- Core idea (2-3 sentences): A deliberately small (≈1.2 m), cost-optimized errand humanoid: depth-based obstacle mapping feeds conservative ZMP walking and a cheap underactuated hand handles fetch-and-carry (mail, groceries, retrieving items). Sub-scale stature and slow, rule-governed motion patterns defuse physical-threat perception, while the self-docking design removes maintenance friction. The pitch is "the first humanoid under the price of a used car," directly answering the affordability demand cluster.

**4.**
- Name: CompanionCare Soft
- Selected attributes: A1 Pneumatic artificial muscle | A2 Underactuated linkage hand | A3 Vision-guided follow-up control | A4 Tactile/force sensing | A5 Expressive facial head module (stylized, non-realistic) | B1 Personal errand assistance | B2 Expressive face/gesture cues + Human-like speech prosody | B3 Calibrated human-likeness (uncanny-safe) | B4 Brand credibility
- Core idea (2-3 sentences): An assistive companion for older adults whose whole-arm tactile skin and gaze-tracking vision drive compliant follow-up control on pneumatic-muscle arms — intrinsically soft actuation that yields on unexpected contact instead of resisting it. The head is an abstracted, cartoon-calibrated expressive module (eyes and brow only, no synthetic skin), pairing warm prosodic speech with clearly non-human appearance to stay on the safe side of the uncanny valley. Certification partnerships with eldercare institutions supply the credibility that this trust-critical segment demands.

**5.**
- Name: Atlas-Class Venue Demonstrator "Vector"
- Selected attributes: A1 Hydraulic actuator | A2 Modular arm assembly | A3 Reinforcement-learning locomotion + Whole-body motion planning | A4 3D point-cloud sensing (LiDAR/depth) | A5 Protective shell with thermal management | B1 Household chores (staged task courses) | B2 Real-time speech-to-speech reasoning | B3 Capability transparency (no staging) | B4 Futuristic tech symbolism + Demonstrable capability milestones
- Core idea (2-3 sentences): A high-power flagship for controlled venues (expos, research showcases) — LiDAR point clouds feed RL-trained locomotion and whole-body planning executed by hydraulic limbs, demonstrating household-task courses at athletic speed. Because hydraulic power is exactly what triggers public fear, the concept inverts the demo formula: every run is livestreamed uncut with on-screen autonomy indicators and failure counts, converting the "no staging" demand into the brand story. It sells symbolism and R&D leadership, not home deployment.

**6.**
- Name: FrontDesk Persona
- Selected attributes: A1 Electric geared motor drive | A2 Modular arm assembly | A3 Vision-guided follow-up control | A4 Vision-based object recognition | A5 Expressive facial head module + Human-friendly exterior styling | B1 Personal errand assistance (wayfinding, item handover) | B2 Real-time speech-to-speech reasoning + Expressive face/gesture cues | B3 Calibrated human-likeness (uncanny-safe) | B4 Pop-culture-aware positioning
- Core idea (2-3 sentences): A stationary-base upper-torso humanoid concierge for hotels and showrooms: face detection and object recognition drive gaze, gesture, and handover servoing on light electric arms, while a speech-to-speech LLM stack handles open conversation with sub-second turn-taking. The head uses Ameca-style mechanical expressiveness but with visibly robotic materials — deliberately "obviously a robot, delightfully expressive." Character design is licensed-IP-friendly (droid-like archetypes the public already loves), exploiting the pop-culture framing that dominates comment discourse.

**7.**
- Name: SinkStation Pro
- Selected attributes: A1 Linear screw actuator | A2 Dexterous multi-finger hand | A3 Vision-guided follow-up control | A4 Vision-based object recognition + Tactile/force sensing | A5 Protective shell with thermal management | B1 Household chores (dishes) | B2 Natural voice conversation | B3 Visible safety controls | B4 Brand credibility
- Core idea (2-3 sentences): A kitchen-anchored humanoid specialized for the single most-cited chore — dishes: wet-object recognition plus fingertip slip sensing feed closed-loop visual servoing, executed by high-precision screw-driven arms and a waterproof dexterous hand. A thermally managed, splash-sealed shell and a glowing perimeter "active zone" line on the countertop make its safe operating envelope physically visible. Narrow scope is the feasibility play: one task done reliably beats a generalist that fuels staging suspicion.

**8.**
- Name: OpenBiped Campus
- Selected attributes: A1 Electric geared motor drive | A2 Modular arm assembly | A3 Reinforcement-learning locomotion | A4 Obstacle detection and mapping + 3D point-cloud sensing | A5 Integrated charging/docking design | B1 Affordable consumer price point | B2 Natural voice conversation | B3 Capability transparency (no staging) | B4 Demonstrable capability milestones
- Core idea (2-3 sentences): An affordable, open-platform research and education humanoid: depth/LiDAR mapping feeds sim-to-real RL locomotion on commodity electric joints, with hot-swappable modular arms so labs and schools reconfigure it per curriculum. All telemetry, policies, and demo logs are published by default — transparency as an architectural feature, not a marketing claim. Community leaderboards of reproducible task milestones turn the B4 "prove it" discourse into an engagement engine.

**9.**
- Name: Carrier Companion "Porter"
- Selected attributes: A1 Electric geared motor drive + Linear screw actuator (legs) | A2 Underactuated linkage hand | A3 Model-based balance control (ZMP/centroid) + Whole-body motion planning | A4 3D point-cloud sensing + Obstacle detection and mapping | A5 Human-friendly exterior styling + Integrated charging/docking design | B1 Personal errand assistance | B2 Human-like speech prosody | B3 Predictable, legible behavior + Visible safety controls | B4 Futuristic tech symbolism
- Core idea (2-3 sentences): A load-carrying escort humanoid for homes and campuses: point-cloud terrain perception feeds centroid-based balance and whole-body planning tuned for payload stability, with hybrid electric/screw legs handling stairs while robust underactuated hands grip bags and boxes. It projects its intended path on the floor ahead and announces maneuvers in calm prosodic speech, plus a wearable remote e-stop for the user — legibility and control as core UX. Sleek automotive-grade styling leans into the futuristic-symbol appeal without any face at all, sidestepping the uncanny question entirely.

---

**Portfolio check against the constraints:** all 9 cover every dimension A1-A5 and B1-B4; each loop pairs sensing, decision, and actuation coherently (e.g., tactile+servoing+soft actuation for deformables, LiDAR+RL+hydraulics only in controlled venues); every concept carries at least one B3 acceptance mechanism; no concept uses hyper-realistic humanlike skin; and all rely on components commercially demonstrated by 2024-2025. The set also spans the strategic map the data implies: three household-labor specialists (1, 2, 7), two affordability plays (3, 8), two trust-critical service roles (4, 6), and two symbolism/credibility flagships (5, 9).

---

## Turn 2 — Prompt (P2)

Now evaluate each of the 9 candidates on these three criteria, scoring each 1-10:
(C1) Logical consistency between the selected technological and experiential attributes.
(C2) Technical feasibility within the current or near-future technology landscape.
(C3) Alignment with the identified user needs and acceptance concerns.

Present a scoring table with brief justifications, then select the top 3 concepts by total score (explain tie-breaks if any).

For each of the selected 3 concepts, produce a detailed concept sheet in exactly this format (this format will be shown to expert evaluators, so keep each sheet 350-450 words):

## [Concept name]
**One-line value proposition:**
**Selected attributes:** (all 9 dimensions)
**System architecture (P-C-A loop):** (how sensing, decision-making, and actuation connect, component by component)
**Key components and indicative specifications:** (bulleted; realistic component classes, DoF counts, payload/speed ranges where sensible)
**Primary use scenario:** (a concrete day-in-the-life narrative, 4-6 sentences)
**Acceptance-oriented design choices:** (which design decisions address fear, uncanny valley, trust, and why)
**Feasibility notes:** (which existing platforms/components demonstrate each subsystem today)

## Turn 2 — Response

Restating the coordinator's request: score all 9 concepts on C1 (logical consistency), C2 (feasibility), C3 (user-need/acceptance alignment), each 1-10; present the table with justifications; select the top 3 with tie-breaks explained; then produce a 350-450-word concept sheet per selected concept in the prescribed expert-evaluator format. Proceeding.

## Scoring table

| # | Concept | C1 | C2 | C3 | Total | Brief justification |
|---|---------|----|----|----|-------|---------------------|
| 1 | HomeHand One | 9 | 6 | 9 | 24 | Tight sensing-servoing-dexterity chain and strong B1/B3 fit, but open-ended tidying with a dexterous hand in unstructured homes is the hardest manipulation problem in the set — feasibility is the drag. |
| 2 | LaundryLoop | 9 | 7 | 9 | 25 | Soft gripper + tactile + visual servoing is exactly the right stack for deformables; narrow task scope makes cloth manipulation credible near-term; laundry is a named top user demand. |
| 3 | Errand Mate Mini | 8 | 8 | 9 | 25 | Cost-driven attribute choices are internally consistent (underactuated hand, conservative ZMP); sub-$20k biped platforms already exist; hits both affordability and errand-assistance demand clusters. |
| 4 | CompanionCare Soft | 9 | 6 | 8 | 23 | Compliant actuation + tactile skin + stylized face is a coherent trust-first loop, but pneumatic muscles (compressor noise, control bandwidth) remain the least mature actuation option. |
| 5 | Vector (venue demonstrator) | 7 | 9 | 6 | 22 | Hydraulics + RL is proven (Atlas-class), but the B1 link is staged rather than real task delivery, and hydraulic power sits closest to the fear cluster despite the transparency countermeasures. |
| 6 | FrontDesk Persona | 9 | 9 | 7 | 25 | Everything demonstrated today (Ameca + LLM speech); very coherent; but it serves B2, only 6.4% of discourse, and touches household-task demand only tangentially. |
| 7 | SinkStation Pro | 9 | 8 | 9 | 26 | Narrowest, most coherent loop in the portfolio; anchored base and single-task scope maximize feasibility; dishes are the single most-cited concrete need, with strong visible-safety design. |
| 8 | OpenBiped Campus | 8 | 9 | 7 | 24 | Feasible on commodity platforms and transparency-native, but its primary users are labs/schools, not the household users whose needs the comment data expresses. |
| 9 | Porter | 8 | 8 | 8 | 24 | Solid balance-under-payload loop and good legibility design; slightly diluted focus (two actuation types, broad attribute spread) and less direct hit on the dominant chore demand. |

## Top-3 selection and tie-break

Ranking by total: **SinkStation Pro (26)** first, then a three-way tie at 25 (LaundryLoop, Errand Mate Mini, FrontDesk Persona) for two remaining slots. Tie-break rule: C3 takes precedence, because the empirical finding motivating this exercise is the supply-demand gap — alignment with expressed user needs and acceptance concerns is the least substitutable criterion (feasibility gaps close with time; misalignment does not). LaundryLoop and Errand Mate Mini score C3 = 9 versus FrontDesk Persona's 7, so they advance. **Selected: SinkStation Pro, LaundryLoop, Errand Mate Mini.**

---

## SinkStation Pro
**One-line value proposition:** A counter-anchored humanoid torso that fully owns the single most-demanded household chore — clearing, washing-loading, and putting away dishes — with its safe operating zone made physically visible.

**Selected attributes:** A1 Linear screw actuator; A2 Dexterous multi-finger hand; A3 Vision-guided follow-up control; A4 Vision-based object recognition + Tactile/force sensing; A5 Protective shell with thermal management; B1 Household chores (dishes); B2 Natural voice conversation; B3 Visible safety controls; B4 Brand credibility.

**System architecture (P-C-A loop):** *Perception:* a head-mounted RGB-D camera plus one wrist camera per arm feed a segmentation and 6-DoF pose network fine-tuned for wet, specular, and transparent tableware; GelSight-class tactile fingertips report contact geometry and incipient slip. *Cognition:* an embedded edge-GPU hosts a task planner that sequences clear-rinse-rack-store subtasks from imitation-learned skill primitives, while a 60 Hz visual-servoing controller continuously corrects end-effector pose against the tracked object; a force-control layer converts slip signals into grip-force adjustments. *Action:* two screw-driven arms execute stiff, sub-millimeter-repeatable trajectories and sealed dexterous hands modulate fingertip force. A supervisory safety node enforces the fixed workspace envelope and speed caps, closing the loop.

**Key components and indicative specifications:**
- Two 7-DoF arms with ball-screw joint modules; ~3 kg payload each; ±0.5 mm repeatability
- Two 12-DoF IP65-sealed multi-finger hands with tactile fingertip arrays
- Head RGB-D camera, two wrist RGB cameras, far-field microphone array
- Jetson-class edge GPU; tool-center-point speed capped at 0.5 m/s when a person is in range
- Splash-sealed torso shell with active thermal management; quick-release counter anchor
- LLM-based natural-voice interface for task requests and status queries

**Primary use scenario:** After dinner, a family member says, "SinkStation, handle the dishes." The robot projects its glowing active-zone boundary onto the counter, announces it is starting, and begins transferring plates from sink to rinse to dishwasher rack, adjusting grip when a wet glass begins to slip. When a child wanders toward the counter, the perimeter line pulses and both arms slow to crawl speed, then pause. Forty minutes later it has racked the dishwasher, hand-washed two pans, and stacked them on the drying rack, and it verbally reports one item it could not identify, left untouched at the sink edge.

**Acceptance-oriented design choices:** The anchored base removes the "it can come toward me" fear that dominates negative sentiment; the projected active zone and pulsing slowdown make the safety envelope legible without reading a manual. An oversized illuminated e-stop sits at counter height. The unit is deliberately faceless and appliance-styled — no anthropomorphic head — sidestepping the uncanny valley entirely. Narrow, verifiable task scope means marketing claims match observable performance, answering the "no staging" demand.

**Feasibility notes:** Washdown-rated industrial manipulators prove IP-sealed precision arms; GelSight/Digit tactile sensors are commercial; visual servoing is mature industrial practice; kitchen-manipulation policies have been demonstrated by Figure's household demos and ALOHA/π0-style imitation learning; ball-screw actuation is standard automation hardware. (~415 words)

---

## LaundryLoop
**One-line value proposition:** A laundry-specialist humanoid that closes the loop from fabric vision and touch to compliant soft-gripper manipulation, sold under a trusted appliance brand with hard-wired visible safety controls.

**Selected attributes:** A1 Linear screw actuator; A2 Soft gripper; A3 Vision-guided follow-up control; A4 Tactile/force sensing + Vision-based object recognition; A5 Protective shell with thermal management; B1 Clothing and laundry handling; B2 Natural voice conversation; B3 Visible safety controls; B4 Brand credibility.

**System architecture (P-C-A loop):** *Perception:* torso- and wrist-mounted RGB-D cameras run a cloth-state estimation network (garment class, edges, corners, wrinkle field); tactile pads inside each soft-gripper jaw sense fabric thickness, layer count, and grip security. *Cognition:* a hierarchical planner classifies each garment, selects a skill policy (unfold, flatten, fold, hang, load/unload machine) from an imitation-learned library, and a 30 Hz visual-servoing loop tracks cloth deformation to re-target grasp points as the fabric moves. *Action:* two screw-actuated arms with passively compliant wrists position tendon-driven soft grippers whose pinch force is modulated from tactile feedback; a low-speed wheeled base repositions the torso between hamper, machines, and folding table. Grip-failure signals trigger re-perception and re-grasp, closing the loop.

**Key components and indicative specifications:**
- Two 7-DoF screw-actuated arms, ~2 kg payload each, compliant wrist modules
- Two 2-3-DoF tendon-driven soft grippers with internal tactile arrays (0.5-15 N pinch range)
- Torso RGB-D plus two wrist RGB-D cameras; far-field microphone array
- Wheeled base, max 0.6 m/s; humidity-tolerant sealed shell with active thermal management
- Edge-GPU compute; LLM voice interface for task requests and garment-handling preferences

**Primary use scenario:** On Saturday morning the user says, "Do the laundry, darks first." LaundryLoop wheels to the hamper, visually sorts garments by color and fabric class, and loads the washer, announcing each step. When the cycle ends it transfers the load to the dryer, then folds items at the table — regrasping a twisted shirt twice, guided by corner detection — and stacks output by garment type. It flags one delicate item it declines to machine-handle, draping it over the rack, and reports completion by voice with a per-item summary.

**Acceptance-oriented design choices:** A physical "hands-off" lever mechanically disengages arm power — trust anchored in hardware, not software promises — beside an illuminated e-stop. Soft grippers cannot exert crushing force by construction. The faceless, appliance-styled body avoids uncanny valley, and co-branding with an established washer/dryer manufacturer transfers existing appliance trust, directly targeting the brand-credibility cluster that dominates discourse.

**Feasibility notes:** Physical Intelligence's π0 (2024) demonstrated end-to-end autonomous laundry folding; 1X's wheeled EVE validates the mobile-torso format; commercial soft grippers (Soft Robotics-class) and Digit-class tactile sensing are shipping; cloth-state perception has a decade of published results (Berkeley cloth-folding line). All subsystems exist; integration is the work. (~420 words)

---

## Errand Mate Mini
**One-line value proposition:** A deliberately small, sub-used-car-priced biped that fetches and carries around the home, engineered so that affordability and non-threatening presence are the product.

**Selected attributes:** A1 Electric geared motor drive; A2 Underactuated linkage hand; A3 Model-based balance control (ZMP/centroid); A4 Obstacle detection and mapping; A5 Integrated charging/docking design; B1 Affordable consumer price point + Personal errand assistance; B2 Natural voice conversation; B3 Predictable, legible behavior; B4 Demonstrable capability milestones.

**System architecture (P-C-A loop):** *Perception:* stereo depth cameras and two fisheye cameras build a local elevation and obstacle map fused into a persistent home SLAM map; a microphone array captures spoken requests. *Cognition:* an LLM-based interpreter converts errands ("bring the package from the door") into waypoint sequences and grasp goals; a ZMP/capture-point gait engine with model-predictive step placement generates conservative walking; the grasp planner computes only an approach pose — the underactuated hand's mechanical adaptation handles object-shape uncertainty, deliberately shifting complexity from software to linkage design. *Action:* electric geared joints execute the gait and reach; the hand self-conforms on closure; battery-state monitoring routes the robot to its dock, closing the loop autonomously.

**Key components and indicative specifications:**
- 1.2 m, ~30 kg biped; 23-27 DoF total; quasi-direct-drive electric geared actuators
- Two 1-motor-per-hand underactuated 3-finger grippers; 2 kg carry payload
- Stereo depth + dual fisheye cameras; IMU; joint torque sensing in legs
- Walking speed capped at 0.5 m/s indoors; ~2 h runtime; self-docking charge station
- Chest LED intent display; target retail in the used-car price band via commodity supply chain

**Primary use scenario:** A courier leaves a box at the door; the user, cooking, says "Mate, bring in the delivery." The robot announces "Going to the front door," its chest display showing a door icon and path arrow as it walks a slow, wide-berth route past the dog. It squats, conforms its fingers around the box, and carries it to the kitchen island, announcing each transition. Afterward it returns three stray mugs to the sink on a standing errand rule, then walks itself to its dock and reports battery status.

**Acceptance-oriented design choices:** Child-height stature with explicitly robotic (non-childlike) styling reads as physically non-threatening — it cannot loom. Every action is announced verbally and mirrored on the intent display, making behavior predictable and legible, the top-weighted B3 attribute. User-defined no-go zones are visualized in the companion app, and published monthly unedited task-milestone videos convert the "prove it, no staging" demand into the marketing engine.

**Feasibility notes:** Unitree G1 (~$16k) already proves the low-cost small-biped price curve; ZMP walking has been production-grade since ASIMO/HRP-4; underactuated adaptive hands are decades-mature (Robotiq-class); home SLAM is commodity robot-vacuum technology; LLM speech stacks are off-the-shelf. (~400 words)

---

Sanity check: all 9 concepts scored on the three criteria with justifications; top-3 selection follows totals with the C3 tie-break explicitly applied (FrontDesk Persona eliminated at 25 on C3 = 7 vs 9); each concept sheet contains all seven required sections in the exact prescribed order and falls within the 350-450-word band.
