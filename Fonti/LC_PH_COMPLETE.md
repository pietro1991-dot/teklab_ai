---
category: Level_Switches
keywords:
- LC-PH
- LC-PH level switch
- 120 bar high pressure
- optical level sensor
- two-part design
- replaceable electronics
- CO2 transcritical
- CO2 subcritical
- ammonia NH3
- cable connection
- M12 connector
- high pressure applications
- sight glass mounting
- G3/8 thread
language: EN
product: LC_PH
document_type: unified_complete
last_updated: 2025-11-15
---

# LC-PH - Complete Product Documentation

**Optical Level Switch for High-Pressure Applications (up to 120 bar)**

---

## 📋 Document Structure

This unified document covers the complete LC-PH product organized in the following sections:

1. **Product Overview** - Description, operating principle, and key advantages
2. **Detection Technology & Features** - Optical sensor, two-part design, construction
3. **Technical Specifications** - Electrical, mechanical, environmental specs
4. **Applications & Selection** - Use cases and selection guide
5. **Installation & Service** - Mounting, wiring, dimensions, maintenance
6. **FAQ** - Frequently asked questions

---

## 1. PRODUCT OVERVIEW

### LC-PH Description

The **LC-PH** is an optical level switch designed for level monitoring in high-pressure refrigeration systems up to 120 bar. This two-part unit provides reliable liquid presence/absence detection with revolutionary replaceable electronics, specifically engineered for CO2 transcritical, CO2 subcritical, ammonia, and high-pressure industrial applications.

**⚠️ IMPORTANT: LC-PH is a LEVEL SWITCH ONLY - It does NOT include a solenoid valve.**
- For automatic oil level regulation with integrated valve, see **TK3+** or **TK4** series.
- LC-PH provides detection signal only (requires external control for automated actions).

**Core Technology:**
- Electro-optic infrared sensor (fused glass hermetic seal)
- Solid-state output (NO or NC, 100mA max)
- Two-part serviceable design (electronics replaceable without depressurization)
- **120 bar maximum working pressure** (CO2 transcritical rated)
- **Extended temperature range** (-40°C to +125°C media temp)
- Factory calibrated, plug-and-play operation

**Primary Applications:**
- **CO2 transcritical systems**: Gas cooler, receiver, separator level monitoring (80-120 bar)
- **CO2 subcritical systems**: Liquid receiver, oil separator monitoring (40-70 bar)
- **Ammonia systems**: High-pressure vessel, receiver, separator level detection
- **High-pressure industrial**: Oil separator, receiver level control (up to 120 bar)

**Key Differentiators:**
- **vs LC-PS**: LC-PH is 120 bar / -40°C to +125°C (extended), LC-PS is 46 bar / -40°C to +85°C (standard)
- **vs LC-XT/XP**: LC-PH has cable/M12 connection, LC-XT/XP have EN175301-803A industrial connector
- **vs LC-XP**: LC-PH cable/M12 connection, LC-XP EN175301-803A + stainless steel housing (both 120 bar)
- **vs TK1+**: LC-PH is 100mA solid-state output, TK1+ has 2A relay output with LED indication
- **vs TK3+/TK4**: LC-PH is detection only (no valve), TK3+/TK4 are complete regulators with valve

**Selection Criteria:**
- Pressure 46-120 bar (for ≤ 46 bar, LC-PS is lower cost)
- Media temperature -40°C to +125°C (extended range vs LC-PS -40°C to +85°C)
- CO2 transcritical applications (gas cooler 80-120 bar)
- Cable or M12 connector preferred (vs EN175301-803A on LC-XT/XP)
- Solid-state output 100mA sufficient (vs relay output on TK1+)

**Operating Principle:**

The LC-PH uses electro-optic infrared detection through a fused glass dome:

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

**Advantages Over Mechanical Level Switches:**
- No moving parts (no float mechanism degradation)
- No magnetic reed switches (no contamination, sticking, or wear)
- Works with all oils and refrigerants (chemically inert glass)
- Immune to foam, bubbles, turbulence (optical detection)
- High-pressure rated (120 bar vs typical 40-60 bar for mechanical)
- Extended temperature range (-40°C to +125°C vs typical -40°C to +85°C)

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
- **High-pressure rated**: 120 bar maximum (thicker glass dome vs 46 bar models)

**Fused Glass Hermetic Seal:**
- **Glass-to-metal fusion**: Molecular-level seal (NOT O-ring)
- **Zero leakage**: 10^-12 mbar·L/s (true hermetic)
- **Chemically inert**: Compatible with all oils and refrigerants (including CO2, ammonia)
- **Pressure rated**: 120 bar maximum working pressure
- **Temperature rated**: -40°C to +125°C media temperature (extended range)
- **Lifetime seal**: No degradation, no maintenance

**Output Signal:**
- **Type**: Solid-state semiconductor output (NOT mechanical relay)
- **Current rating**: 100mA maximum (suitable for PLC inputs, low-power relay coils)
- **Configuration**: NO (Normally Open in air) or NC (Normally Closed in air) - factory-set
- **Voltage**: Matches supply voltage (24VAC/DC, 115VAC, 230VAC)

**Important Output Notes:**
- **Factory-configured**: NO or NC output cannot be changed in field (order correct version)
- **NO in air**: Output OPEN when air, CLOSES when liquid detected
  - Use for: High-level alarms (alarm activates when liquid present)
- **NC in air**: Output CLOSED when air, OPENS when liquid detected
  - Use for: Low-level alarms, fail-safe protection (alarm activates when liquid absent)

### 2.2 Two-Part Revolutionary Design

**Part 1: Sensor Housing (Permanent Pressure Boundary)**
- **Components**: Fused glass dome, nickel-plated steel body, adapter threads
- **Function**: Pressure containment, liquid detection surface
- **Installation**: Permanent (remains on equipment during service)
- **Pressure rating**: 120 bar maximum
- **Temperature rating**: -40°C to +125°C media temperature
- **Service**: Only removed for complete sensor replacement (rare)

**Part 2: Electronic Module (Replaceable Without Depressurization)**
- **Components**: Infrared LED, optical receiver, power supply, output driver, PA glass fiber housing
- **Function**: Detection electronics and signal processing
- **Installation**: Hand-screw onto sensor housing (finger-tight, no tools)
- **Service**: Replaceable in 5-10 minutes without system depressurization
- **Advantages**: Minimal downtime, no refrigerant recovery, no leak risk

**Service Procedure (Electronic Module Replacement):**
1. Disconnect power (lockout/tagout)
2. Disconnect cable or M12 connector
3. Hand-unscrew electronic module from sensor housing (no tools)
4. Install new electronic module (hand-screw, finger-tight)
5. Reconnect cable or M12 connector
6. Restore power and verify operation

**Time**: 5-10 minutes  
**Cost**: Electronic module replacement vs complete sensor assembly (50-60% cost savings)  
**Downtime**: Minimal (no depressurization, no refrigerant recovery)

### 2.3 Construction & Reliability

**Housing Materials:**
- **Sensor housing**: Nickel-plated steel (corrosion resistant, 120 bar rated)
- **Fused glass dome**: Borosilicate glass (chemically inert, pressure rated, thicker than 46 bar models)
- **Electronic module**: PA glass fiber reinforced (high-strength polymer)
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
- **CO2 (R744)**: Transcritical (80-120 bar) and subcritical (40-70 bar)
- **All HFC/HCFC/CFC**: R134a, R404A, R407C, R410A, R22, R502, etc.
- **Ammonia (NH3)**: Fully compatible (high-pressure systems)
- **Hydrocarbons (HC)**: R290, R600a, etc.
- **Low-GWP**: R1234yf, R1234ze, R452A, R454B, etc.
- **All oils**: Mineral, POE, PVE, PAG, AB (fused glass chemically inert)

### 2.4 Electrical Features

**Power Supply:**
- **Voltage options**: 24VAC/DC ±10%, 115VAC ±10% @ 60Hz, 230VAC ±10% @ 50Hz
- **Frequency**: 50/60 Hz (AC models)
- **Power consumption**: 20mA max during normal operation (ultra-low power)
- **Inrush current**: Minimal (no relay coil)

**Electrical Connection:**
- **Cable type**: 3-wire (power, output, ground)
- **Cable length**: 1m standard (longer lengths available on request)
- **M12×1 connector**: Optional (instead of cable, industrial standard)
- **Cable diameter**: ~6mm
- **Bend radius**: 30mm minimum (avoid kinking)

**Electrical Protection:**
- **Transient over-voltage protection**: Built-in (power surges, lightning)
- **Reverse polarity protection**: Internal (24VDC models)
- **Output short-circuit protection**: Current-limited to 100mA

**Customizable Delays (Available on Request):**
- **Activation delay**: Prevents false alarms from turbulence, foam, bubbles (typical 5-30 seconds)
- **Deactivation delay**: Filters transient liquid contact (typical 1-10 seconds)
- **Factory-programmed**: Specify delay requirements at order

### 2.5 Installation & Adapters

**6 Adapter Options:**

| Adapter Type | Thread | B Dimension (mm) | Typical Application |
|-------------|--------|------------------|---------------------|
| **1/2" NPT** | 1/2" NPT male | 24 | CO2 gas cooler, receiver, separator (most common) |
| **3/4" NPT** | 3/4" NPT male | 22 | Larger CO2/ammonia vessels |
| **1" NPT** | 1" NPT male | 27.9 | High-flow applications, large vessels |
| **M20×1.5** | M20×1.5 male | 18.1 | European compressors (metric, shortest) |
| **1" 1/8 UNEF** | 1" 1/8-12 UNEF male | 19 | Compressor service port direct mount |
| **1" 1/4 RLK** | 1" 1/4 RLK male | 30 | Rotalock valve ports (longest) |

**B Dimension** = Projection from mounting surface to end of adapter (sensor housing base)

**Adapter Installation:**
- **Torque**: 50 N·m (critical for sealing, especially high-pressure)
- **Sealant**: PTFE tape or liquid thread sealant per equipment guidelines
- **Orientation**: Typically vertical (sensor pointing downward into liquid)

**Sensor Housing Installation:**
- **Method**: Hand-screw onto adapter (finger-tight, no tools)
- **Torque**: Hand-tight only (do not use wrenches)
- **Seal**: Metal-to-metal seal (no gasket required)

**Electronic Module Installation:**
- **Method**: Hand-screw onto sensor housing (finger-tight, no tools)
- **Torque**: Hand-tight only (do not use wrenches)
- **Connection**: Bayonet-style internal electrical connector (automatic engagement)

---

## 3. TECHNICAL SPECIFICATIONS

### 3.1 Electrical Specifications

| Parameter | Specification |
|-----------|--------------|
| **Supply Voltage** | 24VAC/DC ±10% OR 115VAC ±10% @ 60Hz OR 230VAC ±10% @ 50Hz |
| **Supply Frequency** | 50/60 Hz (AC models) |
| **Supply Current** | 20mA max during normal operation |
| **Output Signal** | Solid-state output, NO or NC in air (factory-configured) |
| **Output Max Current** | 100mA maximum |
| **Output Voltage** | Matches supply voltage (24V, 115V, or 230V) |
| **Electronic Protections** | Transient over-voltage protection, reverse polarity (24VDC) |
| **Electrical Connection** | 3-wire cable 1m standard OR M12×1 connector (optional) |
| **Cable Diameter** | ~6mm |
| **Bend Radius** | 30mm minimum |

### 3.2 Mechanical Specifications

| Parameter | Specification |
|-----------|--------------|
| **Housing Material** | Nickel-plated steel (120 bar rated) / PA glass fiber reinforced |
| **Sensor Dome** | Fused glass technology (hermetic seal, 120 bar rated) |
| **Enclosure Protection** | IP65 (dust-tight, water jet protected) |
| **Adapter Torque** | 50 N·m for adapter installation on equipment |
| **Sensor Assembly** | Hand-screw with normal force (no tools, finger-tight) |
| **Weight** | ~350-400g total assembly (varies by adapter) |

### 3.3 Environmental & Pressure Specifications

| Parameter | Specification |
|-----------|--------------|
| **Media Temperature** | -40°C to +125°C (extended range) |
| **Ambient Temperature** | -40°C to +60°C |
| **Max Working Pressure** | **120 bar** (CO2 transcritical rated) |
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
- **Total height** (from mounting surface to top of electronic module): ~130mm
- **Components**: Adapter (18-30mm) + Sensor housing (~70-90mm) + Electronic module (~40mm)

**Installation Clearances:**
- **Top access**: 100-150mm above module for electronic module removal
- **Side access**: 50mm radial clearance for hand-screw operations
- **Cable routing**: 100-150mm clearance for cable exit and bend radius

### 3.7 Refrigerant & Oil Compatibility

**Compatible Refrigerants:**
- **CO2 (R744)**: Transcritical (80-120 bar) and subcritical (40-70 bar) - primary application
- **Ammonia (NH3)**: High-pressure systems (up to 120 bar)
- All HFC, HCFC, CFC refrigerants (R134a, R404A, R407C, R410A, R22, R502, etc.)
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

**CO2 Transcritical Systems (80-120 bar):**
- **Gas cooler outlet**: High-level alarm (prevent liquid accumulation, 90-110 bar typical)
- **High-pressure receiver**: Minimum/maximum level alarms (80-100 bar)
- **Flash gas separator**: Level control for pump-down or valve operation (70-90 bar)
- **Oil separator**: Oil level monitoring in CO2 transcritical compressors (80-100 bar)

**CO2 Subcritical Systems (40-70 bar):**
- **Liquid receiver**: High/low level alarms (50-65 bar)
- **Oil separator**: Oil return control (40-60 bar)
- **Accumulator**: Level monitoring (30-50 bar)

**Ammonia Systems (High-Pressure):**
- **High-pressure receiver**: Level monitoring (20-40 bar, 120 bar rating provides safety margin)
- **Oil separator**: Oil level detection (18-30 bar)
- **Economizer**: Level control (15-25 bar)

**High-Pressure Industrial:**
- **Oil separators**: High-pressure compressor systems (up to 120 bar)
- **Process vessels**: High-temperature / high-pressure level detection (-40°C to +125°C)

### 4.2 Application Examples

**Example 1: CO2 Transcritical Gas Cooler Outlet (100 bar)**
- **Application**: Prevent liquid accumulation in gas cooler (high-level alarm)
- **Pressure**: 90-110 bar (gas cooler outlet pressure)
- **Temperature**: +40°C to +80°C (gas cooler outlet temperature)
- **Model**: LC-PH7071000101A (1/2" NPT, 24VAC/DC, NO in air)
- **Logic**: Output CLOSES when liquid level high → Alarm activates
- **Action**: Alert technician or trigger automatic liquid drainage

**Example 2: CO2 Transcritical Receiver Low-Level Alarm (85 bar)**
- **Application**: Ensure minimum refrigerant charge (fail-safe)
- **Pressure**: 80-90 bar (receiver pressure)
- **Model**: LC-PH607D010101A (M20×1.5, 230VAC, NC in air)
- **Logic**: Output OPENS when liquid level low → Alarm activates
- **Action**: Alert technician to add refrigerant charge or check for leaks

**Example 3: Ammonia Oil Separator Level (25 bar)**
- **Application**: Monitor oil level in high-pressure ammonia separator
- **Pressure**: 20-30 bar (separator pressure, 120 bar rating provides safety margin)
- **Model**: LC-PH8071010101A (1" 1/8 UNEF, 24VAC/DC, NC in air)
- **Logic**: Output OPENS when oil low → Trigger oil drain valve
- **Action**: Automatic oil return to compressor crankcase

**Example 4: CO2 Subcritical Liquid Receiver (60 bar)**
- **Application**: High/low level alarms for liquid management
- **Pressure**: 50-65 bar (receiver pressure)
- **Configuration**: 2x LC-PH units (one for high level, one for low level)
- **Model High**: LC-PHA071000101A (3/4" NPT, 24VAC/DC, NO in air) - high-level alarm
- **Model Low**: LC-PHA071010101A (3/4" NPT, 24VAC/DC, NC in air) - low-level alarm
- **Benefit**: Comprehensive liquid management with fail-safe low-level protection

### 4.3 Selection Guide

**Step 1: Verify Pressure Requirement**
- **Pressure ≤ 46 bar**: Use LC-PS (46 bar, lower cost)
- **Pressure 46-120 bar**: Use LC-PH (120 bar, this product)
- **Pressure > 120 bar**: Contact Teklab for custom solution

**Step 2: Verify Temperature Requirement**
- **Media temp ≤ +85°C**: LC-PS acceptable (if pressure ≤ 46 bar)
- **Media temp +85°C to +125°C**: LC-PH required (extended temperature range)

**Step 3: Select Adapter Type**

| Application | Recommended Adapter |
|------------|---------------------|
| CO2 gas cooler / receiver / separator (1/2" port) | 1/2" NPT (most common) |
| Larger CO2/ammonia vessels (3/4" port) | 3/4" NPT |
| Large vessel with 1" NPT port | 1" NPT |
| European compressor (metric) | M20×1.5 (shortest projection) |
| Compressor service port | 1" 1/8 UNEF (direct mount) |
| Rotalock valve port | 1" 1/4 RLK (longest projection) |

**Step 4: Select Voltage**

| Application | Recommended Voltage |
|------------|---------------------|
| BMS/PLC integration (most common) | 24VAC/DC |
| North American mains power | 115VAC @ 60Hz |
| European/international mains power | 230VAC @ 50Hz |

**Step 5: Select Output Configuration**

| Application | Recommended Output |
|------------|-------------------|
| High-level alarm (alarm when liquid present) | NO (Normally Open in air) |
| Low-level alarm (fail-safe, alarm when liquid absent) | NC (Normally Closed in air) |
| Pump control (start pump when liquid present) | NO (Normally Open in air) |
| Valve control (open valve when liquid absent) | NC (Normally Closed in air) |

**⚠️ CRITICAL**: Output configuration is factory-set and **cannot be changed in field**. Order correct version.

### 4.4 Selection Decision Tree

```
START
│
├─ Pressure ≤ 46 bar AND Media temp ≤ +85°C? ──YES──> Use LC-PS (46 bar, lower cost)
│   └─NO
│
├─ Pressure 46-120 bar OR Media temp +85°C to +125°C? ──YES──> LC-PH (this product)
│   └─NO (> 120 bar)
│
├─ Industrial connector required? ──YES──> Use LC-XP (120 bar, EN175301-803A, stainless steel)
│   └─NO
│
├─ Relay output > 100mA required? ──YES──> Use TK1+ (100 bar, 2A relay output)
│   └─NO
│
├─ Integrated valve needed? ──YES──> Use TK3+ (46/80/130 bar) or TK4 (46/80/130 bar smart)
│   └─NO
│
└─> LC-PH (Standard choice for 46-120 bar, cable/M12 connection, 100mA output)
```

### 4.5 LC-PH vs Other Level Switches

| Feature | LC-PS | **LC-PH** | LC-XT | LC-XP | TK1+ |
|---------|-------|-----------|-------|-------|------|
| **Pressure** | 46 bar | **120 bar** | 46 bar | 120 bar | 46/100 bar |
| **Media Temp** | -40 to +85°C | **-40 to +125°C** | -40 to +125°C | -40 to +125°C | -40 to +85°C |
| **Output** | 100mA solid-state | **100mA solid-state** | 100mA solid-state | 100mA solid-state | 2A relay |
| **Connection** | 1m cable | **1m cable / M12** | EN175301-803A | EN175301-803A | Cable glands |
| **Housing** | Nickel-plated | **Nickel-plated** | Stainless steel | Stainless steel | Nickel-plated |
| **LED Indication** | No | **No** | No | No | Yes |
| **Mounting** | Threaded adapters | **Threaded adapters** | Threaded adapters | Threaded adapters | Sight-glass |
| **Relative Cost** | Lowest | **Medium** | Medium-High | High | Medium |

**Choose LC-PH when**:
- High pressure 46-120 bar (CO2 transcritical, ammonia, high-pressure systems)
- Extended temperature range (-40°C to +125°C)
- Cable or M12 connector preferred (no industrial connector required)
- 100mA output sufficient for PLC/BMS
- Medium cost acceptable (higher than LC-PS, lower than LC-XP)

---

## 5. INSTALLATION & SERVICE

### 5.1 Pre-Installation Checklist

**Verify Requirements:**
- [ ] Pressure 46-120 bar (use LC-PS if ≤ 46 bar for cost savings)
- [ ] Media temperature -40°C to +125°C (extended range vs LC-PS -40°C to +85°C)
- [ ] Equipment port matches adapter thread type
- [ ] Adequate clearance for sensor assembly (130mm height + 100-150mm top access)
- [ ] Power supply voltage matches LC-PH model (24VAC/DC, 115VAC, or 230VAC)
- [ ] Output configuration correct (NO or NC in air) - **cannot change in field**

**Tools & Materials:**
- Torque wrench (50 N·m for adapter installation)
- PTFE tape or liquid thread sealant (high-pressure rated)
- Multimeter (for wiring verification)
- Electrical conduit/cable protection (as required)
- M12 mating connector (if M12 version ordered)

### 5.2 Adapter Installation

**Step 1: Prepare Equipment Port**
- Clean port threads (remove old sealant, debris)
- Inspect threads for damage (repair if necessary)
- Verify port depth sufficient for adapter thread engagement

**Step 2: Apply Sealant (High-Pressure Critical)**
- PTFE tape: 3-4 wraps clockwise (viewed from thread end), high-pressure rated
- Liquid sealant: Apply per manufacturer instructions, CO2/ammonia compatible
- **Important**: Avoid sealant on first 2 threads (prevent contamination)

**Step 3: Install Adapter**
- Thread adapter into equipment port (hand-start, ensure straight)
- Torque to **50 N·m** (critical for sealing, especially high-pressure)
- Verify adapter orientation (sensor will point downward in most applications)

**Step 4: Leak Test (Critical for High-Pressure)**
- Pressure test equipment per normal procedures (up to 120 bar if transcritical)
- Verify no leakage at adapter threads (use leak detector, soap solution, or ammonia paper)
- Re-torque if necessary (up to 50 N·m max, do not exceed)

### 5.3 Sensor Housing Installation

**Step 1: Inspect Sensor Housing**
- Verify fused glass dome intact (no cracks, chips)
- Check adapter threads on sensor housing (no cross-threading)
- Confirm pressure rating label (120 bar)

**Step 2: Install Sensor Housing**
- Hand-screw sensor housing onto adapter (finger-tight, no tools)
- **Do NOT use wrenches** (hand-tight only, risk of glass damage)
- Verify sensor housing seated flush against adapter

**Step 3: Orientation**
- Typical: Sensor pointing **downward** into liquid
- Horizontal/upward: Verify with application engineer (ensure liquid contact)

### 5.4 Electronic Module Installation

**Step 1: Inspect Electronic Module**
- Verify cable intact (no kinks, cuts, insulation damage) OR M12 connector intact
- Check module threads (no cross-threading)
- Confirm voltage rating label matches power supply

**Step 2: Install Electronic Module**
- Align module with sensor housing (bayonet-style connector inside)
- Hand-screw module onto sensor housing (finger-tight, no tools)
- **Do NOT use wrenches** (hand-tight only)
- Verify module seated flush (internal electrical connection automatic)

**Step 3: Cable Routing (Cable Version)**
- Route cable with minimum 30mm bend radius (avoid kinking)
- Protect cable from sharp edges, hot surfaces (gas cooler outlet), moving parts
- Secure cable with cable ties or clamps (avoid strain on module)
- Allow 100-150mm clearance above module (for future service access)

**Step 4: M12 Connector (M12 Version)**
- Connect M12 mating connector (align keyway, hand-tighten)
- Verify IP67 rating maintained (connector properly seated)
- Secure cable to prevent strain on connector

### 5.5 Electrical Wiring

**3-Wire Connection (Cable Version):**
- **Wire 1**: Power supply (+) [typically brown wire]
- **Wire 2**: Output signal [typically black wire]
- **Wire 3**: Ground/Common (-) [typically blue wire]

**⚠️ WARNING**: Verify wire colors with LC-PH label (colors may vary by model).

**M12 Connector Pinout (M12 Version):**
- **Pin 1**: Power supply (+)
- **Pin 2**: Output signal
- **Pin 3**: Ground/Common (-)
- **Pin 4**: Not used (reserved)

**Wiring Procedure:**
1. **De-energize power supply** (lockout/tagout)
2. Strip wire ends (6-8mm, avoid nicking conductors) OR connect M12 mating connector
3. Connect wires to terminal block or PLC input:
   - Power (+) to supply voltage (24VAC/DC, 115VAC, or 230VAC)
   - Output to PLC input, relay coil, or alarm circuit
   - Ground (-) to common/neutral
4. Verify polarity (especially 24VDC models - reverse polarity protection, but avoid)
5. Secure connections (torque per terminal manufacturer specs)
6. Test continuity (multimeter, de-energized)

**Fuse Protection:**
- Install 1A slow-blow fuse in power supply circuit (per electrical code)

**Output Wiring:**

**NO (Normally Open in air) Configuration:**
```
Power Supply (+) ──> LC-PH Power (+)
LC-PH Output ──> Alarm/PLC Input (+)
Alarm/PLC Input (-) ──> Power Supply (-)
```
- Air: Output OPEN (no current flow to alarm/PLC)
- Liquid: Output CLOSES (current flows to alarm/PLC)

**NC (Normally Closed in air) Configuration:**
```
Power Supply (+) ──> LC-PH Power (+)
LC-PH Output ──> Alarm/PLC Input (+)
Alarm/PLC Input (-) ──> Power Supply (-)
```
- Air: Output CLOSED (current flows to alarm/PLC)
- Liquid: Output OPENS (no current flow to alarm/PLC)

### 5.6 Commissioning

**Step 1: Pre-Startup Verification**
- [ ] Adapter torqued to 50 N·m
- [ ] Sensor housing hand-tight on adapter
- [ ] Electronic module hand-tight on sensor housing
- [ ] Cable routed with adequate bend radius (30mm min) OR M12 connector secure
- [ ] Electrical connections secure and correct polarity
- [ ] Power supply voltage matches LC-PH model
- [ ] Output wiring correct (NO or NC logic verified)
- [ ] High-pressure leak test passed (up to 120 bar)

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

**Step 4: Alarm/Control Integration**
- Trigger alarm or control action (verify external systems respond)
- Test fail-safe logic (de-energize LC-PH, verify alarm activates if NC configuration)

**Step 5: High-Pressure Verification (CO2 Transcritical)**
- Slowly bring system to full operating pressure (80-120 bar)
- Monitor for leaks at adapter, sensor housing
- Verify LC-PH output stable (no false alarms from pressure transients)
- Perform functional test at full pressure (fill/drain cycle)

### 5.7 Maintenance

**Routine Maintenance:**
- **Quarterly**: Visual inspection (check for leaks, cable damage, corrosion)
- **Annually**: Functional test (verify output state changes with liquid level)
- **No scheduled component replacement** (replace only if failed)

**Inspection Checklist:**
- [ ] Adapter and sensor housing secure (no loosening from vibration, pressure cycles)
- [ ] Fused glass dome intact (no cracks, chips, cloudiness)
- [ ] Cable intact (no kinks, cuts, insulation damage) OR M12 connector secure
- [ ] Electrical connections secure (no corrosion, loosening)
- [ ] Output signal correct (test with multimeter)
- [ ] No leaks at adapter or sensor housing (especially after pressure cycles)

**Cleaning (if required):**
- Fused glass dome: Wipe with soft cloth and isopropyl alcohol (if accessible)
- **Do NOT use abrasive cleaners** (risk of scratching glass)
- **Do NOT submerge electronic module** (IP65 rated but avoid unnecessary exposure)

### 5.8 Troubleshooting

**Problem: No Output Signal (No Continuity in Any State)**
- **Cause 1**: Power supply failure
  - **Solution**: Verify voltage at LC-PH terminals (should match rated voltage)
- **Cause 2**: Electronic module failure
  - **Solution**: Replace electronic module (5-10 minutes, no depressurization)
- **Cause 3**: Wiring fault
  - **Solution**: Check continuity of output wire (repair or replace cable) OR M12 connector

**Problem: Output Signal Incorrect (Wrong State for Liquid/Air)**
- **Cause 1**: Wrong model ordered (NO vs NC configuration)
  - **Solution**: Verify model number on label (order correct version, no field change possible)
- **Cause 2**: Sensor dome contaminated or damaged
  - **Solution**: Clean fused glass dome, inspect for cracks (replace sensor housing if damaged)
- **Cause 3**: Wiring error (output wired to wrong terminal)
  - **Solution**: Verify wiring per LC-PH label diagram

**Problem: Output Signal Intermittent or Unstable**
- **Cause 1**: Foam, bubbles, or turbulence at sensor dome (common in CO2 gas cooler)
  - **Solution**: Relocate sensor or specify activation delay (order custom unit)
- **Cause 2**: Loose electrical connections
  - **Solution**: Tighten terminal screws, verify cable secure OR M12 connector locked
- **Cause 3**: Electronic module loose on sensor housing
  - **Solution**: Hand-tighten module (ensure internal connector engaged)
- **Cause 4**: Pressure transients causing vibration
  - **Solution**: Dampen vibration (isolation mount) or specify activation delay

**Problem: False Alarms (Output Triggers Without Liquid Present)**
- **Cause**: Condensation or contamination on fused glass dome
  - **Solution**: Clean dome, verify system not generating excessive moisture (especially CO2 gas cooler)

**Problem: Leakage at Adapter or Sensor Housing (High-Pressure)**
- **Cause 1**: Adapter under-torqued (< 50 N·m)
  - **Solution**: Re-torque to 50 N·m (do not exceed)
- **Cause 2**: Damaged threads or sealant failure
  - **Solution**: Depressurize, remove adapter, inspect threads, reapply sealant, reinstall
- **Cause 3**: Sensor housing loose on adapter
  - **Solution**: Hand-tighten sensor housing (finger-tight, do not use wrenches)

### 5.9 Electronic Module Replacement Procedure

**When to Replace Electronic Module:**
- No output signal (module failure)
- Output signal incorrect (electronic failure, not wrong model)
- Physical damage to module (cable cut, housing cracked, M12 connector damaged)
- Preventive replacement (after lightning strike, power surge)

**Replacement Procedure (5-10 Minutes, No Depressurization):**

1. **Disconnect Power** (lockout/tagout)
2. **Disconnect Cable or M12 Connector** (if external junction box, disconnect at junction)
3. **Hand-Unscrew Electronic Module**:
   - Rotate module counter-clockwise (no tools, finger-tight)
   - Lift module straight up (internal connector disengages automatically)
4. **Inspect Sensor Housing**:
   - Verify threads intact (no cross-threading)
   - Check fused glass dome (no damage, especially after high-pressure service)
5. **Install New Electronic Module**:
   - Align module with sensor housing (bayonet-style connector)
   - Press down gently and rotate clockwise (hand-tight, no tools)
   - Verify module seated flush (internal connector engaged)
6. **Reconnect Cable or M12 Connector** (if external junction box)
7. **Restore Power** and verify operation:
   - Test output state in air and liquid (functional test per commissioning)

**Cost Savings:**
- Electronic module replacement: ~50-60% cost of complete sensor assembly
- No refrigerant recovery: Saves time and refrigerant (especially CO2 transcritical)
- No leak testing: System remains sealed

**Spare Parts Recommendation:**
- Stock 1 electronic module per 5 LC-PH units (for critical CO2 transcritical applications)
- Complete sensor housing rarely needs replacement (fused glass extremely durable even at 120 bar)

---

## 6. FREQUENTLY ASKED QUESTIONS (FAQ)

### 6.1 Product Classification

**Q1: What is the LC-PH and what does it do?**

The LC-PH is an **optical level switch** for detecting liquid presence/absence in high-pressure tanks, separators, receivers up to 120 bar. **It is a level switch only - it does NOT have a valve and cannot regulate oil level automatically.** The LC-PH provides a solid-state output signal (100mA) to external controls (PLC, BMS, alarm, relay) for monitoring or control actions.

**For automatic oil level regulation with integrated valve**, see **TK3+** (46/80/130 bar) or **TK4** (46/80/130 bar smart) series.

**Q2: What is the difference between LC-PH and TK3+?**

| Feature | LC-PH | TK3+ |
|---------|-------|------|
| **Function** | Level detection only (switch) | Automatic oil level regulation (regulator) |
| **Valve** | NO valve (external control required) | Integrated solenoid valve (automatic) |
| **Pressure** | 120 bar | 46/80/130 bar (3 variants) |
| **Output** | 100mA solid-state signal | 2A relay output + alarm |
| **Control** | Requires external PLC/relay/valve | Self-contained automatic control |
| **Cost** | Lower (~40% less than TK3+ 130 bar) | Higher (integrated valve + control) |

**Choose LC-PH** when: Level detection only required, external control available, 120 bar rating needed  
**Choose TK3+** when: Automatic oil regulation needed, no external control, plug-and-play operation

**Q3: Is LC-PH a level switch or level regulator?**

**LC-PH is a LEVEL SWITCH ONLY** (detection, not regulation):
- Detects liquid presence/absence
- Outputs signal to external controls
- Requires external valve, pump, or control for automated actions

**For level regulation** (detection + valve + automatic control), use **TK3+** (46/80/130 bar) or **TK4** (46/80/130 bar smart) series.

### 6.2 Pressure & Temperature

**Q4: What is the maximum pressure rating?**

**120 bar** maximum working pressure. For lower pressures (≤ 46 bar), use **LC-PS** (46 bar, lower cost).

**Q5: Can it be used in CO2 systems?**

**Yes**, LC-PH is specifically designed for **CO2 transcritical** (80-120 bar) and **CO2 subcritical** (40-70 bar):
- CO2 gas cooler outlet (90-110 bar)
- CO2 high-pressure receiver (80-100 bar)
- CO2 flash gas separator (70-90 bar)
- CO2 oil separator (40-80 bar)

**Q6: What is the operating temperature range?**

**Media temperature**: -40°C to +125°C (extended range)  
**Ambient temperature**: -40°C to +60°C

Extended range vs LC-PS (-40°C to +85°C) allows use in:
- CO2 gas cooler outlet (+40°C to +80°C)
- Hot gas defrost cycles (up to +125°C)
- High-temperature industrial processes

**Q7: Can it be used for ammonia systems?**

**Yes**, fully compatible with ammonia (NH3):
- 120 bar pressure rating provides safety margin for ammonia systems (typically 20-40 bar)
- Fused glass chemically inert to ammonia
- Extended temperature range suitable for ammonia applications

### 6.3 Installation & Design

**Q8: What does "two-part design" mean?**

The LC-PH consists of two parts:

1. **Part 1: Sensor Housing** (permanent pressure boundary)
   - Fused glass dome, nickel-plated steel body (120 bar rated)
   - Remains on equipment during service
   - 120 bar pressure rated, -40°C to +125°C temperature rated

2. **Part 2: Electronic Module** (replaceable without depressurization)
   - Infrared LED, optical receiver, power supply, output driver
   - **Can be replaced in 5-10 minutes without emptying or depressurizing system**
   - No refrigerant recovery, no leak testing (especially critical for CO2 transcritical)

**Advantage**: Minimal downtime, lower service cost (module ~50-60% cost of complete sensor), no CO2 recovery.

**Q9: What thread adapters are available?**

**6 adapter options**:
1. **1/2" NPT** - Most common for CO2 gas cooler/receiver/separator (24mm projection)
2. **3/4" NPT** - Larger CO2/ammonia vessels (22mm projection)
3. **1" NPT** - High-flow applications (27.9mm projection)
4. **M20×1.5** - European compressors, shortest projection (18.1mm)
5. **1" 1/8 UNEF** - Compressor service port direct mount (19mm projection)
6. **1" 1/4 RLK** - Rotalock valve ports, longest projection (30mm)

**Adapter included with LC-PH** (specify at order).

**Q10: What is the installation torque?**

- **Adapter to equipment port**: **50 N·m** (critical for sealing, especially high-pressure)
- **Sensor housing to adapter**: Hand-tight only (finger-tight, **do NOT use wrenches**)
- **Electronic module to sensor housing**: Hand-tight only (finger-tight, **do NOT use wrenches**)

### 6.4 Electrical & Output

**Q11: What voltage options are available?**

- **24VAC/DC** ±10% (most common for BMS/PLC integration)
- **115VAC** ±10% @ 60Hz (North American mains)
- **230VAC** ±10% @ 50Hz (European/international mains)

Specify voltage at order (matches supply voltage in facility).

**Q12: What is NO and NC output? How do I choose?**

- **NO (Normally Open in air)**: Output OPEN when air (no liquid), CLOSES when liquid detected
  - **Use for**: High-level alarms (alarm activates when liquid present)
  - **Example**: CO2 gas cooler high-level alarm

- **NC (Normally Closed in air)**: Output CLOSED when air (no liquid), OPENS when liquid detected
  - **Use for**: Low-level alarms, fail-safe protection (alarm activates when liquid absent)
  - **Example**: CO2 receiver low-level alarm

**⚠️ CRITICAL**: Output configuration is **factory-set** and **cannot be changed in field**. Order correct version (NO or NC in air).

**Q13: What is the output current rating?**

**Maximum 100mA** solid-state output. Suitable for:
- PLC digital inputs (typical 10-50mA)
- Low-current relay coils (typical 50-100mA)
- BMS inputs (typical 10-30mA)

**Not suitable for**: High-power loads (use external relay if > 100mA required). For higher current (up to 2A), use **TK1+** with relay output.

**Q14: Does it need calibration?**

**No**. Factory calibrated, plug-and-play operation. No field adjustment needed or possible.

**Q15: Can delays be customized?**

**Yes**, available on request (factory-programmed):
- **Activation delay**: Prevents false alarms from turbulence, foam, bubbles (typical 5-30 seconds) - especially useful in CO2 gas cooler
- **Deactivation delay**: Filters transient liquid contact (typical 1-10 seconds)

Specify delay requirements at order (cannot be changed in field).

**Q16: What is M12 connector option?**

**M12×1 connector** (optional, instead of 1m cable):
- Industrial standard connector (IP67 rated when mated)
- Quick disconnect for service
- Mating connector sold separately (order from electrical supply houses)
- Common in industrial automation and CO2 refrigeration

### 6.5 Comparison & Selection

**Q17: What is the difference between LC-PH and LC-PS?**

| Feature | LC-PS | LC-PH |
|---------|-------|-------|
| **Pressure** | 46 bar | **120 bar** |
| **Media Temp** | -40°C to +85°C | **-40°C to +125°C** (extended) |
| **Output** | 100mA solid-state | 100mA solid-state |
| **Power** | 20mA | 20mA |
| **Connection** | 1m cable | 1m cable / M12 optional |
| **Cost** | Lower | Higher (~30% more) |

**Choose LC-PS**: Standard refrigeration ≤ 46 bar, temperature ≤ +85°C, lower cost  
**Choose LC-PH**: High pressure 46-120 bar (CO2 transcritical) OR extended temperature > +85°C required

**Q18: What is the difference between LC-PH and LC-XP?**

| Feature | LC-PH | LC-XP |
|---------|-------|-------|
| **Pressure** | 120 bar | 120 bar |
| **Connection** | 1m cable / M12 optional | EN175301-803A connector (industrial) |
| **Housing** | Nickel-plated steel | Stainless steel (better corrosion resistance) |
| **Cost** | Medium | Higher (~25% more than LC-PH) |

**Choose LC-PH**: Cable/M12 connection preferred, nickel-plated steel sufficient, medium cost  
**Choose LC-XP**: Industrial connector required (EN175301-803A), stainless steel housing for harsh environments

**Q19: What is the difference between LC-PH and TK1+?**

| Feature | LC-PH | TK1+ |
|---------|-------|------|
| **Pressure** | 120 bar | 46 bar or 100 bar |
| **Output** | 100mA solid-state | 2A relay (NO + NC) |
| **LED Indication** | No | Yes (green/yellow/red) |
| **Mounting** | Threaded adapters (6 types) | Sight-glass flange (3/4/6-hole) |
| **Cost** | Medium | Higher |

**Choose LC-PH**: 100mA output sufficient, threaded adapter mounting, 120 bar rating required  
**Choose TK1+**: Higher output current required (up to 2A), sight-glass replacement, visual LED indication needed

**Q20: How do I select between LC-PH and TK3+ (130 bar)?**

**Decision criteria**:

| Need automatic oil regulation? | Recommendation |
|-------------------------------|----------------|
| **NO** (only need level detection/alarm) | LC-PH (level switch, 120 bar) |
| **YES** (need automatic valve + control) | TK3+ 130 bar (level regulator, 130 bar) |

**LC-PH advantages**:
- Lower cost (~40% less than TK3+ 130 bar)
- Flexible control (external PLC/BMS integration)
- Multiple units for multi-point monitoring

**TK3+ 130 bar advantages**:
- Automatic operation (no external control required)
- Integrated solenoid valve
- Self-contained (plug-and-play)
- Higher output current (2A relay)
- Slightly higher pressure rating (130 bar vs 120 bar)

### 6.6 Compatibility & Reliability

**Q21: What refrigerants are compatible?**

**All refrigerants** (fused glass chemically inert):
- **CO2 (R744)**: Transcritical (80-120 bar) and subcritical (40-70 bar) - primary application
- **Ammonia (NH3)**: High-pressure systems (up to 120 bar)
- HFC/HCFC/CFC: R134a, R404A, R407C, R410A, R22, R502, etc.
- Hydrocarbons (HC): R290, R600a, etc.
- Low-GWP: R1234yf, R1234ze, R452A, R454B, etc.

**All oils**: Mineral, POE, PVE, PAG, AB (fused glass chemically inert).

**Q22: What is the reliability/lifespan?**

**MTTF > 50,000 hours** (5.7+ years continuous operation). 

**Advantages**:
- No moving parts (no floats, reeds, linkages)
- Solid-state electronics (no relay contacts)
- Fused glass hermetic seal (no O-rings, no degradation)
- 120 bar pressure rated (reinforced glass dome)
- Extended temperature range (-40°C to +125°C)
- Typical lifespan: 10-15 years in CO2 transcritical applications

**Only wear component**: Electronic module (LED, receiver) - replaceable without depressurization.

---

## 7. ORDERING INFORMATION

### 7.1 Model Code Structure

**Format**: `LC-PH [Adapter] [Voltage] [Output] 001 [Options] A`

**Example**: **LC-PH7071000101A**
- `LC-PH` = Product series (120 bar, -40°C to +125°C)
- `7` = 1/2" NPT adapter
- `071` = 24VAC/DC voltage
- `0` = Normally Open in air
- `00101A` = Standard suffix

### 7.2 Standard Model Codes

| Adapter | 24VAC/DC NO | 24VAC/DC NC | 230VAC NO | 230VAC NC |
|---------|-------------|-------------|-----------|-----------|
| **1/2" NPT** | LC-PH7071000101A | LC-PH7071010101A | LC-PH707D000101A | LC-PH707D010101A |
| **3/4" NPT** | LC-PHA071000101A | LC-PHA071010101A | LC-PHA07D000101A | LC-PHA07D010101A |
| **1" NPT** | LC-PHB071000101A | LC-PHB071010101A | LC-PHB07D000101A | LC-PHB07D010101A |
| **M20×1.5** | LC-PH6071000101A | LC-PH6071010101A | LC-PH607D000101A | LC-PH607D010101A |
| **1" 1/8 UNEF** | LC-PH8071000101A | LC-PH8071010101A | LC-PH807D000101A | LC-PH807D010101A |
| **1" 1/4 RLK** | LC-PHC071000101A | LC-PHC071010101A | LC-PHC07D000101A | LC-PHC07D010101A |

**Note**: 115VAC @ 60Hz models available - contact Teklab for model codes.

### 7.3 Selection Parameters

**Adapter Selection:**
- **7** = 1/2" NPT (most common for CO2 gas cooler/receiver/separator)
- **A** = 3/4" NPT (larger CO2/ammonia vessels)
- **B** = 1" NPT
- **6** = M20×1.5 (metric, European)
- **8** = 1" 1/8 UNEF
- **C** = 1" 1/4 RLK

**Voltage Selection:**
- **071** = 24VAC/DC ±10%
- **072** = 115VAC ±10% @ 60Hz (contact Teklab)
- **07D** = 230VAC ±10% @ 50Hz

**Output Selection:**
- **0** = NO (Normally Open in air)
- **1** = NC (Normally Closed in air)

### 7.4 Options Available on Request

- **Programmable Delays**: Activation/deactivation timing (specify seconds)
- **M12×1 Connector**: Industrial connector (instead of 1m cable)
- **LED Indicator**: Visual confirmation option
- **Custom Cable Lengths**: > 1m cable length (specify length in meters)
- **115VAC @ 60Hz**: North American voltage (contact Teklab)

### 7.5 What's Included

- LC-PH two-part assembly (sensor housing + electronic module)
- Threaded adapter per model code
- 1m cable (3-wire) standard OR M12×1 connector (if specified)
- Installation instructions

### 7.6 What's NOT Included

- **Mating M12 connector**: If M12 version ordered (purchase from electrical supply houses)
- **External valve**: LC-PH is detection only (use TK3+/TK4 for integrated valve)
- **Mounting hardware**: Adapter threads into existing equipment port

### 7.7 Ordering Examples

**Example 1: CO2 Transcritical Gas Cooler High-Level Alarm (100 bar)**
- Port: 1/2" NPT
- Voltage: 24VAC/DC (BMS integration)
- Logic: Alarm when liquid present (NO in air)
- **Order**: LC-PH7071000101A

**Example 2: CO2 Transcritical Receiver Low-Level Alarm (85 bar)**
- Port: M20×1.5 (European compressor)
- Voltage: 230VAC (mains power)
- Logic: Alarm when liquid absent (NC in air, fail-safe)
- **Order**: LC-PH607D010101A

**Example 3: Ammonia Oil Separator Level (25 bar)**
- Port: 1" 1/8 UNEF (service port)
- Voltage: 24VAC/DC (PLC integration)
- Logic: Trigger oil drain when oil present (NC in air)
- **Order**: LC-PH8071010101A

**Example 4: CO2 Subcritical Receiver with M12 Connector (60 bar)**
- Port: 3/4" NPT
- Voltage: 24VAC/DC (BMS integration)
- Connection: M12×1 connector (quick disconnect)
- Logic: High-level alarm (NO in air)
- **Order**: LC-PHA071000101A + M12 option (specify at order)

---

## Document Information

**Document**: LC-PH Complete Product Documentation  
**Version**: 1.0  
**Date**: 2025-11-12  
**Language**: English  
**Product**: LC-PH Optical Level Switch  
**Category**: Level_Switches  
**Keywords**: LC-PH, optical level switch, 120 bar, CO2 transcritical, CO2 subcritical, ammonia, high-pressure, extended temperature, two-part design, solid-state output, fused glass, level detection

**© 2025 Teklab. All rights reserved.**
