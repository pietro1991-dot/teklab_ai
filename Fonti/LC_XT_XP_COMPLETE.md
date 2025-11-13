---
category: Level_Switches
keywords:
- LC-XT
- LC-XP
- LC-XT 46 bar
- LC-XP 120 bar
- EN175301-803A connector
- industrial connector
- optical level switch
- two-part design
- stainless steel housing
- replaceable electronics
- corrosion resistant
- quick disconnect
- harsh environment
- G3/8 thread
- 9.4mm connector
language: EN
product: LC_XT_XP
document_type: unified_complete
last_updated: 2025-11-15
---

# LC-XT / LC-XP - Complete Product Documentation

**Optical Level Switches with Industrial EN175301-803A Connector**

---

## 📋 Document Structure

This unified document covers the complete LC-XT and LC-XP product family organized in the following sections:

1. **Product Family Overview** - Description, variant comparison, operating principle
2. **Detection Technology & Features** - Optical sensor, two-part design, stainless steel construction
3. **Technical Specifications** - Electrical, mechanical, environmental specs
4. **Applications & Selection** - Use cases and variant selection guide
5. **Installation & Service** - Mounting, wiring, dimensions, maintenance
6. **FAQ** - Frequently asked questions

---

## 1. PRODUCT FAMILY OVERVIEW

### LC-XT / LC-XP Series Description

The **LC-XT** (46 bar) and **LC-XP** (120 bar) are optical level switches designed for industrial applications requiring EN175301-803A connector and enhanced corrosion resistance. These two-part units provide reliable liquid presence/absence detection with stainless steel housing, revolutionary replaceable electronics, and quick-disconnect industrial connector.

**⚠️ IMPORTANT: LC-XT/LC-XP are LEVEL SWITCHES ONLY - They do NOT include a solenoid valve.**
- For automatic oil level regulation with integrated valve, see **TK3+** or **TK4** series.
- LC-XT/LC-XP provide detection signal only (require external control for automated actions).

**Core Technology:**
- Electro-optic infrared sensor (fused glass hermetic seal)
- Solid-state output (NO or NC, 100mA max)
- Two-part serviceable design (electronics replaceable without depressurization)
- **EN175301-803A connector** (DIN 43650 size A industrial standard)
- **Stainless steel housing** (enhanced corrosion resistance)
- **Extended temperature range** (-40°C to +125°C media temp, both variants)
- Factory calibrated, plug-and-play operation

**Product Family:**

| Model | Max Pressure | Media Temp | Primary Applications | Key Features |
|-------|-------------|------------|---------------------|--------------|
| **LC-XT** | 46 bar | -40°C to +125°C | Standard refrigeration with industrial connector | EN175301-803A, stainless steel |
| **LC-XP** | 120 bar | -40°C to +125°C | CO2 transcritical, high-pressure with industrial connector | EN175301-803A, stainless steel, 120 bar rated |

**Key Differentiators:**
- **vs LC-PS/LC-PH**: LC-XT/XP have EN175301-803A connector + stainless steel, LC-PS/PH have cable + nickel-plated steel
- **vs LC-PS**: LC-XT is 46 bar with extended temp (-40°C to +125°C), LC-PS is 46 bar standard temp (-40°C to +85°C)
- **vs LC-PH**: LC-XP is 120 bar with EN175301-803A connector, LC-PH is 120 bar with cable/M12 connector
- **vs TK1+**: LC-XT/XP are 100mA solid-state output, TK1+ has 2A relay output with LED indication
- **vs TK3+/TK4**: LC-XT/XP are detection only (no valve), TK3+/TK4 are complete regulators with valve

**Selection Criteria:**
- **LC-XT (46 bar)**: Standard refrigeration ≤ 46 bar + industrial connector + extended temperature
- **LC-XP (120 bar)**: High-pressure 46-120 bar (CO2 transcritical) + industrial connector
- **Both**: Stainless steel housing for harsh environments, quick-disconnect connector required

**Primary Applications:**
- Industrial refrigeration with connector-based monitoring systems
- CO2 transcritical systems requiring industrial connectors (LC-XP)
- Harsh environments requiring stainless steel corrosion resistance
- Quick-disconnect applications for fast sensor replacement
- PLC/BMS integration with standardized industrial connectors

**Operating Principle:**

Both LC-XT and LC-XP use electro-optic infrared detection through a fused glass dome:

1. **In Air (liquid not present)**:
   - Infrared LED emits light into fused glass dome
   - Light reflects internally (total internal reflection)
   - Optical receiver detects reflected light
   - Output state: Depends on factory configuration (NO or NC in air)

2. **In Liquid (liquid present)**:
   - Liquid contacts fused glass dome
   - Light escapes into liquid (refractive index change)
   - Optical receiver detects loss of reflected light
   - Output state: Changes from air state (NO→closed, NC→open)

3. **Response Time**: < 1 second (virtually instantaneous)

**Advantages Over Cable Models (LC-PS/LC-PH):**
- Quick-disconnect connector (faster sensor replacement, no wire stripping)
- Standardized industrial connector (interchangeable with other sensors)
- Stainless steel housing (better corrosion resistance in harsh environments)
- Cleaner installation (no cable routing, direct connection to mating connector)

---

## 2. DETECTION TECHNOLOGY & FEATURES

### 2.1 Electro-Optic Infrared Sensor

**Detection Method:**
- **Infrared LED emitter**: Generates infrared light into fused glass dome
- **Optical receiver**: Detects reflected light intensity
- **Refractive index principle**: Light behavior changes at glass/liquid interface
- **Digital threshold**: Clean ON/OFF switching (no analog drift)

**Sensor Advantages:**
- **Response time**: < 1 second (instantaneous detection)
- **Reliability**: MTTF > 50,000 hours (5.7+ years continuous)
- **No calibration**: Factory calibrated, no field adjustment needed
- **No wetted electronics**: Sensor electronics isolated from media by fused glass
- **Pressure rated**: 46 bar (LC-XT) or 120 bar (LC-XP)

**Fused Glass Hermetic Seal:**
- **Glass-to-metal fusion**: Molecular-level seal (NOT O-ring)
- **Zero leakage**: 10^-12 mbar·L/s (true hermetic)
- **Chemically inert**: Compatible with all oils and refrigerants
- **Pressure rated**: 46 bar (LC-XT) or 120 bar (LC-XP) maximum working pressure
- **Temperature rated**: -40°C to +125°C media temperature (extended range, both variants)
- **Lifetime seal**: No degradation, no maintenance

**Output Signal:**
- **Type**: Solid-state semiconductor output (NOT mechanical relay)
- **Current rating**: 100mA maximum (suitable for PLC inputs, low-power relay coils)
- **Configuration**: NO (Normally Open in air) or NC (Normally Closed in air) - factory-set
- **Voltage**: Matches supply voltage (24VAC/DC, 115VAC, 230VAC)

**Important Output Notes:**
- **Factory-configured**: NO or NC output cannot be changed in field (order correct version)
- **NO in air**: Output OPEN when air, CLOSES when liquid detected (high-level alarms)
- **NC in air**: Output CLOSED when air, OPENS when liquid detected (low-level alarms, fail-safe)

### 2.2 Two-Part Revolutionary Design

**Part 1: Sensor Housing (Permanent Pressure Boundary)**
- **Components**: Fused glass dome, stainless steel (or nickel-plated steel) body, adapter threads
- **Function**: Pressure containment, liquid detection surface
- **Installation**: Permanent (remains on equipment during service)
- **Pressure rating**: 46 bar (LC-XT) or 120 bar (LC-XP) maximum
- **Temperature rating**: -40°C to +125°C media temperature
- **Material**: Stainless steel (enhanced corrosion resistance)
- **Service**: Only removed for complete sensor replacement (rare)

**Part 2: Electronic Module (Replaceable Without Depressurization)**
- **Components**: Infrared LED, optical receiver, power supply, output driver, stainless steel housing
- **Function**: Detection electronics and signal processing
- **Connector**: EN175301-803A (DIN 43650 size A) on top of module
- **Installation**: Hand-screw onto sensor housing (finger-tight, no tools)
- **Service**: Replaceable in 5-10 minutes without system depressurization
- **Advantages**: Minimal downtime, no refrigerant recovery, no leak risk, quick-disconnect

**Service Procedure (Electronic Module Replacement):**
1. Disconnect mating connector from EN175301-803A connector
2. Disconnect power (lockout/tagout)
3. Hand-unscrew electronic module from sensor housing (no tools)
4. Install new electronic module (hand-screw, finger-tight)
5. Reconnect mating connector
6. Restore power and verify operation

**Time**: 5-10 minutes  
**Cost**: Electronic module replacement vs complete sensor assembly (50-60% cost savings)  
**Downtime**: Minimal (no depressurization, no refrigerant recovery, quick-disconnect)

### 2.3 Stainless Steel Construction

**Housing Materials:**
- **Sensor housing**: Stainless steel (or nickel-plated steel on some models) - 46 bar (LC-XT) or 120 bar (LC-XP) rated
- **Electronic module**: Stainless steel housing (enhanced corrosion resistance)
- **Fused glass dome**: Borosilicate glass (chemically inert, pressure rated)
- **IP65 enclosure**: Dust-tight, water jet protected

**Stainless Steel Advantages:**
- **Enhanced corrosion resistance**: Better than nickel-plated steel in harsh environments
- **Long-term durability**: Resistant to salt spray, moisture, chemicals
- **Outdoor installations**: Suitable for exposed locations (coastal areas, rooftops, wash-down areas)
- **Industrial environments**: Chemical plants, food processing, marine applications

**Reliability Features:**
- **No moving parts**: Eliminates mechanical failure modes (floats, reeds, linkages)
- **Solid-state electronics**: No relay contacts to wear or stick
- **Hermetic seal**: No O-rings or gaskets to degrade
- **Transient protection**: Built-in over-voltage protection (power surges, lightning)

**Environmental Protection:**
- **IP65 rating**: Outdoor/indoor installations, wash-down areas
- **Media temperature**: -40°C to +125°C (extended range, both LC-XT and LC-XP)
- **Ambient temperature**: -40°C to +60°C
- **Humidity**: 5-95% RH non-condensing

**Refrigerant & Oil Compatibility:**
- **All HFC/HCFC/CFC**: R134a, R404A, R407C, R410A, R22, R502, etc.
- **CO2 (R744)**: Subcritical (LC-XT up to 46 bar), Transcritical (LC-XP up to 120 bar)
- **Ammonia (NH3)**: Fully compatible (stainless steel ideal for ammonia systems)
- **Hydrocarbons (HC)**: R290, R600a, etc.
- **Low-GWP**: R1234yf, R1234ze, R452A, R454B, etc.
- **All oils**: Mineral, POE, PVE, PAG, AB (fused glass chemically inert)

### 2.4 EN175301-803A Industrial Connector

**Connector Specifications:**
- **Standard**: EN175301-803A (also known as DIN 43650 size A)
- **Type**: 3-pin + ground (4-position total)
- **Location**: Top of electronic module
- **Rating**: IP65 when mated with compatible connector
- **Advantages**: Industry standard, quick-disconnect, interchangeable

**Pinout:**
- **Pin 1**: Power supply (+)
- **Pin 2**: Output signal
- **Pin 3**: Ground/Common (-)
- **Pin 4 (ground)**: Chassis ground (optional)

**Mating Connector:**
- **Source**: Order separately from electrical supply houses (Lumberg, Phoenix Contact, Hirschmann, etc.)
- **Compatibility**: Standard EN175301-803A mating connectors from any manufacturer
- **Cable**: Mating connector with integrated cable (various lengths available)
- **IP rating**: Verify IP65/IP67 rated mating connector for outdoor use

**Connector Advantages:**
- **Quick-disconnect**: No wire stripping, termination, or conduit required
- **Standardized**: Interchangeable with other industrial sensors
- **Faster installation**: Plug-and-play (vs cable termination)
- **Cleaner appearance**: No loose cables, junction boxes
- **Easier service**: Unplug mating connector, replace sensor, reconnect

### 2.5 Electrical Features

**Power Supply:**
- **Voltage options**: 24VAC/DC ±10%, 115VAC ±10% @ 60Hz (on request), 230VAC ±10% @ 50Hz
- **Frequency**: 50/60 Hz (AC models)
- **Power consumption**: 20mA max during normal operation (ultra-low power)
- **Inrush current**: Minimal (no relay coil)

**Electrical Protection:**
- **Transient over-voltage protection**: Built-in (power surges, lightning)
- **Reverse polarity protection**: Internal (24VDC models)
- **Output short-circuit protection**: Current-limited to 100mA

**Customizable Delays (Available on Request):**
- **Activation delay**: Prevents false alarms from turbulence, foam, bubbles (typical 5-30 seconds)
- **Deactivation delay**: Filters transient liquid contact (typical 1-10 seconds)
- **Factory-programmed**: Specify delay requirements at order

### 2.6 Installation & Adapters

**6 Adapter Options:**

| Adapter Type | Thread | B Dimension (mm) | Typical Application |
|-------------|--------|------------------|---------------------|
| **1/2" NPT** | 1/2" NPT male | 24 | Most common tank/vessel port |
| **3/4" NPT** | 3/4" NPT male | 22 | Larger receiver/separator ports |
| **1" NPT** | 1" NPT male | 27.9 | High-flow applications |
| **M20×1.5** | M20×1.5 male | 18.1 | European compressors (metric, shortest) |
| **1" 1/8 UNEF** | 1" 1/8-12 UNEF male | 19 | Compressor service port direct mount |
| **1" 1/4 RLK** | 1" 1/4 RLK male | 30 | Rotalock valve ports (longest) |

**B Dimension** = Projection from mounting surface to end of adapter (sensor housing base)

**Adapter Installation:**
- **Torque**: 50 N·m (critical for sealing)
- **Sealant**: PTFE tape or liquid thread sealant per equipment guidelines
- **Orientation**: Typically vertical (sensor pointing downward, connector on top for easy access)

---

## 3. TECHNICAL SPECIFICATIONS

### 3.1 Electrical Specifications

| Parameter | Specification |
|-----------|--------------|
| **Supply Voltage** | 24VAC/DC ±10% OR 115VAC ±10% @ 60Hz (on request) OR 230VAC ±10% @ 50Hz |
| **Supply Frequency** | 50/60 Hz (AC models) |
| **Supply Current** | 20mA max during normal operation |
| **Output Signal** | Solid-state output, NO or NC in air (factory-configured) |
| **Output Max Current** | 100mA maximum |
| **Output Voltage** | Matches supply voltage (24V, 115V, or 230V) |
| **Electronic Protections** | Transient over-voltage protection, reverse polarity (24VDC) |
| **Electrical Connection** | EN175301-803A connector (DIN 43650 size A) |

### 3.2 Mechanical Specifications

| Parameter | LC-XT | LC-XP |
|-----------|-------|-------|
| **Housing Material** | Stainless steel / Nickel-plated steel | Stainless steel / Nickel-plated steel |
| **Sensor Dome** | Fused glass (hermetic seal, 46 bar rated) | Fused glass (hermetic seal, 120 bar rated) |
| **Enclosure Protection** | IP65 (dust-tight, water jet protected) | IP65 (dust-tight, water jet protected) |
| **Adapter Torque** | 50 N·m for adapter installation | 50 N·m for adapter installation |
| **Sensor Assembly** | Hand-screw (finger-tight, no tools) | Hand-screw (finger-tight, no tools) |
| **Weight** | ~400-450g total assembly | ~400-450g total assembly |

### 3.3 Environmental & Pressure Specifications

| Parameter | LC-XT | LC-XP |
|-----------|-------|-------|
| **Media Temperature** | -40°C to +125°C (extended) | -40°C to +125°C (extended) |
| **Ambient Temperature** | -40°C to +60°C | -40°C to +60°C |
| **Max Working Pressure** | **46 bar** | **120 bar** |
| **Humidity** | 5-95% RH non-condensing | 5-95% RH non-condensing |
| **Vibration** | IEC 60068-2-6 compliant | IEC 60068-2-6 compliant |

### 3.4 Performance Specifications

| Parameter | Specification |
|-----------|--------------|
| **Response Time** | < 1 second |
| **Repeatability** | ± 1mm |
| **Reliability** | MTTF > 50,000 hours (5.7+ years continuous) |
| **Calibration** | Factory calibrated (no field calibration required) |
| **Hermetic Seal** | 10^-12 mbar·L/s (fused glass-to-metal) |

### 3.5 Compliance

| Standard | Description |
|----------|-------------|
| **2014/30/UE** | EMC Directive (Electromagnetic Compatibility) |
| **2014/35/UE** | Low Voltage Directive |
| **CE Marking** | Compliant and certified |
| **IP Rating** | IP65 (dust-tight, water jet protected) |

### 3.6 Dimensions

**Adapter Dimensions (Projection from Mounting Surface):**

| Adapter Type | B Dimension (mm) |
|-------------|------------------|
| 1/2" NPT | 24 |
| 3/4" NPT | 22 |
| 1" NPT | 27.9 |
| M20×1.5 | 18.1 (shortest) |
| 1" 1/8 UNEF | 19 |
| 1" 1/4 RLK | 30 (longest) |

**Total Assembly Height:**
- **Total height** (from mounting surface to top of EN175301-803A connector): ~139.2mm
- **Components**: Adapter (18-30mm) + Sensor housing (~70-90mm) + Electronic module (~40mm) + Connector (~10mm)

**Installation Clearances:**
- **Top access**: 150-175mm above mounting surface for mating connector + cable routing
- **Side access**: 60-80mm radial clearance for connector mating/unmating
- **Cable routing**: Allow space for mating connector cable exit (varies by cable orientation)

### 3.7 Refrigerant & Oil Compatibility

**Compatible Refrigerants:**
- All HFC, HCFC, CFC refrigerants (R134a, R404A, R407C, R410A, R22, R502, etc.)
- **CO2 (R744)**: LC-XT subcritical (up to 46 bar), LC-XP transcritical (up to 120 bar)
- **Ammonia (NH3)**: Fully compatible (stainless steel ideal)
- Hydrocarbons (HC): R290, R600a, etc.
- Low-GWP refrigerants: R1234yf, R1234ze, R452A, R454B, etc.

**Compatible Oils:**
- Mineral oil
- POE (Polyolester)
- PVE (Polyvinylether)
- PAG (Polyalkylene glycol)
- AB (Alkylbenzene)

**Note**: Fused glass dome is chemically inert and compatible with all refrigerants and oils.

---

## 4. APPLICATIONS & SELECTION GUIDE

### 4.1 Primary Applications

**Industrial Refrigeration with Connector-Based Systems:**
- PLC/BMS integration requiring standardized industrial connectors
- Multi-sensor installations (quick-disconnect for maintenance)
- Harsh environments (stainless steel corrosion resistance)
- Food processing plants (wash-down areas, IP65 rated)

**CO2 Transcritical Systems (LC-XP):**
- Gas cooler outlet level monitoring (90-110 bar, EN175301-803A connector)
- High-pressure receiver level alarms (80-100 bar)
- Flash gas separator level control (70-90 bar)

**Ammonia Systems:**
- High-pressure receiver level monitoring (stainless steel for ammonia compatibility)
- Oil separator level detection
- Economizer level control

**Outdoor/Exposed Installations:**
- Rooftop units (stainless steel, IP65 rated)
- Coastal areas (salt spray resistance)
- Chemical plants (corrosive atmosphere resistance)

### 4.2 Variant Selection Guide

**LC-XT (46 bar) vs LC-XP (120 bar):**

| Criteria | LC-XT (46 bar) | LC-XP (120 bar) |
|----------|---------------|-----------------|
| **Pressure** | ≤ 46 bar | 46-120 bar |
| **Applications** | Standard refrigeration + connector | CO2 transcritical + connector |
| **Temperature** | -40°C to +125°C | -40°C to +125°C |
| **Connector** | EN175301-803A | EN175301-803A |
| **Housing** | Stainless steel | Stainless steel |
| **Cost** | Lower | Higher (~30% more) |

**Decision Tree:**

```
START
│
├─ Pressure ≤ 46 bar? ──YES──> LC-XT (46 bar)
│   └─NO (46-120 bar)
│
├─ Pressure 46-120 bar? ──YES──> LC-XP (120 bar)
│   └─NO (> 120 bar - contact Teklab)
│
├─ Industrial connector required? ──YES──> LC-XT or LC-XP
│   └─NO (cable preferred)
│
├─ Stainless steel housing required? ──YES──> LC-XT or LC-XP
│   └─NO (nickel-plated sufficient)
│
└─> LC-XT (46 bar) or LC-XP (120 bar) - choose based on pressure
```

### 4.3 LC-XT/XP vs Other Level Switches

| Feature | LC-PS | LC-PH | **LC-XT** | **LC-XP** | TK1+ |
|---------|-------|-------|-----------|-----------|------|
| **Pressure** | 46 bar | 120 bar | **46 bar** | **120 bar** | 46/100 bar |
| **Media Temp** | -40 to +85°C | -40 to +125°C | **-40 to +125°C** | **-40 to +125°C** | -40 to +85°C |
| **Output** | 100mA | 100mA | **100mA** | **100mA** | 2A relay |
| **Connection** | 1m cable | 1m cable/M12 | **EN175301-803A** | **EN175301-803A** | Cable glands |
| **Housing** | Nickel-plated | Nickel-plated | **Stainless steel** | **Stainless steel** | Nickel-plated |
| **Relative Cost** | Lowest | Medium | Medium-High | High | Medium |

**Choose LC-XT/XP when**:
- Industrial EN175301-803A connector required
- Stainless steel housing for harsh environments
- Quick-disconnect for maintenance efficiency
- Extended temperature range (-40°C to +125°C)
- PLC/BMS with standardized connector infrastructure

**Choose LC-PS/LC-PH when**:
- Cable connection preferred (simpler, no mating connector needed)
- Lower cost priority (nickel-plated housing sufficient)
- M12 connector option desired (LC-PH only)

---

## 5. INSTALLATION & SERVICE

### 5.1 Pre-Installation Checklist

**Verify Requirements:**
- [ ] Pressure: LC-XT ≤ 46 bar, LC-XP ≤ 120 bar
- [ ] Media temperature -40°C to +125°C (extended range)
- [ ] Equipment port matches adapter thread type
- [ ] Adequate clearance (139.2mm height + 150-175mm top access for connector)
- [ ] Power supply voltage matches LC-XT/XP model (24VAC/DC, 115VAC, or 230VAC)
- [ ] Output configuration correct (NO or NC in air) - **cannot change in field**
- [ ] EN175301-803A mating connector available (order separately)

**Tools & Materials:**
- Torque wrench (50 N·m for adapter installation)
- PTFE tape or liquid thread sealant
- Multimeter (for wiring verification)
- EN175301-803A mating connector with cable (order from electrical supply)

### 5.2 Adapter Installation

**Step 1: Prepare Equipment Port**
- Clean port threads (remove old sealant, debris)
- Inspect threads for damage (repair if necessary)
- Verify port depth sufficient for adapter thread engagement

**Step 2: Apply Sealant**
- PTFE tape: 3-4 wraps clockwise (viewed from thread end)
- Liquid sealant: Apply per manufacturer instructions
- **Important**: Avoid sealant on first 2 threads (prevent contamination)

**Step 3: Install Adapter**
- Thread adapter into equipment port (hand-start, ensure straight)
- Torque to **50 N·m** (critical for sealing)
- Verify adapter orientation (sensor will point downward, connector on top)

**Step 4: Leak Test**
- Pressure test equipment per normal procedures
- Verify no leakage at adapter threads
- Re-torque if necessary (up to 50 N·m max)

### 5.3 Sensor Housing & Module Installation

**Step 1: Install Sensor Housing**
- Hand-screw sensor housing onto adapter (finger-tight, **no tools**)
- Verify stainless steel housing seated flush against adapter
- Orientation: Sensor pointing **downward** into liquid, connector on top

**Step 2: Install Electronic Module**
- Align module with sensor housing (bayonet-style internal connector)
- Hand-screw module onto sensor housing (finger-tight, **no tools**)
- Verify module seated flush (internal electrical connection automatic)
- EN175301-803A connector now accessible on top of module

### 5.4 EN175301-803A Connector Wiring

**Step 1: Prepare Mating Connector**
- Order EN175301-803A mating connector with cable from electrical supply
- Common brands: Lumberg, Phoenix Contact, Hirschmann, Murr Elektronik
- Verify IP65/IP67 rating for outdoor use
- Cable length per application requirements

**Step 2: Connector Pinout**
- **Pin 1**: Power supply (+) [typically brown wire]
- **Pin 2**: Output signal [typically black wire]
- **Pin 3**: Ground/Common (-) [typically blue wire]
- **Pin 4 (ground)**: Chassis ground (optional, green/yellow wire)

**⚠️ WARNING**: Verify pin assignments with mating connector documentation and LC-XT/XP label.

**Step 3: Wiring to Power Supply/PLC**
1. **De-energize power supply** (lockout/tagout)
2. Connect mating connector cable wires to terminal block or PLC:
   - Power (+) to supply voltage (24VAC/DC, 115VAC, or 230VAC)
   - Output to PLC input, relay coil, or alarm circuit
   - Ground (-) to common/neutral
   - Chassis ground to PE (if required)
3. Verify polarity (especially 24VDC models)
4. Secure connections (torque per terminal manufacturer specs)
5. Test continuity (multimeter, de-energized)

**Step 4: Connect Mating Connector to LC-XT/XP**
- Align mating connector with EN175301-803A connector on top of module
- Push connector onto LC-XT/XP connector (verify full seating)
- Secure with screw or bayonet lock (per mating connector type)
- Verify IP65 seal (o-ring or gasket properly compressed)

**Fuse Protection:**
- Install 1A slow-blow fuse in power supply circuit (per electrical code)

### 5.5 Commissioning

**Step 1: Pre-Startup Verification**
- [ ] Adapter torqued to 50 N·m
- [ ] Sensor housing hand-tight on adapter
- [ ] Electronic module hand-tight on sensor housing
- [ ] Mating connector securely attached to EN175301-803A connector
- [ ] Electrical connections secure and correct polarity
- [ ] Power supply voltage matches LC-XT/XP model
- [ ] Output wiring correct (NO or NC logic verified)

**Step 2: Power-On Test (System Empty)**
- Energize power supply
- Verify output state: 
  - **NO in air**: Output should be OPEN (no continuity)
  - **NC in air**: Output should be CLOSED (continuity)
- Measure output voltage with multimeter (should match supply voltage)

**Step 3: Functional Test (System Filled)**
- Fill equipment with liquid to submerge sensor dome
- Verify output state changes:
  - **NO in air**: Output should CLOSE (continuity)
  - **NC in air**: Output should OPEN (no continuity)
- Drain liquid to expose sensor dome
- Verify output returns to air state (< 1 second response)

**Step 4: Connector Verification**
- Disconnect mating connector (verify output signal stops)
- Reconnect mating connector (verify output signal restored)
- Check IP65 seal integrity (visual inspection)

### 5.6 Maintenance

**Routine Maintenance:**
- **Quarterly**: Visual inspection (leaks, connector integrity, corrosion)
- **Annually**: Functional test (verify output state changes)
- **No scheduled component replacement** (replace only if failed)

**Inspection Checklist:**
- [ ] Adapter and sensor housing secure (no loosening)
- [ ] Fused glass dome intact (no cracks, chips, cloudiness)
- [ ] EN175301-803A connector secure (no corrosion, damage)
- [ ] Mating connector cable intact (no kinks, cuts, insulation damage)
- [ ] Electrical connections secure (no corrosion, loosening)
- [ ] Output signal correct (test with multimeter)
- [ ] Stainless steel housing condition (no corrosion, pitting)

**Connector Maintenance:**
- Inspect o-ring/gasket on mating connector (replace if damaged)
- Clean connector pins with contact cleaner (if corrosion detected)
- Verify IP65 seal maintained (no moisture ingress)

### 5.7 Electronic Module Replacement

**When to Replace Electronic Module:**
- No output signal (module failure)
- Physical damage to module or connector
- Connector corrosion (replace module if connector damaged)
- Preventive replacement (after lightning strike, power surge)

**Replacement Procedure (5-10 Minutes, No Depressurization):**

1. **Disconnect Mating Connector** (unscrew or release bayonet lock)
2. **Disconnect Power** (lockout/tagout)
3. **Hand-Unscrew Electronic Module**:
   - Rotate module counter-clockwise (no tools, finger-tight)
   - Lift module straight up (internal connector disengages automatically)
4. **Inspect Sensor Housing**:
   - Verify threads intact (no cross-threading)
   - Check fused glass dome (no damage)
   - Inspect stainless steel housing (no corrosion)
5. **Install New Electronic Module**:
   - Align module with sensor housing (bayonet-style connector)
   - Press down gently and rotate clockwise (hand-tight, no tools)
   - Verify module seated flush (internal connector engaged)
6. **Reconnect Mating Connector** (secure with screw or bayonet lock)
7. **Restore Power** and verify operation:
   - Test output state in air and liquid (functional test per commissioning)

**Cost Savings:**
- Electronic module replacement: ~50-60% cost of complete sensor assembly
- No refrigerant recovery: Saves time and refrigerant
- No leak testing: System remains sealed
- Quick-disconnect: Faster than cable models (no wire stripping, termination)

---

## 6. FREQUENTLY ASKED QUESTIONS (FAQ)

### 6.1 Product Classification

**Q1: What is the difference between LC-XT and LC-XP?**

| Feature | LC-XT | LC-XP |
|---------|-------|-------|
| **Pressure** | 46 bar | 120 bar |
| **Applications** | Standard refrigeration + connector | CO2 transcritical + connector |
| **Temperature** | -40°C to +125°C | -40°C to +125°C |
| **Connector** | EN175301-803A | EN175301-803A |
| **Housing** | Stainless steel | Stainless steel |
| **Cost** | Lower | Higher (~30% more) |

**Both have identical features** except pressure rating. Choose LC-XT for ≤ 46 bar, LC-XP for 46-120 bar.

**Q2: What is EN175301-803A connector?**

**EN175301-803A** (also known as **DIN 43650 size A**) is an **industry-standard electrical connector** common in industrial automation and HVAC&R equipment:
- 3-pin + ground (4-position total)
- Quick-disconnect capability
- IP65 rated when mated
- Standardized pinout (interchangeable)
- Mating connector ordered separately from electrical supply houses

**Q3: What does "two-part design" mean?**

The LC-XT/XP consists of two parts:

1. **Part 1: Sensor Housing** (permanent pressure boundary)
   - Stainless steel body, fused glass dome
   - 46 bar (LC-XT) or 120 bar (LC-XP) rated
   - Remains on equipment during service

2. **Part 2: Electronic Module** (replaceable without depressurization)
   - Stainless steel housing, EN175301-803A connector on top
   - **Can be replaced in 5-10 minutes without emptying or depressurizing system**
   - Quick-disconnect (unplug mating connector, remove module)

### 6.2 Connector & Installation

**Q4: Where do I get the mating connector?**

**Mating connectors** ordered separately from electrical supply houses:
- **Brands**: Lumberg, Phoenix Contact, Hirschmann, Murr Elektronik, Weidmuller
- **Type**: EN175301-803A (DIN 43650 size A) with cable
- **Rating**: Verify IP65/IP67 for outdoor use
- **Cable length**: Per application requirements (1m, 3m, 5m, 10m, etc.)

**Example part numbers**:
- Lumberg: RKMV 3-224/5M (3-pin, 5m cable)
- Phoenix Contact: SACC-M12MS-3CON-PG7 (M12, 3-pin)
- Hirschmann: STAK 3 GDM 0600 LED 24 (3-pin, 6m cable, LED indication)

**Q5: What is the connector pinout?**

**EN175301-803A Pinout** (LC-XT/XP):
- **Pin 1**: Power supply (+)
- **Pin 2**: Output signal
- **Pin 3**: Ground/Common (-)
- **Pin 4 (ground)**: Chassis ground (optional)

**⚠️ WARNING**: Always verify pinout with LC-XT/XP label and mating connector documentation.

**Q6: Can I use a cable instead of the connector?**

**No**. LC-XT/XP have fixed EN175301-803A connector (not removable). For cable connection:
- **Use LC-PS** (46 bar, cable connection, nickel-plated steel)
- **Use LC-PH** (120 bar, cable or M12 connection, nickel-plated steel)

### 6.3 Pressure & Temperature

**Q7: Which model for CO2 transcritical (100 bar)?**

**LC-XP (120 bar)** - CO2 transcritical rated with industrial connector:
- Gas cooler outlet (90-110 bar)
- High-pressure receiver (80-100 bar)
- Flash gas separator (70-90 bar)

**LC-XT (46 bar)** is **NOT suitable** for CO2 transcritical (exceeds 46 bar rating).

**Q8: What is the temperature range?**

**Both LC-XT and LC-XP**: -40°C to +125°C media temperature (extended range)

**Extended range vs LC-PS** (-40°C to +85°C):
- Hot gas defrost cycles (up to +125°C)
- CO2 gas cooler outlet (+40°C to +80°C)
- High-temperature industrial processes

**Q9: Can LC-XT/XP be used for ammonia?**

**Yes**, fully compatible with ammonia (NH3):
- **Stainless steel housing**: Ideal for ammonia systems (corrosion resistance)
- **Pressure rating**: 46 bar (LC-XT) or 120 bar (LC-XP) suitable for most ammonia systems (typically 20-40 bar)
- **Fused glass**: Chemically inert to ammonia
- **EN175301-803A connector**: Industrial standard for ammonia plants

### 6.4 Stainless Steel Housing

**Q10: Why stainless steel housing?**

**Stainless steel advantages** vs nickel-plated steel:
- **Enhanced corrosion resistance**: Better in harsh environments
- **Long-term durability**: Resistant to salt spray, moisture, chemicals
- **Outdoor installations**: Suitable for exposed locations (coastal, rooftops, wash-down areas)
- **Industrial environments**: Chemical plants, food processing, marine applications
- **Ammonia compatibility**: Ideal for ammonia refrigeration systems

**Q11: Is stainless steel required for all applications?**

**No**. Nickel-plated steel sufficient for most applications:
- Indoor installations (controlled environment)
- Non-corrosive atmospheres
- Standard refrigeration (HFC, CO2 non-coastal)

**Stainless steel recommended for**:
- Outdoor/exposed installations
- Harsh environments (coastal, chemical, wash-down)
- Ammonia systems (best practice)
- Long-term reliability priority

### 6.5 Comparison & Selection

**Q12: LC-XT/XP vs LC-PS/PH - which to choose?**

| Need industrial connector? | Need stainless steel? | Recommendation |
|----------------------------|----------------------|----------------|
| **YES** | YES or NO | LC-XT (46 bar) or LC-XP (120 bar) |
| **NO** (cable OK) | YES | LC-XT/XP (has stainless steel) |
| **NO** (cable OK) | NO | LC-PS (46 bar) or LC-PH (120 bar) - lower cost |

**LC-XT/XP advantages**:
- EN175301-803A connector (quick-disconnect, standardized)
- Stainless steel housing (corrosion resistance)
- Extended temperature (-40°C to +125°C)

**LC-PS/PH advantages**:
- Cable connection (simpler, no mating connector needed)
- Lower cost (~20-25% less expensive)
- M12 connector option (LC-PH only)

**Q13: LC-XT vs TK1+ - which to choose?**

| Feature | LC-XT | TK1+ |
|---------|-------|------|
| **Function** | Level detection only (switch) | Level detection only (switch) |
| **Pressure** | 46 bar | 46 bar or 100 bar |
| **Output** | 100mA solid-state | 2A relay (NO + NC) |
| **Connection** | EN175301-803A | Cable glands |
| **LED** | No | Yes (green/yellow/red) |
| **Mounting** | Threaded adapters (6 types) | Sight-glass flange (3/4/6-hole) |

**Choose LC-XT** when: 100mA output sufficient, industrial connector required, threaded adapter mounting  
**Choose TK1+** when: Higher current needed (2A relay), sight-glass replacement, visual LED indication

**Q14: Do LC-XT/XP have automatic valve like TK3+?**

**No**. LC-XT/XP are **level switches only** (detection, not regulation):
- Detect liquid presence/absence
- Output signal to external controls
- Require external valve, pump, or control for automated actions

**For level regulation** (detection + valve + automatic control), use **TK3+** (46/80/130 bar) or **TK4** (46/80/130 bar smart) series.

### 6.6 Reliability & Compatibility

**Q15: What is the reliability/lifespan?**

**MTTF > 50,000 hours** (5.7+ years continuous operation). 

**Advantages**:
- No moving parts (no floats, reeds, linkages)
- Solid-state electronics (no relay contacts)
- Fused glass hermetic seal (no O-rings, no degradation)
- Stainless steel housing (corrosion resistant)
- Typical lifespan: 10-15 years in normal applications

**Q16: What refrigerants are compatible?**

**All refrigerants** (fused glass chemically inert):
- HFC/HCFC/CFC: R134a, R404A, R407C, R410A, R22, R502, etc.
- **CO2 (R744)**: LC-XT subcritical (up to 46 bar), LC-XP transcritical (up to 120 bar)
- **Ammonia (NH3)**: Fully compatible (stainless steel ideal)
- Hydrocarbons (HC): R290, R600a, etc.
- Low-GWP: R1234yf, R1234ze, R452A, R454B, etc.

**All oils**: Mineral, POE, PVE, PAG, AB (fused glass chemically inert).

---

## 7. ORDERING INFORMATION

### 7.1 Model Code Structure

**Format**: `LC-XT/LC-XP [Adapter] [Voltage] [Output] 0001 001 A00`

**Example**: **LC-XT707100001001A00** (LC-XT, 1/2" NPT, 24VAC/DC, NO in air)  
**Example**: **LC-XP707100001001A00** (LC-XP, 1/2" NPT, 24VAC/DC, NO in air)

### 7.2 Standard Model Codes

**LC-XT (46 bar):**

| Adapter | 24VAC/DC NO | 24VAC/DC NC | 230VAC NO | 230VAC NC |
|---------|-------------|-------------|-----------|-----------|
| **1/2" NPT** | LC-XT707100001001A00 | LC-XT707101001001A00 | LC-XT707D00001001A00 | LC-XT707D01001001A00 |
| **3/4" NPT** | LC-XTA07100001001A00 | LC-XTA07101001001A00 | LC-XTA07D00001001A00 | LC-XTA07D01001001A00 |
| **1" NPT** | LC-XTB07100001001A00 | LC-XTB07101001001A00 | LC-XTB07D00001001A00 | LC-XTB07D01001001A00 |
| **M20×1.5** | LC-XT607100001001A00 | LC-XT607101001001A00 | LC-XT607D00001001A00 | LC-XT607D01001001A00 |
| **1" 1/8 UNEF** | LC-XT807100001001A00 | LC-XT807101001001A00 | LC-XT807D00001001A00 | LC-XT807D01001001A00 |
| **1" 1/4 RLK** | LC-XTC07100001001A00 | LC-XTC07101001001A00 | LC-XTC07D00001001A00 | LC-XTC07D01001001A00 |

**LC-XP (120 bar):**

| Adapter | 24VAC/DC NO | 24VAC/DC NC | 230VAC NO | 230VAC NC |
|---------|-------------|-------------|-----------|-----------|
| **1/2" NPT** | LC-XP707100001001A00 | LC-XP707101001001A00 | LC-XP707D00001001A00 | LC-XP707D01001001A00 |
| **3/4" NPT** | LC-XPA07100001001A00 | LC-XPA07101001001A00 | LC-XPA07D00001001A00 | LC-XPA07D01001001A00 |
| **1" NPT** | LC-XPB07100001001A00 | LC-XPB07101001001A00 | LC-XPB07D00001001A00 | LC-XPB07D01001001A00 |
| **M20×1.5** | LC-XP607100001001A00 | LC-XP607101001001A00 | LC-XP607D00001001A00 | LC-XP607D01001001A00 |
| **1" 1/8 UNEF** | LC-XP807100001001A00 | LC-XP807101001001A00 | LC-XP807D00001001A00 | LC-XP807D01001001A00 |
| **1" 1/4 RLK** | LC-XPC07100001001A00 | LC-XPC07101001001A00 | LC-XPC07D00001001A00 | LC-XPC07D01001001A00 |

**Note**: 115VAC @ 60Hz models available on request.

### 7.3 Selection Parameters

**Pressure Rating:**
- **LC-XT**: 46 bar (standard refrigeration)
- **LC-XP**: 120 bar (CO2 transcritical, high-pressure)

**Adapter Selection:**
- **7** = 1/2" NPT (most common)
- **A** = 3/4" NPT
- **B** = 1" NPT
- **6** = M20×1.5 (metric)
- **8** = 1" 1/8 UNEF
- **C** = 1" 1/4 RLK

**Voltage Selection:**
- **071** = 24VAC/DC ±10%
- **072** = 115VAC ±10% @ 60Hz (on request)
- **07D** = 230VAC ±10% @ 50Hz

**Output Selection:**
- **0** = NO (Normally Open in air)
- **1** = NC (Normally Closed in air)

### 7.4 What's Included

- LC-XT or LC-XP two-part assembly (sensor housing + electronic module)
- Threaded adapter per model code
- EN175301-803A connector on top of module
- Installation instructions

### 7.5 What's NOT Included

- **EN175301-803A mating connector with cable**: Order separately from electrical supply houses
- **External valve**: LC-XT/XP are detection only (use TK3+/TK4 for integrated valve)
- **Mounting hardware**: Adapter threads into existing equipment port

### 7.6 Ordering Examples

**Example 1: CO2 Transcritical Gas Cooler (LC-XP)**
- Pressure: 100 bar
- Port: 1/2" NPT
- Voltage: 24VAC/DC
- Logic: High-level alarm (NO in air)
- **Order**: LC-XP707100001001A00 + EN175301-803A mating connector (3m cable)

**Example 2: Ammonia Separator with Connector (LC-XT)**
- Pressure: 25 bar
- Port: M20×1.5
- Voltage: 230VAC
- Logic: Low-level alarm (NC in air, fail-safe)
- **Order**: LC-XT607D01001001A00 + EN175301-803A mating connector (5m cable)

**Example 3: R404A Receiver with Industrial Connector (LC-XT)**
- Pressure: 28 bar
- Port: 3/4" NPT
- Voltage: 24VAC/DC
- Logic: High-level alarm (NO in air)
- **Order**: LC-XTA07100001001A00 + EN175301-803A mating connector (10m cable)

---

## Document Information

**Document**: LC-XT / LC-XP Complete Product Documentation  
**Version**: 1.0  
**Date**: 2025-11-12  
**Language**: English  
**Product**: LC-XT (46 bar) / LC-XP (120 bar) Optical Level Switches  
**Category**: Level_Switches  
**Keywords**: LC-XT, LC-XP, optical level switch, EN175301-803A, DIN 43650, industrial connector, stainless steel, 46 bar, 120 bar, CO2 transcritical, extended temperature, two-part design, level detection

**© 2025 Teklab. All rights reserved.**
