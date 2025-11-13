---
category: Level_Switches
keywords:
- Rotalock RLK02
- Rotalock level switch
- Rotalock mounting
- 1 inch 3/4-12 UNF
- 2 inch 1/4-12 UNF
- 46 bar pressure
- optical level sensor
- EN175301-803A connector
- two-part design
- compact design
- quick installation
- replaceable electronics
- industrial connector
- HVAC&R Rotalock
language: EN
product: Rotalock
document_type: unified_complete
last_updated: 2025-11-15
---

# Rotalock RLK02 - Complete Product Documentation

**Compact Optical Level Switch with Rotalock Connection**

---

## 📋 Document Structure

This unified document covers the complete Rotalock RLK02 product family organized in the following sections:

1. **Product Family Overview** - Description, Rotalock sizes, operating principle
2. **Detection Technology & Features** - Optical sensor, two-part design, Rotalock mounting
3. **Technical Specifications** - Electrical, mechanical, environmental specs
4. **Applications & Selection** - Use cases and Rotalock size selection guide
5. **Installation & Service** - Rotalock mounting, wiring, dimensions, maintenance
6. **FAQ** - Frequently asked questions

---

## 1. PRODUCT FAMILY OVERVIEW

### Rotalock RLK02 Series Description

The **Rotalock RLK02** is a compact optical level switch designed for level monitoring in HVAC&R systems with direct **Rotalock mounting**. This two-part unit provides reliable liquid presence/absence detection through industry-standard Rotalock connections (**1" 3/4-12 UNF** or **2" 1/4-12 UNF**), featuring an EN175301-803A industrial connector and extended temperature range.

**⚠️ IMPORTANT: Rotalock RLK02 is a LEVEL SWITCH ONLY - It does NOT include a solenoid valve.**
- For automatic oil level regulation with integrated valve, see **TK3+** or **TK4** series.
- Rotalock RLK02 provides detection signal only (requires external control for automated actions).

**Core Technology:**
- Electro-optic infrared sensor (fused glass hermetic seal)
- Solid-state output (NO or NC, 100mA max)
- Two-part serviceable design (electronics replaceable without depressurization)
- **Rotalock connection** (1" 3/4-12 UNF or 2" 1/4-12 UNF, no adapters required)
- **EN175301-803A connector** (DIN 43650 size A industrial standard)
- **Extended temperature range** (-40°C to +125°C media temp)
- Compact design (~130mm total height)
- Factory calibrated, plug-and-play operation

**Rotalock Size Options:**

| Model | Rotalock Size | Thread | Height (mm) | Primary Applications | Key Features |
|-------|---------------|--------|-------------|---------------------|--------------|
| **RLK02** (1" 3/4) | 1" 3/4-12 UNF | 1.75" diameter, 12 TPI | 78.3 | Most common Rotalock ports | Compact, direct mount |
| **RLK02** (2" 1/4) | 2" 1/4-12 UNF | 2.25" diameter, 12 TPI | 77.4 | Larger Rotalock ports | Compact, direct mount |

**Key Differentiators:**
- **vs LC-PS/LC-PH/LC-XT/LC-XP**: Rotalock RLK02 has Rotalock connection (no adapters), LC models have threaded adapters
- **vs TK1+**: Rotalock RLK02 has Rotalock connection + EN175301-803A connector, TK1+ has sight glass mount + relay outputs + LED
- **vs TK3+/TK4**: Rotalock RLK02 is detection only (no valve), TK3+/TK4 are complete regulators with valve

**Selection Criteria:**
- **RLK02 (1" 3/4)**: Equipment with 1" 3/4-12 UNF Rotalock port (most common)
- **RLK02 (2" 1/4)**: Equipment with 2" 1/4-12 UNF Rotalock port (larger)

**Primary Applications:**
- **Level monitoring in oil separators, receivers, reservoirs** (Rotalock ports)
- **Minimum/maximum liquid level alarms** (high-level or low-level detection)
- **Direct Rotalock connection to compressors** (service port monitoring)
- **CO2 subcritical systems** (up to 46 bar)
- **Compact installations** (space-constrained equipment)

**Operating Principle:**

Rotalock RLK02 uses electro-optic infrared detection through a fused glass dome:

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

**Advantages Over Threaded Adapter Models (LC-PS/LC-PH):**
- **No adapters required**: Rotalock connection integral to sensor housing (simpler, fewer leak points)
- **Compact design**: ~130mm total height (shorter than LC models with adapters)
- **Direct connection**: Rotalock ports common on compressors, receivers, separators
- **Industrial connector**: EN175301-803A (quick-disconnect, standardized)
- **Extended temperature**: -40°C to +125°C (vs LC-PS -40°C to +85°C)

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
- **Pressure rated**: 46 bar maximum working pressure

**Fused Glass Hermetic Seal:**
- **Glass-to-metal fusion**: Molecular-level seal (NOT O-ring)
- **Zero leakage**: 10^-12 mbar·L/s (true hermetic)
- **Chemically inert**: Compatible with all oils and refrigerants
- **Pressure rated**: 46 bar maximum working pressure
- **Temperature rated**: -40°C to +125°C media temperature (extended range)
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

**Part 1: Sensor Housing with Rotalock (Permanent Pressure Boundary)**
- **Components**: Fused glass dome, nickel-plated steel body, integral Rotalock connection (1" 3/4 or 2" 1/4)
- **Function**: Pressure containment, liquid detection surface, Rotalock mounting
- **Installation**: Permanent (screws directly into equipment Rotalock port)
- **Pressure rating**: 46 bar maximum
- **Temperature rating**: -40°C to +125°C media temperature
- **Material**: Nickel-plated steel (corrosion resistant)
- **Service**: Only removed for complete sensor replacement (rare)

**Part 2: Electronic Module (Replaceable Without Depressurization)**
- **Components**: Infrared LED, optical receiver, power supply, output driver, electronics housing
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

### 2.3 Rotalock Connection

**Rotalock Specifications:**
- **Type 1**: 1" 3/4-12 UNF (1.75" diameter, 12 threads per inch, most common)
- **Type 2**: 2" 1/4-12 UNF (2.25" diameter, 12 threads per inch, larger ports)
- **Thread**: Unified National Fine (UNF) thread standard
- **Installation torque**: 50 N·m (critical for proper sealing)

**Rotalock Advantages:**
- **No adapters required**: Rotalock connection integral to sensor housing (simplest installation)
- **Industry standard**: Rotalock ports common on compressors, receivers, separators, valves
- **Compact design**: Shorter total height than threaded adapter models (~130mm vs 139-150mm)
- **Direct mounting**: Sensor screws directly into equipment port (fewer components, fewer leak points)
- **Service access**: Rotalock ports often located for easy access (side of equipment)

**Rotalock Applications:**
- Compressor crankcase Rotalock service ports
- Receiver Rotalock ports (top, side, bottom)
- Oil separator Rotalock ports
- Rotalock valve ports (suction, discharge, liquid line)
- CO2 subcritical systems with Rotalock ports

### 2.4 Nickel-Plated Steel Construction

**Housing Materials:**
- **Sensor housing**: Nickel-plated steel (corrosion resistant, 46 bar rated)
- **Electronic module**: PA glass fiber reinforced (rugged, impact resistant)
- **Fused glass dome**: Borosilicate glass (chemically inert, pressure rated)
- **IP65 enclosure**: Dust-tight, water jet protected

**Reliability Features:**
- **No moving parts**: Eliminates mechanical failure modes (floats, reeds, linkages)
- **Solid-state electronics**: No relay contacts to wear or stick
- **Hermetic seal**: No O-rings or gaskets to degrade
- **Transient protection**: Built-in over-voltage protection (power surges, lightning)

**Environmental Protection:**
- **IP65 rating**: Outdoor/indoor installations, wash-down areas
- **Media temperature**: -40°C to +125°C (extended range)
- **Ambient temperature**: -40°C to +60°C
- **Humidity**: 5-95% RH non-condensing

**Refrigerant & Oil Compatibility:**
- **All HFC/HCFC/CFC**: R134a, R404A, R407C, R410A, R22, R502, etc.
- **CO2 (R744)**: Subcritical systems up to 46 bar
- **Ammonia (NH3)**: Fully compatible (nickel-plated steel suitable)
- **Hydrocarbons (HC)**: R290, R600a, etc.
- **Low-GWP**: R1234yf, R1234ze, R452A, R454B, etc.
- **All oils**: Mineral, POE, PVE, PAG, AB (fused glass chemically inert)

### 2.5 EN175301-803A Industrial Connector

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

### 2.6 Electrical Features

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

| Parameter | Specification |
|-----------|--------------|
| **Housing Material** | Nickel-plated steel |
| **Sensor Dome** | Fused glass (hermetic seal, 46 bar rated) |
| **Enclosure Protection** | IP65 (dust-tight, water jet protected) |
| **Rotalock Torque** | 50 N·m for Rotalock installation on equipment port |
| **Sensor Assembly** | Hand-screw (finger-tight, no tools) |
| **Weight** | ~350-400g total assembly |

### 3.3 Environmental & Pressure Specifications

| Parameter | Specification |
|-----------|--------------|
| **Media Temperature** | -40°C to +125°C (extended range) |
| **Ambient Temperature** | -40°C to +60°C |
| **Max Working Pressure** | 46 bar |
| **Humidity** | 5-95% RH non-condensing |
| **Vibration** | IEC 60068-2-6 compliant |

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

**Rotalock Connection Dimensions:**

| Rotalock Type | Thread | Height (mm) | Width (mm) | Notes |
|---------------|--------|-------------|------------|-------|
| **1" 3/4-12 UNF** | 1.75" diameter, 12 TPI | 78.3 | 56 | Most common size |
| **2" 1/4-12 UNF** | 2.25" diameter, 12 TPI | 77.4 | 56 | Larger port size |

**Height** = Distance from Rotalock mounting face to base of electronic module  
**Width** = Sensor housing diameter

**Total Assembly Height:**
- **Total height** (from Rotalock mounting face to top of EN175301-803A connector): ~130mm
- **Components**: Rotalock connection (78-78mm) + Electronic module (~40-50mm) + Connector clearance (~20-25mm)

**Installation Clearances:**
- **Top access**: 150-175mm above Rotalock face for mating connector + cable routing
- **Side access**: 60-80mm radial clearance for connector mating/unmating
- **Cable routing**: Allow space for mating connector cable exit (varies by cable orientation)
- **Rotalock service**: Verify clearance for Rotalock service tool (if sensor removal ever needed)

### 3.7 Refrigerant & Oil Compatibility

**Compatible Refrigerants:**
- All HFC, HCFC, CFC refrigerants (R134a, R404A, R407C, R410A, R22, R502, etc.)
- **CO2 (R744)**: Subcritical systems up to 46 bar
- **Ammonia (NH3)**: Fully compatible (nickel-plated steel suitable)
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

**Oil Separator Level Monitoring:**
- High-level detection (alarm when oil accumulates, trigger oil return)
- Low-level detection (verify oil return functioning properly)
- Rotalock ports common on oil separator shells

**Receiver Level Alarms:**
- Overfill protection (high-level alarm prevents liquid overflow)
- Low-level alarm (refrigerant inventory management)
- Rotalock ports often located on receiver shells (top, side, bottom)

**Compressor Rotalock Service Port Monitoring:**
- Direct mount on compressor Rotalock service ports
- Oil level detection in crankcase (if Rotalock port accessible)
- Compact design fits tight spaces around compressor

**CO2 Subcritical Systems:**
- Oil separator level detection (up to 46 bar)
- Receiver level monitoring (subcritical circuits)
- **Note**: For CO2 transcritical (>46 bar), use LC-PH (120 bar) or LC-XP (120 bar)

**Compact Installations:**
- Space-constrained equipment (Rotalock RLK02 ~130mm vs LC models ~139-150mm)
- Multiple sensors on single vessel (Rotalock ports distributed around shell)

### 4.2 Rotalock Size Selection Guide

**1" 3/4-12 UNF vs 2" 1/4-12 UNF:**

| Criteria | 1" 3/4-12 UNF | 2" 1/4-12 UNF |
|----------|---------------|---------------|
| **Diameter** | 1.75" (44.5mm) | 2.25" (57.2mm) |
| **Usage** | Most common Rotalock size | Larger ports (less common) |
| **Applications** | Compressors, separators, receivers, valves | Large receivers, separators |
| **Height** | 78.3mm | 77.4mm (slightly shorter) |

**Decision Tree:**

```
START
│
├─ Verify equipment Rotalock port size:
│   ├─ 1.75" diameter (1" 3/4-12 UNF)? ──YES──> RLK02 (1" 3/4)
│   ├─ 2.25" diameter (2" 1/4-12 UNF)? ──YES──> RLK02 (2" 1/4)
│   └─ Unknown size? ──> Measure existing Rotalock port or check equipment specs
│
├─ Pressure ≤ 46 bar? ──YES──> RLK02 (1" 3/4 or 2" 1/4)
│   └─NO (> 46 bar - use LC-PH 120 bar with Rotalock adapter)
│
├─ Rotalock port available? ──YES──> RLK02 (1" 3/4 or 2" 1/4)
│   └─NO (threaded port) ──> Use LC-PS/LC-PH/LC-XT/LC-XP
│
└─> RLK02 (1" 3/4 or 2" 1/4) - choose based on equipment port size
```

### 4.3 Rotalock RLK02 vs Other Level Switches

| Feature | LC-PS | LC-PH | LC-XT/XP | TK1+ | **Rotalock RLK02** |
|---------|-------|-------|----------|------|--------------------|
| **Pressure** | 46 bar | 120 bar | 46/120 bar | 46/100 bar | **46 bar** |
| **Media Temp** | -40 to +85°C | -40 to +125°C | -40 to +125°C | -40 to +85°C | **-40 to +125°C** |
| **Output** | 100mA | 100mA | 100mA | Relay 2A | **100mA** |
| **Mounting** | Threaded adapters | Threaded adapters | Threaded adapters | Sight glass | **Rotalock** |
| **Connection** | Cable | Cable/M12 | EN175301-803A | Cable glands | **EN175301-803A** |
| **Housing** | Nickel-plated | Nickel-plated | Stainless steel | Nickel-plated | **Nickel-plated** |
| **Height** | ~139-150mm | ~139-150mm | ~139mm | 101.5mm | **~130mm** |
| **Relative Cost** | Lowest | Medium | Medium-High | Medium | Medium |

**Choose Rotalock RLK02 when**:
- Equipment has Rotalock port (1" 3/4 or 2" 1/4)
- Compact design required (~130mm total height)
- No adapters desired (direct Rotalock connection)
- Extended temperature range (-40°C to +125°C)
- EN175301-803A connector preferred (industrial standard)

**Choose LC-PS/LC-PH/LC-XT/LC-XP when**:
- Threaded port mounting required (no Rotalock port)
- Higher pressure required (LC-PH 120 bar, LC-XP 120 bar)
- Multiple adapter options needed (NPT, UNEF, M20, Rotalock adapter)
- Stainless steel housing required (LC-XT/LC-XP)

**Choose TK1+ when**:
- Sight glass port available (sight glass replacement)
- Relay outputs required (230VAC @ 2A)
- LED indicators required (visual status verification)

---

## 5. INSTALLATION & SERVICE

### 5.1 Pre-Installation Checklist

**Verify Requirements:**
- [ ] Pressure ≤ 46 bar (for higher pressure, use LC-PH 120 bar)
- [ ] Media temperature -40°C to +125°C
- [ ] Equipment has Rotalock port (1" 3/4-12 UNF or 2" 1/4-12 UNF)
- [ ] Adequate clearance (130mm height + 150-175mm top access for connector)
- [ ] Power supply voltage matches Rotalock RLK02 model (24VAC/DC, 115VAC, or 230VAC)
- [ ] Output configuration correct (NO or NC in air) - **cannot change in field**
- [ ] EN175301-803A mating connector available (order separately)

**Tools & Materials:**
- Torque wrench (50 N·m for Rotalock installation)
- Rotalock service tool or appropriate wrench (for 1" 3/4 or 2" 1/4 Rotalock)
- Multimeter (for wiring verification)
- EN175301-803A mating connector with cable (order from electrical supply)

### 5.2 Rotalock Installation

**Step 1: Prepare Equipment Rotalock Port**
- De-pressurize equipment per safety procedures (lockout/tagout)
- Remove existing Rotalock cap, plug, or component
- Clean Rotalock port threads (remove old sealant, debris, oil residue)
- Inspect Rotalock threads for damage (verify 1" 3/4-12 UNF or 2" 1/4-12 UNF)

**Step 2: Install Sensor Housing (Rotalock Connection)**
- Thread sensor housing into equipment Rotalock port (hand-start, ensure straight)
- Use Rotalock service tool or appropriate wrench (do not hand-tighten only)
- Torque to **50 N·m** (critical for proper sealing and pressure rating)
- Verify sensor housing orientation (sensor pointing downward into vessel, connector on top)

**⚠️ CRITICAL**: 50 N·m torque required. Under-torquing risks leaks, over-torquing damages threads.

**Step 3: Leak Test**
- Pressure test equipment per normal procedures
- Verify no leakage at Rotalock threads
- Re-torque if necessary (up to 50 N·m max)

### 5.3 Electronic Module Installation

**Step 1: Install Electronic Module**
- Hand-screw module onto sensor housing (finger-tight, **no tools**)
- Verify module seated flush against sensor housing (internal electrical connection automatic)
- EN175301-803A connector now accessible on top of module

**Step 2: Orientation Verification**
- Sensor housing pointing **downward** into vessel (fused glass dome at bottom)
- Electronic module on top (accessible for service)
- EN175301-803A connector facing upward or to side (cable routing)

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

**⚠️ WARNING**: Verify pin assignments with mating connector documentation and Rotalock RLK02 label.

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

**Step 4: Connect Mating Connector to Rotalock RLK02**
- Align mating connector with EN175301-803A connector on top of module
- Push connector onto Rotalock RLK02 connector (verify full seating)
- Secure with screw or bayonet lock (per mating connector type)
- Verify IP65 seal (o-ring or gasket properly compressed)

**Fuse Protection:**
- Install 1A slow-blow fuse in power supply circuit (per electrical code)

### 5.5 Commissioning

**Step 1: Pre-Startup Verification**
- [ ] Sensor housing torqued to 50 N·m (Rotalock connection)
- [ ] Electronic module hand-tight on sensor housing
- [ ] Mating connector securely attached to EN175301-803A connector
- [ ] Electrical connections secure and correct polarity
- [ ] Power supply voltage matches Rotalock RLK02 model
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
- [ ] Rotalock connection secure (no loosening, verify 50 N·m torque if accessible)
- [ ] Sensor housing secure (no vibration loosening)
- [ ] Fused glass dome intact (no cracks, chips, cloudiness)
- [ ] EN175301-803A connector secure (no corrosion, damage)
- [ ] Mating connector cable intact (no kinks, cuts, insulation damage)
- [ ] Electrical connections secure (no corrosion, loosening)
- [ ] Output signal correct (test with multimeter)

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
   - Verify Rotalock connection secure (no leaks)
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

**Q1: What Rotalock sizes are available?**

Two sizes:
- **1" 3/4-12 UNF** (1.75" diameter, 12 threads per inch) - most common
- **2" 1/4-12 UNF** (2.25" diameter, 12 threads per inch) - larger ports

**Verify equipment Rotalock port size** before ordering (measure existing Rotalock port or check equipment specifications).

**Q2: What is EN175301-803A connector?**

**EN175301-803A** (also known as **DIN 43650 size A**) is an **industry-standard electrical connector** common in industrial automation and HVAC&R equipment:
- 3-pin + ground (4-position total)
- Quick-disconnect capability
- IP65 rated when mated
- Standardized pinout (interchangeable)
- Mating connector ordered separately from electrical supply houses

**Q3: What does "two-part design" mean?**

The Rotalock RLK02 consists of two parts:

1. **Part 1: Sensor Housing with Rotalock** (permanent pressure boundary)
   - Nickel-plated steel body, fused glass dome, integral Rotalock connection
   - 46 bar rated
   - Remains on equipment during service

2. **Part 2: Electronic Module** (replaceable without depressurization)
   - EN175301-803A connector on top
   - **Can be replaced in 5-10 minutes without emptying or depressurizing system**
   - Quick-disconnect (unplug mating connector, remove module)

### 6.2 Installation & Mounting

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

**EN175301-803A Pinout** (Rotalock RLK02):
- **Pin 1**: Power supply (+)
- **Pin 2**: Output signal
- **Pin 3**: Ground/Common (-)
- **Pin 4 (ground)**: Chassis ground (optional)

**⚠️ WARNING**: Always verify pinout with Rotalock RLK02 label and mating connector documentation.

**Q6: What is the installation torque?**

**50 N·m** for Rotalock installation on equipment port (critical for proper sealing and 46 bar pressure rating).

**Electronic module**: Hand-tighten only (finger-tight, no tools).

### 6.3 Pressure & Temperature

**Q7: What is the maximum pressure rating?**

**46 bar maximum**. For higher pressures:
- Use **LC-PH** (120 bar) with 1" 1/4 Rotalock adapter
- Contact Teklab for custom high-pressure Rotalock solution

**Q8: What is the temperature range?**

**-40°C to +125°C media temperature** (extended range):
- Low-temperature refrigeration (-40°C to -10°C)
- Standard refrigeration (0°C to +40°C)
- Hot gas defrost cycles (up to +125°C)
- CO2 gas cooler outlet (+40°C to +80°C)

**Extended range vs LC-PS** (-40°C to +85°C): Rotalock RLK02 suitable for +85°C to +125°C applications.

**Q9: Can Rotalock RLK02 be used for ammonia?**

**Yes**, fully compatible with ammonia (NH3):
- **Nickel-plated steel housing**: Suitable for ammonia systems
- **Pressure rating**: 46 bar suitable for most ammonia systems (typically 20-40 bar)
- **Fused glass**: Chemically inert to ammonia
- **Rotalock connection**: Common on ammonia compressors, separators, receivers

**Q10: Can I use Rotalock RLK02 in CO2 systems?**

**Yes, for CO2 subcritical** (up to 46 bar):
- Oil separator level detection (subcritical circuits)
- Receiver level monitoring (subcritical circuits)

**For CO2 transcritical** (>46 bar):
- Use **LC-PH** (120 bar) with 1" 1/4 Rotalock adapter
- Use **LC-XP** (120 bar) with 1" 1/4 Rotalock adapter

### 6.4 Comparison & Selection

**Q11: Rotalock RLK02 vs LC-PH - which to choose?**

| Feature | Rotalock RLK02 | LC-PH |
|---------|----------------|-------|
| **Pressure** | 46 bar | 120 bar |
| **Mounting** | Rotalock (2 sizes) | Threaded adapters (6 options including Rotalock adapter) |
| **Connection** | EN175301-803A | Cable or M12 |
| **Height** | ~130mm | ~139-150mm |
| **Adapters** | None (integral Rotalock) | 6 adapter types (1/2" NPT, 3/4" NPT, 1" NPT, M20×1.5, 1" 1/8 UNEF, 1" 1/4 RLK) |

**Choose Rotalock RLK02** when: Rotalock port available, pressure ≤ 46 bar, compact design preferred  
**Choose LC-PH** when: Higher pressure required (120 bar), multiple adapter options needed, cable connection preferred

**Q12: Rotalock RLK02 vs TK1+ - which to choose?**

| Feature | Rotalock RLK02 | TK1+ |
|---------|----------------|------|
| **Mounting** | Rotalock | Sight glass |
| **Pressure** | 46 bar | 46 or 100 bar |
| **Output** | 100mA solid-state | Relay 2A (NO + NC) |
| **LEDs** | No | Yes (integrated) |
| **Connection** | EN175301-803A | Cable glands |
| **Height** | ~130mm | 101.5mm |

**Choose Rotalock RLK02**: Rotalock port available, compact design, industrial connector  
**Choose TK1+**: Sight glass port available, relay outputs (2A), LED indicators, 46 or 100 bar

**Q13: Does Rotalock RLK02 have automatic valve like TK3+?**

**No**. Rotalock RLK02 is a **level switch only** (detection, not regulation):
- Detects liquid presence/absence
- Output signal to external controls
- Requires external valve, pump, or control for automated actions

**For level regulation** (detection + valve + automatic control), use **TK3+** (46/80/130 bar) or **TK4** (46/80/130 bar smart) series.

### 6.5 Reliability & Compatibility

**Q14: What is the reliability/lifespan?**

**MTTF > 50,000 hours** (5.7+ years continuous operation). 

**Advantages**:
- No moving parts (no floats, reeds, linkages)
- Solid-state electronics (no relay contacts)
- Fused glass hermetic seal (no O-rings, no degradation)
- Nickel-plated steel housing (corrosion resistant)
- Typical lifespan: 10-15 years in normal applications

**Q15: What refrigerants are compatible?**

**All refrigerants** (fused glass chemically inert):
- HFC/HCFC/CFC: R134a, R404A, R407C, R410A, R22, R502, etc.
- **CO2 (R744)**: Subcritical systems up to 46 bar
- **Ammonia (NH3)**: Fully compatible (nickel-plated steel suitable)
- Hydrocarbons (HC): R290, R600a, etc.
- Low-GWP: R1234yf, R1234ze, R452A, R454B, etc.

**All oils**: Mineral, POE, PVE, PAG, AB (fused glass chemically inert).

---

## 7. ORDERING INFORMATION

### 7.1 Model Code Structure

**Format**: `RLK02 [Rotalock Size] [Voltage] [Output] 0001 001 A00`

**Example**: **RLK02007100001001A00** (1" 3/4 Rotalock, 24VAC/DC, NO in air)  
**Example**: **RLK02107100001001A00** (2" 1/4 Rotalock, 24VAC/DC, NO in air)

### 7.2 Standard Model Codes

**Power Supply Options:**

| Rotalock Size | 24VAC/DC NO | 24VAC/DC NC | 230VAC NO | 230VAC NC |
|---------------|-------------|-------------|-----------|-----------|
| **1" 3/4-12 UNF** | RLK02007100001001A00 | RLK02007101001001A00 | RLK02007D00001001A00 | RLK02007D01001001A00 |
| **2" 1/4-12 UNF** | RLK02107100001001A00 | RLK02107101001001A00 | RLK02107D00001001A00 | RLK02107D01001001A00 |

**Note**: 115VAC @ 60Hz models available on request.

### 7.3 Selection Parameters

**Rotalock Size:**
- **00** = 1" 3/4-12 UNF (1.75" diameter, most common)
- **10** = 2" 1/4-12 UNF (2.25" diameter, larger ports)

**Voltage Selection:**
- **071** = 24VAC/DC ±10%
- **072** = 115VAC ±10% @ 60Hz (on request)
- **07D** = 230VAC ±10% @ 50Hz

**Output Selection:**
- **0** = NO (Normally Open in air)
- **1** = NC (Normally Closed in air)

### 7.4 What's Included

- Rotalock RLK02 two-part assembly (sensor housing + electronic module)
- Integral Rotalock connection (1" 3/4-12 UNF or 2" 1/4-12 UNF)
- EN175301-803A connector on top of module
- Installation instructions

### 7.5 What's NOT Included

- **EN175301-803A mating connector with cable**: Order separately from electrical supply houses
- **External valve**: Rotalock RLK02 is detection only (use TK3+/TK4 for integrated valve)
- **Rotalock port cap/plug**: If sensor removed (order from equipment manufacturer)

### 7.6 Ordering Examples

**Example 1: R404A Receiver High-Level Alarm**
- Pressure: 28 bar
- Port: 1" 3/4-12 UNF Rotalock (most common)
- Voltage: 24VAC/DC
- Logic: High-level alarm (NO in air)
- **Order**: RLK02007100001001A00 + EN175301-803A mating connector (3m cable)

**Example 2: Ammonia Separator Low-Level Alarm**
- Pressure: 22 bar
- Port: 2" 1/4-12 UNF Rotalock (larger port)
- Voltage: 230VAC
- Logic: Low-level alarm (NC in air, fail-safe)
- **Order**: RLK02107D01001001A00 + EN175301-803A mating connector (5m cable)

**Example 3: CO2 Subcritical Oil Separator**
- Pressure: 40 bar (subcritical)
- Port: 1" 3/4-12 UNF Rotalock
- Voltage: 24VAC/DC
- Logic: High-level alarm (NO in air)
- **Order**: RLK02007100001001A00 + EN175301-803A mating connector (10m cable)

---

## Document Information

**Document**: Rotalock RLK02 Complete Product Documentation  
**Version**: 1.0  
**Date**: 2025-11-12  
**Language**: English  
**Product**: Rotalock RLK02 (46 bar) Optical Level Switch  
**Category**: Level_Switches  
**Keywords**: Rotalock, RLK02, optical level switch, Rotalock connection, 1" 3/4-12 UNF, 2" 1/4-12 UNF, EN175301-803A, DIN 43650, compact design, 46 bar, extended temperature, two-part design, level detection

**© 2025 Teklab. All rights reserved.**
