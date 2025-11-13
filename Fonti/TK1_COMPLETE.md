---
category: Level_Switches
keywords:
- TK1+
- TK1 level control
- TK1 46 bar
- TK1 100 bar
- sight glass mounting
- relay output
- NO NC contacts
- LED indicators
- optical level sensor
- two-part design
- visual monitoring
- replaceable electronics
- control unit
- HVAC&R level control
language: EN
product: TK1
document_type: unified_complete
last_updated: 2025-11-15
---

# TK1+ - Complete Product Documentation

**Optical Level Control Unit with Sight Glass Mounting and Relay Outputs**

---

## 📋 Document Structure

This unified document covers the complete TK1+ product family organized in the following sections:

1. **Product Family Overview** - Description, pressure options, operating principle
2. **Detection Technology & Features** - Optical sensor, two-part design, relay outputs, LED indicators
3. **Technical Specifications** - Electrical, mechanical, environmental specs
4. **Applications & Selection** - Use cases and pressure rating selection guide
5. **Installation & Service** - Sight glass mounting, wiring, dimensions, maintenance
6. **FAQ** - Frequently asked questions

---

## 1. PRODUCT FAMILY OVERVIEW

### TK1+ Series Description

The **TK1+** is an optical level control unit designed for level monitoring in HVAC&R systems with direct **sight glass mounting**. This two-part unit provides reliable liquid presence/absence detection with **relay outputs (NO and NC)**, **integrated LED status indicators**, and revolutionary replaceable electronics. Available in **46 bar** or **100 bar** pressure ratings.

**⚠️ IMPORTANT: TK1+ is a LEVEL SWITCH ONLY - It does NOT include a solenoid valve.**
- For automatic oil level regulation with integrated valve, see **TK3+** or **TK4** series.
- TK1+ provides detection signal only (requires external control for automated actions).

**Core Technology:**
- Electro-optic infrared sensor (fused glass hermetic seal)
- **Contact-free relay outputs** (NO and NC available simultaneously, 230VAC @ 2A)
- **Integrated LED status indicators** (visual liquid presence/absence verification)
- Two-part serviceable design (electronics replaceable without depressurization)
- **Sight glass mounting** (direct replacement for traditional sight glass)
- **1/4" NPT female connection** (optional oil return line)
- Factory calibrated, plug-and-play operation

**Pressure Options:**

| Model | Max Pressure | Media Temp | Primary Applications | Key Features |
|-------|-------------|------------|---------------------|--------------|
| **TK1+ (46 bar)** | 46 bar | -40°C to +85°C | Standard refrigeration, sight glass replacement | Relay 2A, LED, sight glass mount |
| **TK1+ (100 bar)** | 100 bar | -40°C to +85°C | CO2 transcritical, high-pressure, sight glass replacement | Relay 2A, LED, sight glass mount, 100 bar rated |

**⚠️ CRITICAL**: Pressure rating (46 bar or 100 bar) must be specified at order time.

**Key Differentiators:**
- **vs LC-PS/LC-PH/LC-XT/LC-XP**: TK1+ has relay outputs (2A vs 100mA solid-state) + LED indicators + sight glass mount
- **vs Rotalock**: TK1+ has sight glass mount (vs Rotalock connection) + relay 2A + LED indicators
- **vs TK3+/TK4**: TK1+ is detection only (no valve), TK3+/TK4 are complete regulators with valve

**Selection Criteria:**
- **TK1+ (46 bar)**: Standard refrigeration ≤ 46 bar + sight glass port + relay outputs + LED indication
- **TK1+ (100 bar)**: High-pressure 46-100 bar (CO2 transcritical) + sight glass port + relay outputs + LED indication

**Primary Applications:**
- **Compressor crankcase level monitoring** (sight glass replacement with automated control)
- **Oil separator level control** (high-level alarms, automated oil return)
- **Oil reservoir level alarms** (low-level warnings, system protection)
- **Liquid receiver level monitoring** (overfill protection, automated feed control)
- **CO2 transcritical systems** (100 bar model for high-pressure oil separators)

**Operating Principle:**

TK1+ uses electro-optic infrared detection through a fused glass dome:

1. **In Air (liquid not present)**:
   - Infrared LED emits light into fused glass dome
   - Light reflects internally (total internal reflection)
   - Optical receiver detects reflected light
   - Relay state: NO relay OPEN, NC relay CLOSED
   - LED indication: Green (air/no liquid detected)

2. **In Liquid (liquid present)**:
   - Liquid contacts fused glass dome
   - Light escapes into liquid (refractive index change)
   - Optical receiver detects loss of reflected light
   - Relay state: NO relay CLOSES, NC relay OPENS
   - LED indication: Yellow or Red (liquid detected)

3. **Response Time**: Fast (infrared detection, < 1 second)

**Advantages Over Other Level Switches:**
- **Relay outputs**: 230VAC @ 2A (vs 100mA solid-state on LC-PS/LC-PH/LC-XT/LC-XP) - drives contactors directly
- **NO + NC simultaneous**: Both relay contacts available (high-level and low-level alarms from single unit)
- **Integrated LEDs**: Visual status verification without multimeter (commissioning, troubleshooting)
- **Sight glass mounting**: Direct replacement for traditional sight glass (existing port, no adapters)
- **1/4" NPT female**: Optional oil return line connection integrated on sensor housing
- **Higher current capability**: Suitable for driving larger loads (contactors, solenoids, alarms)

---

## 2. DETECTION TECHNOLOGY & FEATURES

### 2.1 Electro-Optic Infrared Sensor

**Detection Method:**
- **Infrared LED emitter**: Generates infrared light into fused glass dome
- **Optical receiver**: Detects reflected light intensity
- **Refractive index principle**: Light behavior changes at glass/liquid interface
- **Digital threshold**: Clean ON/OFF switching (no analog drift)

**Sensor Advantages:**
- **Response time**: Fast (< 1 second, infrared detection)
- **Reliability**: High (no mechanical moving parts)
- **No calibration**: Factory calibrated, no field adjustment needed
- **No wetted electronics**: Sensor electronics isolated from media by fused glass
- **Pressure rated**: 46 bar or 100 bar (depending on model ordered)

**Fused Glass Hermetic Seal:**
- **Glass-to-metal fusion**: Molecular-level seal (NOT O-ring)
- **Zero leakage**: 10^-12 mbar·L/s (true hermetic)
- **Chemically inert**: Compatible with all oils and refrigerants
- **Pressure rated**: 46 bar or 100 bar maximum working pressure
- **Temperature rated**: -40°C to +85°C media temperature
- **Lifetime seal**: No degradation, no maintenance

### 2.2 Contact-Free Relay Outputs

**Relay Specifications:**
- **Type**: Solid-state relay (contact-free, no mechanical contacts)
- **Output rating**: Up to 230VAC @ 2A maximum
- **Outputs available**: NO (Normally Open) and NC (Normally Closed) **simultaneously**
- **Logic**:
  - **In air (no liquid)**: NO relay OPEN, NC relay CLOSED
  - **In liquid (liquid present)**: NO relay CLOSES, NC relay OPENS

**Contact-Free Advantages:**
- **No mechanical wear**: Solid-state switching eliminates relay contact degradation
- **Longer life**: No contact bounce, arcing, or oxidation
- **Higher reliability**: Typical lifespan exceeds mechanical relays by 5-10x
- **Faster switching**: No mechanical inertia (< 1 second response)

**Output Applications:**
- **NO relay**: High-level alarms (relay closes when liquid detected)
- **NC relay**: Low-level alarms (relay opens when liquid detected, fail-safe)
- **Direct load control**: Drives contactors (230VAC @ 2A), solenoid valves, alarm horns
- **PLC integration**: Relay contacts interface with PLC/BMS inputs
- **Dual monitoring**: NO + NC simultaneous (redundant alarm systems, high + low level)

**Important Output Notes:**
- **2A maximum current**: Verify load current ≤ 2A (contactors typically 0.5-1.5A coil)
- **Inductive load protection**: Use suppression diodes or snubbers for inductive loads (contactors, solenoids)
- **230VAC maximum voltage**: Do NOT exceed 230VAC (relay damage risk)

### 2.3 Integrated LED Status Indicators

**LED Functionality:**
- **Location**: Electronic module face (visible during operation)
- **Purpose**: Visual liquid presence/absence indication without multimeter
- **Colors** (typical):
  - **Green**: Air/no liquid detected (sensor in air)
  - **Yellow or Red**: Liquid detected (sensor submerged)
  - **Flashing**: Possible alarm or module malfunction (verify with supplier documentation)

**LED Advantages:**
- **Commissioning aid**: Verify sensor detection during startup (no multimeter needed)
- **Troubleshooting**: Quick visual check of sensor status during service calls
- **Remote indication**: View sensor status from distance (up to 10-15m with good lighting)
- **Fail-safe verification**: LED pattern indicates proper module operation

**Use Cases:**
- **Startup verification**: Fill equipment and verify LED changes color (liquid detected)
- **Intermittent problems**: Observe LED during operation (unexpected liquid level fluctuations)
- **Preventive maintenance**: LED status check during routine inspections

### 2.4 Two-Part Revolutionary Design

**Part 1: Sensor Housing with Sight Glass Flange (Permanent Pressure Boundary)**
- **Components**: Fused glass dome, nickel-plated steel body, sight glass mounting flange (61.8mm × 59.5mm)
- **Function**: Pressure containment, liquid detection surface, sight glass replacement
- **Installation**: Permanent (mounts directly on existing sight glass port)
- **Pressure rating**: 46 bar or 100 bar maximum (specify at order)
- **Temperature rating**: -40°C to +85°C media temperature
- **Material**: Nickel-plated steel (corrosion resistant), fused glass dome
- **Service**: Only removed for complete sensor replacement (rare)
- **1/4" NPT female**: Optional oil return line connection integrated on housing

**Part 2: Electronic Module (Replaceable Without Depressurization)**
- **Components**: Infrared LED, optical receiver, relay electronics, LED indicators, cable connection
- **Function**: Detection electronics, relay outputs, visual status indication
- **Cable connection**: Cable glands (1m or 3m) or molded cables (depending on model)
- **Installation**: Hand-screw onto sensor housing (finger-tight, no tools)
- **Service**: Replaceable in 5-10 minutes without system depressurization
- **Advantages**: Minimal downtime, no refrigerant recovery, no leak risk

**Service Procedure (Electronic Module Replacement):**
1. Disconnect cable from terminal block or control panel
2. Disconnect power (lockout/tagout)
3. Hand-unscrew electronic module from sensor housing (no tools)
4. Install new electronic module (hand-screw, finger-tight)
5. Reconnect cable to terminal block or control panel
6. Restore power and verify operation (LED indication, relay outputs)

**Time**: 5-10 minutes  
**Cost**: Electronic module replacement vs complete sensor assembly (50-60% cost savings)  
**Downtime**: Minimal (no depressurization, no refrigerant recovery)

### 2.5 Sight Glass Mounting

**Sight Glass Replacement:**
- **TK1+ replaces traditional sight glass** (visual inspection → automated detection)
- **Mounting flange**: 61.8mm × 59.5mm (standard sight glass dimensions)
- **Direct installation**: Mounts on existing sight glass port (no adapters required)
- **Orientation**: Sensor housing points downward into vessel, electronic module on top

**Sight Glass Flange Advantages:**
- **No additional adapters**: Direct mounting on existing sight glass port
- **Proven mounting interface**: Sight glass flange standard in HVAC&R equipment
- **Easy retrofit**: Replace sight glass with TK1+ (minimal modification)
- **Multiple compressor compatibility**: Sight glass ports common on crankcase, oil separators, reservoirs

**Installation Verification:**
- Verify sight glass flange intact (no damage, gasket surface clean)
- Remove old sight glass and gasket
- Install TK1+ sensor housing with new gasket (torque per equipment guidelines)
- Verify sensor housing secure (no leaks)
- Install electronic module (hand-screw, finger-tight)

### 2.6 Electrical Features

**Power Supply:**
- **Voltage options**: 24VAC ±10% or 230VAC ±10% (depending on model)
- **Power consumption**: 10VA per electronic module (ultra-low power)
- **Frequency**: 50/60 Hz (AC models)

**Cable Connection:**
- **Standard**: Cable glands with 1m or 3m cable
- **Optional**: Molded cable versions (sealed cable entry, order separately)
- **Cable type**: PVC CEI 20-22 (working temp -20°C to +70°C fixed laying)
- **Wiring**: 4-5 conductors (power +/-, NO relay, NC relay, optional ground)

**Electrical Protection:**
- **Relay outputs**: Solid-state (no mechanical contacts to fail)
- **Inductive load protection**: Use suppression diodes or snubbers for inductive loads

**Customizable Delays (Available on Request):**
- **Activation delay**: Prevents false alarms from turbulence, foam, bubbles (typical 5-30 seconds)
- **Deactivation delay**: Filters transient liquid contact (typical 1-10 seconds)
- **Factory-programmed**: Specify delay requirements at order

### 2.7 1/4" NPT Female Connection

**Optional Oil Return Line:**
- **Location**: Integrated on sensor housing (side or bottom, depending on model)
- **Thread**: 1/4" NPT female
- **Purpose**: Connect oil return line if needed (automated oil return systems)
- **Usage**: Optional (plug if not used)

**Oil Return Applications:**
- **Oil separator**: TK1+ high-level detection + 1/4" NPT oil return to compressor crankcase
- **Compressor crankcase**: TK1+ high-level detection + 1/4" NPT oil return to oil reservoir
- **Automated systems**: TK1+ relay triggers oil return solenoid + 1/4" NPT mechanical return line

### 2.8 Construction & Reliability

**Housing Materials:**
- **Sensor housing**: Nickel-plated steel (corrosion resistant, 46 bar or 100 bar rated)
- **Electronic module**: PA glass fiber reinforced (rugged, impact resistant)
- **Fused glass dome**: Borosilicate glass (chemically inert, pressure rated)
- **IP65 enclosure**: Dust-tight, water jet protected

**Reliability Features:**
- **No moving parts**: Eliminates mechanical failure modes (floats, reeds, linkages)
- **Contact-free relay**: No relay contacts to wear or stick (solid-state reliability)
- **Hermetic seal**: No O-rings or gaskets to degrade
- **Heavy environment suitable**: Industrial/outdoor installations, harsh conditions

**Environmental Protection:**
- **IP65 rating**: Outdoor/indoor installations, wash-down areas
- **Media temperature**: -40°C to +85°C
- **Ambient temperature**: -40°C to +60°C
- **Humidity**: 5-95% RH non-condensing

**Refrigerant & Oil Compatibility:**
- **All HFC/HCFC/CFC**: R134a, R404A, R407C, R410A, R22, R502, etc.
- **CO2 (R744)**: 46 bar model for subcritical, 100 bar model for transcritical
- **Ammonia (NH3)**: Fully compatible (nickel-plated steel suitable)
- **Hydrocarbons (HC)**: R290, R600a, etc.
- **Low-GWP**: R1234yf, R1234ze, R452A, R454B, etc.
- **All oils**: Mineral, POE, PVE, PAG, AB (fused glass chemically inert)

---

## 3. TECHNICAL SPECIFICATIONS

### 3.1 Electrical Specifications

| Parameter | Specification |
|-----------|--------------|
| **Supply Voltage** | 24VAC ±10% OR 230VAC ±10% (depending on model) |
| **Supply Frequency** | 50/60 Hz (AC models) |
| **Power Consumption** | 10VA per electronic module |
| **Output Signal** | Contact-free relay output NO and NC (simultaneous) |
| **Relay Outputs Rating** | Up to 230VAC @ 2A maximum |
| **LED Indicators** | Integrated LEDs on electronic module (liquid status verification) |
| **Electrical Connection** | Cable wiring via cable glands (1m or 3m) or molded cables |
| **Cable Type** | PVC cable CEI 20-22 (working temp: -20°C to +70°C fixed laying) |

### 3.2 Mechanical Specifications

| Parameter | Specification |
|-----------|--------------|
| **Housing Material** | Nickel-plated steel + fused glass, PA glass fiber reinforced |
| **Sensor Dome** | Fused glass technology (hermetic seal, 46 bar or 100 bar rated) |
| **Enclosure Protection** | IP65 (dust-tight, water jet protected) |
| **Mounting Type** | Sight glass flange (61.8mm × 59.5mm standard sight glass dimensions) |
| **Oil Return Line** | 1/4" NPT female connection (optional, integrated on sensor housing) |
| **Weight** | ~600-700g total assembly (sensor housing ~400-450g, electronic module ~200-250g) |

### 3.3 Environmental & Pressure Specifications

| Parameter | TK1+ (46 bar) | TK1+ (100 bar) |
|-----------|---------------|----------------|
| **Media Temperature** | -40°C to +85°C | -40°C to +85°C |
| **Ambient Temperature** | -40°C to +60°C | -40°C to +60°C |
| **Max Working Pressure** | **46 bar** | **100 bar** |
| **Humidity** | 5-95% RH non-condensing | 5-95% RH non-condensing |
| **Vibration** | IEC 60068-2-6 compliant | IEC 60068-2-6 compliant |
| **Heavy Environment** | Suitable for heavy industrial environments | Suitable for heavy industrial environments |

### 3.4 Performance Specifications

| Parameter | Specification |
|-----------|--------------|
| **Response Time** | Fast (< 1 second, infrared detection) |
| **Repeatability** | ± 1mm |
| **Reliability** | High (no mechanical moving parts) |
| **Calibration** | Factory calibrated (no field calibration required) |
| **Hermetic Seal** | 10^-12 mbar·L/s (fused glass-to-metal) |
| **Delays** | Customizable activation/deactivation delays available on request |

### 3.5 Compliance

| Standard | Description |
|----------|-------------|
| **2014/30/UE** | EMC Directive (Electromagnetic Compatibility) |
| **2014/35/UE** | Low Voltage Directive |
| **CE Marking** | Compliant and certified |
| **IP Rating** | IP65 (dust-tight, water jet protected) |

### 3.6 Dimensions

**Overall Dimensions:**

| Parameter | Dimension (mm) | Notes |
|-----------|----------------|-------|
| **Total Height (L)** | 101.5 | From mounting face to top of electronic module |
| **Sensor Housing Height (L1)** | 37 | From mounting face to sensor housing top |
| **Sensor Housing Width** | 56 | Sensor housing diameter |
| **Sensor Projection** | 80.9 | Sensor housing projection from mounting face (into vessel) |
| **Mounting Flange** | 61.8 × 59.5 | Sight glass mounting flange dimensions |
| **Electronic Module Height** | ~64.5 | From sensor housing top to module top (L - L1) |

**Installation Clearances:**
- **Top access**: 150-200mm above mounting face for electronic module removal
- **Radial access**: 75-100mm around sensor for cable routing and module service
- **Cable routing**: Allow space for cable exit from electronic module (1m or 3m cable)
- **Internal clearance**: Verify 80.9mm sensor projection fits inside vessel

### 3.7 Cable Length Options

| Option | 24VAC Model | 230VAC Model |
|--------|-------------|--------------|
| **1m cable glands** | TK1P-KIT-0150-03 | TK1P-KIT-01E0-03 |
| **3m cable glands** | TK1P-KIT-0130-03 | TK1P-KIT-01C0-03 |

**Molded cable options**: Available on request (consult supplier for ordering codes)

### 3.8 Refrigerant & Oil Compatibility

**Compatible Refrigerants:**
- All HFC, HCFC, CFC refrigerants (R134a, R404A, R407C, R410A, R22, R502, etc.)
- **CO2 (R744)**: 46 bar model for subcritical (up to 46 bar), 100 bar model for transcritical (up to 100 bar)
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

**Compressor Crankcase Level Monitoring:**
- Replace sight glass with TK1+ (automated level detection vs manual visual inspection)
- High-level alarm (NO relay closes when oil high, shuts down compressor)
- Low-level alarm (NC relay opens when oil low, triggers oil feed)
- LED indication for quick visual verification during service

**Oil Separator Level Control:**
- High-level detection (relay activates oil return solenoid to compressor crankcase)
- 1/4" NPT female for mechanical oil return line (optional)
- CO2 transcritical (100 bar model) or standard refrigeration (46 bar model)

**Oil Reservoir Level Alarms:**
- Low-level warning (NC relay fail-safe, opens when oil low)
- High-level alarm (NO relay closes when oil high, prevents overfill)
- LED indication for quick tank level check

**Liquid Receiver Level Monitoring:**
- Overfill protection (NO relay closes when liquid high, stops liquid feed)
- Low-level alarm (NC relay opens when liquid low, triggers refill sequence)
- Dual relay outputs (high + low level alarms from single unit)

**CO2 Transcritical Systems (100 bar model):**
- Oil separator high-level detection (85-100 bar operating pressure)
- Flash gas separator level control
- High-pressure receiver level alarms

### 4.2 Pressure Rating Selection Guide

**TK1+ (46 bar) vs TK1+ (100 bar):**

| Criteria | TK1+ (46 bar) | TK1+ (100 bar) |
|----------|---------------|----------------|
| **Pressure** | ≤ 46 bar | 46-100 bar |
| **Applications** | Standard refrigeration | CO2 transcritical, high-pressure |
| **Temperature** | -40°C to +85°C | -40°C to +85°C |
| **Relay Outputs** | 230VAC @ 2A | 230VAC @ 2A |
| **LED Indicators** | Yes | Yes |
| **Sight Glass Mount** | Yes | Yes |
| **Cost** | Lower | Higher (~30% more) |

**⚠️ CRITICAL**: Pressure rating must be specified at order time. Verify system operating pressure and select appropriate model.

**Decision Tree:**

```
START
│
├─ Pressure ≤ 46 bar? ──YES──> TK1+ (46 bar)
│   └─NO (46-100 bar)
│
├─ Pressure 46-100 bar? ──YES──> TK1+ (100 bar)
│   └─NO (> 100 bar - contact Teklab or use LC-PH 120 bar)
│
├─ Sight glass port available? ──YES──> TK1+ (46 bar or 100 bar)
│   └─NO (threaded port)
│
├─ Relay outputs required (2A)? ──YES──> TK1+ (46 bar or 100 bar)
│   └─NO (100mA sufficient)
│
├─ LED indicators required? ──YES──> TK1+ (46 bar or 100 bar)
│   └─NO (not needed)
│
└─> TK1+ (46 bar) or TK1+ (100 bar) - choose based on pressure
```

### 4.3 TK1+ vs Other Level Switches

| Feature | LC-PS | LC-PH | LC-XT/XP | Rotalock | **TK1+** |
|---------|-------|-------|----------|----------|----------|
| **Pressure** | 46 bar | 120 bar | 46/120 bar | 46 bar | **46/100 bar** |
| **Media Temp** | -40 to +85°C | -40 to +125°C | -40 to +125°C | -40 to +125°C | **-40 to +85°C** |
| **Output** | 100mA | 100mA | 100mA | 100mA | **Relay 2A (NO + NC)** |
| **LEDs** | No | No | No | No | **Yes (integrated)** |
| **Mounting** | Threaded adapters | Threaded adapters | Threaded adapters | Rotalock | **Sight glass** |
| **Connection** | Cable | Cable/M12 | EN175301-803A | EN175301-803A | **Cable glands** |
| **Oil Return** | No | No | No | No | **1/4" NPT female** |
| **Relative Cost** | Lowest | Medium | Medium-High | Medium | Medium |

**Choose TK1+ when**:
- Sight glass port available (existing sight glass replacement)
- Relay outputs required (2A current capability, drives contactors directly)
- NO + NC simultaneous outputs needed (dual alarms from single unit)
- Integrated LED indicators required (visual status verification)
- 1/4" NPT female oil return connection needed
- 46 bar or 100 bar pressure range suitable

**Choose LC-PS/LC-PH/LC-XT/LC-XP when**:
- Threaded port mounting (no sight glass port)
- 100mA solid-state output sufficient (lower power, simpler wiring)
- Higher pressure required (LC-PH 120 bar, LC-XP 120 bar)
- Extended temperature required (LC-PH/LC-XT/LC-XP +125°C)

**Choose Rotalock when**:
- Rotalock connection required (compact design, Rotalock valve ports)

---

## 5. INSTALLATION & SERVICE

### 5.1 Pre-Installation Checklist

**Verify Requirements:**
- [ ] Pressure: TK1+ (46 bar) ≤ 46 bar, TK1+ (100 bar) ≤ 100 bar
- [ ] Media temperature -40°C to +85°C
- [ ] Sight glass port available (61.8mm × 59.5mm flange or compatible)
- [ ] Adequate clearance (101.5mm height + 150-200mm top access for module)
- [ ] Power supply voltage matches TK1+ model (24VAC or 230VAC)
- [ ] Relay load current ≤ 2A (verify contactor coil, solenoid, or alarm current)
- [ ] Cable length sufficient (1m or 3m standard, verify routing distance)
- [ ] Internal vessel clearance for 80.9mm sensor projection

**Tools & Materials:**
- Torque wrench (per sight glass flange gasket requirements)
- Sight glass gasket (new, compatible with refrigerant/oil)
- Multimeter (for relay output verification)
- Wire strippers, crimpers, terminal blocks
- Fuse (1A slow-blow for power supply circuit)

### 5.2 Sensor Housing Installation (Sight Glass Mounting)

**Step 1: Remove Old Sight Glass**
- De-pressurize equipment per safety procedures (lockout/tagout)
- Remove old sight glass and gasket from sight glass port
- Clean sight glass flange surface (remove old gasket residue, debris)
- Inspect sight glass port threads/bolts (verify no damage)

**Step 2: Install Sensor Housing**
- Position new gasket on sight glass port (verify proper alignment)
- Position TK1+ sensor housing with sight glass flange (align bolt holes)
- Install mounting bolts (hand-start all bolts before tightening)
- Torque bolts per equipment manufacturer specifications (typically 15-25 N·m, consult equipment manual)
- Verify sensor housing secure (no movement, gasket compressed evenly)

**Step 3: Orientation Verification**
- Sensor housing pointing **downward** into vessel (fused glass dome at bottom)
- Electronic module mounting surface on top (accessible for module installation)
- 1/4" NPT female connection accessible (if oil return line needed)
- Verify 80.9mm sensor projection fits inside vessel (no interference)

**Step 4: Leak Test**
- Pressure test equipment per normal procedures
- Verify no leakage at sight glass flange gasket
- Re-torque bolts if necessary (up to specified torque max)

### 5.3 Electronic Module Installation

**Step 1: Install Electronic Module**
- Align module with sensor housing (bayonet-style internal connector)
- Hand-screw module onto sensor housing (finger-tight, **no tools**)
- Verify module seated flush (internal electrical connection automatic)
- LED indicators now visible on module face

**Step 2: Cable Routing**
- Route cable from electronic module to junction box or control panel
- Avoid sharp bends (minimum bend radius ~50mm)
- Secure cable with cable ties (avoid excessive tension)
- Keep cable away from hot surfaces, moving parts

### 5.4 Relay Output Wiring

**Step 1: Identify Cable Conductors**
- **Typical 4-5 conductor cable**:
  - Power (+) - typically brown or red
  - Power (-) / Common - typically blue or black
  - NO relay output - typically white or gray
  - NC relay output - typically yellow or orange
  - Ground (optional) - typically green/yellow stripe

**⚠️ WARNING**: Verify conductor colors with TK1+ label or supplier documentation (cable colors may vary).

**Step 2: Wire to Terminal Block or Control Panel**
1. **De-energize power supply** (lockout/tagout)
2. Strip cable conductors (6-8mm, avoid excessive bare wire)
3. Connect to terminal block or PLC inputs:
   - Power (+) to 24VAC or 230VAC supply (per model)
   - Power (-) / Common to supply common/neutral
   - NO relay output to high-level alarm, contactor coil, or PLC input
   - NC relay output to low-level alarm, fail-safe circuit, or PLC input
   - Ground to PE (if required)
4. Verify polarity (especially 24VAC models if polarized)
5. Secure connections (torque per terminal manufacturer specs)
6. Test continuity (multimeter, de-energized)

**Relay Output Wiring Examples:**

**Example 1: High-Level Alarm (NO relay)**
- NO relay output → Alarm horn or indicator lamp (series with 230VAC supply)
- When liquid detected: NO relay closes, alarm activates

**Example 2: Low-Level Alarm (NC relay, fail-safe)**
- NC relay output → Alarm circuit or shutdown relay (series with 230VAC supply)
- When liquid detected: NC relay opens, alarm circuit de-energizes (normal)
- When liquid low: NC relay remains closed, alarm circuit energized (alarm)
- If module fails: NC relay opens, alarm activates (fail-safe)

**Example 3: Contactor Control (NO relay)**
- NO relay output → Contactor coil (230VAC @ 1.5A typical)
- Verify coil current ≤ 2A (relay rating)
- Use suppression diode or snubber (RC network) across coil (inductive load protection)

**Fuse Protection:**
- Install 1A slow-blow fuse in power supply circuit (per electrical code)

### 5.5 Commissioning

**Step 1: Pre-Startup Verification**
- [ ] Sensor housing torqued to specifications (sight glass flange gasket)
- [ ] Electronic module hand-tight on sensor housing
- [ ] Cable secure and routed properly (no kinks, tension)
- [ ] Electrical connections secure and correct polarity
- [ ] Power supply voltage matches TK1+ model
- [ ] Relay output wiring correct (NO, NC logic verified)
- [ ] Fuse installed (1A slow-blow)

**Step 2: Power-On Test (System Empty, Air)**
- Energize power supply
- Verify LED indication: **Green** (air/no liquid detected)
- Measure relay outputs with multimeter:
  - **NO relay**: Should be OPEN (no continuity)
  - **NC relay**: Should be CLOSED (continuity)
- If incorrect: Verify wiring, power supply voltage, module seating

**Step 3: Functional Test (System Filled, Liquid)**
- Fill equipment with liquid to submerge sensor dome (80.9mm depth minimum)
- Verify LED indication changes: **Yellow or Red** (liquid detected)
- Measure relay outputs with multimeter:
  - **NO relay**: Should CLOSE (continuity)
  - **NC relay**: Should OPEN (no continuity)
- Verify relay output changes in < 1 second (fast response)

**Step 4: Drain Test (Liquid → Air)**
- Drain liquid to expose sensor dome
- Verify LED indication returns to **Green** (air/no liquid detected)
- Verify relay outputs return to air state (NO open, NC closed)
- Response time < 1 second

**Step 5: Load Test (Relay Outputs)**
- Connect relay outputs to actual loads (contactors, alarms, etc.)
- Verify loads activate correctly when relay outputs change state
- Verify no excessive voltage drop or current (relay rated 2A max)

### 5.6 Maintenance

**Routine Maintenance:**
- **Quarterly**: Visual inspection (leaks, cable integrity, LED status)
- **Annually**: Functional test (verify relay output state changes)
- **No scheduled component replacement** (replace only if failed)

**Inspection Checklist:**
- [ ] Sight glass flange gasket secure (no leaks)
- [ ] Sensor housing secure (no loosening)
- [ ] Electronic module secure (hand-tight, no vibration loosening)
- [ ] Fused glass dome intact (no cracks, chips, cloudiness)
- [ ] Cable intact (no kinks, cuts, insulation damage)
- [ ] Electrical connections secure (no corrosion, loosening)
- [ ] LED indication correct (green in air, yellow/red in liquid)
- [ ] Relay outputs correct (measure with multimeter)
- [ ] 1/4" NPT female connection plugged or oil return line secure (if used)

**LED Status Verification:**
- **Normal operation**: Green (air) or Yellow/Red (liquid), steady
- **Abnormal**: Flashing LED (possible module malfunction, verify with supplier)
- **No LED**: Module power failure (check power supply, fuse, cable connections)

### 5.7 Electronic Module Replacement

**When to Replace Electronic Module:**
- No LED indication (module power failure)
- Incorrect relay output states (module electronics failure)
- Physical damage to module or cable
- Preventive replacement (after lightning strike, power surge)

**Replacement Procedure (5-10 Minutes, No Depressurization):**

1. **Disconnect Cable** (terminal block or control panel)
2. **Disconnect Power** (lockout/tagout)
3. **Hand-Unscrew Electronic Module**:
   - Rotate module counter-clockwise (no tools, finger-tight)
   - Lift module straight up (internal connector disengages automatically)
4. **Inspect Sensor Housing**:
   - Verify threads intact (no cross-threading)
   - Check fused glass dome (no damage)
   - Verify sight glass flange gasket secure (no leaks)
5. **Install New Electronic Module**:
   - Align module with sensor housing (bayonet-style connector)
   - Press down gently and rotate clockwise (hand-tight, no tools)
   - Verify module seated flush (internal connector engaged)
6. **Reconnect Cable** (terminal block or control panel)
7. **Restore Power** and verify operation:
   - Test LED indication (green in air, yellow/red in liquid)
   - Test relay outputs (NO, NC state changes per commissioning)

**Cost Savings:**
- Electronic module replacement: ~50-60% cost of complete sensor assembly
- No refrigerant recovery: Saves time and refrigerant
- No leak testing: System remains sealed
- Minimal downtime: 5-10 minutes

---

## 6. FREQUENTLY ASKED QUESTIONS (FAQ)

### 6.1 Product Classification

**Q1: What is the difference between TK1+ (46 bar) and TK1+ (100 bar)?**

**Pressure rating only**:
- **TK1+ (46 bar)**: Standard refrigeration (R134a, R404A, R407C, R410A, ammonia ≤ 46 bar)
- **TK1+ (100 bar)**: CO2 transcritical systems, high-pressure applications (46-100 bar)

**All other features identical**: Relay outputs (230VAC @ 2A), LED indicators, sight glass mounting, 1/4" NPT female, -40°C to +85°C temperature range.

**⚠️ CRITICAL**: Specify pressure rating at order time (46 bar or 100 bar).

**Q2: What does "sight glass replacement" mean?**

TK1+ mounts directly on existing **sight glass ports** (replaces traditional sight glass):
- **Traditional sight glass**: Manual visual inspection through glass
- **TK1+ level switch**: Automated detection with relay outputs + LED indicators
- **Mounting**: Same sight glass flange (61.8mm × 59.5mm), no additional adapters
- **Advantage**: Automated control vs manual inspection, relay outputs for alarms/control

**Q3: What does "two-part design" mean?**

The TK1+ consists of two parts:

1. **Part 1: Sensor Housing with Sight Glass Flange** (permanent pressure boundary)
   - Nickel-plated steel body, fused glass dome, sight glass flange
   - 46 bar or 100 bar rated
   - Remains on equipment during service

2. **Part 2: Electronic Module** (replaceable without depressurization)
   - Relay electronics, LED indicators, cable connection
   - **Can be replaced in 5-10 minutes without emptying or depressurizing system**
   - Hand-screw removal (no tools)

### 6.2 Relay Outputs & LEDs

**Q4: What are the relay output ratings?**

**Contact-free relay outputs**: NO (Normally Open) and NC (Normally Closed) available **simultaneously**
- **Rating**: Up to 230VAC @ 2A maximum
- **Type**: Solid-state relay (no mechanical contacts)
- **Applications**: Drives contactors, solenoid valves, alarm circuits, PLC inputs

**Q5: What does "contact-free relay" mean?**

**Solid-state relay** with no mechanical contacts:
- **Higher reliability**: No contact wear, bounce, or oxidation
- **Longer life**: Typical lifespan exceeds mechanical relays by 5-10x
- **Faster switching**: No mechanical inertia (< 1 second response)
- **No maintenance**: No contact cleaning or replacement

**Q6: Can I use both NO and NC relay outputs at the same time?**

**Yes**. NO and NC relay outputs available **simultaneously**:
- **NO relay**: High-level alarm (closes when liquid detected)
- **NC relay**: Low-level alarm (opens when liquid detected, fail-safe)
- **Dual monitoring**: Redundant alarm systems, high + low level from single unit

**Q7: What are the integrated LEDs for?**

**LED status indicators** on electronic module face:
- **Green**: Air/no liquid detected (sensor in air)
- **Yellow or Red**: Liquid detected (sensor submerged)
- **Purpose**: Visual verification without multimeter (commissioning, troubleshooting, quick status check)

**Advantages**:
- Commissioning aid (verify detection during startup)
- Troubleshooting (quick visual check during service)
- Remote indication (visible from 10-15m)

### 6.3 Pressure & Temperature

**Q8: Which model for CO2 transcritical (85 bar)?**

**TK1+ (100 bar)** - CO2 transcritical rated:
- Oil separator high-level detection (85-100 bar)
- Flash gas separator level control
- High-pressure receiver level alarms

**TK1+ (46 bar)** is **NOT suitable** for CO2 transcritical (exceeds 46 bar rating).

**Q9: What is the temperature range?**

**Both TK1+ (46 bar) and TK1+ (100 bar)**: -40°C to +85°C media temperature

**Note**: Temperature range **lower than LC-PH/LC-XT/LC-XP** (-40°C to +125°C). For higher temperature (>+85°C), use LC-PH or LC-XT/LC-XP.

**Q10: Can TK1+ be used for ammonia?**

**Yes**, fully compatible with ammonia (NH3):
- **Nickel-plated steel housing**: Suitable for ammonia systems
- **Pressure rating**: 46 bar (TK1+) suitable for most ammonia systems (typically 20-40 bar)
- **Fused glass**: Chemically inert to ammonia
- **Sight glass mounting**: Common on ammonia compressors, separators, reservoirs

### 6.4 Installation & Mounting

**Q11: What is the 1/4" NPT female connection for?**

**Optional oil return line** connection integrated on sensor housing:
- **Purpose**: Connect mechanical oil return line (TK1+ high-level detection triggers oil return solenoid, 1/4" NPT line returns oil)
- **Usage**: Optional (plug if not used)
- **Applications**: Oil separator with automated oil return, compressor crankcase oil transfer

**Q12: Can I mount TK1+ horizontally?**

**Yes**, if sight glass port is horizontal:
- Verify proper liquid contact with sensor dome (orientation affects liquid coverage)
- Verify cable routing and module accessibility (horizontal mount may complicate cable exit)
- **Preferred**: Vertical mount (sensor pointing downward, module on top for easy access)

**Q13: What if my sight glass flange is different size?**

**Standard**: TK1+ sight glass flange 61.8mm × 59.5mm (common sight glass dimensions)

**If different**:
- Consult supplier for adapter or custom sight glass flange
- Verify existing sight glass flange dimensions (measure bolt hole spacing, flange size)
- Custom adapters may be available (contact Teklab with equipment details)

### 6.5 Comparison & Selection

**Q14: TK1+ vs LC-PS/LC-PH - which to choose?**

| Need sight glass mounting? | Need relay outputs (2A)? | Need LED indicators? | Recommendation |
|----------------------------|-------------------------|---------------------|----------------|
| **YES** | YES or NO | YES or NO | **TK1+** (46 bar or 100 bar) |
| **NO** (threaded port) | NO (100mA sufficient) | NO | LC-PS (46 bar) or LC-PH (120 bar) - lower cost |
| **NO** (threaded port) | YES | YES | **TK1+** (if sight glass adapter available) |

**TK1+ advantages**:
- Sight glass mounting (no adapters, direct replacement)
- Relay outputs 230VAC @ 2A (vs 100mA solid-state)
- NO + NC simultaneous (dual alarms from single unit)
- Integrated LED indicators (visual status verification)
- 1/4" NPT female (oil return line)

**LC-PS/LC-PH advantages**:
- Multiple threaded adapters (1/2" NPT, 3/4" NPT, M20×1.5, 1" 1/8 UNEF, 1" 1/4 RLK)
- LC-PH: 120 bar high pressure (vs 100 bar TK1+)
- LC-PH: Extended temperature +125°C (vs +85°C TK1+)
- Lower cost (~20-30% less expensive)

**Q15: TK1+ vs Rotalock - which to choose?**

| Feature | TK1+ | Rotalock |
|---------|------|----------|
| **Mounting** | Sight glass | Rotalock connection |
| **Pressure** | 46 or 100 bar | 46 bar |
| **Output** | Relay 2A (NO + NC) | 100mA solid-state |
| **LEDs** | Yes (integrated) | No |
| **Connection** | Cable glands | EN175301-803A connector |
| **Oil Return** | 1/4" NPT female | No |

**Choose TK1+**: Sight glass port available, relay outputs (2A), LED indicators, 1/4" NPT oil return  
**Choose Rotalock**: Rotalock port required, compact design, industrial connector

**Q16: Does TK1+ have automatic valve like TK3+?**

**No**. TK1+ is a **level switch only** (detection, not regulation):
- Detects liquid presence/absence
- Relay outputs signal external controls
- Requires external valve, pump, or control for automated actions

**For level regulation** (detection + valve + automatic control), use **TK3+** (46/80/130 bar) or **TK4** (46/80/130 bar smart) series.

### 6.6 Reliability & Compatibility

**Q17: What is the reliability/lifespan?**

**High reliability** (no mechanical moving parts):
- **No floats, reeds, linkages**: Eliminates mechanical failure modes
- **Contact-free relay**: Solid-state (no contact wear, longer life than mechanical relays)
- **Fused glass hermetic seal**: No O-rings, no degradation
- **Typical lifespan**: 10-15 years in normal applications

**Q18: What refrigerants are compatible?**

**All refrigerants** (fused glass chemically inert):
- HFC/HCFC/CFC: R134a, R404A, R407C, R410A, R22, R502, etc.
- **CO2 (R744)**: 46 bar model for subcritical (up to 46 bar), 100 bar model for transcritical (up to 100 bar)
- **Ammonia (NH3)**: Fully compatible (nickel-plated steel suitable)
- Hydrocarbons (HC): R290, R600a, etc.
- Low-GWP: R1234yf, R1234ze, R452A, R454B, etc.

**All oils**: Mineral, POE, PVE, PAG, AB (fused glass chemically inert).

---

## 7. ORDERING INFORMATION

### 7.1 Model Code Structure

**Format**: `TK1P-KIT-[Voltage Code][Cable Length]-03`

**Example**: **TK1P-KIT-0150-03** (24VAC, cable glands, 1m)  
**Example**: **TK1P-KIT-01E0-03** (230VAC, cable glands, 1m)

### 7.2 Standard Model Codes

**Cable Length & Voltage Options:**

| Cable Length | 24VAC Model | 230VAC Model |
|--------------|-------------|--------------|
| **1m cable glands** | TK1P-KIT-0150-03 | TK1P-KIT-01E0-03 |
| **3m cable glands** | TK1P-KIT-0130-03 | TK1P-KIT-01C0-03 |

**⚠️ CRITICAL**: Specify pressure rating at order time (46 bar or 100 bar) - contact supplier to specify.

**Molded cable options**: Available on request (consult supplier for ordering codes).

### 7.3 Selection Parameters

**Pressure Rating:**
- **46 bar model**: Standard refrigeration (R134a, R404A, R407C, R410A, ammonia ≤ 46 bar)
- **100 bar model**: CO2 transcritical systems, high-pressure applications (46-100 bar)

**Voltage Selection:**
- **015** = 24VAC ±10%
- **01E** = 230VAC ±10%

**Cable Length:**
- **0** (4th digit) = 1m cable glands
- **3** (4th digit) = 3m cable glands

### 7.4 What's Included

- TK1+ two-part assembly (sensor housing + electronic module)
- Sight glass mounting flange (61.8mm × 59.5mm, integrated on sensor housing)
- Cable with cable glands (1m or 3m depending on model)
- 1/4" NPT female connection (oil return line, optional use)
- Integrated LED status indicators on electronic module
- Contact-free relay outputs (NO + NC simultaneous)
- Installation instructions

### 7.5 What's NOT Included

- **Sight glass gasket**: Order separately (compatible with refrigerant/oil)
- **External valve**: TK1+ is detection only (use TK3+/TK4 for integrated valve)
- **Relay coils/contactors**: External control devices driven by TK1+ relay outputs (if needed)
- **Molded cable versions**: Order separately if required (specify at order)

### 7.6 Ordering Examples

**Example 1: R404A Compressor Crankcase (Sight Glass Replacement)**
- Application: Replace sight glass with TK1+ level control, 18 bar operating pressure
- Voltage: 24VAC (BMS integration)
- Cable: 1m (nearby control panel)
- Pressure rating: 46 bar (specify at order)
- **Order**: TK1P-KIT-0150-03 (24VAC, 1m cable, **46 bar specified**)
- Logic: NO relay closes when oil high (shutdown), NC relay opens when oil low (alarm)

**Example 2: CO2 Transcritical Oil Separator (High-Level Alarm)**
- Application: 85 bar operating pressure, 3m cable run to control panel
- Voltage: 24VAC (PLC integration)
- Cable: 3m (extended cable run)
- Pressure rating: 100 bar (specify at order)
- **Order**: TK1P-KIT-0130-03 (24VAC, 3m cable, **100 bar specified**)
- Logic: NO relay activates oil return solenoid when oil level high

**Example 3: Ammonia Receiver (Low-Level Shutdown)**
- Application: 22 bar operating pressure, 230VAC control system
- Voltage: 230VAC (European mains)
- Cable: 1m (nearby electrical panel)
- Pressure rating: 46 bar (specify at order)
- **Order**: TK1P-KIT-01E0-03 (230VAC, 1m cable, **46 bar specified**)
- Logic: NC relay opens (fail-safe) when refrigerant level low, triggers shutdown

---

## Document Information

**Document**: TK1+ Complete Product Documentation  
**Version**: 1.0  
**Date**: 2025-11-12  
**Language**: English  
**Product**: TK1+ (46 bar / 100 bar) Optical Level Control Unit  
**Category**: Level_Switches  
**Keywords**: TK1+, TK1P, optical level switch, sight glass replacement, relay outputs, LED indicators, 46 bar, 100 bar, CO2 transcritical, two-part design, level detection, contact-free relay, 1/4" NPT female, oil return

**© 2025 Teklab. All rights reserved.**
