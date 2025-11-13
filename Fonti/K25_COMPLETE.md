---
category: Sensors
keywords:
- K25
- 150 bar
- ultra-high-pressure
- dual output
- CO2 transcritical
- temperature sensor
- 4-20mA
- NPN output
- level switch
- infrared technology
language: EN
product: K25
document_type: unified_complete
last_updated: 2025
---

# K25 Ultra-High-Pressure Level Switch with Temperature Sensor - Complete Technical Documentation

## Table of Contents
1. [Product Overview](#1-product-overview)
2. [Detection Technology & Key Features](#2-detection-technology--key-features)
3. [Technical Specifications](#3-technical-specifications)
4. [Applications & Selection Guide](#4-applications--selection-guide)
5. [Installation & Service Guidelines](#5-installation--service-guidelines)
6. [Frequently Asked Questions](#6-frequently-asked-questions)

---

## 1. Product Overview

### Introduction

The **K25** is Teklab's premier ultra-high-pressure optical level switch, specifically engineered for **CO2 transcritical and subcritical refrigeration systems**. With a working pressure rating of **150 bar**—the highest in Teklab's sensor lineup—the K25 sets itself apart by combining **two independent sensors in one compact unit**: a digital infrared level detector (NPN output) and an analog temperature sensor (4-20 mA output).

This dual-output design eliminates the need for separate level and temperature sensors, reducing installation complexity, cost, and potential failure points in critical high-pressure applications where comprehensive system monitoring is essential.

### Key Positioning

| Feature | K25 Advantage |
|---------|---------------|
| **Pressure Rating** | 150 bar (highest in Teklab range) |
| **Dual Output** | Level (NPN 50mA) + Temperature (4-20mA) in one sensor |
| **Target Application** | CO2 transcritical/subcritical refrigeration |
| **Technology** | Infrared optical detection + analog temperature sensing |
| **Design Philosophy** | Maximum pressure capability with comprehensive monitoring |

### Primary Applications

**CO2 Refrigeration Systems:**
- **Transcritical CO2**: Level and temperature monitoring in high-pressure receivers (up to 150 bar)
- **Subcritical CO2**: Liquid CO2 management in heat pumps and commercial refrigeration
- **Oil Separators**: Oil level monitoring in CO2 compressor systems with temperature alarm
- **Compressor Protection**: Crankcase oil level with simultaneous temperature monitoring

**High-Pressure Industrial:**
- **Hydraulic Reservoirs**: Oil level monitoring in 150 bar hydraulic systems
- **Process Vessels**: High-pressure tank level control with temperature data
- **CO2 Storage**: Liquid CO2 storage tank monitoring in industrial gas applications

### Why K25?

**When to Choose K25:**
- System pressures exceed 60 bar (K11's maximum rating)
- Both level AND temperature monitoring required in same location
- CO2 transcritical applications where pressure exceeds 100 bar
- Space constraints demand integrated sensing (eliminates second sensor installation)
- Temperature data critical for system optimization or safety monitoring

**When to Consider Alternatives:**
- **K11**: If pressure ≤60 bar and only level detection needed (no temperature output)
- **ATEX**: If explosive atmosphere certification required (K25 is not ATEX-certified)

---

## 2. Detection Technology & Key Features

### Infrared Level Detection Principle

The K25 employs the same proven **solid-state infrared optical technology** used across Teklab's sensor range, adapted for extreme pressure environments:

#### Operating Principle

1. **In Air (No Liquid Present)**:
   - Infrared LED emits light into the **fused glass dome** (hemisphere at sensor tip)
   - Light undergoes **total internal reflection** within the glass (refractive index difference: glass ≈ 1.5, air ≈ 1.0)
   - Reflected light returns to the **optical receiver (phototransistor)**
   - Receiver detects **high light intensity** → Output contact remains in "air" state

2. **In Liquid (Liquid Contacts Dome)**:
   - Liquid covers the glass dome (most liquids have refractive index 1.3-1.5, similar to glass)
   - Refractive index matching causes light to **refract into the liquid** instead of reflecting
   - Dramatically reduced light returns to receiver (**>90% light loss**)
   - Receiver detects **low light intensity** → Output contact switches to "liquid" state

3. **High Repeatability**:
   - Switching accuracy: **±2 mm**
   - No mechanical moving parts = no wear, no drift
   - Glass dome is **chemically inert** and compatible with oils, refrigerants (CO2, R134a, R410A), water, glycol

#### Advantages for 150 Bar Applications

- **No Seals or O-Rings in Sensing Element**: Fused glass dome is hermetically sealed (eliminates high-pressure seal failure risk)
- **Solid-State Reliability**: No floats, reeds, or mechanical parts that could bind under extreme pressure
- **Pressure-Independent Operation**: Detection principle unaffected by pressure (works equally at 1 bar or 150 bar)
- **Immune to Pressure Transients**: Rapid pressure changes (common in CO2 systems) do not cause false switching

### Analog Temperature Sensing

The K25 integrates a **precision temperature sensor** with **4-20 mA current loop output**:

#### Temperature Measurement

- **Sensing Element**: Industrial-grade temperature sensor embedded in sensor body
- **Measurement Range**: -40°C to +125°C (full Teklab sensor range)
- **Output Signal**: 4-20 mA current loop (industry-standard analog signal)
- **Scaling**: Typically 4 mA = -40°C, 20 mA = +125°C (can be customized for specific temperature ranges)
- **Response Time**: Fast thermal response suitable for real-time monitoring

#### Why Temperature Matters in CO2 Systems

In **CO2 refrigeration**, temperature and pressure are **directly correlated** due to CO2's thermodynamic properties:

1. **System Optimization**: Monitor subcooling or superheat by comparing temperature to system pressure
2. **Safety Monitoring**: Detect abnormal temperature rises indicating refrigerant loss, compressor issues, or system blockage
3. **Efficiency Control**: Optimize gas cooler pressure, evaporator superheat, or receiver subcooling based on real-time temperature
4. **Predictive Maintenance**: Temperature trends reveal developing problems (bearing wear, lubrication issues) before catastrophic failure

**Single Sensor, Comprehensive Data**: The K25's dual output provides complete system visibility at one installation point.

### Key Features Summary

#### Ultra-High Pressure Capability
- **150 bar working pressure** (highest in Teklab sensor range)
- **Nickel-plated steel body** designed for extreme pressure environments
- **Fused glass dome** with no pressure-sensitive seals
- Factory pressure-tested for compliance

#### Dual Output System
- **Digital Level Output**: NPN transistor, 50 mA maximum load current
- **Analog Temperature Output**: 4-20 mA current loop (simultaneous with level output)
- **Single Power Supply**: 24 VDC ±10% powers both outputs
- **Independent Operation**: Level and temperature outputs function independently

#### Solid-State Reliability
- **No Moving Parts**: Eliminates mechanical wear and failure modes
- **Infrared Technology**: Proven optical principle with 20+ years field history
- **Long Service Life**: Glass dome does not degrade; LED/receiver rated for 100,000+ hours
- **High Repeatability**: ±2 mm level switching accuracy maintained over sensor lifetime

#### Programmable Timer (Level Output)
- **Adjustable Delay**: Customizable time delay filters transients, foam, splashing
- **Application-Specific**: Contact Teklab to specify required delay (typical range 0.5-30 seconds)
- **Purpose**: Prevent false alarms in turbulent conditions (oil separator foam, compressor startup surges)

#### Built-in Protection
- **Reverse Polarity Protection**: Prevents damage from incorrect wiring
- **Overvoltage Protection**: Protects internal electronics from voltage spikes
- **Short-Circuit Protection**: NPN output protected against short-circuit to ground

#### Chemical Compatibility
- **Glass Sensing Element**: Compatible with all common refrigerants (CO2, R134a, R410A, ammonia), oils (mineral, POE, PAG), water, glycol
- **Nickel-Plated Steel Body**: Corrosion-resistant for long-term reliability in refrigeration environments

---

## 3. Technical Specifications

### Electrical Specifications

| Parameter | Specification |
|-----------|---------------|
| **Power Supply** | 24 VDC ± 10% (21.6 - 26.4 VDC) |
| **Current Consumption** | Max 100 mA (total for both outputs) |
| **Digital Level Output** | NPN transistor (open collector) |
| **Level Output Current** | 50 mA maximum load current |
| **Level Output Modes** | Normally Open (NO) or Normally Closed (NC) in air |
| **Analog Temperature Output** | 4-20 mA current loop |
| **Temperature Output Load** | Max 500 Ω (for 4-20 mA loop) |
| **Temperature Scaling** | Typically 4 mA @ -40°C, 20 mA @ +125°C (customizable) |
| **Programmable Timer** | Adjustable delay (contact Teklab for customization) |
| **Protection Features** | Reverse polarity, overvoltage, short-circuit protection |

### Pressure & Temperature Ratings

| Parameter | Specification |
|-----------|---------------|
| **Working Pressure** | **150 bar (2175 psi)** - Highest in Teklab range |
| **Temperature Range** | -40°C to +125°C (-40°F to +257°F) |
| **Level Repeatability** | ±2 mm (±0.08") |
| **Temperature Accuracy** | ±2°C (typical, over full range) |

### Mechanical Specifications

| Parameter | Specification |
|-----------|---------------|
| **Overall Dimensions** | 90 mm length × Ø20 mm diameter |
| **Body Material** | Nickel-plated steel (high-pressure rated) |
| **Sensing Element** | Fused glass dome (hemispherical, chemically inert) |
| **Thread Connection** | 3/4" NPT (standard) |
| **Thread Options** | NPT, ISO Metric (M18, M20, M22), UNEF, custom threads available |
| **Tightening Torque** | 15 N·m (11 lb-ft) - Do not exceed 20 N·m |
| **Cable Connection** | Pre-wired cable (standard length available, custom lengths on request) |
| **Weight** | Approx. 250 g (depending on cable length) |

### Environmental Specifications

| Parameter | Specification |
|-----------|---------------|
| **IP Rating** | IP67 (cable gland sealed) |
| **Vibration Resistance** | Suitable for compressor-mounted applications |
| **Installation Position** | Any orientation (no mechanical parts to bind) |
| **Fluid Compatibility** | CO2, R134a, R410A, R404A, R407C, ammonia (NH3), oils (mineral, POE, PAG), water, glycol, most industrial fluids |

### Ordering Codes (Standard Models)

#### 3/4" NPT Thread

| Output Mode (Level) | Code Number | Description |
|---------------------|-------------|-------------|
| **Normally Open in air** | 32517308304002003150 | Contact closes when liquid detected |
| **Normally Closed in air** | 32517308305002003150 | Contact opens when liquid detected |

**Note**: Both models include dual output (NPN level + 4-20 mA temperature) powered by 24 VDC ±10%.

### Custom Options Available

**Thread Customization:**
- NPT (other sizes beyond 3/4")
- ISO Metric: M18, M20, M22, or custom sizes
- UNEF (Unified Extra Fine Thread)
- Special threads for specific applications (e.g., Rotalock adapters)

**Timer Customization:**
- Programmable delay for level output (specify required delay time in seconds)

**Cable Customization:**
- Extended cable lengths for remote installations
- Special cable types (e.g., high-temperature insulation)

**Temperature Range Optimization:**
- Custom temperature output scaling (e.g., 4 mA @ 0°C, 20 mA @ +80°C for specific application range)

**Special Voltages:**
- Contact Teklab for non-standard voltage requirements

---

## 4. Applications & Selection Guide

### Primary Application: CO2 Refrigeration Systems

The K25 is **specifically optimized for CO2 transcritical and subcritical refrigeration**, where system pressures routinely exceed 100 bar and comprehensive monitoring is critical.

#### CO2 Transcritical Systems

**High-Pressure Receiver Monitoring:**
- **Pressure**: Transcritical CO2 systems operate at 90-150 bar on the high-pressure side
- **K25 Advantage**: Only Teklab sensor rated for these extreme pressures
- **Dual Output Benefit**: Level output ensures proper refrigerant charge; temperature output enables subcooling calculation (compare receiver temp to gas cooler outlet temp)

**Oil Separator Level Control:**
- **Challenge**: CO2's low viscosity causes oil to separate easily; oil management is critical in CO2 systems
- **K25 Solution**: Monitor oil level in separator with simultaneous temperature monitoring (abnormal temp indicates insufficient oil return)
- **Programmable Timer**: Filters foam/bubbles common during oil drainage cycles

**Compressor Crankcase Protection:**
- **Risk**: Liquid CO2 slugging can destroy compressor; insufficient oil causes bearing wear
- **K25 Protection**: Level output detects dangerous liquid CO2 accumulation; temperature output warns of overheating due to oil starvation
- **Fail-Safe**: Normally Closed configuration ensures alarm if sensor loses power

#### CO2 Subcritical Systems (Heat Pumps)

**Liquid Receiver Monitoring:**
- **Pressure**: Subcritical CO2 operates at 50-80 bar (still exceeds K11's 60 bar rating)
- **K25 Advantage**: Adequate pressure margin ensures long-term reliability
- **Temperature Data**: Optimize system charge by monitoring subcooling in receiver

**Evaporator Outlet Superheat:**
- **Advanced Application**: In some configurations, K25 can monitor evaporator outlet superheat by detecting liquid carryover (level output) and measuring temperature (analog output)
- **System Optimization**: Fine-tune expansion valve control for maximum efficiency

### Industrial High-Pressure Applications

#### Hydraulic Systems (150 bar)

**Hydraulic Reservoir Monitoring:**
- **Challenge**: High-pressure hydraulic systems require reliable level monitoring to prevent pump cavitation
- **K25 Solution**: 150 bar rating handles high-pressure reservoirs; temperature output detects hydraulic fluid overheating (indicates pump/motor inefficiency or fluid degradation)

**Oil Filtration Systems:**
- **Application**: Monitor oil level in high-pressure filter housings
- **Benefit**: Temperature output warns of filter clogging (temperature rise indicates pressure drop and inefficiency)

#### Process Vessels (Chemical/Petrochemical)

**High-Pressure Process Tanks:**
- **Pressure Range**: 100-150 bar process vessels in chemical plants
- **K25 Advantage**: Handles extreme pressures; dual output provides process control data (level) and safety monitoring (temperature)
- **Chemical Compatibility**: Glass dome compatible with most process fluids (consult Teklab for corrosive chemicals)

#### Liquid CO2 Storage (Industrial Gas)

**Bulk CO2 Storage Tanks:**
- **Application**: Industrial gas suppliers store liquid CO2 at high pressure
- **K25 Monitoring**: Level output controls filling/dispensing; temperature output ensures proper storage conditions (temperature affects CO2 vapor pressure and quality)

### K25 vs. Alternative Sensors - Selection Guide

#### Compare: K25, K11, ATEX

| Feature | K25 | K11 | ATEX |
|---------|-----|-----|------|
| **Working Pressure** | **150 bar** | 60 bar | 20 bar |
| **Level Output** | NPN 50mA | NPN/PNP 100mA or 24VAC relay | NPN 40mA open collector |
| **Temperature Output** | **4-20 mA (Yes)** | No | No |
| **Dimensions** | 90mm × Ø20mm | 59mm × Ø27mm | ~80mm × Ø18mm |
| **Power Supply** | 24 VDC ±10% | 10-28 VDC or 24 VAC | 9-28 Vdc |
| **Programmable Timer** | Yes | Yes | No |
| **ATEX Certification** | No | No | **Ex ia IIC T6 (Yes)** |
| **Primary Application** | CO2 transcritical, ultra-high-pressure | Compact installations, high-pressure | Explosive atmospheres (Zone 0/1/2) |
| **Key Advantage** | Highest pressure + dual output | Most compact + multiple output options | Intrinsically safe certification |

#### Decision Matrix

**Choose K25 when:**
- ✅ Pressure >60 bar (exceeds K11 rating) or application requires 150 bar capability
- ✅ Both level AND temperature monitoring required in same location
- ✅ CO2 transcritical refrigeration (90-150 bar high side)
- ✅ Space/cost savings from eliminating separate temperature sensor
- ✅ Temperature data critical for system optimization or safety

**Choose K11 when:**
- ✅ Pressure ≤60 bar (sufficient for most subcritical refrigeration)
- ✅ Only level detection needed (no temperature output required)
- ✅ Most compact sensor needed (59mm × Ø27mm vs. K25's 90mm × Ø20mm)
- ✅ Budget-sensitive application where temperature monitoring not required

**Choose ATEX when:**
- ✅ Explosive atmosphere classification requires intrinsically safe sensor (Zone 0, 1, or 2)
- ✅ Petrochemical, offshore, or hazardous gas applications
- ✅ Pressure ≤20 bar (ATEX rating sufficient for application)

### Wiring Diagrams

#### K25 Dual Output Wiring - NPN Level + 4-20 mA Temperature

**4-Wire Configuration (Standard):**

```
K25 SENSOR                          PLC / CONTROLLER
┌──────────────┐
│              │
│   K25 Sensor │
│   150 bar    │
│              │
└──────────────┘
     │  │  │  │
     │  │  │  │
     │  │  │  └─── Brown (+24 VDC) ────────► +24 VDC Supply (+)
     │  │  └────── Blue (0V GND) ───────────► Power Supply GND (-)
     │  └───────── Black (NPN Level) ───────► Digital Input (Level Detection)
     └──────────── White (4-20 mA Temp) ────► Analog Input (Temperature Measurement)
                                              (Connect to 250-500Ω load resistor 
                                               or PLC analog input)

Notes:
- NPN Level Output: Sinks current when active (connect to +24V through digital input)
- 4-20 mA Temperature: Current source (loop powered by 24 VDC supply)
- Both outputs operate simultaneously from single 24 VDC supply
```

**NPN Level Output (Normally Open in Air) - Detailed:**

```
         +24 VDC ───┬──── To PLC Digital Input (+) (10kΩ pull-up typical)
                    │
                    └──── Black Wire (NPN Collector)
                          │
                          │  When LIQUID detected: NPN conducts
                          │  → Digital input sees 0V (LOW)
                          │
                          │  When AIR: NPN off
                          │  → Digital input sees +24V (HIGH via pull-up)
                          │
                         GND (Blue Wire)
```

**4-20 mA Temperature Output - Detailed:**

```
White Wire (4-20 mA) ───► Analog Input (PLC)
                          │
                          └─── 250Ω Resistor (if not internal to PLC)
                               │
                              GND (Blue Wire)

Temperature Scaling Example:
- 4 mA   = -40°C  →  Voltage across 250Ω = 1.0 V
- 12 mA  = +42.5°C →  Voltage across 250Ω = 3.0 V
- 20 mA  = +125°C →  Voltage across 250Ω = 5.0 V

PLC reads voltage (0-5V) or current (4-20mA) depending on analog input type.
```

---

## 5. Installation & Service Guidelines

### Pre-Installation Checklist

**Verify Application Suitability:**
- ✅ System pressure ≤150 bar (K25 working pressure rating)
- ✅ Fluid temperature within -40°C to +125°C range
- ✅ Fluid compatible with nickel-plated steel and glass (consult Teklab for corrosive chemicals)
- ✅ 24 VDC ±10% power supply available
- ✅ PLC/controller has digital input (for NPN level output) and analog input (for 4-20 mA temperature)

**Select Correct Model:**
- **Normally Open (NO) in air**: Contact closes when liquid detected → Low-level alarm or pump start
- **Normally Closed (NC) in air**: Contact opens when liquid detected → High-level alarm or pump stop

**Check Thread Compatibility:**
- Standard: 3/4" NPT
- Custom threads available (contact Teklab before ordering if non-standard thread required)

### Mechanical Installation

#### Mounting Location Selection

**Critical Factors:**

1. **Representative Level**: Install where liquid level accurately reflects tank/vessel condition
   - **Avoid**: Turbulent zones near inlet pipes, baffles, or agitators (unless programmable timer configured to filter transients)
   - **Prefer**: Calm zones with stable liquid surface

2. **Temperature Measurement Accuracy**:
   - **For Liquid Temperature**: Ensure sensor tip is immersed in liquid when level is present
   - **For Gas/Vapor Temperature**: Mount above normal liquid level if measuring vapor temperature
   - **Avoid**: Dead zones, thermal stratification areas, or direct contact with hot/cold pipes

3. **Accessibility**: Ensure access for installation and future maintenance (sensor is generally maintenance-free, but may require replacement after decades of service)

4. **Pressure Relief**: In high-pressure systems, ensure sensor installation point can be isolated for service without depressurizing entire system (install isolation valve if required)

#### Thread Installation Procedure

**Step 1: Thread Preparation**
- Clean threads in tank/vessel boss (remove metal chips, old sealant)
- Inspect threads for damage (damaged threads may leak under 150 bar pressure)

**Step 2: Thread Sealant Application**
- Apply **PTFE tape** (2-3 wraps) or **thread sealant paste** compatible with system fluid
- **Critical**: Do NOT allow sealant to enter sensor tip (keep sealant away from first 2 threads)
- For CO2 systems, use CO2-compatible sealant (many standard sealants degrade in CO2)

**Step 3: Sensor Installation**
- Hand-tighten sensor into boss
- Use wrench on **hexagonal body** (typically 27mm or 30mm hex, depending on thread size)
- **Torque Specification**: **15 N·m (11 lb-ft)** recommended
  - **Minimum**: 12 N·m (adequate seal in most applications)
  - **Maximum**: **20 N·m** (do NOT exceed – over-torquing can damage sensor body or threads)

**Step 4: Orientation (Not Critical)**
- K25 has no moving parts → Can be installed in **any orientation** (horizontal, vertical, upside-down)
- **Recommendation**: Orient cable exit to minimize strain on cable and facilitate wiring route

**Step 5: Vibration Considerations**
- In high-vibration environments (compressor-mounted applications), ensure sensor is securely tightened and cable is strain-relieved
- Consider vibration-dampening mounts if vibration is severe

#### Pressure Testing (Before System Operation)

**After Installation:**
- Pressurize system slowly to working pressure (observe for leaks at sensor threads)
- If leak detected, depressurize, remove sensor, inspect threads, reapply sealant, reinstall
- **Never attempt to tighten sensor under pressure** (extremely dangerous at 150 bar)

### Electrical Installation

#### Wiring Guidelines

**Cable Routing:**
- Route sensor cable away from high-voltage AC power cables (>50V AC)
- Use cable tray or conduit to protect cable from mechanical damage
- Avoid sharp bends (minimum bend radius: 10× cable diameter, typically 50-80mm)

**Cable Length:**
- Standard cable lengths available (contact Teklab for specific options)
- For long cable runs, consider voltage drop on 24 VDC supply line (use larger wire gauge if >10m cable run)
- 4-20 mA current loop can tolerate long cables (voltage drop across load resistor, not cable)

**Strain Relief:**
- Secure cable near sensor to prevent mechanical stress on sensor body
- Use cable gland or zip tie to anchor cable to nearby structure (prevent vibration fatigue)

#### Electrical Connections (PLC/Controller)

**Power Supply Connection:**
- **Brown (+24 VDC)**: Connect to +24 VDC regulated power supply output
- **Blue (0V GND)**: Connect to power supply ground (common with PLC ground)
- **Power Supply Requirements**: 24 VDC ±10%, minimum 100 mA available current

**NPN Level Output Connection:**
- **Black (NPN Output)**: Connect to PLC digital input
  - **NPN Configuration**: PLC digital input must have pull-up to +24V (most PLCs have internal pull-up; if not, add external 10kΩ resistor between digital input and +24V)
  - **Logic**: 
    - **Liquid Present (NO mode)**: NPN conducts → Digital input sees ~0V (LOW/False)
    - **Air (NO mode)**: NPN off → Digital input sees +24V (HIGH/True via pull-up)
    - **Note**: Logic inverted for NC mode (contact opens when liquid detected)

**4-20 mA Temperature Output Connection:**
- **White (4-20 mA)**: Connect to PLC analog input or temperature controller
  - **Analog Input Type**:
    - **Current Input (4-20 mA)**: Connect directly to PLC analog input configured for 4-20 mA
    - **Voltage Input (0-5V or 0-10V)**: Place 250Ω resistor between white wire and blue (GND) wire; measure voltage across resistor (4 mA → 1.0V, 20 mA → 5.0V)
  - **Maximum Load Resistance**: 500Ω (for 4-20 mA loop)
  - **Scaling**: Configure PLC analog input scaling to match temperature range (typical: 4 mA = -40°C, 20 mA = +125°C; or custom scaling if specified during ordering)

**Grounding:**
- Connect power supply ground to earth ground (especially in industrial environments with electrical noise)
- Ensure PLC ground and sensor power supply ground are at same potential (avoid ground loops)

### Commissioning & Testing

#### Initial Power-Up

**Step 1: Verify Power Supply**
- Measure voltage at sensor: Brown (+) to Blue (-) should read 21.6-26.4 VDC (24V ±10%)
- Verify current consumption <100 mA (measure in series with Brown wire)

**Step 2: Test Level Output (NPN)**
- **In Air** (sensor tip not submerged):
  - **NO mode**: Digital input should read HIGH (+24V via pull-up)
  - **NC mode**: Digital input should read LOW (~0V)
- **In Liquid** (submerge sensor tip in test liquid or system liquid):
  - **NO mode**: Digital input should switch to LOW (~0V) within programmable timer delay
  - **NC mode**: Digital input should switch to HIGH (+24V)
- **Repeatability Test**: Remove sensor from liquid, resubmerge several times → Output should switch consistently at same level (±2mm)

**Step 3: Test Temperature Output (4-20 mA)**
- **Room Temperature Check**: 
  - Measure current on white wire (use multimeter in series): Should read 4-20 mA corresponding to ambient temperature
  - Example: At 20°C, expect ~7 mA (based on -40°C to +125°C scaling)
- **Temperature Range Verification**:
  - If accessible, expose sensor to known temperature (e.g., ice water 0°C, or hot fluid +60°C) → Verify 4-20 mA output matches expected value within ±2°C accuracy
- **PLC Analog Input Verification**:
  - Check PLC reads temperature correctly (verify scaling configuration matches sensor output)

**Step 4: Programmable Timer Verification (if configured)**
- **Purpose**: Timer delays level output switching to filter transients (foam, splashing)
- **Test**: Rapidly submerge and remove sensor tip in liquid
  - Without timer: Output switches immediately
  - With timer (e.g., 3-second delay): Output does NOT switch until sensor is continuously submerged for 3 seconds
- **Adjustment**: If timer delay inadequate or excessive, contact Teklab to reprogram (requires factory reconfiguration)

### Maintenance & Service

#### Routine Maintenance (Minimal Required)

The K25 is a **solid-state sensor with no moving parts** → Routine maintenance is minimal:

**Annual Inspection (Recommended):**
- **Visual Inspection**: Check cable for damage (abrasion, cuts, or insulation degradation)
- **Thread Inspection**: Check for refrigerant/fluid leaks at sensor threads (especially critical at 150 bar)
- **Glass Dome Inspection**: Visually inspect sensing tip for cracks, chips, or heavy contamination (if accessible)
  - **Light contamination** (oil film, dust) does NOT affect performance (infrared detection principle tolerates films)
  - **Heavy deposits** (salt crystals, polymerized oil) may require cleaning

**Cleaning Procedure (if needed):**
- **Isolate & Depressurize**: Shut isolation valve, depressurize sensor installation point (NEVER attempt to remove sensor under pressure)
- **Remove Sensor**: Unscrew sensor from boss
- **Clean Glass Dome**: 
  - Use soft cloth with **isopropyl alcohol** (IPA) or **mild detergent solution**
  - **Do NOT use abrasive cleaners** or hard brushes (may scratch glass)
  - Rinse with clean water, dry with soft cloth
- **Reinstall**: Follow installation procedure (new thread sealant, torque to 15 N·m)

#### Troubleshooting

**Problem: Level Output Not Switching**

| Symptom | Possible Cause | Solution |
|---------|---------------|----------|
| Output stuck HIGH (NO mode) | - Sensor tip contaminated (heavy deposit blocking light)<br>- Glass dome damaged<br>- Internal fault | - Clean glass dome (see cleaning procedure)<br>- Inspect for cracks → Replace if damaged<br>- Check power supply voltage → If >26.4V, sensor may be damaged<br>- Replace sensor if cleaning does not resolve |
| Output stuck LOW (NO mode) | - No power to sensor<br>- NPN output shorted to ground<br>- Internal fault | - Verify 24 VDC present at Brown/Blue wires<br>- Disconnect Black wire, measure voltage → Should read +24V (via pull-up)<br>- If 0V with wire disconnected, PLC digital input may be damaged<br>- Replace sensor if fault persists |
| Intermittent switching (false alarms) | - Foam or bubbles in liquid<br>- Turbulent installation location<br>- Programmable timer not configured or inadequate | - Verify installation location (move to calmer zone if possible)<br>- Contact Teklab to configure/adjust programmable timer delay<br>- Consider longer timer delay for applications with persistent foam |

**Problem: Temperature Output Incorrect or No Signal**

| Symptom | Possible Cause | Solution |
|---------|---------------|----------|
| No current on white wire (reads 0 mA) | - Open circuit in cable<br>- Internal temperature sensor fault<br>- Power supply issue | - Check cable continuity (white wire to PLC analog input)<br>- Verify 24 VDC power present at Brown/Blue wires<br>- Measure current with multimeter in series → If 0 mA, replace sensor<br>- Check PLC analog input wiring (250Ω load resistor if required) |
| Current reads 4 mA (minimum) at all temperatures | - Temperature sensor fault (sensor reading <-40°C)<br>- Cable short circuit | - Disconnect white wire from PLC, measure current → Should vary with temperature<br>- If stuck at 4 mA, replace sensor<br>- Check for short circuit between white and blue wires |
| Current reads 20 mA (maximum) at all temperatures | - Temperature sensor fault (sensor reading >+125°C)<br>- Cable short circuit | - Disconnect white wire from PLC, measure current → Should vary with temperature<br>- If stuck at 20 mA, replace sensor<br>- Check for short circuit between white and brown wires |
| Temperature reading incorrect (e.g., reads 50°C when actual temp is 20°C) | - PLC analog input scaling incorrect<br>- Custom temperature range ordered but PLC configured for default scaling | - Verify PLC analog input scaling matches sensor configuration<br>- Default: 4 mA = -40°C, 20 mA = +125°C<br>- If custom scaling ordered, check order documentation for correct scaling<br>- Reconfigure PLC scaling or contact Teklab to verify sensor calibration |

**Problem: Sensor Leaking Refrigerant/Fluid at Threads**

| Symptom | Possible Cause | Solution |
|---------|---------------|----------|
| Leak at sensor threads | - Insufficient thread sealant<br>- Damaged threads in boss<br>- Under-torqued sensor<br>- Damaged sensor threads | - **Depressurize system immediately** (do NOT attempt to tighten under pressure at 150 bar)<br>- Remove sensor, inspect threads (both sensor and boss)<br>- Replace boss if threads damaged (re-tap threads or weld new boss)<br>- Apply fresh thread sealant (PTFE tape or CO2-compatible paste)<br>- Reinstall sensor, torque to 15 N·m (verify with torque wrench)<br>- Repressurize slowly, monitor for leaks |

#### Replacement Procedure

**When to Replace:**
- Glass dome cracked or chipped (cannot be repaired)
- Internal fault confirmed (level or temperature output failure after troubleshooting)
- Cable damaged beyond repair (sensor cable typically not field-replaceable)
- After 15-20 years of continuous service (preventive replacement before end-of-life failure)

**Replacement Steps:**
1. Isolate and depressurize sensor installation point (install isolation valve if not present)
2. Remove old sensor (note orientation and installation depth for reference)
3. Clean threads in boss, apply fresh thread sealant
4. Install new sensor (same model/configuration to avoid PLC reprogramming)
5. Reconnect wiring (verify wire colors match old sensor: Brown=+24V, Blue=GND, Black=NPN, White=4-20mA)
6. Commission new sensor (power-up test, level output test, temperature output verification)
7. Return system to service

**Disposal:**
- K25 contains electronic components → Dispose according to local WEEE regulations (Waste Electrical and Electronic Equipment)
- Nickel-plated steel body can be recycled as scrap metal

---

## 6. Frequently Asked Questions

### Q1: What makes the K25 different from other Teklab sensors?

The K25 is Teklab's **only dual-output sensor**, combining **level detection (NPN)** and **temperature measurement (4-20 mA)** in a single unit. It also has the **highest pressure rating** in the Teklab range (**150 bar**), making it uniquely suited for **CO2 transcritical refrigeration** and other ultra-high-pressure applications where both level and temperature monitoring are required.

**Key Differentiators:**
- **150 bar pressure rating** (vs. K11's 60 bar, ATEX's 20 bar)
- **Dual output** eliminates need for separate temperature sensor (reduces cost, installation complexity, failure points)
- **CO2-optimized design** addresses specific challenges of transcritical CO2 systems (high pressure, temperature-dependent system behavior)

---

### Q2: Why is a dual output (level + temperature) important in CO2 systems?

In **CO2 refrigeration**, temperature and pressure are **thermodynamically coupled**:

1. **Subcooling Optimization**: By measuring liquid temperature in the receiver and comparing to system pressure, you can calculate subcooling (difference between saturation temperature and actual liquid temperature). Proper subcooling ensures maximum refrigeration capacity and prevents flash gas formation in liquid lines.

2. **Safety Monitoring**: Abnormal temperature rise in a receiver or oil separator indicates potential problems:
   - **Refrigerant Loss**: Temperature increases as liquid level drops (reduced thermal mass)
   - **Compressor Issues**: Oil temperature rise in crankcase indicates bearing wear or oil starvation
   - **System Blockage**: Temperature spike may indicate restricted flow or valve failure

3. **Efficiency Control**: Real-time temperature data enables advanced control algorithms (e.g., gas cooler pressure optimization based on ambient conditions and receiver temperature)

4. **Predictive Maintenance**: Temperature trends over weeks/months reveal degrading system performance before catastrophic failure occurs.

**Single-Sensor Solution**: The K25 provides both critical parameters at one installation point, reducing hardware cost and simplifying system architecture.

---

### Q3: Can K25 be used in ammonia (NH3) refrigeration?

**Yes, with precautions**:

**Materials Compatibility:**
- **Glass Dome**: Chemically inert, fully compatible with ammonia
- **Nickel-Plated Steel Body**: Generally compatible with ammonia in refrigeration applications (dry ammonia does not significantly corrode steel; wet ammonia with air/water can cause stress corrosion cracking over time)

**Pressure Compatibility:**
- Ammonia systems typically operate at 10-25 bar (low/high side) → Well within K25's 150 bar rating

**Recommendations for Ammonia:**
- **Dry System**: Ensure ammonia system is dry (moisture-free) to minimize corrosion risk
- **Monitor Corrosion**: Periodic inspection during maintenance (check for pitting or stress corrosion on body)
- **Alternative**: For long-term ammonia service (>10 years), consider requesting **316L stainless steel body** as custom option (contact Teklab) for enhanced corrosion resistance

**Application Examples:**
- High-pressure ammonia receivers (though ammonia rarely exceeds 25 bar, K25's 150 bar rating provides large safety margin)
- Ammonia oil separators (temperature output useful for detecting oil degradation)

---

### Q4: What is the difference between Normally Open (NO) and Normally Closed (NC) modes?

**Normally Open (NO) in Air:**
- **Definition**: Output contact is **open (non-conducting) when sensor is in air**
- **Behavior**: Contact **closes (conducts) when liquid is detected**
- **PLC Logic (NPN with pull-up)**: 
  - Air → Digital input reads HIGH (+24V)
  - Liquid → Digital input reads LOW (0V)
- **Common Applications**:
  - **Low-level alarm**: "Add refrigerant when contact closes" (liquid level drops below sensor → output opens → alarm)
  - **Pump start**: "Start fill pump when contact closes" (low level detected)

**Normally Closed (NC) in Air:**
- **Definition**: Output contact is **closed (conducting) when sensor is in air**
- **Behavior**: Contact **opens (non-conducting) when liquid is detected**
- **PLC Logic (NPN with pull-up)**:
  - Air → Digital input reads LOW (0V)
  - Liquid → Digital input reads HIGH (+24V)
- **Common Applications**:
  - **High-level alarm**: "Stop filling when contact opens" (liquid reaches sensor → output opens → stop pump)
  - **Fail-safe monitoring**: NC mode ensures alarm if sensor loses power (power loss → contact opens → alarm triggers)

**Selection Tip**: Choose based on desired fail-safe behavior:
- **NO mode**: Alarm on low level (common for reservoir monitoring)
- **NC mode**: Alarm on high level or fail-safe design (power loss triggers alarm)

**Note**: The 4-20 mA temperature output operates continuously in both NO and NC modes (output mode only affects level detection, not temperature measurement).

---

### Q5: How accurate is the temperature measurement?

**Temperature Accuracy**: ±2°C (typical) over the full -40°C to +125°C range

**Factors Affecting Accuracy:**

1. **Calibration**: K25 is factory-calibrated; accuracy is maintained over sensor lifetime (no field calibration required or supported)

2. **Installation**: Temperature sensor is embedded in sensor body → Measures temperature at installation point:
   - **For Liquid Temperature**: Ensure sensor is immersed in liquid (not in vapor space) when liquid is present
   - **Thermal Lag**: In rapidly changing temperatures, sensor body has thermal mass → 30-60 second response time to stabilize (faster than thermowell-mounted sensors, slower than bare-element thermocouples)

3. **Ambient Effects**: In applications with extreme ambient temperature (e.g., sensor body in +50°C ambient, sensing -20°C liquid), heat conduction through sensor body may affect accuracy (typically <1°C error in most installations)

**Comparison to Dedicated Temperature Sensors:**
- K25 accuracy (±2°C) is adequate for **system monitoring and control** (subcooling calculation, safety alarms)
- For **precision temperature control** (±0.5°C or better), use dedicated high-accuracy temperature sensor (e.g., RTD Pt100) in addition to K25 (K25 provides level + approximate temperature; RTD provides precision temperature)

---

### Q6: Can K25 replace two separate sensors (level + temperature)?

**Yes! This is a primary design advantage:**

**Traditional Approach (Two Sensors):**
- **Level Sensor**: K11 or equivalent (one installation point, one wiring run)
- **Temperature Sensor**: RTD or thermocouple (second installation point, second wiring run)
- **Total Cost**: Hardware cost of two sensors + two installation labor costs + two potential failure points

**K25 Integrated Approach (One Sensor):**
- **Single Device**: Provides both level (NPN) and temperature (4-20 mA) outputs
- **One Installation Point**: Reduces tank/vessel penetrations (fewer leak points at 150 bar)
- **One Wiring Run**: Single 4-wire cable (Brown/Blue/Black/White) instead of two separate cable runs
- **Reduced Complexity**: Simplified BOM (bill of materials), inventory, and maintenance

**Cost-Benefit Analysis:**

| Factor | Two Sensors (K11 + Temp Sensor) | K25 (Integrated) | Savings |
|--------|--------------------------------|------------------|---------|
| **Hardware Cost** | ~$X (K11) + ~$Y (temp sensor) | ~$Z (K25) | Typically 10-20% lower |
| **Installation Labor** | 2× installations (thread sealing, wiring) | 1× installation | ~50% labor reduction |
| **Tank Penetrations** | 2 bosses (more welding/threading) | 1 boss | Reduced leak risk at 150 bar |
| **Maintenance** | 2 sensors to inspect/replace | 1 sensor to inspect/replace | 50% fewer maintenance items |
| **Reliability** | 2 potential failure points | 1 potential failure point (but dual-function) | Trade-off: fewer devices, but single-point-of-failure for both functions |

**When to Use Separate Sensors:**
- **Precision Temperature**: If temperature accuracy >±2°C required (use K25 for level, dedicated RTD for precision temperature)
- **Redundancy**: Critical applications may require separate level and temperature sensors for redundancy (if K25 fails, both functions lost; separate sensors allow one to continue if other fails)

---

### Q7: Is the K25 compatible with all refrigerants?

**Yes, K25 is compatible with common refrigerants**:

**Confirmed Compatible Refrigerants:**
- **CO2 (R744)**: Primary design target (transcritical/subcritical)
- **HFC Refrigerants**: R134a, R404A, R407C, R410A, R32
- **HFO Refrigerants**: R1234yf, R1234ze, R513A
- **Ammonia (NH3 / R717)**: Compatible with dry ammonia (see Q3 for ammonia-specific considerations)
- **Hydrocarbons**: R290 (propane), R600a (isobutane) - compatible, but verify ATEX requirements for hydrocarbon systems (K25 is NOT ATEX-certified; use ATEX sensor for explosive atmosphere applications)

**Lubrication Oils:**
- **Mineral Oil (MO)**
- **Polyolester (POE)**
- **Polyalkylene Glycol (PAG)**
- **Polyvinyl Ether (PVE)**

**Other Fluids:**
- **Water** and **water-glycol mixtures** (heating/cooling systems)
- **Hydraulic Oils** (mineral-based, synthetic)

**Incompatible / Consult Teklab:**
- **Highly Corrosive Chemicals**: Strong acids, strong bases (may corrode nickel-plated steel body or glass over time)
- **Solvents**: Aggressive solvents (e.g., chlorinated hydrocarbons) may degrade cable insulation or body coating
- **Cryogenic Fluids**: <-40°C (below K25 minimum temperature rating)
- **High-Temperature Fluids**: >+125°C (exceeds K25 maximum temperature rating)

**Verification**: For unusual fluids or extreme conditions, contact Teklab Technical Support (info@teklab.it) with fluid specifications and operating conditions.

---

### Q8: What is the purpose of the programmable timer in the K25?

The **programmable timer** (also called "delay timer" or "anti-transient filter") delays the level output switching to filter **temporary liquid contact** or **false triggers**:

**Common False Trigger Scenarios:**

1. **Foam / Bubbles**: 
   - **Problem**: Liquid foam or air bubbles in turbulent systems can intermittently contact sensor dome → Rapid on/off switching → False alarms, relay chatter, compressor cycling
   - **Timer Solution**: Sensor output does NOT switch until liquid continuously present for timer duration (e.g., 3 seconds) → Foam collapses or bubbles dissipate before output switches

2. **Splashing / Transients**:
   - **Problem**: Liquid splashing during compressor startup, defrost cycles, or solenoid valve opening → Brief liquid contact → False high-level alarm
   - **Timer Solution**: Timer filters out splashes lasting <timer duration → Output switches only for sustained liquid level

3. **Oil Drainage (Oil Separators)**:
   - **Problem**: During oil return cycles, liquid oil level may fluctuate rapidly → Unstable level output
   - **Timer Solution**: Timer stabilizes output → Prevents unnecessary oil drain valve cycling

**Timer Configuration:**
- **Factory Setting**: Timer delay is configurable at Teklab factory (not user-adjustable in field)
- **Typical Range**: 0.5 to 30 seconds (most applications use 1-5 second delay)
- **Ordering**: Specify required timer delay when ordering (contact Teklab Technical Support to determine optimal delay for your application)

**Trade-Off:**
- **Advantage**: Eliminates false alarms, reduces control system chatter, improves reliability
- **Disadvantage**: Delays response to real level changes by timer duration (e.g., 3-second timer means 3-second delay before alarm triggers after liquid reaches sensor)

**Recommendation**: For most CO2 receivers and oil separators, a **2-3 second timer** provides good balance between transient filtering and acceptable response time.

---

### Q9: Can K25 be installed in any orientation?

**Yes, absolutely!**

The K25 uses **solid-state infrared optical detection** with **no mechanical moving parts** (no floats, no reed switches, no tilt sensors) → Operates identically in **any orientation**:

**Supported Orientations:**
- **Vertical (tip down)**: Most common for tank bottom or side mounting
- **Vertical (tip up)**: Acceptable (e.g., inverted installation in tank top)
- **Horizontal**: Acceptable (e.g., side-mounted in pipes or horizontal vessels)
- **Angled**: Any angle works (detection principle unaffected by gravity)

**Installation Recommendations (Practical, Not Technical):**

1. **Cable Exit Orientation**: Orient sensor so cable exit minimizes strain on cable (avoid tight bends immediately at sensor body)

2. **Mechanical Stress**: In vibration environments (compressor crankcase), ensure sensor is securely tightened (15 N·m torque) and cable is strain-relieved

3. **Accessibility**: Orient sensor for easy access during future maintenance (inspection, cleaning, replacement)

**Temperature Measurement Consideration:**
- Temperature sensor is in **sensor body** (not at glass dome tip) → For accurate liquid temperature, ensure sensor body is immersed or in good thermal contact with liquid/metal vessel wall
- In horizontal pipe installations, liquid may not fully surround sensor body → Temperature reading may be influenced by vapor temperature or pipe wall temperature

---

### Q10: How do I troubleshoot incorrect temperature readings?

**Step-by-Step Troubleshooting:**

**Problem: Temperature Reading Too High or Too Low (but not stuck at 4 mA or 20 mA)**

**Step 1: Verify Reference Temperature**
- Use calibrated thermometer or RTD to measure actual fluid temperature at sensor location
- Ensure reference sensor is at same location as K25 (temperature gradients can cause apparent discrepancy)

**Step 2: Check PLC Analog Input Scaling**
- **Default Scaling**: 4 mA = -40°C, 20 mA = +125°C
  - **Formula**: Temperature (°C) = [(Current_mA - 4) / 16] × 165 - 40
  - **Example**: 12 mA → [(12 - 4) / 16] × 165 - 40 = 42.5°C
- **Verify PLC Configuration**: Ensure PLC analog input scaling matches sensor scaling
  - If custom temperature range ordered (e.g., 4 mA = 0°C, 20 mA = +80°C), verify PLC configured for custom scaling

**Step 3: Measure Current at Sensor (Bypass PLC)**
- Disconnect white wire from PLC analog input
- Connect multimeter (set to mA mode) in series: White wire → Multimeter (+) → Multimeter (-) → Blue wire (GND)
- Read current: Should correspond to actual temperature within ±2°C
  - **If current correct but PLC reads incorrectly**: PLC scaling misconfigured → Fix PLC scaling
  - **If current incorrect**: Proceed to Step 4

**Step 4: Check for Wiring Issues**
- Inspect white wire for damage (cuts, pinches, exposed conductor)
- Measure resistance between white wire and blue wire (with sensor disconnected from power): Should read **open circuit** (>1 MΩ)
  - **If low resistance**: Short circuit in cable → Replace sensor (cable typically not field-repairable)

**Step 5: Verify Power Supply Voltage**
- Measure voltage between brown (+24V) and blue (GND): Should read 21.6-26.4 VDC
  - **If voltage outside range**: Adjust/replace power supply (overvoltage can damage sensor, undervoltage can cause incorrect temperature reading)

**Step 6: Test with Known Temperature (if possible)**
- Expose sensor to known temperature (e.g., ice water 0°C, or boiling water +100°C at sea level)
- Verify 4-20 mA output matches expected value within ±2°C
  - **If reading incorrect at known temperature**: Sensor calibration fault → Replace sensor (field recalibration not supported)

**Problem: Temperature Reading Stuck at 4 mA (minimum)**

**Likely Cause**: Temperature sensor reading <-40°C (below minimum range) OR sensor fault

**Solution**:
- Verify actual temperature >-40°C (use reference thermometer)
- If actual temperature within range but output stuck at 4 mA: Replace sensor (temperature sensor element failure)

**Problem: Temperature Reading Stuck at 20 mA (maximum)**

**Likely Cause**: Temperature sensor reading >+125°C (above maximum range) OR sensor fault

**Solution**:
- Verify actual temperature <+125°C (use reference thermometer)
- If actual temperature within range but output stuck at 20 mA: Replace sensor (temperature sensor element failure)

**Problem: Temperature Reading Noisy (fluctuates rapidly)**

**Likely Cause**: Electrical noise coupling into 4-20 mA signal

**Solution**:
- Route sensor cable away from high-voltage AC cables (>50V AC) and VFD (variable frequency drive) cables
- Use shielded cable if available (shield connected to ground at PLC end only, not at sensor end)
- Add low-pass filter in PLC software (average temperature over 5-10 seconds to smooth noise)
- Ensure power supply ground and PLC ground are at same potential (eliminate ground loops)

**When to Replace Sensor**:
- Temperature reading incorrect after verifying PLC scaling, wiring, and power supply
- Temperature output stuck at 4 mA or 20 mA when actual temperature is within range
- Physical damage to sensor body or cable

---

**End of K25 Complete Technical Documentation**

For additional technical support, custom configurations, or product inquiries:

**Teklab S.r.l.**  
Email: info@teklab.it  
Web: www.teklab.it

---

*This unified documentation consolidates all technical information for the K25 ultra-high-pressure level switch with temperature sensor. For the latest product updates, certifications, and ordering information, please contact Teklab directly.*
