---
category: Sensors
keywords:
- ATEX
- Ex ia IIC T6
- intrinsically safe
- explosive atmosphere
- Zone 0 1 2
- NPN output
- level switch
- infrared technology
language: EN
product: ATEX
document_type: unified_complete
last_updated: 2025
---

# ATEX Ex ia Intrinsically Safe Level Switch - Complete Technical Documentation

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

The **ATEX Ex ia Electro-Optic Level Switch** is Teklab's certified intrinsically safe sensor designed for **explosive atmosphere applications** in petrochemical, oil & gas, offshore, and hazardous gas environments. With **Ex ia IIC T6...T4 Ga** certification, this sensor meets the strictest European safety standards for equipment used in Zone 0, 1, and 2 hazardous areas where explosive gases or vapors may be present.

Unlike standard industrial sensors, the ATEX model incorporates **intrinsic safety design** that limits electrical energy to levels incapable of igniting explosive atmospheres, even under fault conditions. This makes it the only choice when safety regulations mandate explosion-proof equipment.

### Key Positioning

| Feature | ATEX Advantage |
|---------|----------------|
| **Certification** | Ex ia IIC T6...T4 Ga (intrinsically safe for Zone 0/1/2) |
| **Safety Design** | Energy-limited electronics prevent ignition under all conditions |
| **Target Application** | Explosive atmospheres: petrochemical, offshore, hazardous gas |
| **Construction** | Stainless steel AISI 303/304/316L with fused glass dome |
| **Temperature Classes** | T6 (-20°C to +60°C), T5 (-20°C to +80°C), T4 (-20°C to +100°C) |

### Primary Applications

**Petrochemical & Refining:**
- **Crude Oil Storage**: Level monitoring in explosive Zone 1/2 tank farms
- **Gasoline/Diesel Tanks**: Flammable liquid storage with vapor explosion risk
- **Solvent Storage**: Chemical process vessels containing volatile organics
- **Separator Vessels**: Oil/gas/water separators in refineries

**Oil & Gas (Offshore/Onshore):**
- **Production Platforms**: Offshore oil/gas separation and storage
- **Wellhead Separators**: Level control in gas-liquid separators
- **Glycol Dehydration**: TEG (triethylene glycol) regeneration systems
- **Compressor Lubrication**: Oil reservoirs in hazardous gas areas

**Chemical Manufacturing:**
- **Explosive Atmospheres**: Process vessels with flammable vapor zones
- **Hazardous Gas Handling**: Storage tanks in Zone 1 classified areas
- **Pharmaceutical**: Solvent storage in explosive-rated facilities

**Industrial Gas:**
- **LPG/Propane Storage**: Liquefied petroleum gas tanks
- **Ammonia Refrigeration**: Ammonia (NH3) systems in Zone 2 areas

### Why ATEX?

**When to Choose ATEX:**
- Explosive atmosphere classification requires intrinsically safe equipment (Zone 0, 1, or 2)
- Petrochemical, oil & gas, offshore, or flammable gas applications
- Local safety regulations mandate ATEX/IECEx certification
- Hazardous area with Group IIC gases (most stringent group: hydrogen, acetylene)

**When to Consider Alternatives:**
- **K11**: If non-hazardous environment and pressure ≤60 bar (more output options, programmable timer)
- **K25**: If non-hazardous environment and pressure >60 bar or dual output (level + temperature) required

---

## 2. Detection Technology & Key Features

### Infrared Level Detection Principle

The ATEX sensor uses **electro-optic infrared detection** identical to other Teklab sensors, but with **intrinsically safe electronics** that limit energy to prevent ignition:

#### Operating Principle

1. **In Air (No Liquid)**:
   - Infrared LED emits low-energy light into **fused glass dome**
   - Light undergoes **total internal reflection** within glass (air refractive index ~1.0, glass ~1.5)
   - Reflected light returns to **optical receiver (phototransistor)**
   - High light intensity detected → Output remains in "air" state

2. **In Liquid (Liquid Contacts Dome)**:
   - Liquid covers glass dome (liquid refractive index ~1.3-1.5, similar to glass)
   - Light **refracts into liquid** instead of reflecting (refractive index matching)
   - Minimal light returns to receiver (~90% loss)
   - Low light intensity detected → Output switches to "liquid" state

3. **Intrinsic Safety**:
   - LED and receiver operate at **energy-limited levels** (Ui=30V, Ii=160mA, Pi=1.2W maximum)
   - Even under fault conditions (short circuit, component failure), energy remains below ignition threshold
   - **Certified safe** for Group IIC gases (hydrogen, acetylene - most easily ignited gases)

#### Advantages for Explosive Atmospheres

- **No Mechanical Parts**: Eliminates sparks from moving contacts, floats, or reeds
- **Solid-State Electronics**: No relays or switching contacts that could arc in explosive atmosphere
- **Energy-Limited Design**: Intrinsic safety certification ensures sub-ignition energy levels
- **Hermetically Sealed**: Fused glass dome prevents gas ingress into sensor electronics
- **No Hot Surfaces**: Low-power LED does not generate ignition-capable heat

### ATEX Certification Details

#### Certification Standard

- **Ex ia IIC T6...T4 Ga**: 
  - **Ex**: Explosive atmosphere equipment
  - **ia**: Intrinsic safety (energy limited under normal and fault conditions)
  - **IIC**: Gas Group IIC (hydrogen, acetylene - most sensitive group)
  - **T6...T4**: Temperature class (maximum surface temperature)
  - **Ga**: Equipment Protection Level (suitable for Zone 0, 1, 2)

#### Zone Classification Suitability

| Zone | Description | ATEX Sensor Suitability |
|------|-------------|------------------------|
| **Zone 0** | Explosive atmosphere present continuously or for long periods (>1000 hrs/year) | ✅ **Suitable** (Ex ia Ga certification) |
| **Zone 1** | Explosive atmosphere likely to occur occasionally during normal operation (10-1000 hrs/year) | ✅ **Suitable** (Ex ia Ga certification) |
| **Zone 2** | Explosive atmosphere unlikely, but if occurs, only briefly (<10 hrs/year) | ✅ **Suitable** (Ex ia Ga certification) |

#### Temperature Classes

Temperature class defines **maximum surface temperature** of sensor (critical to prevent ignition):

| Temp Class | Operating Range | Max Surface Temp | Gas Examples |
|------------|----------------|------------------|--------------|
| **T6** | -20°C to +60°C | +85°C | Carbon disulfide (CS2), ethyl nitrite |
| **T5** | -20°C to +80°C | +100°C | Gasoline, diesel vapor |
| **T4** | -20°C to +100°C | +135°C | Acetaldehyde, ethanol vapor |

**Selection**: Choose temperature class based on application's liquid/ambient temperature and required gas group classification.

### Intrinsic Safety Parameters

Critical electrical parameters for ATEX barrier/isolator selection:

| Parameter | Value | Description |
|-----------|-------|-------------|
| **Ui** | 30 V | Maximum input voltage (intrinsically safe) |
| **Ii** | 160 mA | Maximum input current (intrinsically safe) |
| **Pi** | 1.2 W | Maximum input power (intrinsically safe) |
| **Ci** | 140 pF/m | Cable capacitance per meter |
| **Li** | 1.25 µH/m | Cable inductance per meter |

**Critical**: When installing ATEX sensor, you must use **certified intrinsically safe barrier or galvanic isolator** in non-hazardous area to ensure sensor parameters (Ui, Ii, Pi) are not exceeded. Barrier selection must account for cable capacitance/inductance.

### Key Features Summary

#### Intrinsically Safe Design
- **Ex ia IIC T6...T4 Ga** certification for Zone 0/1/2
- **Energy-limited electronics** prevent ignition under all fault conditions
- **No hot surfaces** or spark-generating components
- **Group IIC compatibility** (most stringent gas group)

#### Solid-State Reliability
- **No Moving Parts**: Eliminates mechanical wear and spark sources
- **Infrared Technology**: Proven optical detection with 20+ years field history
- **Hermetically Sealed**: Fused glass dome prevents gas ingress
- **Long Service Life**: LED/receiver rated for 100,000+ hours

#### Robust Construction
- **Stainless Steel Body**: AISI 303, 304, or 316L (corrosion-resistant)
- **IP68 Rating**: Submersible 20 bar for 30 minutes (dust/water ingress protection)
- **Fused Glass Dome**: Chemically inert, compatible with oils, fuels, solvents
- **Wide Temperature Range**: -20°C to +100°C (depending on T-class selection)

#### Versatile Output
- **NPN Open Collector**: 40 mA maximum load current
- **Two Modes**: Normally Open (NO) or Normally Closed (NC) in air
- **PLC Compatible**: Standard digital input connection via safety barrier

#### Chemical Compatibility
- **Glass Sensing Element**: Compatible with petroleum products, solvents, oils, water, glycol
- **Stainless Steel Body**: AISI 316L option for corrosive chemicals (acids, seawater)

---

## 3. Technical Specifications

### Electrical Specifications

| Parameter | Specification |
|-----------|---------------|
| **Power Supply** | 9-28 Vdc (via intrinsically safe barrier) |
| **Output Type** | NPN open collector transistor |
| **Output Current** | 40 mA maximum load current |
| **Output Modes** | Normally Open (NO) or Normally Closed (NC) in air |
| **Intrinsic Safety Parameters** | Ui=30V, Ii=160mA, Pi=1.2W |
| **Cable Capacitance** | 140 pF/m (for barrier selection) |
| **Cable Inductance** | 1.25 µH/m (for barrier selection) |

### ATEX Certification

| Parameter | Specification |
|-----------|---------------|
| **Certification** | Ex ia IIC T6...T4 Ga |
| **Zone Suitability** | Zone 0, Zone 1, Zone 2 |
| **Gas Group** | IIC (hydrogen, acetylene - most sensitive) |
| **Temperature Classes** | T6 (-20°C to +60°C), T5 (-20°C to +80°C), T4 (-20°C to +100°C) |
| **Equipment Protection Level** | Ga (highest protection level) |

### Pressure & Environmental Ratings

| Parameter | Specification |
|-----------|---------------|
| **Pressure Rating** | 20 bar (IP68 for 30 min submersion) |
| **Temperature Range** | -20°C to +100°C (depending on T-class: T6/T5/T4) |
| **IP Rating** | IP68 (dust-tight, submersible) |
| **Level Repeatability** | ±2 mm (±0.08") |

### Mechanical Specifications

| Parameter | Specification |
|-----------|---------------|
| **Overall Dimensions** | ~80 mm length × Ø18 mm diameter (typical) |
| **Body Material** | Stainless Steel AISI 303, 304, or 316L |
| **Sensing Element** | Fused glass dome (hemispherical, chemically inert) |
| **Thread Options** | NPT (3/8" to 3/4"), GAS (3/8" to 3/4"), UNEF (5/8"-24 to 1" 1/8-18), ISO Metric (M18 to M30) |
| **Tightening Torque** | 15 N·m (11 lb-ft) recommended |
| **Cable Connection** | Pre-wired cable (intrinsically safe certified cable required) |
| **Weight** | Approx. 200 g (depending on thread/cable) |

### Fluid Compatibility

| Fluid Type | Compatibility |
|------------|---------------|
| **Petroleum Products** | Crude oil, gasoline, diesel, kerosene, jet fuel |
| **Solvents** | Acetone, ethanol, toluene, xylene, methanol |
| **Refrigerants** | Ammonia (NH3), R134a, R404A, CO2 (if temperature permits) |
| **Oils** | Mineral oil, synthetic oil, hydraulic oil |
| **Glycols** | Ethylene glycol, propylene glycol, TEG (triethylene glycol) |
| **Water** | Fresh, seawater (use AISI 316L for seawater) |

**Corrosive Fluids**: For strong acids/bases or highly corrosive chemicals, specify AISI 316L body material.

### Ordering Codes - T6 Temperature Class Examples

#### AISI 304 Housing - Normally Open (NO) in Air

| Thread Type | Code Number | Application |
|-------------|-------------|-------------|
| 3/4" NPT | 51244001001400 | North America standard |
| 1/2" NPT | 51249001001400 | Compact installations |
| 1" 1/8-18 UNEF | 5124B001001400 | Refrigeration industry standard |

#### AISI 304 Housing - Normally Closed (NC) in Air

| Thread Type | Code Number | Application |
|-------------|-------------|-------------|
| 3/4" NPT | 51254001001400 | Fail-safe high-level alarm |
| 1/2" NPT | 51259001001400 | Compact fail-safe installations |
| 1" 1/8-18 UNEF | 5124C001001400 | Refrigeration fail-safe |

**Note**: Codes shown are T6 temperature class (-20°C to +60°C) with AISI 304 body. Other temperature classes (T5, T4) and materials (AISI 303, 316L) available on request.

### Custom Options

**Temperature Class Selection:**
- T6 (-20°C to +60°C) - coldest environments, most gas compatibility
- T5 (-20°C to +80°C) - moderate temperature applications
- T4 (-20°C to +100°C) - high-temperature applications

**Housing Material Selection:**
- AISI 303 - standard industrial applications
- AISI 304 - general corrosion resistance (most common)
- AISI 316L - superior corrosion resistance (seawater, acids)

**Thread Customization:**
- NPT (3/8", 1/2", 3/4", or custom sizes)
- GAS cylindrical or conical (3/8", 1/2", 3/4")
- UNEF (5/8"-24, 7/8"-20, 1" 1/8-18)
- ISO Metric (M18, M20, M22, M24, M27, M30)

---

## 4. Applications & Selection Guide

### Primary Application: Explosive Atmosphere Environments

The ATEX sensor is **mandatory** when safety regulations classify installation area as explosive atmosphere (Zone 0, 1, or 2).

#### Petrochemical & Refining

**Crude Oil Tank Farms (Zone 1/2):**
- **Challenge**: Crude oil storage tanks have flammable vapor space classified Zone 1 (vapor likely during normal operation) or Zone 2 (vapor unlikely)
- **ATEX Solution**: Intrinsically safe sensor monitors oil level without ignition risk; NPN output signals level to DCS via safety barrier
- **Configuration**: Normally Open (NO) output for low-level alarm; T5 or T6 temperature class depending on ambient

**Gasoline/Diesel Storage (Zone 1):**
- **Challenge**: Gasoline vapor is highly flammable (Zone 1 classification); standard sensors prohibited
- **ATEX Solution**: Ex ia certification allows installation in vapor space; fused glass dome compatible with petroleum products
- **Configuration**: Normally Closed (NC) output for high-level alarm (fail-safe: sensor power loss triggers alarm); T6 temperature class for gasoline vapor (low ignition energy)

**Solvent Recovery Systems (Zone 1/2):**
- **Challenge**: Chemical process vessels contain volatile organic compounds (acetone, toluene, ethanol) with explosive vapor
- **ATEX Solution**: Intrinsically safe design prevents ignition even if sensor fails internally (short circuit, component failure)
- **Configuration**: T6 temperature class for most solvents; AISI 316L body for corrosive solvents

#### Oil & Gas (Offshore/Onshore)

**Offshore Production Platforms (Zone 1/2):**
- **Challenge**: Offshore separators and storage vessels operate in Zone 1 hazardous areas (natural gas, condensate)
- **ATEX Solution**: IP68 rating handles harsh marine environment; stainless steel body resists saltwater corrosion
- **Configuration**: AISI 316L body for seawater exposure; T5 temperature class for warm offshore climates; Normally Closed (NC) for fail-safe operation

**Wellhead Gas-Liquid Separators (Zone 1):**
- **Challenge**: High-pressure separators (up to 20 bar) in gas field areas with methane/propane vapor
- **ATEX Solution**: 20 bar pressure rating adequate for separator applications; Group IIC certification covers natural gas (methane is Group IIA, but IIC certification is more stringent and therefore compatible)
- **Configuration**: Normally Open (NO) output for liquid level control; T5 or T6 depending on climate

**Glycol Dehydration Units (Zone 2):**
- **Challenge**: TEG (triethylene glycol) regeneration systems have occasional explosive vapor (Zone 2)
- **ATEX Solution**: Cost-effective intrinsically safe solution for Zone 2 (less stringent than Zone 1); glass dome compatible with glycol
- **Configuration**: T4 temperature class (TEG regenerators operate at 80-100°C); Normally Open (NO) for glycol level control

**Compressor Oil Reservoirs (Zone 2):**
- **Challenge**: Gas compressor lubrication systems may have explosive atmosphere during upset conditions
- **ATEX Solution**: Intrinsically safe design ensures compliance in gas compressor buildings
- **Configuration**: Normally Closed (NC) for low-level alarm (fail-safe compressor protection)

#### Chemical Manufacturing

**Explosive-Rated Process Vessels (Zone 1):**
- **Challenge**: Chemical reactors or storage tanks containing flammable intermediates (explosive atmosphere classified)
- **ATEX Solution**: Ex ia Ga certification allows installation in Zone 1 areas; compatible with most organic solvents
- **Configuration**: AISI 316L body for corrosive chemicals; T6/T5/T4 depending on process temperature

**Pharmaceutical Solvent Storage (Zone 2):**
- **Challenge**: Pharmaceutical manufacturing uses ethanol, methanol, isopropanol (flammable solvents) in explosive-rated facilities
- **ATEX Solution**: Intrinsically safe sensor meets GMP (Good Manufacturing Practice) requirements for pharma equipment
- **Configuration**: T6 temperature class for ethanol vapor; AISI 304 or 316L depending on cleaning chemicals used

#### Industrial Gas & Refrigeration

**LPG/Propane Storage (Zone 1/2):**
- **Challenge**: Liquefied petroleum gas tanks have flammable vapor space (propane/butane)
- **ATEX Solution**: Intrinsically safe sensor monitors liquid level without ignition risk; low-temperature capability handles refrigerated LPG (-40°C)
- **Configuration**: T6 temperature class (propane has low ignition temperature); Normally Closed (NC) for high-level fail-safe alarm

**Ammonia Refrigeration (Zone 2):**
- **Challenge**: Large industrial ammonia systems may have Zone 2 classification in compressor rooms or equipment areas
- **ATEX Solution**: Intrinsically safe design meets ammonia system safety requirements; stainless steel compatible with dry ammonia
- **Configuration**: T5 or T6 temperature class; AISI 304 body for dry ammonia (upgrade to 316L if wet ammonia or seawater exposure)

### ATEX vs. Alternative Sensors - Selection Guide

#### Compare: ATEX, K11, K25

| Feature | ATEX | K11 | K25 |
|---------|------|-----|-----|
| **ATEX Certification** | **Ex ia IIC T6...T4 Ga (Yes)** | No | No |
| **Zone Suitability** | **Zone 0/1/2** | Non-hazardous only | Non-hazardous only |
| **Working Pressure** | 20 bar (IP68) | 60 bar | 150 bar |
| **Temperature Range** | -20°C to +100°C (T-class dependent) | -40°C to +125°C | -40°C to +125°C |
| **Output Type** | NPN 40mA (via barrier) | NPN/PNP/24VAC relay | NPN 50mA + 4-20mA temp |
| **Output Current** | 40 mA max | 100 mA (NPN/PNP) or 2A (relay) | 50 mA (level) |
| **Programmable Timer** | No | Yes | Yes |
| **Dual Output (Level+Temp)** | No | No | Yes (4-20mA temp) |
| **Body Material** | AISI 303/304/316L | Stainless/nickel-plated | Nickel-plated steel |
| **Dimensions** | ~80mm × Ø18mm | 59mm × Ø27mm | 90mm × Ø20mm |
| **Primary Application** | Explosive atmospheres | Compact high-pressure | Ultra-high-pressure CO2 |
| **Key Advantage** | Intrinsically safe certification | Smallest + programmable timer | Highest pressure + dual output |

#### Decision Matrix

**Choose ATEX when:**
- ✅ **Mandatory**: Installation area classified as explosive atmosphere (Zone 0, 1, or 2)
- ✅ Petrochemical, oil & gas, offshore, or flammable gas/vapor applications
- ✅ Local safety regulations require ATEX/IECEx certification (Europe, Middle East, Asia)
- ✅ Explosive gas Group IIC present (hydrogen, acetylene) or any lower group (IIB, IIA)
- ✅ Pressure ≤20 bar (ATEX pressure rating)

**Choose K11 when:**
- ✅ Non-hazardous environment (no explosive atmosphere classification)
- ✅ Pressure ≤60 bar (K11 rating higher than ATEX)
- ✅ Programmable timer required (ATEX does not have timer)
- ✅ Multiple output options needed (NPN, PNP, or 24VAC relay - ATEX only has NPN)
- ✅ Compact installation (K11 is smallest Teklab sensor)

**Choose K25 when:**
- ✅ Non-hazardous environment and pressure >60 bar (up to 150 bar)
- ✅ Dual output required (level NPN + temperature 4-20mA in one sensor)
- ✅ CO2 transcritical refrigeration (150 bar high-pressure side)
- ✅ Temperature monitoring critical for system optimization or safety

### Intrinsically Safe Barrier Selection

**Critical**: ATEX sensor **must** be powered through certified intrinsically safe barrier or galvanic isolator in non-hazardous area to ensure intrinsic safety parameters (Ui, Ii, Pi) are not exceeded.

#### Barrier Requirements

**Barrier Output Must Meet:**
- **Uo** (barrier output voltage) ≤ **Ui** (sensor input voltage) = **30V**
- **Io** (barrier output current) ≤ **Ii** (sensor input current) = **160mA**
- **Po** (barrier output power) ≤ **Pi** (sensor input power) = **1.2W**
- **Co + Ccable** (total capacitance) ≤ barrier's **maximum allowable capacitance**
- **Lo + Lcable** (total inductance) ≤ barrier's **maximum allowable inductance**

**Cable Considerations:**
- Sensor cable: **Ci = 140 pF/m**, **Li = 1.25 µH/m**
- For 50m cable run: **Ccable = 50m × 140 pF/m = 7000 pF (7 nF)**, **Lcable = 50m × 1.25 µH/m = 62.5 µH**
- Select barrier with sufficient capacitance/inductance margin

#### Example Barrier Calculation

**Application**: ATEX sensor in 50m cable run, 24V PLC digital input

**Step 1**: Calculate total cable parameters
- Ccable = 50m × 140 pF/m = 7000 pF
- Lcable = 50m × 1.25 µH/m = 62.5 µH

**Step 2**: Select barrier (example: MTL7728+ Zener barrier)
- Uo = 28V (≤ Ui = 30V ✓)
- Io = 93mA (≤ Ii = 160mA ✓)
- Po = 0.65W (≤ Pi = 1.2W ✓)
- Max Co = 0.8 µF (= 800 nF > 7 nF ✓)
- Max Lo = 10 mH (> 62.5 µH ✓)

**Step 3**: Verify barrier certified for Zone 0/1/2 (Ex ia IIC certification)

**Wiring**:
```
PLC (Non-Hazardous Area)          ATEX Sensor (Hazardous Area Zone 1)
┌──────────────┐                  ┌──────────────┐
│ +24V Supply  ├─► Barrier IN(+) ──► OUT(+) ─────► Brown (+9-28Vdc)
│ Digital Input├─► Barrier IN(-) ──► OUT(-) ─────► Black (NPN output)
│ Ground       ├─► Barrier GND ────► GND ────────► Blue (0V)
└──────────────┘    (MTL7728+)                    └──────────────┘
                    Earth Ground
```

**Consult Barrier Manufacturer**: Provide sensor intrinsic safety parameters (Ui, Ii, Pi, Ci, Li) and cable length for barrier compatibility verification.

---

## 5. Installation & Service Guidelines

### Pre-Installation ATEX Requirements

**ATEX Installation Regulations (Critical):**

1. **Qualified Personnel**: ATEX installations must be performed by personnel trained and certified in hazardous area installation practices
2. **Hot Work Permit**: If welding/cutting required for sensor boss installation, obtain hot work permit and ensure area gas-free
3. **Installation Documentation**: Maintain records of sensor serial number, barrier type, cable length, and Zone classification
4. **Local Safety Authority**: Consult local safety regulations (ATEX in Europe, IECEx internationally, NEC in USA/Canada) for specific requirements

**Verify Application Compliance:**
- ✅ Installation area Zone classification (0, 1, or 2) matches sensor Ga rating
- ✅ Gas group present is IIC or lower (IIB, IIA - sensor is IIC-certified, suitable for all groups)
- ✅ Temperature class (T6/T5/T4) adequate for gas present (check gas auto-ignition temperature)
- ✅ Intrinsically safe barrier selected and certified for sensor parameters (Ui, Ii, Pi, Ci, Li)

### Mechanical Installation

#### Mounting Location Selection

**Explosive Atmosphere Considerations:**

1. **Avoid Ignition Sources**: Install sensor away from other potential ignition sources (even though sensor is intrinsically safe, minimize cumulative risk)
2. **Representative Level**: Choose location where liquid level accurately reflects tank/vessel condition (avoid turbulent zones)
3. **Accessibility**: Ensure access for maintenance while minimizing entry into Zone 0 areas (prefer Zone 2 installation points if level monitoring permits)
4. **Vapor Space**: If mounting in vapor space (above liquid), ensure sensor exposure to explosive gas mixture does not exceed rated temperature class limits

#### Thread Installation Procedure

**Step 1: Thread Preparation**
- Ensure tank/vessel is **gas-free and depressurized** (verify with gas detector before starting)
- Clean threads in boss (remove metal chips, old sealant)
- Inspect threads for damage

**Step 2: Thread Sealant Selection (Critical for ATEX)**
- Use **PTFE tape** or **thread sealant paste** compatible with:
  - System fluid (oil, fuel, solvent)
  - Explosive atmosphere (no sealants that outgas flammable vapors)
  - ATEX requirements (some jurisdictions prohibit certain sealants in Zone 0)
- Apply sealant without allowing material into sensor tip (keep away from first 2 threads)

**Step 3: Sensor Installation**
- Hand-tighten sensor into boss
- Use wrench on hexagonal body (typically 27mm hex)
- **Torque**: **15 N·m (11 lb-ft)** recommended (max 20 N·m - do NOT exceed)

**Step 4: Cable Routing (ATEX-Specific)**
- Route cable in **certified cable tray or conduit** per ATEX installation code
- Use **cable glands rated for ATEX** (e.g., EEx e certified glands for cable entry into junction boxes)
- Ensure cable protected from mechanical damage (abrasion, impact)
- Maintain **minimum bend radius**: 10× cable diameter

**Step 5: Grounding/Bonding**
- Ensure **tank/vessel is properly grounded** (prevents static electricity accumulation)
- If sensor body requires bonding, follow local ATEX grounding requirements
- Barrier in non-hazardous area must be connected to **earth ground** (intrinsic safety circuit reference)

### Electrical Installation (ATEX-Specific)

#### Intrinsically Safe Wiring Requirements

**Cable Selection:**
- Use cable with **capacitance ≤140 pF/m** and **inductance ≤1.25 µH/m** (or account for higher values in barrier selection)
- Cable must be **rated for temperature class** of installation (e.g., T6 requires cable rated for 85°C maximum surface temp)
- **Blue cable** (IEC standard for intrinsically safe circuits) recommended but not mandatory if properly labeled

**Barrier Location:**
- Install barrier in **non-hazardous area** (outside Zone 0/1/2 boundary)
- Mount barrier in **accessible location** for inspection and maintenance
- Barrier must be **earth-grounded** (critical for intrinsic safety)

**Wiring Connections:**

```
NON-HAZARDOUS AREA                 HAZARDOUS AREA (Zone 1)
┌────────────────────┐            ┌─────────────────────┐
│ PLC / Controller   │            │ ATEX Sensor         │
│                    │            │                     │
│ +24V DC ────►──────┼──┐         │                     │
│                    │  │         │                     │
│ Digital Input ─►───┼──┼───┐     │                     │
│                    │  │   │     │                     │
│ Ground ────►───────┼──┼───┼──┐  │                     │
└────────────────────┘  │   │  │  │                     │
                        │   │  │  │                     │
                    ┌───▼───▼──▼──┐│                     │
                    │ IS Barrier  ││                     │
                    │ (e.g.       ││                     │
                    │ MTL7728+)   ││                     │
                    │             ││                     │
                    │ IN(+) OUT(+)├┼──Blue Cable──►Brown─┤ (+9-28Vdc)
                    │ IN(-) OUT(-)├┼──Blue Cable──►Black─┤ (NPN Output)
                    │ GND   GND   ├┼──Blue Cable──►Blue──┤ (0V Ground)
                    └─────────────┘│                     │
                         │          │                     │
                    Earth Ground    └─────────────────────┘
                    (Safety Critical)
```

**NPN Output Wiring (via Barrier):**

```
Barrier Output (+) ──┬──► PLC Digital Input (+) (10kΩ pull-up to barrier voltage)
                     │
                     └──► Black Wire (NPN Collector from ATEX Sensor)
                          │
                          │  When LIQUID: NPN conducts → Digital input sees LOW (0V)
                          │  When AIR: NPN off → Digital input sees HIGH (via pull-up)
                          │
                         Blue Wire (GND from ATEX Sensor) ──► Barrier Output (-)
```

**Critical ATEX Wiring Rules:**

1. **No Galvanic Connection**: Intrinsically safe circuit (hazardous area) and non-IS circuit (safe area) must be **isolated** by barrier (no direct connection)
2. **Cable Segregation**: IS cables (blue) must be **separated from non-IS cables** in cable trays (minimum 50mm spacing or physical barrier)
3. **Labeling**: All IS cables must be **labeled "Intrinsically Safe"** or "IS Circuit" at both ends
4. **No Field Modifications**: Do NOT splice, extend, or modify IS cable without recalculating capacitance/inductance and verifying barrier compatibility
5. **Earth Ground**: Barrier earth ground is **safety-critical** - do NOT omit or use high-resistance ground connection

### Commissioning & Testing (ATEX-Specific)

#### Pre-Energization Checks

**Step 1: Documentation Review**
- Verify sensor certification matches Zone classification (Ex ia IIC T6...T4 Ga for Zone 0/1/2)
- Verify temperature class (T6/T5/T4) adequate for gas present in area
- Verify barrier certification and compatibility with sensor parameters

**Step 2: Visual Inspection**
- Check sensor installation torque (15 N·m)
- Inspect cable routing (no damage, proper gland seals, blue cable segregated from non-IS cables)
- Verify barrier earth ground connection (low resistance to earth)
- Check cable length does not exceed barrier's maximum allowable capacitance/inductance

**Step 3: Electrical Continuity Test**
- **With sensor disconnected from barrier**:
  - Measure resistance Brown-to-Blue: Should read >1 MΩ (power supply insulation)
  - Measure resistance Black-to-Blue: Should read open circuit or high resistance (NPN output in "off" state)
- If low resistance detected, check for cable short circuit or sensor damage

**Step 4: Gas Detection (Before Energization)**
- Use **gas detector** to verify explosive atmosphere concentration in installation area
- If gas concentration >25% LEL (Lower Explosive Limit), **do NOT energize** sensor until area is purged and gas-free
- Even though sensor is intrinsically safe, minimize energization during high gas concentration as best practice

#### Functional Testing

**Step 1: Power-Up Test**
- Energize barrier from PLC/controller (+24V supply)
- Measure voltage at sensor (Brown to Blue): Should read 9-28 Vdc (voltage drop across barrier is normal)
- Verify current consumption <40 mA (within intrinsic safety limit Ii=160mA)

**Step 2: NPN Output Test - In Air**
- Sensor tip in air (no liquid):
  - **NO mode**: PLC digital input reads HIGH (barrier output voltage via pull-up)
  - **NC mode**: PLC digital input reads LOW (~0V)

**Step 3: NPN Output Test - In Liquid**
- Submerge sensor tip in test liquid (if accessible) or wait for process liquid to reach sensor:
  - **NO mode**: PLC digital input switches to LOW (~0V) - confirms liquid detection
  - **NC mode**: PLC digital input switches to HIGH - confirms liquid detection
- **Repeatability Check**: Remove sensor from liquid, resubmerge → Output should switch consistently at same level (±2mm)

**Step 4: System Integration Test**
- Verify PLC/DCS logic responds correctly to sensor output (alarm triggers, pump control, etc.)
- Test fail-safe behavior (if NC mode): Disconnect sensor power → Verify alarm triggers (fail-safe to alarm condition)

### Maintenance & Service (ATEX-Specific)

#### Routine Maintenance

**Annual Inspection (Mandatory for ATEX):**

1. **Certification Verification**: Check sensor nameplate for ATEX marking (Ex ia IIC T6...T4 Ga) - ensure marking legible
2. **Visual Inspection**: 
   - Check cable for damage (abrasion, cuts, chemical attack)
   - Inspect cable glands for seal integrity (gas ingress prevention)
   - Verify barrier earth ground connection (low resistance)
3. **Thread Inspection**: Check for fluid leaks at sensor threads (especially critical in flammable liquid tanks)
4. **Glass Dome Inspection**: Inspect sensing tip for cracks, heavy contamination (if accessible during turnaround/maintenance)

**Cleaning (if required):**
- **Isolate & Gas-Free**: Before removing sensor, ensure tank/vessel is **gas-free** (gas detector verification) and **depressurized**
- **Hot Work Permit**: If area still classified (not gas-free), obtain permit before sensor removal
- **Remove Sensor**: Unscrew sensor from boss
- **Clean Glass Dome**: Use **isopropyl alcohol (IPA)** and soft cloth (no abrasive cleaners)
- **Reinstall**: Apply fresh thread sealant (ATEX-approved), torque to 15 N·m

#### Troubleshooting (ATEX Context)

**Problem: Output Not Switching (Stuck HIGH or LOW)**

| Symptom | Possible Cause | Solution |
|---------|---------------|----------|
| Output stuck (NO mode: HIGH, NC mode: LOW) | - Glass dome contaminated<br>- Sensor internal fault<br>- Cable damage | - Clean glass dome (see cleaning procedure)<br>- Check cable continuity (Brown-Blue, Black-Blue)<br>- Replace sensor if fault persists |
| Output stuck (opposite of expected) | - Incorrect sensor mode (NO vs. NC)<br>- Wiring error | - Verify sensor ordered as NO or NC (check nameplate)<br>- Check wiring: Black wire to barrier output(-) via digital input |
| Intermittent output | - Loose cable connection<br>- Barrier malfunction<br>- Gas detector alarm (if integrated) | - Check cable terminations at barrier and sensor<br>- Test barrier (disconnect sensor, check barrier output voltage)<br>- Verify no gas alarm interfering with IS circuit |

**Problem: No Power to Sensor (0V at Brown-Blue)**

| Symptom | Possible Cause | Solution |
|---------|---------------|----------|
| 0V at sensor | - Barrier not energized<br>- Cable open circuit<br>- Barrier fuse blown | - Check PLC +24V supply to barrier input<br>- Measure voltage at barrier output (should read barrier Uo, e.g., 28V)<br>- If voltage at barrier OK, check cable continuity Brown-to-Blue<br>- Replace barrier fuse if blown (investigate cause: short circuit in cable?) |

**Problem: Gas Detector Alarm in Sensor Area**

**Action**: 
1. **Do NOT remove or service sensor** while explosive atmosphere present (wait for area to be purged gas-free)
2. Sensor is intrinsically safe → Can remain energized during gas presence (will not ignite gas)
3. After area gas-free, inspect sensor for damage or leak at threads (may be source of gas release)

#### Replacement Procedure (ATEX-Specific)

**When to Replace:**
- Glass dome cracked or damaged (cannot be repaired)
- Internal fault confirmed (output failure after troubleshooting)
- Certification expired or damaged nameplate (sensor cannot be re-certified in field)
- After major incident (fire, explosion, chemical exposure) - replace as precaution even if functional

**Replacement Steps:**

1. **Obtain Hot Work Permit** (if required) and ensure area **gas-free** (gas detector verification <10% LEL)
2. **De-energize**: Disconnect sensor from barrier (or isolate barrier power) and lockout/tagout
3. **Depressurize**: Release pressure from tank/vessel at sensor installation point
4. **Remove Old Sensor**: Unscrew sensor (note installation depth/orientation)
5. **Install New Sensor**: 
   - Verify **new sensor certification** matches Zone/Gas Group/Temp Class requirements (check nameplate: Ex ia IIC T6...T4 Ga)
   - Apply ATEX-approved thread sealant, install, torque to 15 N·m
6. **Reconnect Wiring**: Connect cable to barrier (verify cable length/capacitance/inductance unchanged)
7. **Commission**: Power-up test, functional test (in air / in liquid), system integration test
8. **Documentation**: Update maintenance records (sensor serial number, installation date, barrier verification)

**Disposal:**
- Dispose according to local WEEE regulations (electronic components)
- If sensor contaminated with hazardous chemicals, follow hazardous waste disposal procedures

---

## 6. Frequently Asked Questions

### Q1: What is ATEX certification and why is it mandatory for my application?

**ATEX** (ATmosphères EXplosibles) is the **European regulatory framework** for equipment used in explosive atmospheres. If your installation area is classified as **Zone 0, 1, or 2** (explosive gas/vapor present), local safety regulations **mandate** ATEX-certified equipment to prevent ignition and explosion.

The **Ex ia IIC T6...T4 Ga** certification means this sensor is **intrinsically safe**—its electronics are energy-limited to levels that cannot ignite explosive gases, even under fault conditions (short circuit, component failure). This makes it the **only legal choice** for level monitoring in explosive atmosphere areas.

**Non-Compliance Risk**: Installing non-ATEX sensor in explosive atmosphere violates safety regulations, voids insurance, and creates catastrophic explosion risk. Always verify Zone classification with safety engineer before sensor selection.

---

### Q2: What do the ATEX markings "Ex ia IIC T6...T4 Ga" mean?

**Breakdown of Certification Code:**

- **Ex**: Equipment for explosive atmospheres
- **ia**: Intrinsic safety (energy limited under normal AND fault conditions - highest safety level)
- **IIC**: Gas Group IIC (most sensitive gases: hydrogen, acetylene - sensor suitable for ALL gas groups)
- **T6...T4**: Temperature class range:
  - **T6**: Max surface temp +85°C (operating range -20°C to +60°C)
  - **T5**: Max surface temp +100°C (operating range -20°C to +80°C)
  - **T4**: Max surface temp +135°C (operating range -20°C to +100°C)
- **Ga**: Equipment Protection Level "a" (suitable for Zone 0, 1, and 2 - highest protection level)

**Practical Meaning**: This sensor can be installed in **any explosive atmosphere zone** (0/1/2) with **any gas group** (IIC/IIB/IIA), as long as temperature class (T6/T5/T4) is compatible with gas auto-ignition temperature.

---

### Q3: How do I choose the correct temperature class (T6, T5, or T4)?

**Temperature Class Selection Rule**: Choose T-class such that **maximum surface temperature** is **at least 20°C below auto-ignition temperature** of explosive gas present.

**Step 1**: Identify gas in your application (example: methane, gasoline vapor, hydrogen)

**Step 2**: Look up gas auto-ignition temperature:
- **Methane (natural gas)**: 595°C (T1 gas)
- **Gasoline vapor**: 280-456°C (T3 gas)
- **Hydrogen**: 560°C (T1 gas)
- **Acetylene**: 305°C (T2 gas)
- **Ethanol**: 363°C (T2 gas)

**Step 3**: Match sensor temperature class to gas:
- **T6** (surface max +85°C): Safe for ALL gases (most conservative choice)
- **T5** (surface max +100°C): Safe for T1-T5 gases (most common industrial gases)
- **T4** (surface max +135°C): Safe for T1-T4 gases (excluding only T5/T6 gases like carbon disulfide)

**Step 4**: Verify operating temperature in application:
- If liquid/ambient temp >+60°C, **cannot use T6** (exceeds T6 operating range -20°C to +60°C)
- If liquid/ambient temp >+80°C, **cannot use T5** (exceeds T5 operating range)
- If liquid/ambient temp >+100°C, **cannot use T4 or ATEX sensor** (exceeds all T-class ranges)

**Recommendation**: If uncertain, choose **T6** (safest, compatible with all gases) unless application temperature >+60°C.

---

### Q4: What is an intrinsically safe barrier and why is it required?

An **intrinsically safe barrier** (also called "Zener barrier" or "galvanic isolator") is a device installed in the **non-hazardous area** that **limits voltage, current, and power** supplied to the ATEX sensor, ensuring energy remains below ignition threshold even under fault conditions.

**Why Required**:
- PLC/controller operates at **24V DC** (potentially above intrinsic safety limit Ui=30V under fault)
- Without barrier, sensor could receive excessive energy → Could ignite explosive gas under fault (short circuit, insulation breakdown)
- Barrier ensures sensor **never exceeds Ui=30V, Ii=160mA, Pi=1.2W** → Intrinsically safe under all conditions

**How It Works**:
- **Normal Operation**: Barrier passes voltage/current to sensor (with small voltage drop)
- **Fault Condition**: If sensor short-circuits or overvoltage occurs, barrier's Zener diodes clamp voltage to safe level and current-limiting resistor prevents excessive current
- **Galvanic Isolation**: Barrier isolates hazardous area circuit from non-hazardous area circuit (prevents fault propagation)

**Barrier Selection**: Provide barrier manufacturer with sensor parameters (Ui, Ii, Pi, Ci, Li) and cable length → Manufacturer confirms barrier compatibility.

---

### Q5: Can I use the ATEX sensor without a barrier if my PLC is only 12V DC?

**No, barrier is still required** even at 12V DC. Here's why:

1. **Fault Condition Protection**: Intrinsic safety certification assumes **worst-case faults** (e.g., PLC power supply fails to 30V, sensor internal short circuit). Barrier provides protection under these fault scenarios, not just normal operation.

2. **Regulatory Requirement**: ATEX installation codes **mandate intrinsically safe barrier** for all ia circuits, regardless of normal operating voltage. Omitting barrier voids ATEX certification and violates safety regulations.

3. **Cable Capacitance/Inductance**: Long cables store energy (capacitance stores voltage energy, inductance stores current energy). Barrier accounts for this stored energy and prevents it from being released in hazardous area as spark.

**Exception**: If you use a **PLC with intrinsically safe outputs** (e.g., PLC is itself Ex ia certified), then external barrier may not be required—but PLC's intrinsically safe parameters (Uo, Io, Po) must still be compatible with sensor (Ui, Ii, Pi). Most standard PLCs are NOT intrinsically safe and require external barriers.

---

### Q6: What is the difference between Normally Open (NO) and Normally Closed (NC) modes in ATEX applications?

**Normally Open (NO) in Air:**
- Output contact **open (non-conducting) when sensor in air**
- Output contact **closes (conducts) when liquid detected**
- **Use Case**: Low-level alarm ("add liquid when contact closes"), pump start control

**Normally Closed (NC) in Air:**
- Output contact **closed (conducting) when sensor in air**
- Output contact **opens (non-conducts) when liquid detected**
- **Use Case**: High-level alarm ("stop filling when contact opens"), **fail-safe design**

**Fail-Safe Consideration (Critical for ATEX)**:

In explosive atmosphere applications, **fail-safe design** is critical:

- **NC Mode Advantage**: If sensor loses power, cable is cut, or sensor fails, output opens → PLC detects fault and triggers alarm
- **NO Mode Risk**: If sensor loses power, output remains open → PLC cannot distinguish between "no liquid" and "sensor failure"

**Recommendation for ATEX**: Use **Normally Closed (NC) mode** for critical safety alarms (high-level alarm to prevent overfill, low-level alarm to prevent pump dry-run) to ensure fail-safe operation.

---

### Q7: Can the ATEX sensor be used in Zone 0 areas?

**Yes!** The **Ex ia IIC T6...T4 Ga** certification includes **Equipment Protection Level Ga**, which is suitable for **Zone 0** (explosive atmosphere present continuously or for long periods >1000 hrs/year).

**Zone 0 is the most stringent** explosive atmosphere classification. Most ATEX equipment is only certified for Zone 1 or Zone 2 (lower protection levels Gb or Gc). The ATEX sensor's **Ga rating** makes it suitable for all zones (0, 1, 2), providing maximum flexibility.

**Zone 0 Examples**:
- Inside storage tanks containing gasoline, diesel, or solvents (vapor space above liquid)
- Confined spaces with continuous flammable gas release
- Vapor recovery units with constant explosive atmosphere

**Installation Note**: Zone 0 installations have **additional requirements** beyond sensor certification (e.g., cable glands, junction boxes, barriers must all be Zone 0-rated). Consult local ATEX installation codes and safety engineer.

---

### Q8: Is the ATEX sensor compatible with ammonia (NH3) refrigeration?

**Yes, with considerations:**

**Materials Compatibility:**
- **Glass Dome**: Chemically inert, fully compatible with ammonia
- **Stainless Steel Body**: AISI 304 or 316L compatible with dry ammonia (moisture-free systems)
- **Dry Ammonia**: Does not significantly corrode stainless steel
- **Wet Ammonia**: If moisture or air present, ammonia can cause stress corrosion cracking over time → Use AISI 316L body for wet ammonia applications

**ATEX Classification:**
- **Ammonia Gas Group**: Ammonia (NH3) is Group IIA gas (less sensitive than Group IIC)
- **Sensor Compatibility**: ATEX sensor is certified for Group IIC (most stringent) → Compatible with Group IIA ammonia

**Pressure Compatibility:**
- Ammonia systems typically 10-25 bar → Within ATEX sensor's 20 bar IP68 rating

**Temperature Class**:
- Ammonia refrigeration operates -40°C to +40°C → Use T6 or T5 temperature class (both adequate)

**Zone Classification**: Large industrial ammonia systems may have Zone 2 classification in compressor rooms or equipment areas (ammonia release possible during maintenance) → ATEX sensor required.

---

### Q9: What cable length is allowed for ATEX sensor installation?

**Cable length is limited by barrier's maximum allowable capacitance and inductance**, not by sensor itself.

**Calculation Example**:

**Sensor Cable Parameters**:
- Ci = 140 pF/m (capacitance per meter)
- Li = 1.25 µH/m (inductance per meter)

**Example Barrier** (MTL7728+):
- Maximum allowable capacitance: Co = 0.8 µF (800 nF)
- Maximum allowable inductance: Lo = 10 mH

**Maximum Cable Length**:
- By capacitance: Cable_length_max = Co / Ci = 800,000 pF / 140 pF/m = **5714 meters** (capacitance limit)
- By inductance: Cable_length_max = Lo / Li = 10,000 µH / 1.25 µH/m = **8000 meters** (inductance limit)
- **Practical Limit**: **5714 meters** (limited by capacitance for this barrier)

**Real-World Constraints**:
- Most ATEX installations use **50-100m cable** (well within barrier limits)
- For very long cables (>500m), verify barrier compatibility before installation
- Voltage drop in cable may reduce sensor supply voltage at long distances (check voltage at sensor is ≥9 Vdc)

**If Cable Too Long**: Use **galvanic isolator** (higher capacitance/inductance tolerance than Zener barrier) or install **repeater barrier** at intermediate point.

---

### Q10: How do I troubleshoot false alarms or intermittent output in ATEX sensor?

**Step-by-Step Troubleshooting**:

**Problem: Intermittent Output (Random Switching)**

**Step 1: Check for Electrical Noise**
- **Symptom**: Output switches randomly without corresponding liquid level change
- **Cause**: Electrical noise from VFDs (variable frequency drives), large motors, or welding equipment coupling into intrinsically safe circuit
- **Solution**:
  - Verify IS cable (blue) is **segregated from non-IS cables** (minimum 50mm spacing)
  - Check barrier earth ground connection (low resistance to earth)
  - Add **low-pass filter in PLC software** (ignore output changes lasting <1 second)

**Step 2: Verify Barrier Function**
- **Test**: Disconnect sensor from barrier, measure barrier output voltage (should read Uo, e.g., 28V for MTL7728+)
- **If 0V**: Barrier fuse blown or barrier malfunction → Replace barrier or fuse
- **If voltage correct**: Barrier OK, issue is in sensor or cable

**Step 3: Check Cable Integrity**
- **Test**: With sensor disconnected from barrier, measure resistance:
  - Brown-to-Blue: Should read >1 MΩ (insulation resistance)
  - Black-to-Blue: Should read high resistance or open circuit (NPN output off)
  - Brown-to-Black: Should read >1 MΩ (insulation resistance)
- **If low resistance (<1 kΩ)**: Cable short circuit → Inspect cable for damage (pinch point, chemical attack, abrasion)

**Step 4: Inspect Sensor (if Accessible)**
- **Visual Check**: Inspect glass dome for cracks, heavy contamination, or damage
- **Cleaning**: If dome contaminated, clean with isopropyl alcohol and soft cloth (see cleaning procedure)

**Problem: False High-Level Alarm (Output Indicates Liquid, But Tank is Empty)**

**Step 1: Verify Liquid Absence**
- Confirm tank is actually empty (sight glass, manual dip stick) - sensor may be correct!

**Step 2: Check for Liquid Residue on Dome**
- **Symptom**: After tank drainage, sensor continues to indicate liquid
- **Cause**: Liquid film or droplet on glass dome (especially viscous oils, sticky residues)
- **Solution**: 
  - Wait for residue to evaporate/drain (may take minutes to hours for viscous fluids)
  - If persistent, remove sensor and clean glass dome with IPA

**Step 3: Check Wiring**
- Verify digital input wiring: Black wire to barrier output (-), not reversed
- For NO mode, digital input should read HIGH when sensor in air (via pull-up resistor)

**Step 4: Verify Sensor Mode**
- Confirm sensor ordered as NO or NC (check nameplate or order documentation)
- If PLC expects NO but sensor is NC (or vice versa), output logic will be inverted

**Problem: Sensor Not Detecting Liquid (Output Stuck in "Air" State)**

**Step 1: Verify Liquid Present**
- Confirm liquid level has reached sensor (sight glass, manual measurement)

**Step 2: Check for Vapor/Gas Bubbles**
- **Symptom**: Sensor tip submerged but output does not switch
- **Cause**: Gas bubbles or foam on dome prevent liquid contact with glass
- **Solution**: Wait for bubbles to dissipate, or relocate sensor to calmer zone

**Step 3: Test Sensor in Known Liquid**
- Remove sensor (after gas-freeing and depressurizing area), test in water or oil
- If output switches correctly in test liquid, sensor OK → Issue is in installation (wrong location, gas bubbles, etc.)
- If output does NOT switch in test liquid, sensor fault → Replace sensor

---

**End of ATEX Complete Technical Documentation**

For ATEX certification documentation, barrier compatibility verification, or custom configurations:

**Teklab S.r.l.**  
Email: info@teklab.it  
Web: www.teklab.it

**ATEX Compliance Consulting**: For Zone classification verification, barrier selection, or installation code compliance, consult certified ATEX consultant or local safety authority.

---

*This unified documentation consolidates all technical and safety information for the ATEX Ex ia intrinsically safe level switch. ATEX installations must comply with local safety regulations (ATEX Directive 2014/34/EU in Europe, IECEx internationally). Always consult qualified personnel for hazardous area installations.*
