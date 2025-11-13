---
category: Sensors
keywords:
- K11 sensor
- K11 level switch
- compact level sensor
- programmable timer
- 60 bar high pressure
- electro-optic sensor
- solid state output
- transient filtering
- foam detection
- turbulent liquid
- HVAC&R sensor
- hydraulic sensor
- 59x27mm compact
- M18x1.5 thread
language: EN
product: K11
document_type: unified_complete
last_updated: 2025-11-15
---

# K11 - Complete Product Documentation

**Compact High-Pressure Level Switch with Programmable Timer**

---

## 📋 Document Structure

This unified document covers the complete K11 sensor family organized in the following sections:

1. **Product Overview** - Description, key features, operating principle
2. **Detection Technology & Features** - Optical sensor, programmable timer, construction
3. **Technical Specifications** - Electrical, mechanical, environmental specs
4. **Applications & Selection** - Use cases and output selection guide
5. **Installation & Service** - Thread mounting, wiring, dimensions, maintenance
6. **FAQ** - Frequently asked questions

---

## 1. PRODUCT OVERVIEW

### K11 Series Description

The **K11** is a **compact high-pressure level switch** (59 x 27 mm) designed for demanding HVAC&R, hydraulic, and industrial applications up to **60 bar**. This solid-state infrared sensor features a **programmable timer** to filter transient conditions, making it ideal for applications with turbulent liquids, foam, or splashing.

**Core Technology:**
- Electro-optic infrared sensor (fused glass hermetic seal)
- Solid-state output (AC or DC, 100mA max)
- **Programmable timer** (customizable delay 0.5-30 seconds, filters transients)
- **Compact design** (59 x 27 mm, smallest sensor in Teklab lineup)
- **High pressure rating** (60 bar working, 120 bar burst)
- **Wide temperature range** (-40°C to +125°C)
- Multiple output options (NPN, NPN open collector, PNP, 24VAC)
- Factory calibrated, plug-and-play operation

**Key Specifications:**

| Parameter | Specification |
|-----------|--------------|
| **Dimensions** | 59 x 27 mm (ultra-compact) |
| **Pressure Rating** | 60 bar working, 120 bar burst (2:1 safety factor) |
| **Temperature Range** | -40°C to +125°C (operating and storage) |
| **Output Options** | NPN, NPN open collector, PNP (DC 10-28V) or 24VAC |
| **Output Current** | Up to 100mA (temperature dependent) |
| **Repeatability** | ±2 mm |
| **Body Materials** | Stainless steel or nickel-plated steel |
| **Sensing Dome** | Fused glass (hermetically sealed) |

**Key Differentiators:**
- **vs K25**: K11 is more compact (59x27mm vs 90xØ20mm), K25 has higher pressure (150 bar) + dual output (level + temp 4-20mA)
- **vs ATEX**: K11 is non-intrinsically-safe (standard areas), ATEX is Ex ia certified (explosive atmospheres Zone 0/1/2)
- **vs LC-PS/LC-PH/TK1+**: K11 is compact universal sensor (60 bar), LC/TK1+ are refrigeration-specific with 2-part design

**Selection Criteria:**
- **K11**: Compact size critical, 60 bar pressure, programmable timer needed, non-hazardous areas
- **K25**: Ultra-high pressure (150 bar), CO2 transcritical, dual output (level + temp 4-20mA)
- **ATEX**: Explosive atmospheres (Zone 0/1/2), intrinsically safe Ex ia IIC T6

**Primary Applications:**
- **HVAC Systems**: Condensate level monitoring, refrigerant level control
- **Refrigeration**: Compressor crankcase oil level (60 bar CO2 subcritical)
- **Pressurized Vessels**: High-pressure tanks up to 60 bar
- **Motors**: Oil level monitoring in motor housings
- **Hydraulic Systems**: Fluid level detection in hydraulic reservoirs (60 bar)
- **Compact Installations**: Space-constrained equipment requiring small sensor footprint

**Operating Principle:**

K11 uses electro-optic infrared detection through a fused glass dome:

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
   - **Programmable timer**: Optional delay before output switches (filters transients)

3. **Response Time**: < 1 second (without programmable delay), 0.5-30 seconds (with delay configured)

**Advantages Over Other Sensors:**
- **Most compact**: 59 x 27 mm (vs 90-150mm typical)
- **High pressure**: 60 bar (vs 20-46 bar typical compact sensors)
- **Programmable timer**: Built-in (no external time-delay relay needed)
- **Flexible outputs**: AC/DC, NPN/PNP options
- **Wide temperature**: -40°C to +125°C (wider than many 60 bar sensors)

---

## 2. DETECTION TECHNOLOGY & FEATURES

### 2.1 Electro-Optic Infrared Sensor

**Detection Method:**
- **Infrared LED emitter**: Generates infrared light into fused glass dome
- **Optical receiver**: Detects reflected light intensity
- **Refractive index principle**: Light behavior changes at glass/liquid interface
- **Digital threshold**: Clean ON/OFF switching (no analog drift)

**Sensor Advantages:**
- **Response time**: < 1 second (without programmable delay)
- **Reliability**: MTTF > 50,000 hours (5.7+ years continuous)
- **No calibration**: Factory calibrated, no field adjustment needed
- **No wetted electronics**: Sensor electronics isolated from media by fused glass
- **Pressure rated**: 60 bar working, 120 bar burst (2:1 safety factor)

**Fused Glass Hermetic Seal:**
- **Glass-to-metal fusion**: Molecular-level seal (NOT O-ring)
- **Zero leakage**: 10^-12 mbar·L/s (true hermetic)
- **Chemically inert**: Compatible with all oils, refrigerants, water, glycol, hydraulic fluids
- **Pressure rated**: 60 bar working, 120 bar burst
- **Temperature rated**: -40°C to +125°C
- **Lifetime seal**: No degradation, no maintenance

**Output Signal:**
- **Type**: Solid-state semiconductor output (NOT mechanical relay)
- **Current rating**: 100mA maximum (temperature dependent)
- **Configuration**: NO (Normally Open in air) or NC (Normally Closed in air) - factory-set
- **Voltage options**: 
  - **DC models**: 10-28 VDC (NPN, NPN open collector, PNP)
  - **AC models**: 24 VAC ±10% (50/60 Hz)

**Important Output Notes:**
- **Factory-configured**: NO or NC output cannot be changed in field (order correct version)
- **NO in air**: Output OPEN when air, CLOSES when liquid detected (high-level alarms)
- **NC in air**: Output CLOSED when air, OPENS when liquid detected (low-level alarms, fail-safe)

### 2.2 Programmable Timer Feature

**Purpose:**
The **programmable timer** filters false alarms from transient conditions common in industrial applications:
- **Liquid splashing or turbulence**: Prevents nuisance alarms from brief liquid contact
- **Foam or bubbles**: Ignores foam temporarily covering sensor dome
- **Brief level fluctuations**: Filters unstable liquid levels in agitated tanks

**Function:**
Adds customizable delay before output switches:
- **ON delay**: Output switches after liquid detected for X seconds (filters brief splashing)
- **OFF delay**: Output switches after liquid absent for X seconds (filters brief uncovering)
- **Typical range**: 0.5 to 30 seconds (customizable at order)

**Configuration:**
- **Factory-programmed**: Specify delay time when ordering (contact Teklab)
- **No external components**: Timer integrated in sensor electronics (no external relay or timer module)
- **No additional space**: Entire timer circuitry within 59 x 27 mm housing

**Applications:**
- **Turbulent liquid applications**: Agitators, pumps, high-flow vessels
- **Foam-prone liquids**: Lubricants, hydraulic oils, refrigerants with oil
- **Splash zones**: Fill/drain cycles, liquid transfer operations
- **Unstable levels**: Varying flow rates, intermittent feeds

**Advantages:**
- **Cost savings**: Eliminates external time-delay relay (~$50-100 USD)
- **Space savings**: No external relay panel or DIN rail mounting
- **Simplified wiring**: Direct sensor-to-PLC connection (no intermediate relay)
- **Application-specific**: Custom delay tuned to specific application conditions

### 2.3 Compact Design

**Dimensions:**
- **Total height**: 59 mm (from bottom of thread to top of sensor)
- **Body width**: 27 mm (maximum width of sensor body)
- **Weight**: ~150-180 g (depending on body material and cable length)

**Compact Advantages:**
- **Smallest sensor in Teklab lineup**: 59 x 27 mm footprint
- **Tight installations**: Fits where larger sensors cannot (compressor crankcases, small tanks)
- **Multiple sensor arrays**: Close spacing for multi-level detection (40-50mm center spacing)
- **Space-constrained equipment**: Retrofit installations with limited clearance

**Installation Clearances:**
- **Above sensor**: 40 mm minimum (electrical connection access)
- **Below sensor**: Ensure dome not obstructed by tank bottom or debris
- **Lateral**: 25 mm minimum from adjacent sensors or piping

### 2.4 Construction & Reliability

**Body Materials:**
- **Stainless steel**: Superior corrosion resistance (harsh chemicals, marine, outdoor, food processing)
- **Nickel-plated steel**: Cost-effective (standard industrial, compressor crankcases, hydraulic reservoirs)

**Sensing Dome:**
- **Fused glass**: Hermetically sealed, chemically inert, -40°C to +125°C

**Reliability Features:**
- **No moving parts**: Eliminates mechanical failure modes (floats, reeds, linkages)
- **Solid-state electronics**: No relay contacts to wear or stick
- **Hermetic seal**: No O-rings or gaskets to degrade
- **Electronic protections**: Transient overvoltage protection (power surges, lightning), reverse polarity protection (DC models)

**Environmental Protection:**
- **Operating temperature**: -40°C to +125°C
- **Storage temperature**: -40°C to +125°C
- **Pressure rating**: 60 bar working, 120 bar burst
- **Cable exit**: Top of sensor (secure cable to prevent strain)

**Refrigerant & Oil Compatibility:**
- **All HFC/HCFC/CFC**: R134a, R404A, R407C, R410A, R22, R502, etc.
- **CO2 (R744)**: Subcritical systems up to 60 bar
- **Ammonia (NH3)**: Fully compatible (stainless steel recommended)
- **Hydrocarbons (HC)**: R290, R600a, etc.
- **Low-GWP**: R1234yf, R1234ze, R452A, R454B, etc.
- **All oils**: Mineral, POE, PVE, PAG, AB (fused glass chemically inert)
- **Water, glycol**: HVAC condensate, chillers
- **Hydraulic oils**: Mineral, synthetic

### 2.5 Electrical Features

**Power Supply:**
- **DC models**: 10-28 VDC (wide voltage range, ideal for industrial/automotive)
- **AC models**: 24 VAC ±10% (50/60 Hz)

**Output Options:**

| Output Type | Supply Voltage | Description | Applications |
|-------------|----------------|-------------|--------------|
| **NPN** | 10-28 VDC | Sinking output | PLC inputs (European/Asian) |
| **NPN Open Collector** | 10-28 VDC | Flexible sinking output | Pull-up resistor configurations |
| **PNP** | 10-28 VDC | Sourcing output | PLC inputs (North American), special order |
| **24 VAC** | 24 VAC ±10% (50/60 Hz) | AC output | AC relay/contactor control |

**Output Modes:**
- **NO (Normally Open)**: Output closes when liquid detected (high-level alarms)
- **NC (Normally Closed)**: Output opens when liquid detected (low-level alarms, fail-safe)

**Output Current**: Up to 100 mA (temperature dependent, derate at high temperatures)

**Electronic Protections:**
- **Transient overvoltage protection**: Guards against voltage spikes (relay switching, motor starts)
- **Reverse polarity protection**: Prevents damage if wiring reversed (DC models)

### 2.6 Thread Options

**Standard Threads:**
- **3/4" NPT** (most common, North American standard)
- **1/2" NPT** (medium ports)
- **3/8" NPT** (small ports)

**Optional Threads** (contact Teklab for availability):
- **UNEF**: 5/8"-24, 3/4"-20, 1" 1/8-18 (Unified Extra Fine, refrigeration/automotive)
- **ISO Metric**: M18, M20, M22, M24 (European/Asian standard)
- **GAS**: Cylindrical or conical (British standard pipe threads)
- **Custom**: OEM-specific threads available on request

**Thread Installation:**
- **Torque**: 15 N·m recommended (do not over-torque)
- **Minimum engagement**: 5-7 threads for 60 bar rating
- **Thread sealant**: Compatible with media, rated for -40°C to +125°C and 60 bar minimum

**Sealing Method:**
- **NPT threads**: Metal-to-metal taper seal (use PTFE tape or liquid thread sealant)
- **Parallel threads (ISO Metric)**: Requires O-ring, copper washer, or sealant per equipment specifications

---

## 3. TECHNICAL SPECIFICATIONS

### 3.1 Electrical Specifications

| Parameter | DC Models | AC Models |
|-----------|-----------|-----------|
| **Supply Voltage** | 10-28 VDC | 24 VAC ±10% (50/60 Hz) |
| **Output Type** | NPN, NPN open collector, or PNP | AC output |
| **Output Current** | Up to 100mA max (temperature dependent) | Up to 100mA max (temperature dependent) |
| **Output Mode** | Normally Open or Normally Closed in air | Normally Open or Normally Closed in air |
| **Electronic Protections** | Transient overvoltage, reverse polarity | Transient overvoltage |

### 3.2 Mechanical Specifications

| Parameter | Specification |
|-----------|--------------|
| **Detection Method** | Infrared electro-optic (liquid presence with contact) |
| **Body Materials** | Stainless steel or nickel-plated steel |
| **Sensing Dome** | Fused glass (hermetically sealed) |
| **Repeatability** | ±2 mm |
| **Torque** | 15 N·m recommended for thread installation |
| **Overall Dimensions** | 59 x 27 mm (ultra-compact) |
| **Weight** | ~150-180 g (depending on body material and cable length) |

### 3.3 Environmental & Pressure Specifications

| Parameter | Specification |
|-----------|--------------|
| **Operating Temperature** | -40°C to +125°C |
| **Storage Temperature** | -40°C to +125°C |
| **Max Working Pressure** | 60 bar |
| **Burst Pressure** | 120 bar (2:1 safety factor) |
| **Humidity** | 5-95% RH non-condensing (typical industrial conditions) |

### 3.4 Performance Specifications

| Parameter | Specification |
|-----------|--------------|
| **Response Time** | < 1 second (without programmable delay) |
| **Programmable Delay** | 0.5 to 30 seconds (customizable at order) |
| **Repeatability** | ±2 mm |
| **Reliability** | MTTF > 50,000 hours (5.7+ years continuous) |
| **Calibration** | Factory calibrated (no field calibration required) |
| **Hermetic Seal** | 10^-12 mbar·L/s (fused glass-to-metal) |

### 3.5 Thread Options

**Standard Threads:**
- 3/4" NPT (most common)
- 1/2" NPT
- 3/8" NPT

**Optional Threads** (contact Teklab):
- UNEF: 5/8"-24, 3/4"-20, 1" 1/8-18
- ISO Metric: M18, M20, M22, M24
- GAS: Cylindrical or conical
- Custom specifications for OEM

### 3.6 Installation Clearances

| Clearance Type | Minimum (mm) | Purpose |
|----------------|--------------|---------|
| **Above Sensor** | 40 | Electrical connection access |
| **Below Sensor** | Variable | Ensure dome not obstructed by tank bottom or debris |
| **Lateral** | 25 | Adjacent sensors or piping clearance |
| **Cable Bend Radius** | 25-30 | Prevent cable strain at sensor connection |

### 3.7 Liquid Compatibility

**Compatible with virtually all liquids:**
- Refrigeration oils (mineral, POE, PAG, PVE, AB)
- Refrigerants (R134a, R404A, R407C, R410A, CO2 up to 60 bar, ammonia)
- Water, glycol solutions
- Hydraulic oils (mineral, synthetic)
- Most chemicals (verify with Teklab for aggressive media)

**Fused glass dome**: Chemically inert, no degradation from refrigerant or oil exposure.

---

## 4. APPLICATIONS & SELECTION GUIDE

### 4.1 Primary Applications

**HVAC Systems:**
- Condensate level monitoring (drain pans, chillers)
- Refrigerant level control (receivers, accumulators)
- Chiller low-level protection

**Refrigeration:**
- Compressor crankcase oil level (CO2 subcritical up to 60 bar)
- Oil separator level detection
- Receiver liquid level monitoring
- Economizer level control

**Pressurized Vessels:**
- High-pressure tanks up to 60 bar
- Process vessels level detection
- Chemical storage tanks

**Motors:**
- Oil level monitoring in motor housings
- Bearing lubrication level detection
- Gearbox oil level control

**Hydraulic Systems:**
- Fluid level detection in hydraulic reservoirs (60 bar)
- Mobile hydraulic equipment (10-28 VDC wide voltage range)
- Industrial hydraulic presses

**Compact Installations:**
- Space-constrained equipment (59 x 27 mm footprint)
- Multiple sensor arrays (40-50mm center spacing for multi-level detection)
- Retrofit installations with limited clearance

### 4.2 K11 vs K25 vs ATEX Selection Guide

| Feature | K11 | K25 | ATEX |
|---------|-----|-----|------|
| **Dimensions** | 59 x 27 mm | 90 x Ø20 mm | 98 x Ø30 mm |
| **Pressure** | 60 bar | 150 bar | 20 bar |
| **Temperature** | -40 to +125°C | -40 to +125°C | -20 to +100°C (T4) |
| **Output** | 100mA (AC/DC, NPN/PNP) | 50mA (NPN) + 4-20mA temp | 40mA (NPN open collector) |
| **Key Feature** | Programmable timer, ultra-compact | Dual output (level + temp) | Ex ia intrinsically safe |
| **Application Focus** | Compact, high-pressure, timer | CO2 transcritical, ultra-high pressure | Explosive atmospheres (Zone 0/1/2) |
| **Certification** | CE | CE | ATEX/IECEx (Ex ia IIC T6) |
| **Relative Cost** | Lower | Medium | Higher (certification premium) |

**Choose K11 when**:
- Compact size critical (59 x 27 mm)
- Pressure ≤ 60 bar
- Programmable timer needed (filter transients, foam, splashing)
- Non-hazardous areas
- Flexible output options required (AC/DC, NPN/PNP)

**Choose K25 when**:
- Ultra-high pressure (>60 bar, up to 150 bar)
- CO2 transcritical systems
- Dual output required (level + temperature 4-20mA)
- Real-time temperature monitoring needed

**Choose ATEX when**:
- Explosive atmospheres (Zone 0/1/2)
- Intrinsically safe Ex ia IIC T6 required
- Hazardous area compliance mandatory
- Pressure ≤ 20 bar

### 4.3 Output Selection Guide

**NPN (Sinking Output)**:
- Most common for PLC inputs (European/Asian controls)
- Output pulls low (sinks current) when activated
- Typical wiring: Sensor output → PLC input → PLC common

**NPN Open Collector**:
- Flexible sinking output with external pull-up resistor
- Custom voltage levels (different from supply voltage)
- Typical wiring: Supply voltage → Pull-up resistor → Sensor output → Ground

**PNP (Sourcing Output)**:
- Common for North American PLC inputs
- Output pulls high (sources current) when activated
- Special order (contact Teklab)
- Typical wiring: Supply voltage → PLC input → Sensor output → Ground

**24 VAC**:
- AC relay/contactor control (direct drive)
- No DC power supply needed
- Typical wiring: 24VAC supply → Sensor → Relay coil → Common

**Decision Tree:**

```
START
│
├─ Control system uses AC relays/contactors? ──YES──> 24 VAC output
│   └─NO (DC PLC/controller)
│
├─ PLC input type NPN (sinking)? ──YES──> NPN output
│   └─NO (PNP/sourcing)
│
├─ PLC input type PNP (sourcing)? ──YES──> PNP output (special order)
│   └─NO (custom configuration)
│
├─ Need custom voltage level? ──YES──> NPN open collector (with pull-up)
│   └─NO
│
└─> Contact Teklab for custom requirements
```

---

## 5. INSTALLATION & SERVICE

### 5.1 Pre-Installation Checklist

**Verify Requirements:**
- [ ] Pressure ≤ 60 bar (for higher pressure, use K25 150 bar)
- [ ] Temperature -40°C to +125°C
- [ ] Equipment port has compatible thread (3/4" NPT standard, others available)
- [ ] Adequate clearance (59mm height + 40mm above sensor for cable access)
- [ ] Power supply voltage matches K11 model (10-28 VDC or 24 VAC)
- [ ] Output configuration correct (NO or NC in air, NPN/PNP/AC)
- [ ] Programmable timer delay specified (if required)

**Tools & Materials:**
- Torque wrench (15 N·m for thread installation)
- Thread sealant (PTFE tape or liquid sealant rated for media and pressure)
- Multimeter (for wiring verification)
- Cable ties or strain relief (secure cable to prevent strain on sensor)

### 5.2 Thread Installation

**Step 1: Prepare Equipment Port**
- Clean port threads (remove old sealant, debris)
- Inspect threads for damage (repair if necessary)
- Verify port depth sufficient for thread engagement (5-7 threads minimum)

**Step 2: Apply Thread Sealant**
- **PTFE tape**: 3-4 wraps clockwise (viewed from thread end)
- **Liquid sealant**: Apply per manufacturer instructions
- **Important**: Avoid sealant on first 2 threads (prevent contamination)

**Step 3: Install Sensor**
- Thread sensor into equipment port (hand-start, ensure straight)
- Torque to **15 N·m** (do not over-torque, risk cracking glass dome or damaging threads)
- Verify sensor orientation (dome facing downward or horizontal, avoid upward-facing)

**Mounting Orientation:**
- **Preferred**: Sensor dome facing **downward** or **horizontal** (into liquid)
- **Avoid**: Upward-facing dome (may trap air bubbles in oil, affect detection)

**Step 4: Leak Test**
- Pressure test equipment per normal procedures
- Verify no leakage at sensor threads
- Re-torque if necessary (up to 15 N·m max)

### 5.3 Electrical Wiring

**Step 1: Identify Cable Conductors**

**DC Models (NPN, NPN Open Collector, PNP):**
- **Typical 3-4 conductor cable**:
  - Power (+) - typically brown or red
  - Power (-) / Ground - typically blue or black
  - Output signal - typically white or yellow
  - Shield / Ground (optional) - typically green/yellow stripe

**AC Models (24 VAC):**
- **Typical 3 conductor cable**:
  - AC Line 1 - typically brown
  - AC Line 2 / Common - typically blue
  - Output signal - typically white or black

**⚠️ WARNING**: Verify conductor colors with K11 label or supplier documentation (cable colors may vary).

**Step 2: Wire to Power Supply/PLC**

**NPN Output Wiring:**
1. **De-energize power supply** (lockout/tagout)
2. Connect power (+) to DC supply positive (10-28 VDC)
3. Connect power (-) to DC supply negative/ground
4. Connect output to PLC input
5. Connect PLC common to DC supply negative/ground
6. Verify polarity (reverse polarity protection on DC models, but verify correct wiring)

**PNP Output Wiring:**
1. **De-energize power supply** (lockout/tagout)
2. Connect power (+) to DC supply positive (10-28 VDC)
3. Connect power (-) to DC supply negative/ground
4. Connect PLC input to DC supply positive
5. Connect output to PLC input (through load)
6. Verify polarity

**24 VAC Output Wiring:**
1. **De-energize power supply** (lockout/tagout)
2. Connect AC Line 1 to 24 VAC supply
3. Connect AC Line 2 / Common to 24 VAC common
4. Connect output to relay coil or alarm circuit
5. Verify AC voltage (24 VAC ±10%, 50/60 Hz)

**Step 3: Cable Management**
- Secure cable with strain relief (prevent stress on sensor connection)
- Cable bend radius: 25-30 mm minimum
- Route cable away from hot surfaces, moving parts, sharp edges
- Use cable ties to secure cable along equipment or conduit

**Fuse Protection:**
- Install appropriate fuse in power supply circuit (per electrical code)

### 5.4 Commissioning

**Step 1: Pre-Startup Verification**
- [ ] Sensor torqued to 15 N·m (thread installation)
- [ ] Sensor orientation correct (dome facing downward or horizontal)
- [ ] Cable secure with strain relief
- [ ] Electrical connections secure and correct polarity
- [ ] Power supply voltage matches K11 model
- [ ] Output wiring correct (NO, NC logic verified)

**Step 2: Power-On Test (System Empty, Air)**
- Energize power supply
- Verify output state: 
  - **NO in air**: Output should be OPEN (no continuity)
  - **NC in air**: Output should be CLOSED (continuity)
- Measure output voltage with multimeter (should match expected state)

**Step 3: Functional Test (System Filled, Liquid)**
- Fill equipment with liquid to submerge sensor dome
- Verify output state changes:
  - **NO in air**: Output should CLOSE (continuity)
  - **NC in air**: Output should OPEN (no continuity)
- If programmable timer configured: Wait for delay period before output switches
- Drain liquid to expose sensor dome
- Verify output returns to air state (< 1 second response, or after delay period)

**Step 4: Programmable Timer Verification** (if configured)
- Briefly submerge sensor dome (< delay time)
- Verify output does NOT switch (timer filtering transient)
- Submerge sensor dome for > delay time
- Verify output switches (timer delay elapsed)

### 5.5 Maintenance

**Routine Maintenance:**
- **Quarterly**: Visual inspection (leaks, cable integrity)
- **Annually**: Functional test (verify output state changes)
- **No scheduled component replacement** (replace only if failed)

**Inspection Checklist:**
- [ ] Thread connection secure (no loosening, verify 15 N·m torque if accessible)
- [ ] Fused glass dome intact (no cracks, chips, cloudiness)
- [ ] Cable intact (no kinks, cuts, insulation damage)
- [ ] Electrical connections secure (no corrosion, loosening)
- [ ] Output signal correct (test with multimeter)
- [ ] Sensor body condition (no corrosion, pitting)

**Troubleshooting:**

| Symptom | Possible Cause | Solution |
|---------|----------------|----------|
| No output signal | Power supply failure | Verify power voltage at sensor |
| | Cable damage | Inspect cable, test continuity |
| | Sensor failure | Replace sensor |
| False alarms | Transient liquid contact | Configure programmable timer delay |
| | Foam covering dome | Configure programmable timer delay, clean dome |
| | Incorrect wiring | Verify NO/NC logic correct |
| Intermittent output | Cable strain | Secure cable with strain relief |
| | Loose thread connection | Re-torque sensor to 15 N·m |
| | Electrical noise | Add shielding or ferrite cores to cable |

---

## 6. FREQUENTLY ASKED QUESTIONS (FAQ)

### 6.1 Product Classification

**Q1: What is K11 and when should I use it?**

**K11** is a **compact infrared level switch** (59 x 27 mm) for **high-pressure applications up to 60 bar**:
- Pressurized vessels, HVAC, refrigeration, motors, hydraulics
- Solid-state optical detection (no moving parts)
- **Programmable timer** to filter transients (foam, splashing, turbulence)
- Wide temperature range (-40°C to +125°C)

**Choose K11 when**: Compact size critical, pressure ≤ 60 bar, programmable delay needed, non-hazardous areas.

**Q2: How does infrared detection work?**

**In Air (no liquid)**:
- Infrared LED emits light into glass dome
- Light reflects internally back to receiver
- Output remains in default state (NO open, NC closed)

**In Liquid (liquid present)**:
- Liquid contacts glass dome
- Light refracts into liquid (lost, not reflected)
- Receiver detects light loss, output switches (NO closes, NC opens)

**Accuracy**: ±2 mm repeatability, no mechanical wear.

**Q3: What is the programmable timer feature?**

**Purpose**: Filters false alarms from transient conditions:
- Liquid splashing or turbulence
- Foam or bubbles temporarily covering sensor
- Brief level fluctuations

**Function**: Adds customizable delay (0.5-30 seconds) before output switches. Prevents nuisance alarms in unstable liquid applications.

**Configuration**: Contact Teklab to specify delay time when ordering (factory-programmed).

### 6.2 Output Options & Wiring

**Q4: What output options are available?**

| Output Type | Supply Voltage | Applications |
|-------------|----------------|--------------|
| **NPN** | 10-28 VDC | Sinking output for PLC inputs |
| **NPN Open Collector** | 10-28 VDC | Flexible sinking output |
| **PNP** | 10-28 VDC | Sourcing output (European controls, special order) |
| **24 VAC** | 24 VAC ±10% (50/60 Hz) | AC relay/contactor control |

**Output Modes**: NO (Normally Open) or NC (Normally Closed) in air  
**Output Current**: Up to 100 mA (temperature dependent)

**Q5: What is the difference between NPN and PNP outputs?**

**NPN (Sinking)**:
- Output pulls low (sinks current) when activated
- Common for European/Asian PLC inputs
- Wiring: Sensor output → PLC input → PLC common

**PNP (Sourcing)**:
- Output pulls high (sources current) when activated
- Common for North American PLC inputs
- Special order (contact Teklab)
- Wiring: Supply voltage → PLC input → Sensor output → Ground

**Q6: Can I use K11 with different supply voltages?**

**DC models**: 10-28 VDC (wide voltage range)
- Automotive/mobile equipment (12V, 24V systems)
- Industrial PLCs (24V standard)
- Battery-powered systems (12V)

**AC models**: 24 VAC ±10% (50/60 Hz)
- AC control circuits
- Direct relay/contactor drive

### 6.3 Pressure & Temperature

**Q7: What pressure rating does K11 have?**

**Working pressure**: 60 bar  
**Burst pressure**: 120 bar (2:1 safety factor)

**Suitable for**:
- CO2 subcritical systems (up to 60 bar)
- High-pressure HVAC/refrigeration
- Hydraulic reservoirs (60 bar)
- Pressurized process vessels

**Not suitable for**:
- CO2 transcritical (>60 bar) → Use **K25** (150 bar)

**Q8: What temperature range does K11 support?**

**Operating**: -40°C to +125°C  
**Storage**: -40°C to +125°C

**Applications**:
- Low-temp: Cold storage, freezer rooms (-40°C)
- High-temp: Compressor oil sumps, heated hydraulic systems (+125°C)

**Note**: Output current may derate at high temperatures - consult specifications.

**Q9: Can K11 be used for ammonia systems?**

**Yes**, fully compatible with ammonia (NH3):
- **Stainless steel body recommended**: Better corrosion resistance for ammonia
- **Pressure rating**: 60 bar suitable for most ammonia systems (typically 20-40 bar)
- **Fused glass**: Chemically inert to ammonia
- **Temperature range**: -40°C to +125°C (suitable for ammonia applications)

### 6.4 Comparison & Selection

**Q10: K11 vs K25 - which to choose?**

| Feature | K11 | K25 |
|---------|-----|-----|
| **Dimensions** | 59 x 27 mm | 90 x Ø20 mm |
| **Pressure** | 60 bar | 150 bar |
| **Output** | 100mA (AC/DC, NPN/PNP) | 50mA (NPN) + 4-20mA temp |
| **Key Feature** | Programmable timer, ultra-compact | Dual output (level + temp) |
| **Application** | Compact, high-pressure, timer | CO2 transcritical, ultra-high pressure |

**Choose K11**: Compact size critical, pressure ≤ 60 bar, programmable timer needed  
**Choose K25**: Ultra-high pressure (>60 bar, up to 150 bar), CO2 transcritical, dual output (level + temp 4-20mA)

**Q11: K11 vs ATEX - which to choose?**

| Feature | K11 | ATEX |
|---------|-----|------|
| **Certification** | CE (standard areas) | ATEX/IECEx (Ex ia IIC T6, explosive atmospheres) |
| **Pressure** | 60 bar | 20 bar |
| **Temperature** | -40 to +125°C | -20 to +100°C (T4) |
| **Dimensions** | 59 x 27 mm | 98 x Ø30 mm |

**Choose K11**: Non-hazardous areas, higher pressure (60 bar), wider temperature  
**Choose ATEX**: Explosive atmospheres (Zone 0/1/2), intrinsically safe Ex ia IIC T6 required

### 6.5 Installation & Maintenance

**Q12: What thread options are available?**

**Standard**: NPT (3/8", 1/2", 3/4" - most common)  
**Optional**: UNEF, ISO Metric (M18, M20, M22, M24), GAS threads  
**Custom**: Available on request for OEM applications

Specify thread type when ordering. Default: 3/4" NPT.

**Q13: What is the installation torque?**

**15 N·m** (do not over-torque, risk cracking glass dome or damaging threads).

**Thread engagement**: 5-7 threads minimum for 60 bar rating.

**Q14: Does K11 need calibration?**

**No**. Factory calibrated, plug-and-play operation. No field calibration required.

**Q15: What liquids is K11 compatible with?**

**Compatible with virtually all liquids**:
- Refrigeration oils (mineral, POE, PAG, PVE, AB)
- Refrigerants (R134a, R404A, R407C, R410A, CO2 up to 60 bar, ammonia)
- Water, glycol solutions
- Hydraulic oils (mineral, synthetic)
- Most chemicals (verify with Teklab for aggressive media)

**Glass dome**: Chemically inert, no degradation from refrigerant or oil exposure.

---

## 7. ORDERING INFORMATION

### 7.1 Model Selection

**Body Materials:**
- **Stainless Steel**: High corrosion resistance for harsh environments
- **Nickel-Plated Steel**: Cost-effective option for standard applications

**Power Supply Options:**
- **DC Models**: 10-28 VDC
  - NPN output
  - NPN open collector
  - PNP output (special order)
- **AC Models**: 24 VAC ±10% (50 or 60 Hz)

**Output Modes:**
- **Normally Open in Air**: Contact closes when liquid is detected
- **Normally Closed in Air**: Contact opens when liquid is detected

**Thread Options:**
- **Standard**: NPT (3/8", 1/2", 3/4")
- **Optional**: UNEF, Metric, GAS, custom threads

**Customization:**
- **Delay Times**: Programmable timer settings (0.5-30 seconds typical)
- **Cable Lengths**: Standard and custom lengths available
- **Special Voltages**: Custom voltage ranges available on request

### 7.2 What's Included

- K11 sensor assembly (sensor body, fused glass dome, cable)
- Installation instructions

### 7.3 What's NOT Included

- **Thread sealant**: Order separately (PTFE tape or liquid sealant rated for media and pressure)
- **Power supply**: External DC or AC power supply required
- **Cable strain relief**: Order separately if needed

### 7.4 Ordering Notes

**For specific ordering codes and customization options, please contact Teklab technical support with your application requirements:**
- Body material (stainless steel or nickel-plated steel)
- Power supply (10-28 VDC or 24 VAC)
- Output type (NPN, NPN open collector, PNP, AC)
- Output mode (NO or NC in air)
- Thread type (3/4" NPT standard, others available)
- Programmable timer delay (if required, specify seconds)
- Cable length (if custom length required)

---

## Document Information

**Document**: K11 Complete Product Documentation  
**Version**: 1.0  
**Date**: 2025-11-12  
**Language**: English  
**Product**: K11 Compact High-Pressure Level Switch  
**Category**: Sensors  
**Keywords**: K11, compact level switch, 60 bar, programmable timer, infrared optical, NPN PNP, 24VAC, stainless steel, nickel-plated, 59x27mm, level detection

**© 2025 Teklab. All rights reserved.**
