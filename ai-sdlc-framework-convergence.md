# AI-SDLC: framework ไหนกำลังเป็น de facto standard และ interoperate กันยังไง?

> รายงานวิจัยเชิงลึก (deep research) — fan-out 5 มุม, ดึง 20 แหล่ง, สกัด 92 claims, ตรวจสอบแบบ adversarial 25 ข้อ (ยืนยัน 23, ตีตก 2)
> ข้อมูล ณ ช่วง พ.ย. 2025 – ก.ค. 2026 · จัดทำ 2026-07-11

---

## 🎯 คำตอบสั้น (TL;DR)

**ยังไม่มี framework ไหนกลายเป็น de facto standard** — ณ กลางปี 2026 สนามนี้กำลัง **แตกออก (fragmenting) มากกว่าจะรวมกัน (converging)**

แต่สัญญาณที่ชัดที่สุดคือ: **Spec-Driven Development (SDD)** กำลังกลายเป็น **"substrate/ชั้นฐานร่วม"** ที่เป็นจุดเริ่มต้น (entry point) ของแทบทุก vendor framework:

- Microsoft/GitHub วาง **Spec Kit** (~120,000 ⭐) ไว้หัวขบวนของ pipeline 5 สเตจ
- AWS **AI-DLC** ปล่อยออกมาเป็น spec/steering rules
- **specs.md** เอา AI-DLC ของ AWS ไป re-implement เป็น methodology แบบ pluggable

**ถ้าจะบอกว่าอะไร "ชนะ mindshare" — คือ *paradigm ของ spec-driven* ในฐานะภาษากลาง ไม่ใช่ framework ตัวใดตัวหนึ่ง หรือ standards body ใด**

> ⚠️ หลักฐานจาก analyst ที่เป็นกลางที่สุด (Thoughtworks Technology Radar Vol. 34) วาง SDD ไว้แค่วง **"Assess"** (ต่ำกว่า Trial/Adopt) และเตือนเรื่อง MCP — หักล้างทั้งทฤษฎี "มีตัวหนึ่งกำลังชนะ" และ "MCP คือ substrate interop"

---

## 📊 เปรียบเทียบ frameworks ทั้ง 5

| Framework | ประเภท | โครงสร้าง | สถานะ / adoption | ความเป็นกลาง |
|---|---|---|---|---|
| **V-Bounce** (Crowdbotics/arXiv) | Academic proposal | ดัดแปลง V-model, AI เป็น engine + คนเป็น validator | **บนกระดาษเท่านั้น** — ไม่พบหลักฐาน adoption จริง | เป็นกลาง (academic) |
| **AWS AI-DLC** | Vendor methodology (open-sourced) | 3 เฟส: Inception → Construction → Operations | ปล่อยเป็น Amazon Q Rules + Kiro Steering Files, tool-agnostic | Vendor (แต่ open) |
| **Microsoft/GitHub agentic pipeline** | Vendor pipeline | 5 สเตจ / 3 กลุ่ม (Plan&Code, Verify/Deploy, Operate) | รูปธรรมที่สุด, มี reference จริง | Vendor blog |
| **Phase-mapping (7-8 phases)** | Generic pattern | map AI tools เข้าแต่ละเฟส SDLC | เป็น pattern ทั่วไปในบทความ | บทความ/agency |
| **Spec-driven (Spec Kit / Kiro)** | ชั้น substrate ร่วม | specify → plan → tasks → implement | ⭐ **สัญญาณแรงที่สุด** (~120k stars) | ผสม |

---

## 1. Spec-Driven Development = "ชั้นฐานร่วม" (common substrate)

**นี่คือ finding สำคัญที่สุด** — SDD ไม่ใช่ framework เต็มรูปแบบ แต่เป็น **substrate/entry point** ที่ไป structure และ trigger flow ของ agent ปลายน้ำในทุก vendor framework

- Microsoft: *"Spec Kit really is the entry point that triggers the flow"* — วาง specification ไว้ตรงกลางของ engineering process
- specs.md: กรอบ Spec Kit/Kiro/OpenSpec/BMAD ว่าเป็นเครื่องมือ *"specification-focused"* ที่ยังไม่พอเป็น methodology สมบูรณ์ (*"specifications alone don't solve the fundamental problem"*)

> **ความหมาย:** SDD เป็นชั้นฐาน ไม่ใช่ framework — ทุกเจ้าเอามันมาต่อหัวขบวนของตัวเอง

**หลักฐาน adoption ที่แรงที่สุด:** GitHub **Spec Kit**
- ~119,505 ⭐ / ~10,594 forks (GitHub API, 2026-07-11), สร้าง ส.ค. 2025
- tool-agnostic ทำงานกับ AI coding agent **30+ ตัว** (official 42) — Copilot, Claude Code, Gemini, Codex, Cursor
- workflow: `specify → plan → tasks → implement` (ขยายเป็น 7-8 คำสั่ง รวม Constitution, Clarify, Analyze, Converge)

*(นี่วัด traction ของ paradigm spec-driven มากกว่า framework end-to-end ตัวใดตัวหนึ่ง)*

---

## 2. framework ต่าง ๆ compose กันยังไง

```
┌─────────────────────────────────────────────────────────────────┐
│  FRONT-END: Spec-Driven Development (substrate ร่วม)              │
│  Spec Kit / Kiro / OpenSpec / BMAD                                │
│  → specify → plan → tasks → constitution                          │
└───────────────────────────┬─────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│  MIDDLE: Agentic coding + review                                  │
│  Copilot coding agent / Claude Code / Cursor / Devin              │
│  → commits, PR, AI code-quality review                            │
└───────────────────────────┬─────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│  TAIL: Ops / SRE agents                                           │
│  Azure SRE Agent → เฝ้า telemetry → เปิด issue → ปิด loop        │
│  เชื่อมด้วย MCP (40+ connectors) ← แต่ยัง "contested"            │
└─────────────────────────────────────────────────────────────────┘
```

- **AWS AI-DLC** เป็น 3 เฟส (Inception → Construction → Operations) ที่ **open-source เป็น Q Rules + Kiro Steering Files** → ใช้ข้าม tool ได้ (Q Developer, Kiro, Cursor, Cline, Claude Code, Copilot)
  - Inception = business intent → requirements/stories/units ผ่าน "Mob Elaboration"
  - Construction = architecture/domain model/code/test ผ่าน "Mob Construction"
  - Operations = infrastructure-as-code + deployment ภายใต้การกำกับ
- **Microsoft/GitHub** = 5 สเตจ (Spec Kit → Copilot agent → Code Quality → GitHub Actions → Azure SRE Agent) จัดเป็น 3 กลุ่ม โดย SRE Agent **ปิด loop** กลับไปหา coding agent ผ่าน GitHub issues

---

## 3. MCP (Model Context Protocol) — interop layer ที่ยัง "ถกเถียง"

MCP เกี่ยวข้องกับ interoperability จริง แต่ **ยังไม่ใช่ substrate ที่ตกลงกันได้**

| มุมมอง | จุดยืน |
|---|---|
| **Microsoft (สนับสนุน)** | Azure SRE Agent เชื่อม observability/DevOps/incident/code ผ่าน MCP (*"avoids lock-in"*) — 40+ connectors |
| **Thoughtworks (เตือน)** | วาง *"MCP by default"* ไว้วง **Caution** — *"every protocol layer between an agent and an API loses fidelity"* (อ้าง Simon Willison ว่า CLI tool มักแทน MCP ได้) |

> **สรุป:** MCP เป็น "ตัวเลือก" interop ที่ใช้ได้จริง แต่ยังไม่ใช่มาตรฐานที่ settle แล้ว

---

## 4. จุดที่ frameworks ขัดแย้งกันจริง (genuine disagreement)

สนามกำลัง **แตกเป็น 2 ค่าย** (ตาม Thoughtworks Radar Vol. 34: *"Two broad camps are emerging"*):

1. **ค่าย minimal-structure** — พึ่ง agent เป็นหลัก, spec เบา
2. **ค่าย defined-workflow** — spec ละเอียด, workflow ชัด

ประเด็นที่เห็นต่างกัน:
- **ความเข้มงวดของ spec** — Tessl มองว่า spec คือ artifact ที่ต้อง maintain / Kiro ใช้ markdown แบบ spec-first เป็นสเตจ / Spec Kit เพิ่ม "constitution"
- **Tool-agnostic vs vendor lock-in** — OpenSpec (iterative, tool-agnostic) ปะทะ Kiro (ผูก IDE เฉพาะ) และ BMAD (หนัก, rigid)
- **Greenfield vs brownfield** — เหมาะกับงานใหม่หรืองานเก่าต่างกัน

**สถานะ maturity:** Thoughtworks วาง SDD + Spec Kit ไว้วง **"Assess"** (ต่ำกว่า Trial/Adopt) — *"Several of our teams are experimenting... mostly in brownfield environments"* → ยังเป็น early-stage ไม่ converged

---

## 5. มีมาตรฐานกลาง (standards body) กำลังเกิดไหม?

**ยังไม่มี** standards body ที่กำหนด operating model:
- **Forbes/Forrester** ตั้งชื่อ category *"Agentic Software Development"* แต่ไม่ prescribe operating model — แค่ตั้งคำถาม (*"งานไหนควร delegate ให้ agent vs คนทำ?"*)
- คำเรียกต่าง ๆ (AWS AI-DLC, Forrester ASD, Microsoft pipeline, V-Bounce) อยู่ร่วมกันโดยไม่มี spec รวม
- มีสัญญาณ third-party re-implement: **specs.md** เอา AI-DLC ไปแพ็กเป็น 1 ใน 3 flow (Simple, FIRE, AI-DLC) — แต่เป็นข้อมูลจุดเดียว (โปรเจกต์เล็ก), เป็น *สัญญาณ* ไม่ใช่ *หลักฐาน adoption กว้าง*

---

## 🔭 เจาะลึก: มุมมองของ Thoughtworks (Technology Radar Vol. 34)

> **ทำไมสำคัญ:** แหล่ง primary ส่วนใหญ่เป็น vendor blog (Microsoft, AWS, GitHub) ที่โปรโมตของตัวเอง — **Thoughtworks Technology Radar เป็น analyst อิสระเจ้าเดียว** ที่ประเมินเป็นกลาง (ไม่มี Gartner MQ / Forrester Wave ครอบคลุมเรื่องนี้) จึงเป็น "ตัวถ่วงดุล" กับคำโฆษณาของ vendor

### 1. 🟡 วาง Spec-Driven Development ไว้แค่วง "Assess" (ยังไม่สุก)

> *"Ring: Assess — Worth exploring to understand enterprise impact"*
> *"Several of our teams are experimenting with spec-driven practices using GitHub Spec Kit, mostly in brownfield environments."*

- **"Assess" = วงต่ำสุดเชิงความพร้อม** (ต่ำกว่า Trial และ Adopt) → "น่าลองเพื่อทำความเข้าใจ" ไม่ใช่ "พร้อมใช้จริง"
- ทีมของเขาแค่ **"ทดลอง" (experimenting)** ยังไม่ adopt เต็มตัว
- **นัยสำคัญ:** ตอกย้ำว่าสนามยัง early-stage ไม่ converged — ขัดกับภาพที่ vendor วาดว่ามันพร้อมแล้ว

### 2. 🔀 มอง SDD กำลัง "แตกเป็น 2 ค่าย" (fragmenting)

> *"Two broad camps are emerging: teams that rely on the continually improving capabilities of coding agents with minimal structure, and those that favor defined workflows and detailed specifications."*

| ค่าย A | ค่าย B |
|---|---|
| **พึ่ง coding agent เป็นหลัก** โครงสร้างน้อย (minimal structure) | **เน้น workflow ชัด + spec ละเอียด** |

→ หลักฐานหลักที่บอกว่าสนาม **แตกออก ไม่ได้รวมกัน**

### 3. 🧩 เครื่องมือแต่ละตัว "ตีความ SDD ต่างกัน" (distinct interpretations)

| เครื่องมือ | ลักษณะเฉพาะ | เหมาะกับ |
|---|---|---|
| **Spec Kit** (GitHub) | workflow ละเอียด มี "**constitution**" (rulebook พื้นฐาน) | greenfield |
| **Kiro** (AWS) | spec-first markdown, **ผูก IDE เฉพาะ** (vendor lock-in) | — |
| **Tessl** | มอง spec เป็น artifact ที่ต้อง maintain ตลอด | — |
| **OpenSpec** | **iterative + tool-agnostic** (เบา ยืดหยุ่น) | brownfield |
| **BMAD** | หนัก, workflow เข้มงวด (rigid) | — |

> ข้อสังเกต: SDD framework ส่วนใหญ่ (เช่น Spec Kit) **เหมาะกับ greenfield มากกว่า brownfield** — แต่ทีม Thoughtworks กลับใช้ในงาน brownfield เป็นหลัก ซึ่งเป็นความตึงที่น่าจับตา

### 4. ⚠️ เตือนเรื่อง MCP — วาง "MCP by default" ไว้วง "Caution"

> *"We caution against using MCP by default... every protocol layer between an agent and an API loses fidelity."*
> อ้าง **Simon Willison**: *"almost everything I might achieve with an MCP can be handled by a CLI tool instead."*

- **"Caution" = วงเตือน** ("ระวังในการใช้")
- เหตุผล: ทุกชั้น protocol ที่คั่นระหว่าง agent กับ API ทำให้ **สูญเสีย fidelity** ("abstraction tax")
- **นัยสำคัญ:** หักล้างทฤษฎี "MCP คือ substrate สำหรับ interoperability" โดยตรง — Microsoft เชียร์ MCP แต่ Thoughtworks บอกว่าบ่อยครั้ง **CLI tool ธรรมดาก็แทนได้**

### 🎯 สรุปจุดยืน Thoughtworks (หนึ่งย่อหน้า)

Thoughtworks มองว่า AI-SDLC/spec-driven **ยังเป็นของ "น่าลอง" ไม่ใช่ "พร้อมใช้"** (Assess ring), สนามกำลัง **แตกเป็น 2 ค่าย** และเครื่องมือแต่ละตัว **ตีความไปคนละทาง** — ไม่ได้ converge สู่มาตรฐานเดียว, พร้อมกับ **เตือนไม่ให้ใช้ MCP เป็นค่าเริ่มต้น** เพราะเพิ่มความซับซ้อนโดยไม่จำเป็น มุมมองนี้เป็น "ตัวถ่วงดุล" สำคัญต่อความคึกคักของ vendor — คือ **ให้ระวัง อย่าเพิ่งเชื่อว่ามันสุกงอมแล้ว**

> 📝 หมายเหตุ: claim "สองค่าย" และวันที่ Radar (พ.ย. 2025 vs เม.ย. 2026) มี vote 2-1 (ไม่เอกฉันท์); Radar เองยอมรับว่ามี convergence *บางส่วน* ที่ loop `spec → plan → implement` — เป็น counter-signal เล็ก ๆ

---

## 🆕 UPDATE: Tech Radar เวอร์ชันล่าสุด (Vol. 34, เมษายน 2026)

> อัปเดต 2026-07-11 — ดึงจากหน้า Thoughtworks โดยตรง
> **แก้ไขวันที่:** รายงานเดิมปน "Vol. 34 Nov 2025/Apr 2026" — ที่ถูกคือ **Vol. 33 = พ.ย. 2025, Vol. 34 = เม.ย. 2026 (ล่าสุด)** · ยังไม่มี Vol. 35

**สรุป: มุมมองไม่ได้อ่อนลง — กลับระวังมากขึ้น**

### สถานะยังเหมือนเดิม — SDD ยังอยู่วง "Assess"
ผ่านมา 2 รอบ (Vol. 33 → Vol. 34) spec-driven development **ยังไม่ขยับขึ้น Trial/Adopt** = ยังไม่สุก

### ⚠️ ข้อกังวลใหม่ที่เพิ่มเข้ามา
- workflow ยัง **"elaborate and opinionated"** (ซับซ้อนเกิน + มีความเห็นฝังมาเยอะ)
- สร้าง **"lengthy spec files that are hard to review"** (ไฟล์ spec ยาวจนรีวิวยาก)
- **ไม่ชัดว่าใครคือผู้ใช้เป้าหมาย** (unclear intended users)
- 🔑 *"teams may be relearning a bitter lesson — that handcrafting detailed rules for AI ultimately doesn't scale"* (การนั่งเขียนกฎละเอียดให้ AI สุดท้ายไม่ scale)

### 🎯 ธีมใหญ่ 4 ข้อของ Vol. 34
1. **Retaining principles, relinquishing patterns** — เก็บหลักการวิศวกรรม (zero trust, DORA) ทิ้ง pattern เก่า
2. **Securing permission-hungry agents** — agent หิว permission → ต้อง sandbox + defense in depth
3. **"Putting coding agents on a leash"** — คุม agent ด้วย **harness**: feedforward (Agent Skills + **spec-driven development**) + feedback (mutation testing) ← SDD ถูกจัดเป็น "สายจูง" ตัวหนึ่ง
4. **Evaluating technology in an agentic world** — tool โผล่เร็วจน assess ยาก

### 🆕 แนวคิด/สัญญาณใหม่
- **Cognitive Debt** — AI สร้างโค้ดเยอะขึ้น → ช่องว่างระหว่าง dev กับระบบถ่างออก
- **Semantic Diffusion** — ศัพท์ใหม่ (spec-driven, harness engineering) เกิดเร็วกว่าความหมายจะนิ่ง → สับสน
- **OpenSpec** ถูกยกเด่นขึ้น (workflow เบา: `propose → apply → archive`) — ตอกย้ำค่าย "minimal/tool-agnostic"
- CTO **Rachel Laycock**: *"The inflection point isn't so much about technology — it's about technique"* (จุดเปลี่ยนไม่ใช่เรื่องเทคโนโลยี แต่เป็นเรื่องเทคนิค/วินัยวิศวกรรม)

### 💡 นัยต่อคำถามหลัก
Radar ล่าสุดยิ่ง **ตอกย้ำว่ายังไม่ converge** — และเสริมมุมใหม่ว่า *ความเสี่ยงไม่ใช่แค่ "ยังไม่มีมาตรฐาน" แต่คือ "cognitive debt + semantic diffusion"* ที่ทำให้แม้แต่การประเมินว่าอะไรดีก็ยากขึ้น จุดยืนหลักของ Thoughtworks: **AI เร่งความเร็ว แต่ยิ่งต้องกลับไปหา engineering fundamentals** ไม่ใช่วิ่งตาม framework/tool ใหม่

*แหล่ง: [Spec-driven development — TW Radar](https://www.thoughtworks.com/en-us/radar/techniques/spec-driven-development) · [Radar Vol. 34 news release](https://www.thoughtworks.com/about-us/news/2026/combat-ai-cognitive-debt-radar-v34)*

---

## ⚠️ ข้อควรระวัง (caveats)

1. **แหล่ง primary ส่วนใหญ่เป็น vendor/marketing blog** (Microsoft, AWS, GitHub) — เชื่อถือได้ว่า "แต่ละเจ้าอธิบายอะไร" แต่ไม่ใช่หลักฐานกลางเรื่อง adoption จริง
2. **แหล่ง analyst อิสระจริงมีแค่ Thoughtworks Radar** — **ไม่มี** Gartner Magic Quadrant หรือ Forrester Wave ที่ครอบคลุม category AIDLC รวม (claim ที่บอกว่ามี ถูกตีตก 0-3) → การ triangulate ข้าม analyst จึงบาง
3. **ข้อมูลเปลี่ยนเร็วมาก** — star count, ring placement, tool list เปลี่ยนรายเดือน (Spec Kit integration โต 17→42)
4. **V-Bounce เป็น proposal บนกระดาษ** — ไม่พบหลักฐาน adoption
5. **ข้อสรุป "winning mindshare" อิงจาก star count ของ Spec Kit** + การที่มันโผล่เป็น entry point ซ้ำ ๆ → วัด traction ของ *paradigm* มากกว่า framework end-to-end ตัวเดียว
6. claim เรื่อง "สองค่าย" และวันที่ Radar มี vote แบบ 2-1 (ไม่เอกฉันท์); Radar ยังบอกว่ามี convergence บางส่วนที่ loop `spec→plan→implement` — เป็น counter-signal

### ❌ Claims ที่ถูกตีตก (refuted)
- *"AI-DLC วางตัวเป็นตัวแทน (replacement) ของ SDLC แบบ human-centric เดิม"* — ตีตก 1-2
- *"ไม่มี Gartner MQ / Forrester Wave ครอบคลุม AIDLC เป็น construct เดียว"* — ตีตก 0-3

---

## ❓ คำถามที่ยังเปิดอยู่

1. จะมี standards body เป็นกลาง (Linux Foundation, OpenSSF, แบบ W3C) เกิดขึ้นไหม หรือ de facto จะมาจาก vendor (Spec Kit open-source) เท่านั้น?
2. สองค่าย spec-driven (minimal vs detailed) จะรวมกันไหม และ loop `spec→plan→tasks→implement` เป็น substrate ที่ converge จริงหรือไม่ แม้ตีความ tool ต่างกัน?
3. ชั้น interop ไหนจะชนะจริง — MCP, CLI tools, หรือ vendor-native connectors? (Thoughtworks เตือน "MCP by default")
4. adoption จริงระดับ production (ไม่ใช่แค่ทดลอง) ของ AWS AI-DLC และ Microsoft/GitHub pipeline ลึกแค่ไหน — ในเมื่อไม่มีข้อมูลตลาดเชิงปริมาณจาก Gartner/Forrester?

---

## 📚 แหล่งอ้างอิงหลัก

| แหล่ง | ประเภท |
|---|---|
| Thoughtworks Technology Radar Vol. 34 (PDF + SDD page) | primary/secondary (analyst อิสระ) |
| arXiv 2408.03416 — "The AI-Native SDLC" (Cory Hymel, Crowdbotics) | primary (academic) |
| AWS DevOps Blog — AI-DLC + open-sourcing AI-DLC + awslabs/aidlc-workflows | primary (vendor) |
| Microsoft Tech Community — agentic SDLC + Azure SRE Agent | primary (vendor) |
| github/spec-kit + integrations reference | primary |
| martinfowler.com — SDD 3 tools (Birgitta Böckeler) | blog |
| specs.md — methodology/sdlc-reimagined + vs-kiro | blog |
| augmentcode, reenbit, dev.to, zenn.dev | blog (contrarian/tooling) |

---

*หมายเหตุ: Cognition ซื้อ Windsurf ธ.ค. 2025 และกำลังรวมเข้า Devin กลางปี 2026 — รายละเอียด tool อาจเปลี่ยน*
